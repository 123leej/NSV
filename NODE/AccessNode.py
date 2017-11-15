import subprocess


def run_node_proc(nodes):
    nodes_data = {}
    for i in range(1, int(nodes)+1):
        node_run_port = subprocess.check_output("python NODE/node.py " + str(i), shell=True)
        nodes_data['node'+str(i)] = {"port": node_run_port}
        print(i)

    return nodes_data
