from GUI.NSV_First_Dialog import NSVUi
from NODE.AccessNode import run_node_proc


def selected_menu(param_len):
    return {
        1: "Performance_Analysis",
        2: "Sync_Simulation"
    }.get(param_len, "Error")


if __name__ == "__main__":
    NSV = NSVUi()
    params = NSV.start()

    if selected_menu(len(params)) is "Sync_Simulation":
        algorithm_file_path = params["file_path"]
        number_of_node = params["number_of_nodes"]
        nodes_init_data = run_node_proc(number_of_node)

    if selected_menu(len(params)) is "Performance_Analysis":
        result_data_path = params["file_path"]
