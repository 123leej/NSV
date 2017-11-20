from PyQt5 import QtCore, QtGui, QtWidgets

import os
import sys
import math
import datetime

from Gui.NSV_Analysis_Window import AnalysisResultUi

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, '..'))

from pygooglechart import GroupedVerticalBarChart

class Analyzer:
    def show_result_data(self):
        # get_data
        f = open('Log.txt', 'r')
        json_list = {}
        i = 0

        # parse_to_json
        while True:
            line = f.readline()

            if not line:
                break

            line_list = line.split("|")
            temp_list = {}
            temp_list['Time'] = line_list[0]
            temp_list['Command'] = line_list[1]
            temp_list['From'] = line_list[2]
            temp_list['To'] = line_list[3]
            temp_list['Msg'] = line_list[4]

            json_list[i] = temp_list
            i += 1
        '''
        import json
        with open('parse_to_json.json', mode='w', encoding='utf-8') as f2:
            json.dump(json_list, f2)
        '''
        sync_time = (datetime.datetime.strptime(json_list[1]['Time'], "%H:%M:%S.%f") - datetime.datetime.strptime(
            json_list[0]['Time'], "%H:%M:%S.%f"))
        input_data = round(sync_time.microseconds * 0.000001, 2)
        print(input_data)
        f.close()

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

        frame_width = 30 + 20 * number_of_nodes + 10 * (number_of_nodes - 1)
        frame_height = 200

        chart = GroupedVerticalBarChart(frame_width, frame_height, \
                                        title="Simulation Result Anaylsis", y_range=(0, 1))
        chart.set_bar_width(20)
        chart.set_colours(['ff0000'])
        # chart.set_axis_labels('x', "Number of Nodes")
        chart.set_axis_range('x', 1, number_of_nodes)
        chart.set_axis_range('y', 0, 1)
        chart.add_data([0.5, 0.6, input_data, 0.8, 0.1, 0.5, 0.6, 0.3, 0.5, 0.2])
        chart.download('Analysis_Result_Chart.png')

        return True

    def start(self, dialog):
        self.window = AnalysisResultUi(dialog, "1.jpeg", "Analysis_Result_Chart.png", "test")
'''
def main():
    Analysis = ShowResultDataUi()
    Analysis.show_result_data()

if __name__ == "__main__":
    main()
'''