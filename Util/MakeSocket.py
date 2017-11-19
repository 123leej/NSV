import socket

HOST = '127.0.0.1'


def make_socket_object(_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, _port))
    sock.listen()
    socket_object, address = sock.accept()
    return socket_object
