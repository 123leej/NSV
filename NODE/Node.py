from sys import argv

# TODO Define Node Parameters


class Node:
    def __init__(self, argv):
        # setup Node
        script, node_num = argv
        self.node_num = node_num
        print("Node #", self.node_num, sep="")

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
