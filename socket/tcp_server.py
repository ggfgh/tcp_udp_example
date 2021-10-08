import socket
import threading

#AF_INET: 基于IPv4的网络通信 SOCK_STREAM 基于TCP的流式socket通信
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#将套接字绑定到地址
s.bind(('127.0.0.1',9999))
#监听TCP传入连接(同时连接的最大数量)
s.listen(5)

def handle_tcp(sock,addr):
    print('new connection from %s:%s' %(addr))
    #放送数据
    sock.send(b'Welcome!!!')

    while True:
        #每次最多接受1024字节的数据
        data = sock.recv(1024)
        if not data:
            break
        sock.send(b'Hello,%s!' %data)
    sock.close()

while True:
    #等待客户端连接
    sock,addr = s.accept()
    t = threading.Thread(target=handle_tcp,args=(sock,addr))
    t.start()
