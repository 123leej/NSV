import pickle


def send_signal(sock, msgDict):
    nodeNum = msgDict['node_num']
    msg = msgDict['msg']
    if msg == "IN":
        sock.send(pickle.dumps(msg+"_"+str(nodeNum)))
    else:
        sock.send(pickle.dumps(msg))
