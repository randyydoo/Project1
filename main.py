def toFloat(time: str) -> float:
    time = time.replace(':', '.')
    return float(time)

def floatToTime(f: float) -> float:
    decimal = f - int(f)
    if decimal > .60:
        remainder = decimal - .60
        return (1 + int(f)) + remainder

    return f

def greedy(input1: list[list[str, str]], act1: list[str,str], input2: list[list[str,str]], act2: list[str, str]) -> list[list[str, str]]:
    # check if daily activties have an open interval
    act1[0], act1[1] = toFloat(act1[0]), toFloat(act1[1])
    act2[0], act2[1] = toFloat(act2[0]), toFloat(act2[1])

    if act1[1] < act2[0] or act2[1] < act1[0]:
        return []

    # initalize start and end time for both person's
    interval = [max(act1[0], act2[0]), min(act1[1], act2[1])]

    # replace all values in inputs to floats for comparison
    for i in range(len(input1)):
        start, end = input1[i][0], input1[i][1]
        start, end = toFloat(start), toFloat(end)
        input1[i][0], input1[i][1] = start, end

    for i in range(len(input2)):
        start, end = input2[i][0], input2[i][1]
        start, end = toFloat(start), toFloat(end)
        input2[i][0], input2[i][1] = start, end
    

    # sort by end time
    input1 = sorted(input1, key=lambda x: x[1])
    input2 = sorted(input2, key=lambda x: x[1])
    
    
    # find avaliable times in input1 and compare with input2
    start, end = interval[0], interval[0], interval[1]


    duration = float(duration)


     
greedy([['16:00', '18:00'], ['7:00', '8:30'], ['12:00', '13:00']], ['9:00', '19:00'], [['9:00', '10:30'], ['16:00', '17:00'], ['12:20', '13:30'], ['14:00', '15:00']], ['9:00', '18:30'])




