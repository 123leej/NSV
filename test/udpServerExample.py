import socket

sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )

# Server
sock.bind(('127.0.0.1', 8000)) #실제 Server IP로 변경
print("listen: ", 8000)
while True:
	data, addr = sock.recvfrom(65535)
	#print("ip: ", addr[0], "port: ", addr[1])
	print(data.decode())
	sock.sendto(data, addr)
