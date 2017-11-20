import socket

host = '127.0.0.1'
port = 10000
s = socket.socket()
s.connect((host, port))
init_data = ":)"
s.send(str(init_data).encode('utf-8'))

if s.recv(1024).decode('utf-8'):
    print(s.recv(1024).decode('utf-8'))
    s.close()
