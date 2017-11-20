import socket
import time
HOST = '127.0.0.1'

time.sleep(30)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, 10000))
sock.listen()
print('[Waiting for connection...]')
socket_object, address = sock.accept()
print('Got connection from', address)

print(sock.recv(1024).decode('utf-8'))
q = "ok signal"
sock.send(q.encode('utf-8'))
sock.close()
