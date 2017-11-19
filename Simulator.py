import os
import sys
import threading
import time

from Gui.NSV_Sync_Window import SimulatorUi
from Util.RunProcess import run_process
from Util.KillProcess import kill_process
from Util.LogManager import LogManager
from Util.MakeSocket import make_socket_object
from Util.SendSignal import send_signal
from Util.Parser import string_parser


class Simulator:
    def __init__(self, _dialog):
        self.zone_range = 0
        self.node_info = {}
        self.thread_list = []
        self.log_manager = LogManager()
        self.window = SimulatorUi(_dialog)

    def make_node_threads(self, _number_of_nodes):
        for node_number in range(0, int(_number_of_nodes)):
            self.log_manager.open_log_file(node_number+1)
            self.thread_list.append(threading.Thread(target=self.run_node, args=(str(node_number+1),)))
            self.thread_list[node_number].start()

    def run_algorithm(self, _file, _node, _zone_range):
        self.zone_range = _zone_range
        for idx, data in enumerate(run_process(_file + " " + str(_node) + " " + str(_zone_range))):
            data = data.decode('utf-8')
            if idx is not 0:
                data = string_parser(data)
                self.detect_event(data)
                self.window.node_update(data)
                time.sleep(0.1)
            else:
                agent_a, agent_b, data = string_parser(data, option="init")
                self.set_nodes("agent_a", agent_a)
                self.set_nodes("agent_b", agent_b)
                self.detect_event(data)
                self.window.draw_nodes(self.node_info["agent_a"], self.node_info["agent_b"], data)

    def stop_algorithm(self, _file):
        non_extension = os.path.splitext(_file)[0]
        process_name = os.path.split(non_extension)[1]
        kill_process(process_name)

    def run_node(self, _node_number):
        for idx, log in enumerate(run_process("python3 NODE/node.py "+str(_node_number))):
            log.decode('utf-8')
            if idx is not 0:
                self.log_manager.write_log(_node_number, log)
            else:
                print(int(log))
                self.set_nodes(_node_number, {"port": int(log), "sock_obj": make_socket_object(int(log))})

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
        sys.exit(self.app.exec_())

    def detect_event(self, _update_data):
        for node in _update_data:
            len_from_a = node[3]
            len_from_b = node[4]

            if len_from_a > self.zone_range and len_from_b > self.zone_range:
                '''
                send_signal(
                    self.node_info[node[0]]["sock_obj"],
                    {"msg": "OUT"}
                )
                '''
                self.set_nodes(node[0], {"agent": None})

            else:
                if len_from_a > len_from_b:
                    try:
                        if self.node_info[node[0]]["agent"] is not "B":
                            '''
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
                            '''

                            self.set_nodes(node[0], {"agent": "B", "recent_agent": "B"})
                    except KeyError:
                        self.set_nodes(node[0], {"agent": "B", "recent_agent": "B"})
                        '''
                        send_signal(
                            self.node_info[self.node_info["agent_b"]]["sock_obj"],
                            {"node_num": node[0], "msg": "IN"}
                        )
                        send_signal(
                            self.node_info[node[0]]["sock_obj"],
                            {"node_num": self.node_info["agent_b"], "msg": "IN"}
                        )
                        '''
                if len_from_a < len_from_b:
                    try:
                        if self.node_info[node[0]]["agent"] is not "A":
                            '''
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
                            '''
                            self.set_nodes(node[0], {"agent": "A", "recent_agent": "A"})
                    except KeyError:
                        self.set_nodes(node[0], {"agent": "A", "recent_agent": "A"})
                        '''
                        send_signal(
                            self.node_info[self.node_info["agent_a"]]["sock_obj"],
                            {"node_num": node[0], "msg": "IN"}
                        )
                        send_signal(
                            self.node_info[node[0]]["sock_obj"],
                            {"node_num": self.node_info["agent_a"], "msg": "IN"}
                        )
                        '''
    def set_nodes(self, _node_num, _info):
        self.node_info[_node_num] = _info
