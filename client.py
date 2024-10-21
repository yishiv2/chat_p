import socket


host = 'localhost'
port = 8080
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

message = s.recv(1024)
while message:
    print("Res:", message.decode()) #バイト列->文字列
    message=s.recv(1024)

s.close()
