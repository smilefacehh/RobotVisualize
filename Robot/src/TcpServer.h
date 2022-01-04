#pragma once
#include <arpa/inet.h>
#include <errno.h>
#include <sys/socket.h>
#include <string>
#include <thread>
#include <vector>

namespace RobotVis {
class TcpServer
{
public:
    TcpServer(int port);
    ~TcpServer();

    bool Send(const int fd, const std::string& msg);

private:
    void ListenClient();
    void CloseAll();
    bool ClientAlreadyConnected(const std::string& client_ip);

    std::thread listen_thread_;
    int socket_fd_;

    // 连接的客户端列表
    std::vector<int> accept_fds_;
    std::vector<std::string> accept_ips_;
    std::vector<int> to_be_deleted_fds_;
    std::vector<std::string> to_be_deleted_ips_;
};
}