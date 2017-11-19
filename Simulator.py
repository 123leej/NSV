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


class Simulator:
    def __init__(self):
        self.zone_range = 0
        self.node_info = {}
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

    def run_algorithm(self, _file, _node, _zone_range):
        self.zone_range = _zone_range
        for idx, data in enumerate(run_process(_file + " " + _node + " " + _zone_range)):
            data = data.decode('utf-8')
            if idx is not 0:
                self.detect_event(data)
                self.window.node_update(self.graphics_view, self.graphics_scene, data)
            else:
                self.set_nodes("agent_a", data[0])
                self.set_nodes("agent_b", data[1])
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
                self.set_nodes(_node_number, {"port": log, "sock_obj": make_socket_object(log)})

    def stop_node(self):
        for node_number in self.node_info:
            if node_number != "agent_a" or node_number != "agent_b":
                send_signal(
                    self.node_info[node_number]["sock_obj"],
                    {"msg": "END"}
                )

    def stop_all_simulation(self, _file):
        self.stop_algorithm(_file)
        self.stop_node()
        self.log_manager.merge_log_files()

    def detect_event(self, _update_data):
        for node in _update_data:
            len_from_a = node[3]
            len_from_b = node[4]

            if len_from_a > self.zone_range and len_from_b > self.zone_range:
                send_signal(
                    self.node_info[node[0]]["sock_obj"],
                    {"msg": "OUT"}
                )

                self.set_nodes(node[0], {"agent": None})

            else:
                if len_from_a > len_from_b:
                    if self.node_info[node[0]]["agent"] is not "B":
                        if self.node_info[node[0]]["recent_agent"] is "A":
                            send_signal(
                                self.node_info[self.node_info["agent_a"]]["sock_obj"],
                                {"msg": "REQ"}
                            )

                        send_signal(
                            self.node_info[self.node_info["agent_b"]]["sock_obj"],
                            {"node_num": node[0], "msg": "IN"}
                        )
                        send_signal(
                            self.node_info[node[0]]["sock_obj"],
                            {"node_num": self.node_info["agent_b"], "msg": "IN"}
                        )

                        self.set_nodes(node[0], {"agent": "B", "recent_agent": "B"})

                if len_from_a < len_from_b:
                    if self.node_info[node[0]]["agent"] is not "A":
                        if self.node_info[node[0]]["recent_agent"] is "B":
                            send_signal(
                                self.node_info[self.node_info["agent_b"]]["sock_obj"],
                                {"msg": "REQ"}
                            )

                        send_signal(
                            self.node_info[self.node_info["agent_a"]]["sock_obj"],
                            {"node_num": node[0], "msg": "IN"}
                        )
                        send_signal(
                            self.node_info[node[0]]["sock_obj"],
                            {"node_num": self.node_info["agent_a"], "msg": "IN"}
                        )

                        self.set_nodes(node[0], {"agent": "A", "recent_agent": "A"})

    def set_nodes(self, _node_num, _info):
        self.node_info[_node_num] = _info
