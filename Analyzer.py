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

        sync_time = (datetime.datetime.strptime(json_list[1]['Time'], "%H:%M:%S.%f") - datetime.datetime.strptime(
            json_list[0]['Time'], "%H:%M:%S.%f"))
        input_data_1 = round(sync_time.microseconds * 0.000001, 2)
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
        number_of_nodes = 10
        self.result_1 = self.make_chart_data(number_of_nodes, input_data_1, 1)
        self.result_2 = self.make_chart_data(number_of_nodes, input_data_1, 2)

        self.average_data_1 = self.get_average_data("Fuck!!")
        self.average_data_2 = self.get_average_data("You!!")

        return True

    def get_average_data(self, _msg):
        data = "Average Data: " + _msg + "\n\n"
        return data

    def make_chart_data(self, _number_of_nodes, _input_data, _num):
        frame_width = 30 + 20 * _number_of_nodes + 10 * (_number_of_nodes - 1)
        frame_height = 200

        chart = GroupedVerticalBarChart(
            frame_width,
            frame_height,
            title="Simulation Result Anaylsis",
            y_range=(0, 1)
        )

        chart.set_bar_width(20)
        chart.set_colours(['ff0000'])
        chart.set_axis_range('x', 1, _number_of_nodes)
        chart.set_axis_range('y', 0, 1)
        chart.add_data([0.5, 0.6, _input_data, 0.8, 0.1, 0.5, 0.6, 0.3, 0.5, 0.2])
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
