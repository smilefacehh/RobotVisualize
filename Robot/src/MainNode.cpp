// #include <ros/ros.h>
// #include "TcpServer.h"

// #define TCP_PORT 10002

// int main(int argc, char** argv)
// {
//     // ros::init(argc, argv, "robot_vis");
    
//     RobotVis::TcpServer tcp_server(TCP_PORT);
//     // ros::spin();
//     return 0;
// }

#include <iostream>
#include <curl/curl.h>
#include <string>

using namespace std;

size_t ncWriteFile(void* buffer, size_t size, size_t nmemb, void* lpVoid)
{
    FILE* stream = (FILE *)lpVoid;
    if (nullptr == stream || nullptr == buffer)
    {
        return -1;
    }
    size_t nWrite = fwrite(buffer, size, nmemb, stream);
    return nWrite;
}

void SendGet()
{
    FILE *fp;
    fp = fopen("1.txt", "w");

    CURL *curl;
    CURLcode res;

    struct curl_slist *headers = NULL;
    //headers = curl_slist_append(headers, "Content-Type:application/json");
    std::string url = "http://www.baidu.com";
    curl = curl_easy_init();    // 初始化
    if (curl)
    {
        res = curl_easy_setopt(curl, CURLOPT_URL, url.c_str());         //请求地址
        res = curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);      //请求头
        res = curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, ncWriteFile);   //写入数据的回调
        res = curl_easy_setopt(curl, CURLOPT_WRITEDATA, (void *)fp);        //文件指针
        res = curl_easy_perform(curl);   // 执行

        if (res != 0)
        {
            curl_slist_free_all(headers);
            curl_easy_cleanup(curl);
        }
    }
    fclose(fp);
}

void SendPost()
{
    CURL *curl;
    CURLcode res;

    struct curl_slist *headers = NULL;
    //headers = curl_slist_append(headers, "Content-Type:application/json");
    std::string url = "http://127.0.0.1:5000/client/msg/";
    curl = curl_easy_init();    // 初始化
    if (curl)
    {
        std::string c = "msg=hello";
        res = curl_easy_setopt(curl, CURLOPT_URL, url.c_str());         //请求地址
        res = curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);      //请求头
        res = curl_easy_setopt(curl, CURLOPT_POSTFIELDS, c.c_str());         //请求参数
        res = curl_easy_setopt(curl, CURLOPT_POSTFIELDSIZE, c.length());//post内容长度
        res = curl_easy_setopt(curl, CURLOPT_POST, 1);                  //设置非0表示本次操作为post
        res = curl_easy_perform(curl);   // 执行
        if (res != 0)
        {
            curl_slist_free_all(headers);
            curl_easy_cleanup(curl);
        }
    }
}

int main()
{
    SendPost();
    return 0;
}