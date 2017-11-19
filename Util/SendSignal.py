import pickle


def send_signal(sock, msgDict):
    msg = msgDict['msg']
    if msg == "IN":
        nodeNum = msgDict['node_num']
        sock.send(pickle.dumps(msg+"_"+str(nodeNum)))
    else:
        sock.send(pickle.dumps(msg))
