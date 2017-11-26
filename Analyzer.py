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

    def make_result_data(self):
        marker_1 = []
        marker_2 = []
        agent_node = []
        number_of_nodes = 0

        with open(self.log_file, 'r') as f:
            json_list = json_parser(f)
        # start
        agent_node = self.get_agent_nodes(json_list)
        number_of_nodes = self.get_number_of_nodes(json_list)

        marker_2, handover_time_list = self.get_handover_time(json_list, agent_node)

        marker_1, sync_time_list = self.get_sync_time(json_list, agent_node, number_of_nodes)

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

    def get_sync_time(self, json_list, agent_node, number_of_nodes):
        marker_1 = []
        sync_time_list = []
        head_time = 0
        for i in range(0, number_of_nodes):
            if i in agent_node:
                continue
            for json in json_list:
                if self.find_keyword_from_log({"From": str(i)}, json):
                    if self.find_keyword_from_log({"Cmd": "IN"}, json):
                        head_time = datetime.datetime.strptime(json["Time"], "%H:%M:%S.%f")
                    elif self.find_keyword_from_log({"Msg": "Agent Update."}, json):
                        tail_time = datetime.datetime.strptime(json["Time"], "%H:%M:%S.%f")
                        tmp_sync_time = tail_time - head_time
                        sync_time = float(tmp_sync_time.seconds) + round(tmp_sync_time.microseconds * 0.000001, 3)
                        marker_1.append("Node " + str(i))
                        sync_time_list.append(sync_time)
                        break
        return [marker_1, sync_time_list]

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
            if self.find_keyword_from_log({"Msg": "Node Created."}, json):
                result += 1
        return result

    def get_agent_nodes(self, json_list):
        result = []
        temp = 0
        for json in json_list:
            if self.find_keyword_from_log({"Msg": "This Node is Agent."}, json):
                result.append(json["From"])
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
                    json
            ):
                in_event_buffer.append([json["From"], json["To"]])

        # filter only hand_over start event
        for in_event in in_event_buffer:
            for idx, json in enumerate(json_list):
                if self.find_keyword_from_log(
                        {
                            "Cmd": "GET_REQ",
                            "To": agent[not in_event[1]],
                            "Msg": "Request Node #" + in_event[0] + " info."
                        },
                        json
                ):
                    hand_over_start_data.append(json)
                    json_list.pop(idx)
                    hand_over_buffer.append(in_event)
                    break

        # filter end event match with start event
        for hand_over in hand_over_buffer:
            for idx, json in enumerate(json_list):
                if self.find_keyword_from_log(
                        {
                            "Cmd": "SET",
                            "From": agent[not hand_over[1]],
                            "Msg": "Prev Agent Delete Node."
                        },
                        json
                ):
                    hand_over_end_data.append(json)
                    json_list.pop(idx)
                    break

        for i in range(0, len(hand_over_buffer)):
            temp = datetime.datetime.strptime(hand_over_end_data[i]['Time'], "%H:%M:%S.%f") - \
                   datetime.datetime.strptime(hand_over_start_data[i]['Time'], "%H:%M%S.%f")
            hand_over_time.append(float(temp.seconds) + round(temp.microseconds * 0.000001, 3))
            marker.append(
                "Node " + str(hand_over_buffer[i][0]) + " moved " +
                str(hand_over_end_data[i]["From"]) + " to " + str(hand_over_buffer[i][1]))

        return marker, hand_over_time

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
            file_name = str(_num) + '.png'
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
