
def string_parser(data, option=None):
    result = []
    data = data.replace(" ", "")
    if option is not None:
        temp = data.split(",")
        agent_a = int(temp[0][1:])
        agent_b = int(temp[1])
        data = str.join(",", temp[2:])
        temp = data[1:]
    else:
        temp = data[2:]

    temp = temp[:len(temp)-2]
    for i in temp.split("],["):
        temp_list = []
        for j in i.split(","):
            temp_list.append(int(j))
        result.append(temp_list)

    if option is not None:
        return agent_a, agent_b, result
    else:
        return result


def json_parser(_log_file):
    json_list = {}
    i = 0
    while True:
        line = _log_file.readline()
        line = line.rstrip('\n')

        if not line:
            break

        line_list = line.split("|")
        temp_list = {}
        temp_list['Time'] = line_list[0]
        temp_list['Cmd'] = line_list[1]
        temp_list['From'] = line_list[2]
        temp_list['To'] = line_list[3]
        temp_list['Msg'] = line_list[4]

        json_list[i] = temp_list
        i += 1
    return json_list