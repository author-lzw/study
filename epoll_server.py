"""
    epoll io阻塞多路复用并发服务器模型
"""
from socket import *
from select import *

HOST = "0.0.0.0"
PORT = 1111
ADDRESS = (HOST, PORT)

# 创建监听套接字
sockfd = socket()
sockfd.bind(ADDRESS)
sockfd.listen()

# 设置为非阻塞
sockfd.setblocking(False)

# 创建epoll对象
ep = epoll()

# 创建查询字典
map = {sockfd.fileno(): sockfd}

# 关注io
ep.register(sockfd, EPOLLIN)

# 循环监听io
while True:
    events = ep.poll()
    for fd, event in events:
        # 分情况讨论不同io事件类型
        if fd == sockfd.fileno():
            connfd, address = map[fd].accept()
            # 设置非阻塞
            connfd.setblocking(False)
            # 关注链接io
            ep.register(connfd, EPOLLIN)
            # 查询字典添加
            map[connfd.fileno()] = connfd
        else:
            # 链接套接字接收数据
            data = map[fd].recv(1024).decode()
            if not data:
                # 取消关注io
                ep.unregister(fd)
                # 关闭套接字
                map[fd].close()
                # 删除查询字典
                del map[fd]
                continue
            # 链接套接字发送数据
            map[fd].send("ok".encode())
