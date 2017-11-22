import os
import sys
import datetime

from Gui.NSV_Analysis_Window import AnalysisResultUi
from Util.Parser import json_parser
from pygooglechart import GroupedVerticalBarChart

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, '..'))


class Analyzer:
    def __init__(self, _log_file):
        self.log_file = _log_file
        self.result_1 = ""
        self.result_2 = ""

    def show_result_data(self):
        log_data = open(self.log_file, 'r')

        json_list = json_parser(log_data)

        number_of_nodes = 0
        agent_node = []

        index = 0
        # find the number of nodes
        while index < len(json_list):
            if json_list[index]['Msg'] == "Node Created.":
                number_of_nodes += 1
            index += 1

        index = 0
        # find the agent nodes
        while index < len(json_list):
            if json_list[index]['Msg'] == "This Node is Agent.":
                agent_node.append(json_list[index]['From'])
            index += 1

        sync_time_list = []
        handover_time_list = []
        head_index = 0
        tail_index = 0
        node_number = ""

        index = 0
        # (1) calculate node synchronization time
        while index < len(json_list):
            # if all node synchronization time is collected, close loop.
            if number_of_nodes == len(sync_time_list):
                break

            # Find creating nodes log.
            if json_list[index]['Cmd'] == "SET" and\
                json_list[index]['To'] == '' and\
                json_list[index]['Msg'] == "Node Created.":

                # If creation node is a agent, pass this log.
                if json_list[index]['From'] == agent_node[0] or\
                    json_list[index]['From'] == agent_node[1]:
                    index += 1
                    continue
                else:
                    # save node creation log index & node number.
                    head_index = index
                    node_number = json_list[index]['From']

                    while (index + 1) < len(json_list):
                        if json_list[index]['Cmd'] == "IN" and\
                            json_list[index]['From'] == node_number:

                            tail_index = index
                            sync_time = (datetime.datetime.strptime(json_list[tail_index]['Time'], "%H:%M:%S.%f") -
                                         datetime.datetime.strptime(json_list[head_index]['Time'], "%H:%M:%S.%f"))
                            input_data = round(sync_time.microseconds * 0.000001, 3)

                            sync_time_list.append(input_data)
                            index = head_index + 1
                            break
                        else:
                            index += 1
            else:
                index += 1

        print(sync_time_list)

        index = 0
        # (2) calculate node's hand-over time
        while index < len(json_list):
            if json_list[index]['Cmd'] == "OUT":
                # saves log index & node number who occurs zone_out event.
                head_index = index
                node_number = json_list[index]['From']
                recent_agent = json_list[index]['To']

                while (index + 1) < len(json_list):
                    if json_list[index]['Cmd'] == "GET_REQ" and json_list[index]['To'] == recent_agent:

                        while (index + 1) < len(json_list):
                            if json_list[index]['Cmd'] == "IN" and json_list[index]['From'] == node_number:
                                new_agent = json_list[index]['To']

                                while(index + 1) < len(json_list):
                                    if json_list[index]['Cmd'] == "SET" and\
                                        json_list[index]['From'] == new_agent and\
                                        json_list[index]['Msg'] == "Agent Update Node List.":\

                                        tail_index = index
                                        print("handover start : " + str(head_index))
                                        print("handover end : " + str(tail_index))
                                        sync_time = (datetime.datetime.strptime(json_list[tail_index]['Time'], "%H:%M:%S.%f") -
                                                    datetime.datetime.strptime(json_list[head_index]['Time'], "%H:%M:%S.%f"))
                                        input_data = round(sync_time.microseconds * 0.000001, 3)

                                        handover_time_list.append(input_data)
                                        index = head_index + 1
                                        break
                                    else:
                                        index += 1
                                break
                            else:
                                index += 1
                        break
                    else:
                        index += 1
            else:
                index += 1

        print(handover_time_list)
        log_data.close()

        # Making result chart process
        '''
        1) set chart info(bar width, color, etc)
        2) input chart data : chart.add_data()
        3) make chart picture : chart,download()
        4) make dialog
        5) input chart picture to dialog
        6) so, barchart shows in dialog
        '''
        # need to get number of nodes.

        self.result_1 = self.make_chart_data(number_of_nodes, sync_time_list, 1)
        self.result_2 = self.make_chart_data(number_of_nodes, handover_time_list, 2)

        self.average_data_1 = self.get_average_data("Fuck!!")
        self.average_data_2 = self.get_average_data("You!!")

        return True

    def get_average_data(self, _msg):
        data = "Average Data: " + _msg + "\n\n"
        return data

    def make_chart_data(self, _number_of_nodes, _sync_time_list, _num):
        frame_width = 30 + 20 * _number_of_nodes + 10 * (_number_of_nodes - 1)
        frame_height = 200

        chart = GroupedVerticalBarChart(
            frame_width,
            frame_height,
            title="Simulation Result Anaylsis",
            y_range=(0, 0.5)
        )

        chart.set_bar_width(20)
        chart.set_colours(['ff0000'])
        chart.set_axis_range('x', 1, _number_of_nodes - 2) # The -2 is two agent nodes.
        chart.set_axis_range('y', 0, 0.5)
        chart.add_data(_sync_time_list)
        file_name = str(_num)+'.png'
        chart.download(file_name)

        return file_name

    def get_log_to_string(self):
        result = ""
        with open(self.log_file, "r") as file:
            while True:
                temp = file.readline()
                if not temp:
                    break
                result += temp
        return str(result)

    def result_text(self):
        return [self.average_data_1 + self.get_log_to_string(), self.average_data_2 + self.get_log_to_string()]


    def start(self, dialog):
        self.window = AnalysisResultUi(dialog, self.result_1, self.result_2, self.result_text())
