#include "TcpServer.h"
#include <fcntl.h>
#include <unistd.h>
#include <cstring>
#include <sstream>
#include "Util.h"


namespace RobotVis {

// socket最大监听数量
#define SOCKET_LISTEN_NUM 5
#define MAX_BUFFER_SIZE 1024

TcpServer::TcpServer(int port)
{
    socket_fd_ = socket(PF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (socket_fd_ == -1)
    {
        printf("Create socket error: %s, errno: %d\n", strerror(errno), errno);
        exit(-1);
    }

    if (fcntl(socket_fd_, F_SETFL, O_NONBLOCK) == -1)
    {
        printf("Set nonblock socket error: %s, errno: %d\n", strerror(errno), errno);
        exit(-1);
    }

    int reused = 1;
    if (setsockopt(socket_fd_, SOL_SOCKET, SO_REUSEADDR, (const void*)&reused, sizeof(int)) == -1)
    {
        printf("Set reused socket error: %s, errno: %d\n", strerror(errno), errno);
        exit(-1);
    }

    sockaddr_in my_addr;
    memset(&my_addr, 0, sizeof(my_addr));
    my_addr.sin_family = AF_INET;
    my_addr.sin_addr.s_addr = htonl(INADDR_ANY);
    my_addr.sin_port = htons(port);

    if (bind(socket_fd_, (sockaddr*)&my_addr, sizeof(my_addr)) == -1)
    {
        printf("Bind error: %s, errno: %d\n", strerror(errno), errno);
        exit(-1);
    }

    if (listen(socket_fd_, SOCKET_LISTEN_NUM) < 0)
    {
        printf("Listen error: %s, errno: %d\n", strerror(errno), errno);
        exit(-1);
    }
    listen_thread_ = std::thread(&TcpServer::ListenClient, this);
}

TcpServer::~TcpServer()
{
    listen_thread_.join();
    CloseAll();
}

bool TcpServer::Send(const int fd, const std::string& msg)
{
    send(fd, (const void*)msg.c_str(), msg.length(), 0);
    return true;
}

void TcpServer::ListenClient()
{
    printf("Start listen ...\n");
    sockaddr_in remote_addr;
    socklen_t sin_size = sizeof(sockaddr_in);
    char buffer[MAX_BUFFER_SIZE];

    double last_t = TimeNow();
    while (1)
    {
        int accept_fd = accept(socket_fd_, (sockaddr*)&remote_addr, &sin_size);
        if (accept_fd >= 0)
        {
            std::string client_ip = inet_ntoa(remote_addr.sin_addr);
            if (ClientAlreadyConnected(client_ip))
            {
                to_be_deleted_fds_.push_back(accept_fd);
                to_be_deleted_ips_.push_back(client_ip);
                Send(accept_fd, "close");
                printf("Client %s is already connected, reject duplicate connection.\n", client_ip.c_str());
            }
            else
            {
                accept_fds_.push_back(accept_fd);
                accept_ips_.push_back(client_ip);
                printf("Received a connection from %s, total: %d\n", client_ip.c_str(), accept_fds_.size());
            }
        }

        for (size_t i = 0; i < accept_fds_.size(); ++i)
        {
            int fd = accept_fds_[i];
            std::string client_ip = accept_ips_[i];

            memset(buffer, 0, MAX_BUFFER_SIZE);
            ssize_t n = 0;
            if ((n = recv(fd, buffer, MAX_BUFFER_SIZE, MSG_DONTWAIT)) > 0)
            {
                printf("Received from client %s, msg: %s\n", client_ip.c_str(), buffer);
            }
            else if (n == 0)
            {
                printf("Cannot read from client %s-%d, maybe closed, now close it.\n", client_ip.c_str(), fd);
                close(fd);
                accept_fds_.erase(accept_fds_.begin() + i);
                accept_ips_.erase(accept_ips_.begin() + i);
            }
        }

        for (size_t i = 0; i < to_be_deleted_fds_.size(); ++i)
        {
            int fd = to_be_deleted_fds_[i];
            std::string client_ip = to_be_deleted_ips_[i];

            memset(buffer, 0, MAX_BUFFER_SIZE);
            if ((recv(fd, buffer, MAX_BUFFER_SIZE, MSG_DONTWAIT)) == 0)
            {
                printf("Client %s-%d is already closed, now close.\n", client_ip.c_str(), fd);
                close(fd);
                to_be_deleted_fds_.erase(to_be_deleted_fds_.begin() + i);
                to_be_deleted_ips_.erase(to_be_deleted_ips_.begin() + i);
            }
        }

        double t = TimeNow();
        if(t - last_t > 1)
        {
            last_t = t;
            for (size_t i = 0; i < accept_fds_.size(); ++i)
            {
                int fd = accept_fds_[i];
                std::ostringstream ss;
                ss << "recv msg, t:" << t;
                Send(fd, ss.str());
            }
        }
    }
}

void TcpServer::CloseAll()
{
    for (auto& fd : accept_fds_)
    {
        close(fd);
    }
}

bool TcpServer::ClientAlreadyConnected(const std::string& client_ip)
{
    for (const auto& ip : accept_ips_)
    {
        if (ip == client_ip)
        {
            return true;
        }
    }
    return false;
}
}