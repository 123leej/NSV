import socket

host = '127.0.0.1'
port = 20000
s = socket.socket()
s.connect((host, port))
init_data=":)"
s.send(str(init_data).encode('utf-8'))

if s.recv(1024).decode('utf-8'):
    print(s.recv(1024).decode('utf-8'))
    s.close()



'''
s = socket.socket()
host = socket.gethostname()
port = 8000

s.connect((host, port))
print( 'Connected to', host)

while True:
    z = input("Enter something for the server: ")
    s.send(z.encode('utf-8'))
    # Halts
    print ('[Waiting for response...]')
    print ((s.recv(1024)).decode('utf-8'))
'''