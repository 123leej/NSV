
def string_parser(data):
    result = []
    temp = data[2:]
    temp = temp[:len(temp)-2]
    temp = temp.replace(" ", "")
    for i in temp.split("],["):
        temp_list = []
        for j in i.split(","):
            temp_list.append(int(j))
        result.append(temp_list)
    return result