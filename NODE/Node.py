from sys import argv
import socket
import pickle
import time

# TODO Define Node Parameters


class Node:
    def __init__(self, argv):
        # setup Node
        script, nodeNum = argv
        self.nodeNum = int(nodeNum)
        print("Node #", self.nodeNum, sep="")
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = socket.gethostname()
        self.port = 20000 + self.nodeNum
        self.s.connect((self.host, self.port))
        self.isAgent = self.get_type()
        self.recentAgent = None
        self.nodeList = []
        self.agentInfo = None
        self.listen_request()

    def get_type(self):
        devType = pickle.loads(self.s.recv(1024))
        return devType

    def listen_request(self):
        # This part's code is need to fix later.
        while True:
            self.request = pickle.loads(self.s.recv(1024))
            # self.request may contain request value: END, IN, OUT
            # "IN" type structure: IN_[NODE_NUMBER]
            if self.request == "END":
                self.s.close()
                break
            if self.isAgent is True:
                if self.request[:2] == "IN":
                    self.agent_in(int(self.request[3:]))
                else:
                    # This is for Previous Agent
                    self.prev_agent()
            else:
                if self.request[:2] == "IN":
                    self.node_in(int(self.request[3:]))
                else:
                    self.node_out()

    def agent_in(self, nodeNum):
        # nodeNum is new Node's ID.
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.host, 40000+nodeNum))
        print("Agent #", self.nodeNum, " Detect New Node #", nodeNum, sep="")
        rcvData = sock.recv(1024)
        data = pickle.loads(rcvData)
        if data == "None":
            rcvData = sock.recv(1024)
            data = pickle.loads(rcvData)
            # data structure: [ [newNodeNum], [newNodePort] ]
            sock.close()
        else:
            # data structure: [ [prevAgentNum], [prevAgentPort] ]
            prevAgentPort = data[1]
            sock.close()
            sock.connect((self.host, 40000+prevAgentPort))
            sock.send(pickle.dumps(nodeNum))
            rcvData = sock.recv(1024)
            data = pickle.loads(rcvData)
            # data structure: [ [newNodeNum], [newNodePort] ]
            sock.close()
        self.nodeList.append(data)

    def prev_agent(self):
        print("Agent #", self.nodeNum, " Get Signal", sep="")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('', 40000+self.port))
        sock.listen(5)
        tgtSock, addr = sock.accept()
        rcvData = tgtSock.recv(1024)
        nodeNum = pickle.loads(rcvData)
        nodeIndex = 0
        for i in self.nodeList:
            if i[0] == nodeNum:
                tgtSock.send(pickle.loads(i))
                break
            nodeIndex += 1
        tgtSock.close()
        self.nodeList.remove(nodeIndex)

    def node_in(self, nodeNum):
        # nodeNum is new Agent's ID.
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.host, 40000+nodeNum))
        print("Node #", self.nodeNum, " Come In to Agent #", nodeNum, sep="")
        if self.recentAgent is not None:
            sock.send(pickle.dumps(self.recentAgent))
        else:
            sock.send(pickle.dumps("None"))
            time.sleep(1)
            sock.send(pickle.dumps([self.nodeNum, self.port]))
        sock.close()
        self.recentAgent = nodeNum
        self.agentInfo = [nodeNum, 20000+nodeNum]

    def node_out(self):
        print("Node #", self.nodeNum, " Go Out!")
        self.agentInfo = None


if __name__ == '__main__':
    n = Node(argv)
