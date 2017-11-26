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
        #start

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

    def find

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
