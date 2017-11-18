import os
import sys
import threading

from PyQt5 import QtWidgets

from Gui.NSV_Sync_Window import SimulatorUi
from Util.RunProcess import run_process
from Util.KillProcess import kill_process
from Util.LogManager import LogManager
from Util.MakeSocket import make_socket_object
from Util.SendSignal import send_signal


# TODO set Zone range???????

class Simulator:
    def __init__(self):
        self.zone_range = 150
        self.agent_a = 0
        self.agent_b = 0
        self.node_info = {}
        self.linked_socket = {}
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
            data = data.decode('utf-8')
            if idx is not 0 :
                self.detect_event(data)
                self.window.node_update(self.graphics_view, self.graphics_scene, data)
            else:
                self.agent_a = data[0]
                self.agent_b = data[1]
                self.detect_event(data)
                self.window.draw_nodes(data[0], data[1], data[2:])


    def stop_algorithm(self, _file):
        non_extension = os.path.splitext(_file)[0]
        process_name = os.path.split(non_extension)[1]
        kill_process(process_name)

    def run_node(self, _node_number):
        for idx, log in enumerate(run_process("./NODE/node.py "+str(_node_number))):
            log.decode('utf-8')
            if idx is not 0:
                self.log_manager.write_log(_node_number, log)
            else:
                self.linked_socket[str(_node_number)] = make_socket_object(log)

    def stop_node(self):
        for node_number in self.linked_socket:
            send_signal(self.linked_socket[node_number], {"msg": "END"})

    def stop_all_simulation(self, _file, _number_of_nodes):
        self.stop_algorithm(_file)
        self.stop_node()
        self.log_manager.merge_log_files()

    def detect_event(self, _data):
        for node_info in _data:
            len_from_a = node_info[3]
            len_from_b = node_info[4]

            if len_from_a > self.zone_range and len_from_b > self.zone_range:
                send_signal(self.linked_socket[node_info[0]], {"msg": "OUT"})
            else:
                if len_from_a > len_from_b:
                    if agent is not b:
                        if recentagent is a:
                            send_signal(self.linked_socket[self.agent_a], {"msg": "REQ"})
                        send_signal(self.linked_socket[self.agent_b], {"node_num": node_info[0], "msg": "IN"})
                        send_signal(self.linked_socket[node_info[0]], {"node_num": node_info[0], "msg": "IN"})
                if len_from_a < len_from_b:
                    if agent is not a:
                        if recentagent is b:
                            send_signal(self.linked_socket[self.agent_b], {"msg": "REQ"})
                        send_signal(self.linked_socket[self.agent_a], {"node_num": node_info[0], "msg": "IN"})
                        send_signal(self.linked_socket[node_info[0]], {"node_num": node_info[0],"msg": "IN"})

    def set_nodes(self, _info):
