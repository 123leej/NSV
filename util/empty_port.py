port_list = [20000, 20001, 20002, 20003, 20004, 20005, 20006, 20007, 20008, 20009, 20010, 20011, 20012, 20013, 20014,
             20015, 20016, 20017, 20018, 20019]

in_use_port = []


def get_port():
    idx = 0
    while port_list[idx] in in_use_port:
        idx = idx + 1
    in_use_port.append(port_list[idx])
    return port_list[idx]


def release_port(port):
    del in_use_port[in_use_port.index(port)]
