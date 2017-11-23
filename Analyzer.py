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
        marker_1 = []
        marker_2 = []
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
        non_sync_nodes = 0

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
                            json_list[index]['From'] == node_number and\
                            json_list[index]['Msg'] == "NODE_SIDE.":\

                            marker_1.append("Node " + str(json_list[index]['From']))

                            tail_index = index
                            sync_time = (datetime.datetime.strptime(json_list[tail_index]['Time'], "%H:%M:%S.%f") -
                                         datetime.datetime.strptime(json_list[head_index]['Time'], "%H:%M:%S.%f"))
                            input_data = float(sync_time.seconds) + round(sync_time.microseconds * 0.000001, 3)

                            sync_time_list.append(input_data)
                            index = head_index + 1

                            break
                        else:
                            index += 1
                            tail_index = 0
                    if tail_index == 0:
                        index = head_index + 1
                        non_sync_nodes += 1
            else:
                index += 1

        index = 0
        # (2) calculate node's hand-over time
        while index < len(json_list):
            if json_list[index]['Cmd'] == "IN" and json_list[index]['From'] == "NSV":
                # saves log index & node number who occurs zone_out event.
                recent_agent = json_list[index]['To']
                node_number = json_list[index]['Msg']

                while (index + 1) < len(json_list):
                    if json_list[index]['Cmd'] == "IN" and json_list[index]['From'] == "NSV" and \
                        json_list[index]['To'] != recent_agent and json_list[index]['Msg'] == node_number:
                        head_index = index
                        new_agent = json_list[index]['To']

                        while (index + 1) < len(json_list):
                            if json_list[index]['Cmd'] == "RECV" and json_list[index]['To'] == new_agent:
                                temp_index = index

                                while (index + 1) < len(json_list):
                                    if json_list[index]['Cmd'] == "SET" and\
                                        json_list[index]['From'] == new_agent and\
                                        json_list[index]['Msg'] == "Agent Update Node List.":

                                        marker_2.append("Node " + str(json_list[head_index]['Msg']) + " moved " +
                                                        str(json_list[temp_index]['From']) + " to " +
                                                        str(json_list[temp_index]['To']))
                                        tail_index = index
                                        sync_time = (datetime.datetime.strptime(json_list[tail_index]['Time'], "%H:%M:%S.%f") -
                                                    datetime.datetime.strptime(json_list[head_index]['Time'], "%H:%M:%S.%f"))
                                        input_data = float(sync_time.seconds) + round(sync_time.microseconds * 0.000001, 3)

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

        log_data.close()

        self.result_1 = self.make_chart_data(number_of_nodes - non_sync_nodes, sync_time_list, marker_1, 1)
        self.result_2 = self.make_chart_data(number_of_nodes, handover_time_list, marker_2, 2)

        try:
            self.average_data_1 = self.get_average_data(str(sum(sync_time_list) / len(sync_time_list)))
        except ZeroDivisionError:
            self.average_data_1 = "None\n\n"

        try:
            self.average_data_2 = self.get_average_data(str(sum(handover_time_list) / len(handover_time_list)))
        except ZeroDivisionError:
            self.average_data_2 = "None\n\n"

        return True

    def get_average_data(self, _msg):
        data = "Average Data: " + _msg + " seconds. \n\n"
        return data

    def make_chart_data(self, _number_of_nodes, _sync_time_list, _marker, _num):
        frame_width = 20 * (_number_of_nodes - 2) + 100
        frame_height = 215
        try:
            range = int(max(_sync_time_list)) + 1
        except ValueError:
            range = 2
        if _num == 1:
            chart = GroupedVerticalBarChart(
                frame_width,
                frame_height,
                y_range=(0, range),
                x_range=(20, 20),
                colours=['ff0000', 'ff4000', 'ff8000', 'ffbf00', 'ffff00', 'bfff00', '80ff00', '40ff00', '00ff00',
                         '00ff40', '00ff80', '00ffbf', '00ffff', '00bfff', '0080ff', '0040ff', '0000ff', '4000ff',
                         '8000ff', 'bf00ff', 'ff00ff', 'ff00bf', 'ff0080', 'ff0040']
            )
            chart.set_axis_range('y', 0, 2)
            chart.set_axis_labels('y', ("", "sec"))
            chart.set_bar_width(10)
            chart.set_legend(_marker)
            chart.add_data(_sync_time_list)
            file_name = str(_num)+'.png'
            chart.download(file_name)

        elif _num == 2:
            chart = GroupedVerticalBarChart(
                frame_width,
                frame_height,
                y_range=(0, range),
                x_range=(20, 20),
                colours=['ff0000', 'ff4000', 'ff8000', 'ffbf00', 'ffff00', 'bfff00', '80ff00', '40ff00', '00ff00',
                         '00ff40', '00ff80', '00ffbf', '00ffff', '00bfff', '0080ff', '0040ff', '0000ff', '4000ff',
                         '8000ff', 'bf00ff', 'ff00ff', 'ff00bf', 'ff0080', 'ff0040']
            )
            chart.set_axis_range('y', 0, 2)
            chart.set_axis_labels('y', ("", "sec"))
            chart.set_bar_width(10)
            chart.set_legend(_marker)
            chart.add_data(_sync_time_list)
            chart.data_x_range()
            file_name = str(_num) + '.png'
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
