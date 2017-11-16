import sys
import threading
from PyQt5 import QtWidgets
from GUI.NSV_Sync_Window import SimulatorUi
from utill.RunProcess import run_process

# TODO UPDATE NODES : receive data format ([[node_idx, x, y, len_from_agentA, len_from_agentB],[node_idx, x, y, len_from_agentA, len_from_agentB],[node_idx, x, y, len_from_agentA, len_from_agentB],[node_idx, x, y, len_from_agentA, len_from_agentB],[node_idx, x, y, len_from_agentA, len_from_agentB],[node_idx, x, y, len_from_agentA, len_from_agentB],[node_idx, x, y, len_from_agentA, len_from_agentB],[node_idx, x, y, len_from_agentA, len_from_agentB],[node_idx, x, y, len_from_agentA, len_from_agentB],[node_idx, x, y, len_from_agentA, len_from_agentB],.....] )
# TODO UPDATE NODES : set Node number as ObjectName, draw Nodes by x, y  agnet_list = [num1, num2] -> receive_data[num1], receive_data[num2] set as a bigger circle?
# TODO UPDATE NODES : this function must have udp server function to get data from udp client(Algorithm)


class Simulator:
    def __init__(self):
        self.agent_A = None
        self.agent_B = None
        self.thread_list = []
        self.log_file = []

        app = QtWidgets.QApplication(sys.argv)
        window = QtWidgets.QDialog()
        ui = SimulatorUi()
        ui.setup_ui(window)
        window.show()
        sys.exit(app.exec_())

    def make_node_threads(self, _number_of_nodes):
        for node_number in range(1, int(_number_of_nodes)):
            self.open_log_file(node_number+1)
            self.thread_list[node_number] = threading.Thread(target=self.run_node, args=node_number+1)
            self.thread_list[node_number].start()

    def run_node(self, _node_number):
        for idx, log in enumerate(run_process("./NODE/node.py "+str(_node_number))):
            if idx is not 0:
                # TODO save node info
                pass
            else:
                self.write_log(_node_number, log.decode('utf-8'))

    def open_log_file(self, _node_number):
        self.log_file[_node_number] = open("./log/node" + _node_number + "_log.txt", "a")

    def write_log(self, _node_number, _log):
        try:
            self.log_file[_node_number].write(_log + "\n")
        except ValueError:
            exit(0)

    def save_logs(self):
        for i in range(0, len(self.log_file)):
            self.log_file[i].close()

    def run_algorithm(self, _file, _node):
        for idx, data in enumerate(run_process(_file + " " + _node)):
            if idx is not 0 :
                self.draw_data(data)
            else:
                self.agent_A = data[0]
                self.agent_A = data[1]

    def set_nodes(self):

    def update_nodes(self):

# for test - it will run in NSV
Simulator()
