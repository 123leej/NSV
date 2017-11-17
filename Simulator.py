import os
import sys
import threading

from PyQt5 import QtWidgets

from Gui.NSV_Sync_Window import SimulatorUi
from Util.RunProcess import run_process
from Util.KillProcess import kill_process
from Util.LogManager import LogManager


class Simulator:
    def __init__(self):
        self.agent_A = None
        self.agent_B = None
        self.thread_list = []
        self.log_manager = LogManager()

        app = QtWidgets.QApplication(sys.argv)
        dialog = QtWidgets.QDialog()
        self.window = SimulatorUi()
        self.graphics_view, self.graphics_scene = self.window.setup_ui(dialog)
        dialog.show()
        sys.exit(app.exec_())

    def make_node_threads(self, _number_of_nodes):
        for node_number in range(0, int(_number_of_nodes)):
            self.log_manager.open_log_file(node_number+1)
            self.thread_list.append(threading.Thread(target=self.run_node, args=node_number+1))
            self.thread_list[node_number].start()

    def run_algorithm(self, _file, _node):
        for idx, data in enumerate(run_process(_file + " " + _node)):
            if idx is not 0 :
                self.window.node_update(self.graphics_view, self.graphics_scene)
            else:
                self.agent_A = data[0]
                self.agent_A = data[1]

    def stop_algorithm(self, _file):
        non_extension = os.path.splitext(_file)[0]
        process_name = os.path.split(non_extension)[1]
        kill_process(process_name)

    def run_node(self, _node_number):
        for idx, log in enumerate(run_process("./NODE/node.py "+str(_node_number))):
            if idx is not 0:
                # TODO save node info
                pass
            else:
                self.log_manager.write_log(_node_number, log.decode('utf-8'))

    def stop_node(self, _number_of_nodes):
        # TODO Edit after send signal

    def stop_all_simulation(self, _file, _number_of_nodes):
        self.stop_algorithm(_file)
        self.stop_node(_number_of_nodes)
        self.log_manager.merge_log_files()
