import socket
import time
HOST = '127.0.0.1'

time.sleep(3)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, 15000))
sock.listen()
print('[Waiting for connection...]')
socket_object, address = sock.accept()
print('Got connection from', address)


msg = socket_object.recv(1024).decode('utf-8')

print(msg)

q = "ok signal"
socket_object.send(q.encode('utf-8'))
socket_object.close()
