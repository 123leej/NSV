from sys import argv
import socket

# TODO Define Node Parameters


class Node:
    def __init__(self, argv):
        # setup Node
        script, node_num = argv
        self.node_num = node_num
        print("Node #", self.node_num, sep="")
        self.s = socket.socket()
        self.host = socket.gethostname()
        self.port = 20000 + self.node_num
        self.s.connect((self.host, self.port))
        self.listen_request()

    def listen_request(self):
        # This part's code is need to fix later.
        while True:
            self.request = self.s.recv(1024).decode()
            if self.request == "END":
                self.s.close()
                break
            if self.isAgent is True:
                if self.request == "IN":
                    self.agent_in(12)
                else:
                    print("Ignore")
            else:
                if self.request == "IN":
                    self.node_in(12)
                else:
                    self.node_out()

    def agent_in(self, node_num):
        # node_num is new Node's ID.
        print("Agent #", self.node_num, " Detect New Node #", node_num, sep="")

    def node_in(self, node_num):
        # node_num is new Agent's ID.
        print("Node #", self.node_num, " Come In to Agent #", node_num, sep="")

    def node_out(self):
        print("Node #", self.node_num, " Go Out!")


if __name__ == '__main__':
    n = Node(argv)
