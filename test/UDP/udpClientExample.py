import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', 0))

while True:
	init_data = "a"
	sock.sendto(str(init_data).encode(), ('127.0.0.1', 8000))
	data, addr = sock.recvfrom(65535)

# recive
# print(data.decode())





'''
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.bind(('', 0))

while True:
	data = input()
	sock.sendto(data.encode(), ('127.0.0.1', 10000)) #실제 Server IP로 변경

	data, addr = sock.recvfrom(65535)
	print(data.decode())
'''