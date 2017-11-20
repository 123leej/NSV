import socket
import time

while True:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('127.0.0.1', 15000))
        break
    except Exception:
        time.sleep(0.1)

init_data = ":)"
s.send(str(init_data).encode('utf-8'))


