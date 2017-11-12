import socket

sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )

# Server
sock.bind(('192.168.43.171', 10000))
print("listen: ", 10000)
while True:
	data, addr = sock.recvfrom(65535)
	print("ip: ", addr[0], "port: ", addr[1])
	print("echo data: ", data.decode())
	sock.sendto(data, addr)
