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
    def __init__(self):
        self.zone_range = 0
        self.node_info = {}
        self.log_manager = LogManager()
        self.is_thread_run = []
        self.lock = threading.Lock()

    def make_node_threads(self, _number_of_nodes):
        for i in range(0, int(_number_of_nodes)):
            self.is_thread_run.append(False)

        for node_number in range(0, int(_number_of_nodes)):
            self.log_manager.open_log_file(node_number+1)
            t = threading.Thread(target=self.run_node, args=(str(node_number+1),))
            t.start()

    def get_thread_is_running(self):
        return self.is_thread_run

    def run_algorithm(self, _file, _node, _zone_range, _app):
        self.zone_range = _zone_range
        for idx, data in enumerate(run_process(_file + " " + str(_node) + " " + str(_zone_range))):
            data = data.decode('utf-8')
            if idx is not 0:
                data = string_parser(data)
                self.detect_event(data)
                self.window.node_update(self.node_info["agent_a"], self.node_info["agent_b"], data)
                time.sleep(0.1)
            else:
                agent_a, agent_b, data = string_parser(data, option="init")
                self.set_nodes_info(data, agent_a, agent_b)
                self.detect_event(data)
                self.window.draw_nodes(self.node_info["agent_a"], self.node_info["agent_b"], _zone_range, data)
            if not self.window.get_runtime_flag():
                self.stop_all_simulation(_file, _app)

    def stop_algorithm(self, _file):
        non_extension = os.path.splitext(_file)[0]
        process_name = os.path.split(non_extension)[1]
        return kill_process(process_name)

    def run_node(self, _node_number):
        for idx, log in enumerate(run_process("python3 NODE/Node.py "+str(_node_number))):
            log = log.decode('utf-8')
            if idx is not 0:
                self.log_manager.write_log(int(_node_number), log)
                # TODO print log to ui
            else:
                self.lock.acquire()
                sock_object = make_socket_object(int(log))
                self.set_nodes(int(_node_number)-1, {"port": int(log), "sock_obj": sock_object}, option="init")
                self.is_thread_run[int(_node_number) - 1] = True
                self.lock.release()

    def stop_node(self):
        for node_number in self.node_info:
            if node_number != "agent_a" and node_number != "agent_b":
                send_signal(
                    self.node_info[node_number]["sock_obj"],
                    {"msg": "END"}
                )
        self.log_manager.save_logs()

    def stop_all_simulation(self, _file, _app):
        if self.stop_algorithm(_file):
            self.stop_node()
            if self.log_manager.merge_log_files():
                sys.exit(_app.exec_())

    def detect_event(self, _update_data):
        for node in _update_data:
            if node[0] is not self.node_info["agent_a"] or node[0] is not self.node_info["agent_b"]:
                len_from_a = node[3]
                len_from_b = node[4]

                if len_from_a > self.zone_range and len_from_b > self.zone_range:
                    if self.node_info[node[0]]["recent_agent"] is not None:
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

                    if len_from_a <= len_from_b:
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
            else:
                pass

    def set_nodes_info(self, _init_data, _agent_a, _agent_b):
        self.set_nodes("agent_a", _agent_a, option="init")
        self.set_nodes("agent_b", _agent_b, option="init")

        for node in _init_data:
            if node[0] is not self.node_info["agent_a"] or node[0] is not self.node_info["agent_b"]:
                len_from_a = node[3]
                len_from_b = node[4]

                if len_from_a > self.zone_range and len_from_b > self.zone_range:
                    self.set_nodes(node[0], {"agent": None, "recent_agent": None})

                else:
                    if len_from_a > len_from_b:
                        self.set_nodes(node[0], {"agent": "B", "recent_agent": "B"})

                    if len_from_a <= len_from_b:
                        self.set_nodes(node[0], {"agent": "A", "recent_agent": "A"})
            else:
                pass

    def set_nodes(self, _node_num, _info, option=None):
        try:
            if option is None:
                for i in _info:
                    self.node_info[_node_num][i] = _info[i]
            else:
                self.node_info[_node_num] = _info
        except KeyError:
            self.node_info[_node_num] = _info

    def show(self, _dialog):
        self.window = SimulatorUi(_dialog)
