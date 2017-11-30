import os
import sys
import datetime

from Gui.NSV_Analysis_Window import AnalysisResultUi
from Util.Parser import json_parser
from pygooglechart import StackedHorizontalBarChart

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, '..'))


class Analyzer:
    def __init__(self, _log_file):
        self.log_file = _log_file
        self.result_1 = ""
        self.result_2 = ""
        self.result_3 = ""

    def make_result_data(self):
        with open(self.log_file, 'r') as f:
            json_list = json_parser(f)

        agent_node = self.get_agent_nodes(json_list)
        number_of_nodes = self.get_number_of_nodes(json_list)

        marker_1, sync_in_list = self.get_sync_in(json_list, agent_node, number_of_nodes)
        marker_2, handover_time_list = self.get_handover_time(json_list, agent_node)
        marker_3, sync_out_list = self.get_sync_out(json_list, agent_node, number_of_nodes)

        self.result_1 = self.make_chart_data(number_of_nodes, sync_in_list, self.reverse_marker(marker_1), 1)
        self.result_2 = self.make_chart_data(number_of_nodes, handover_time_list, self.reverse_marker(marker_2), 2)
        self.result_3 = self.make_chart_data(number_of_nodes, sync_out_list, self.reverse_marker(marker_3), 3)

        try:
            self.average_data_1 = self.get_average_data(str(round((sum(sync_in_list) / len(sync_in_list)), 5)))
        except ZeroDivisionError:
            self.average_data_1 = "None\n\n"

        try:
            self.average_data_2 = self.get_average_data(str(round((sum(handover_time_list) / len(handover_time_list)), 5)))
        except ZeroDivisionError:
            self.average_data_2 = "None\n\n"

        try:
            self.average_data_3 = self.get_average_data(str(round((sum(sync_out_list) / len(sync_out_list)), 5)))
        except ZeroDivisionError:
            self.average_data_3 = "None\n\n"

        return True

    def get_sync_in(self, json_list, agent_node, number_of_nodes):
        marker_1 = []
        sync_in_list = []
        head_time = 0
        for i in range(0, number_of_nodes):
            if i in agent_node:
                continue
            for json in json_list:
                if self.find_keyword_from_log({"From": str(i)}, json_list[json]):
                    if self.find_keyword_from_log({"Cmd": "IN"}, json_list[json]):
                        head_time = datetime.datetime.strptime(json_list[json]["Time"], "%H:%M:%S.%f")
                    elif self.find_keyword_from_log({"Msg": "Agent Update."}, json_list[json]):
                        tail_time = datetime.datetime.strptime(json_list[json]["Time"], "%H:%M:%S.%f")
                        tmp_sync_time = tail_time - head_time
                        sync_time = float(tmp_sync_time.seconds) + round(tmp_sync_time.microseconds * 0.000001, 3)
                        marker_1.append("Node " + str(i))
                        sync_in_list.append(sync_time)
                        break

        return marker_1, sync_in_list

    def get_sync_out(self, json_list, agent_node, number_of_nodes):
        marker_3 = []
        sync_out_list = []
        head_time = 0
        for i in range(0, number_of_nodes):
            for json in json_list:
                if self.find_keyword_from_log({"From": str(i)}, json_list[json]) and self.find_keyword_from_log({"Cmd": "SEND"}, json_list[json]):
                    head_time = datetime.datetime.strptime(json_list[json]["Time"], "%H:%M:%S.%f")
                elif self.find_keyword_from_log({"To": str(i)}, json_list[json]) and self.find_keyword_from_log({"Cmd": "RECV"}, json_list[json]):
                    tail_time = datetime.datetime.strptime(json_list[json]["Time"], "%H:%M:%S.%f")
                    tmp_sync_time = tail_time - head_time
                    sync_time = float(tmp_sync_time.seconds) + round(tmp_sync_time.microseconds * 0.000001, 3)
                    marker_3.append("Agent " + str(i))
                    sync_out_list.append(sync_time)
                    break

        return marker_3, sync_out_list

    # keyword = {"msg" : key} (dict)  type - 'Time''Cmd''From''To''Msg'
    def find_keyword_from_log(self, keyword, log):
        flag = True
        for key in keyword:
            if log[key] == keyword[key]:
                pass
            else:
                flag = False
                break
        return flag

    def get_number_of_nodes(self, json_list):
        result = 0
        for json in json_list:
            if self.find_keyword_from_log({"Msg": "Node Created."}, json_list[json]):
                result += 1
        return result

    def get_agent_nodes(self, json_list):
        result = []
        temp = 0
        for json in json_list:
            if self.find_keyword_from_log({"Msg": "This Node is Agent."}, json_list[json]):
                result.append(json_list[json]["From"])
                temp += 1
            if temp == 2:
                break
        return result

    def get_handover_time(self, json_list, agent):
        hand_over_time = []
        marker = []
        in_event_buffer = []
        hand_over_buffer = []
        hand_over_start_data = []
        hand_over_end_data = []

        # get all in event
        for json in json_list:
            if self.find_keyword_from_log(
                    {
                        "Cmd": "IN",
                        "Msg": "AGENT_SIDE."
                    },
                    json_list[json]
            ):
                in_event_buffer.append([json_list[json]["From"], json_list[json]["To"]])

        # filter only hand_over start event
        for in_event in in_event_buffer:
            for json in json_list:
                if agent.index(in_event[1]) is 0:
                    temp = 1
                if agent.index(in_event[1]) is 1:
                    temp = 0
                if self.find_keyword_from_log(
                        {
                            "Cmd": "GET_REQ",
                            "To": agent[temp],
                            "Msg": "Request Node #" + in_event[0] + " info."
                        },
                        json_list[json]
                ):
                    hand_over_start_data.append(json_list[json])
                    json_list.pop(json)
                    hand_over_buffer.append(in_event)
                    break

        # filter end event match with start event
        for hand_over in hand_over_buffer:
            for json in json_list:
                if agent.index(hand_over[1]) is 0:
                    temp = 1
                if agent.index(hand_over[1]) is 1:
                    temp = 0
                if self.find_keyword_from_log(
                        {
                            "Cmd": "SET",
                            "From": agent[temp],
                            "Msg": "Prev Agent Delete Node."
                        },
                        json_list[json]
                ):
                    hand_over_end_data.append(json_list[json])
                    json_list.pop(json)
                    break

        for i in range(0, len(hand_over_buffer)):
            temp = datetime.datetime.strptime(hand_over_end_data[i]['Time'], "%H:%M:%S.%f") - \
                   datetime.datetime.strptime(hand_over_start_data[i]['Time'], "%H:%M:%S.%f")
            hand_over_time.append(float(temp.seconds) + round(temp.microseconds * 0.000001, 3))
            if agent.index(hand_over_end_data[i]["From"]) is 0:
                temp = 1
            if agent.index(hand_over_end_data[i]["From"]) is 1:
                temp = 0
            marker.append(
                "Node " + str(hand_over_buffer[i][0]) + " moved " +
                str(hand_over_end_data[i]["From"]) + " to " + str(agent[temp]))

        return marker, hand_over_time

    def get_average_data(self, _msg):
        data = "Average Data: " + _msg + " seconds. \n\n"
        return data

    def make_chart_data(self, _number_of_nodes, _data_list, _marker, _num):
        if _num == 1:
            chart = StackedHorizontalBarChart(
                484,
                281,
                x_range=(0, 0.5),
                y_range=(0, 20),
                colours=['ff0000', 'ff4000', 'ff8000', 'ffbf00', 'ffff00', 'bfff00', '80ff00', '40ff00', '00ff00',
                         '00ff40', '00ff80', '00ffbf', '00ffff', '00bfff', '0080ff', '0040ff', '0000ff', '4000ff',
                         '8000ff', 'bf00ff', 'ff00ff', 'ff00bf', 'ff0080', 'ff0040']
            )
            chart.set_bar_width(10)
            chart.set_axis_range('x', 0, 0.5)
            chart.set_axis_labels('x', ("", "sec"))
            chart.set_axis_labels('y', _marker)
            chart.add_data(_data_list)
            file_name = str(_num) + '.png'
            chart.download(file_name)

        elif _num == 2:
            chart = StackedHorizontalBarChart(
                550,
                281,
                x_range=(0, 0.5),
                y_range=(0, 20),
                colours=['ff0000', 'ff4000', 'ff8000', 'ffbf00', 'ffff00', 'bfff00', '80ff00', '40ff00', '00ff00',
                         '00ff40', '00ff80', '00ffbf', '00ffff', '00bfff', '0080ff', '0040ff', '0000ff', '4000ff',
                         '8000ff', 'bf00ff', 'ff00ff', 'ff00bf', 'ff0080', 'ff0040']
            )

            chart.set_bar_width(10)
            chart.set_axis_range('x', 0, 0.5)
            chart.set_axis_labels('x', ("", "sec"))
            chart.set_axis_labels('y', _marker)
            chart.add_data(_data_list)
            file_name = str(_num) + '.png'
            chart.download(file_name)

        elif _num == 3:
            chart = StackedHorizontalBarChart(
                480,
                281,
                x_range=(0, 0.5),
                y_range=(0, 20),
                colours=['ff0000', 'ff4000', 'ff8000', 'ffbf00', 'ffff00', 'bfff00', '80ff00', '40ff00', '00ff00',
                         '00ff40', '00ff80', '00ffbf', '00ffff', '00bfff', '0080ff', '0040ff', '0000ff', '4000ff',
                         '8000ff', 'bf00ff', 'ff00ff', 'ff00bf', 'ff0080', 'ff0040']
            )
            chart.set_bar_width(10)
            chart.set_axis_range('x', 0, 0.5)
            chart.set_axis_labels('x', ("", "sec"))
            chart.set_axis_labels('y', _marker)
            chart.add_data(_data_list)
            file_name = str(_num) + '.png'
            chart.download(file_name)

        return file_name

    def reverse_marker(self, _marker):
        temp = []
        _len = len(_marker)
        for idx in range(1, _len+1):
            temp.append(_marker[_len-idx])
        return temp

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
        return [
            self.average_data_1 + self.get_log_to_string(),
            self.average_data_2 + self.get_log_to_string(),
            self.average_data_3 + self.get_log_to_string()
        ]

    def start(self, dialog):
        self.window = AnalysisResultUi(dialog, self.result_1, self.result_2, self.result_3, self.result_text())
