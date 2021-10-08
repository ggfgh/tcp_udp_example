import socket

#SOCK_DGRAM 基于 udp 的流式socket通信
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#将套接字绑定地址
s.bind(('127.0.0.1',4444))

while True:
    data,addr = s.recvfrom(1024)
    print('Received from %s:%s' %addr)
    s.sendto(b'hello,%s' %data,addr)
