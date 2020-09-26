def convert_string_to_list(ini_list):

    ini_list = ini_list.replace('"', '')
    ini_list = ini_list[1:-1]
    # print(ini_list)
    # print(ini_list,type(ini_list))
    res = ini_list.split('],[')
    # print(res, type(res))
    for x in range(len(res)):
        if res[x].startswith('['):
            res[x] = res[x][1:]
            # print("if ",res[x])

        if res[x].endswith(']'):
            res[x] = res[x][:-1]
            # print("else ", res[x])
        # print(res[x],type(res[x]))

        ele = res[x].split(",")
        res[x] = ele
        # print(res[x],type(res[x]))
    # print(res)
    # print(len(res))
    return res
# print(convert_string_to_list())