import sys
from Gui.NSV_First_Dialog import NSVUi
from Simulator import Simulator
from Analyze_Result_Data import ShowResultDataUi
from Exception.NSVExceptions import SimulationFinishException
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

        try:
            simulator = Simulator(dialog)
            simulator.make_node_threads(number_of_node)
            time.sleep(10)
            simulator.run_algorithm(algorithm_file_path, number_of_node, zone_range)

        except InterruptedError:
            simulator.stop_all_simulation(algorithm_file_path)

        except SimulationFinishException:
            simulator.stop_all_simulation(algorithm_file_path)

    if selected_menu(params['flag']) is "Performance_Analysis":
        result_data_path = params["file_path"]
        analyze_result = ShowResultDataUi(dialog)

