import sys
from Gui.NSV_First_Dialog import NSVUi
from Simulator import Simulator
from Analyzer import Analyzer
from PyQt5 import QtCore, QtWidgets
import time


PORT = 8000


def selected_menu(menu):
    return {
        1: "Sync_Simulation",
        2: "Performance_Analysis"
    }.get(menu, "Error")


if __name__ == "__main__":
    simulator = None

    NSV = NSVUi()
    params = NSV.start()

    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QDialog()
    dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)

    if selected_menu(params['flag']) is "Sync_Simulation":
        algorithm_file_path = params["file_path"]
        number_of_node = params["number_of_nodes"]
        zone_range = params["zone_range"]

        simulator = Simulator()
        simulator.make_node_threads(number_of_node)
        while True:
            if False not in simulator.get_thread_is_running():
                break
            time.sleep(0.1)

        simulator.show(dialog, algorithm_file_path, app)
        simulator.run_algorithm(algorithm_file_path, number_of_node, zone_range)

    if selected_menu(params['flag']) is "Performance_Analysis":
        result_data_path = params["file_path"]
        analyzer = Analyzer(result_data_path)
        if analyzer.show_result_data():
            analyzer.start(dialog)
            app.exec_()
