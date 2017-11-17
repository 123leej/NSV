import os
import sys
import datetime
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
        self.log_file = []
        self.log_file_buffer = []

        app = QtWidgets.QApplication(sys.argv)
        window = QtWidgets.QDialog()
        ui = SimulatorUi()
        ui.setup_ui(window)
        window.show()
        sys.exit(app.exec_())

    def make_node_threads(self, _number_of_nodes):
        for node_number in range(0, int(_number_of_nodes)):
            self.open_log_file(node_number+1)
            self.thread_list.append(threading.Thread(target=self.run_node, args=node_number+1))
            self.thread_list[node_number].start()

    def run_algorithm(self, _file, _node):
        for idx, data in enumerate(run_process(_file + " " + _node)):
            if idx is not 0 :
                # TODO Edit after drawing nodes objects
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
                self.write_log(_node_number, log.decode('utf-8'))

    def stop_node(self, _number_of_nodes):
        # TODO Edit after send signal

    def stop_all_simulation(self, _file, _number_of_nodes):
        self.stop_algorithm(_file)
        self.stop_node(_number_of_nodes)
        self.merge_log_files()

    def open_log_file(self, _node_number):
        self.log_file.append("node" + str(_node_number) + "_log.txt")
        self.log_file_buffer.append(open("./log/" + self.log_file[_node_number], "a"))

    def write_log(self, _node_number, _log):
        try:
            self.log_file_buffer[_node_number].write(_log + "\n")
        except ValueError:
            self.stop_all_simulation()
            # TODO Edit after stop_all_simulation

    def save_logs(self):
        for i in range(0, len(self.log_file_buffer)):
            self.log_file_buffer[i].close()

        self.log_file_buffer = None

    def merge_log_files(self):
        with open("./log/"+datetime.datetime.now().strftime('%Y-%m-%d')+"_simulation", "w") as result_file:
            for i in range(0, len(self.log_file)):
                with open("./log/"+self.log_file[i], "r") as node_log_file:
                    while True:
                        temp = node_log_file.readline()
                        if not temp:
                            result_file.write('\n')
                        result_file.write(temp)
        # TODO PARSE log datas by timelaps