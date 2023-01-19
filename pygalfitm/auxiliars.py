def string_times_x(string, x):
    res = ""
    for i in range(x): ## Use lambda instead
        res += "," + str(string) 
    return res[1: ]