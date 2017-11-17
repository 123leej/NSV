from PyQt5 import QtCore, QtGui, QtWidgets

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

