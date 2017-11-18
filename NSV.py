from Gui.NSV_First_Dialog import NSVUi
from Simulator import Simulator
from Exception.NSVExceptions import SimulationFinishException

PORT = 8000


def selected_menu(param_len):
    return {
        1: "Performance_Analysis",
        2: "Sync_Simulation"
    }.get(param_len, "Error")


if __name__ == "__main__":
    simulator = None
    
    NSV = NSVUi()
    params = NSV.start()

    if selected_menu(len(params)) is "Sync_Simulation":
        algorithm_file_path = params["file_path"]
        number_of_node = params["number_of_nodes"]
        zone_range = params["zone_range"]

        try:
            simulator = Simulator()
            simulator.make_node_threads(number_of_node)
            simulator.run_algorithm(algorithm_file_path, number_of_node, zone_range)

        except InterruptedError:
            simulator.stop_all_simulation(algorithm_file_path)

        except SimulationFinishException:
            simulator.stop_all_simulation(algorithm_file_path)

    if selected_menu(len(params)) is "Performance_Analysis":
        result_data_path = params["file_path"]
