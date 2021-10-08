import socket

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(('127.0.0.1',9999))
print(s.recv(1024))

for data in [b'dog']:
    s.send(data)
    print(s.recv(1024))
s.close()
