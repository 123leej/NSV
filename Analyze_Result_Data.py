from PyQt5 import QtCore, QtGui, QtWidgets

import os
import sys
import math

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, '..'))

from pygooglechart import StackedHorizontalBarChart, StackedVerticalBarChart, \
    GroupedHorizontalBarChart, GroupedVerticalBarChart

import settings

class ShowResultDataUi(object):
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

        import json
        with open('parse_to_json.json', mode='w', encoding='utf-8') as ff:
            json.dump(json_list, ff)

        f.close()

        chart = StackedVerticalBarChart(settings.width, settings.height,
                                        y_range=(0, 35))


        # Making result chart process
        '''
        1) set chart info(bar width, color, etc)
        2) input chart data : chart.add_data()
        3) make chart picture : chart,download()
        4) make dialog
        5) input chart picture to dialog
        6) so, barchart shows in dialog
        '''

        chart.set_bar_width(10)
        chart.set_colours(['00ff00', 'ff0000'])
        chart.add_data([1, 2, 3, 4, 5])
        chart.add_data([1, 4, 9, 16, 25])
        chart.download('bar-vertical-stacked.png')
        # chart.get_url() : get Google Chart URL

    def main():
        Analysis = ShowResultDataUi()
        ShowResultDataUi.show_result_data()

    if __name__ == '__main    __':
        main()