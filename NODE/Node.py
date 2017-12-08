from sys import argv
import socket
import pickle
import time
import threading
from datetime import datetime


class Node:
    def __init__(self, argv):
        # setup Node
        script, nodeNum = argv
        self.nodeNum = int(nodeNum)
        # print("Node #", self.nodeNum, sep="")
        self.host = '127.0.0.1'
        self.port = 20000 + self.nodeNum
        self.hand_over_sequence_number = 0
        print(self.port)
        while True:
            try:
                self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.s.connect((self.host, self.port))
                break
            except Exception:
                pass
        self.print_log("SET", self.nodeNum, "", "Node Created.")
        self.isAgent = self.get_type()
        self.recentAgent = None
        self.nodeList = []
        self.requestQueue = []
        self.agentInfo = None
        threading.Thread(target=self.listen_request).start()
        self.do_request()

    def get_type(self):
        devType = pickle.loads(self.s.recv(1024))
        self.s.send(pickle.dumps("ok"))
        if devType is True:
            self.print_log("SET", self.nodeNum, "", "This Node is Agent.")
        return devType

    def listen_request(self):
        while True:
            temp = pickle.loads(self.s.recv(1024))
            self.s.send(pickle.dumps("ok"))
            if temp == "END":
                self.s.close()
                self.print_log("SET", self.nodeNum, "", "Node Destroyed.")
                self.requestQueue.append(temp)
                break
            self.requestQueue.append(temp)

    def do_request(self):
        # This part's code is need to fix later.
        while True:
            while len(self.requestQueue) == 0:
                pass
            req = self.requestQueue[0]
            del(self.requestQueue[0])
            # req may contain request value: END, IN, OUT
            # "IN" type structure: IN_[NODE_NUMBER]
            if req == "END":
                break
            if self.isAgent is True:
                if req[:2] == "IN":
                    self.agent_in(int(req[3:]))
                else:
                    # This is for Previous Agent
                    self.prev_agent(int(req[4:]))
            else:
                if req[:2] == "IN":
                    self.node_in(int(req[3:]))
                else:
                    self.node_out()

    def agent_in(self, nodeNum):
        # nodeNum is new Node's ID.
        if len(self.nodeList) != 0:
            nodeInList = False
            for i in self.nodeList:
                if i[0] == nodeNum:
                    nodeInList = True
                    break
            if nodeInList is True:
                self.print_log("IN", nodeNum, self.nodeNum, "NODE #" + str(nodeNum) + "info is already in Agent.")
                return
        self.print_log("IN", "NSV", self.nodeNum, str(nodeNum))
        sock_temp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_temp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock_temp.bind(('', 40000 + (self.nodeNum*100) + nodeNum))
        sock_temp.listen()
        tgtSock, addr = sock_temp.accept()
        self.print_log("IN", nodeNum, self.nodeNum, "AGENT_SIDE.")
        rcvData = tgtSock.recv(1024)
        data = pickle.loads(rcvData)
        if data == "None":
            tgtSock.send(pickle.dumps("OK"))
            rcvData = tgtSock.recv(1024)
            data = pickle.loads(rcvData)
            # data structure: [ [newNodeNum], [newNodePort] ]
            tgtSock.close()
        else:
            # data structure: prevAgentNum
            prevAgentNum = data
            tgtSock.close()
            self.hand_over_sequence_number += 1
            self.print_log("AGENT", "", "", str(50000 + (nodeNum * 100) + self.hand_over_sequence_number))
            while True:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.connect((self.host, 50000 + (nodeNum*100) + self.hand_over_sequence_number))
                    break
                except Exception:
                    pass
            self.print_log("SEND", self.nodeNum, prevAgentNum,
                "Request Node's Info to Prev Agent.")
            sock.send(pickle.dumps(self.nodeNum))
            rcvData = sock.recv(1024)
            time.sleep(0.2)
            self.print_log("RECV", prevAgentNum, self.nodeNum,
                "Receive Node's Info from Prev Agent.")
            data = pickle.loads(rcvData)
            # data structure: [ [newNodeNum], [newNodePort] ]
            sock.close()
        self.nodeList.append(data)
        self.print_log("SET", self.nodeNum, "", "Agent Update Node List.:"+str(nodeNum))

    def prev_agent(self, nodeNum):
        self.print_log("GET_REQ", "NSV", self.nodeNum, "Request Node #" + str(nodeNum) + " info.")
        self.hand_over_sequence_number += 1
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.print_log("PREV", "", "", str(50000 + (nodeNum*100) + self.hand_over_sequence_number))
        sock.bind((self.host, 50000 + (nodeNum*100) + self.hand_over_sequence_number))
        sock.listen()
        tgtSock, addr = sock.accept()
        rcvData = tgtSock.recv(1024)
        node_info = pickle.loads(rcvData)
        #self.print_log("SEND", self.nodeNum, node_info, "Send Node #" + str(nodeNum) + " info.")
        for i in self.nodeList:
            if i[0] == nodeNum:
                tgtSock.send(pickle.dumps(i))
                self.nodeList.remove(i)
                break
        tgtSock.close()
        sock.close()
        time.sleep(0.3)
        self.print_log("SET", self.nodeNum, "", "Prev Agent Delete Node.")

    def node_in(self, nodeNum):
        self.print_log("IN", self.nodeNum, nodeNum, "NODE_SIDE.")
        if self.recentAgent == nodeNum:
            # Node Just Re-Enter in Agent's Zone.
            self.agentInfo = [nodeNum, 20000+nodeNum]
            self.print_log("SET", self.nodeNum, "", "Agent Update.")
            return
        # nodeNum is new Agent's ID.
        while True:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((self.host, 40000 + (nodeNum*100) + self.nodeNum))
                time.sleep(0.1)
                break
            except Exception:
                pass
        if self.recentAgent is not None:
            sock.send(pickle.dumps(self.recentAgent))
        else:
            sock.send(pickle.dumps("None"))
            sock.recv(1024)
            sock.send(pickle.dumps([self.nodeNum, self.port]))
        sock.close()
        self.recentAgent = nodeNum
        self.agentInfo = [nodeNum, 20000+nodeNum]
        time.sleep(0.2)
        self.print_log("SET", self.nodeNum, "", "Agent Update.")

    def node_out(self):
        self.print_log("OUT", self.nodeNum, self.recentAgent, "")
        self.agentInfo = None

    def print_log(self, cmd, dataFrom, dataTo, details):
        now = datetime.now().strftime("%H:%M:%S.%f")
        print(now, cmd, dataFrom, dataTo, details, sep="|")


if __name__ == '__main__':
    n = Node(argv)
