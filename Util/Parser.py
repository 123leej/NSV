
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
