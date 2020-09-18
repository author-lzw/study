"""
    select io阻塞多路复用并发服务器模型
    适用于 window;linux;unix
"""
from socket import *
from select import select
from typing import List

HOST = "0.0.0.0"
PORT = 1111
ADDRESS = (HOST, PORT)

# 关注监听套接字
sockfd = socket()
sockfd.bind(ADDRESS)
sockfd.listen(5)

# 设置监听为非阻塞
sockfd.setblocking(False)

# 创建关注列表
rlist = [sockfd]  # type:List[socket]
wlist = []
xlist = []

# 循环监控io
while True:
    rl, wl, xl = select(rlist, wlist, xlist)  # type: List[socket]
    for r in rl:
        # 分情况套路不同套接字执行情况
        if r is sockfd:
            # 绑定链接套接字
            connfd, address = r.accept()
            # 设置为非阻塞
            connfd.setblocking(False)
            # 关注链接套接字
            rlist.append(connfd)
        else:
            # 链接套接字接收数据
            data = r.recv(1024).decode()
            if not data:
                # 取消关注io
                rlist.remove(r)
                # 关闭套接字
                r.close()
                continue
            # 链接套接字发送数据
            r.send("ok".encode())
