import sys
from PyQt5 import QtWidgets
from GUI.NSV_Sync_Window import SimulatorUi
from utill.RunProcess import run_process

# TODO UPDATE NODES : receive data format ([[node_idx, x, y, len_from_agentA, len_from_agentB],[node_idx, x, y, len_from_agentA, len_from_agentB],[node_idx, x, y, len_from_agentA, len_from_agentB],[node_idx, x, y, len_from_agentA, len_from_agentB],[node_idx, x, y, len_from_agentA, len_from_agentB],[node_idx, x, y, len_from_agentA, len_from_agentB],[node_idx, x, y, len_from_agentA, len_from_agentB],[node_idx, x, y, len_from_agentA, len_from_agentB],[node_idx, x, y, len_from_agentA, len_from_agentB],[node_idx, x, y, len_from_agentA, len_from_agentB],.....] )
# TODO UPDATE NODES : set Node number as ObjectName, draw Nodes by x, y  agnet_list = [num1, num2] -> receive_data[num1], receive_data[num2] set as a bigger circle?
# TODO UPDATE NODES : this function must have udp server function to get data from udp client(Algorithm)


class Simulator:
    def __init__(self):
        app = QtWidgets.QApplication(sys.argv)
        window = QtWidgets.QDialog()
        ui = SimulatorUi()
        ui.setup_ui(window)
        window.show()
        sys.exit(app.exec_())

    def run_algorithm(self, _file, _node, _port):
        for data in run_process(_file + " " + _node + " " + str(_port)):
            self.draw_data(data)

    def update_nodes(self):

# for test - it will run in NSV
Simulator()
