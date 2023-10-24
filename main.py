def toFloat(time: str) -> float:
    time = time.replace(':', '.')
    return float(time)

def timeAddition(time: float, duration: float) -> float:
    remainder = (time - int(time)) + duration
    if remainder >= .60:
        res = (1 + int(time)) + (remainder - .60)
        return res 

    return time + duration


def greedy(input1: list[list[str, str]], act1: list[str,str], input2: list[list[str,str]], act2: list[str, str], duration: int) -> list[list[str, str]]:
    # check if daily activties have an open interval
    act1[0], act1[1] = toFloat(act1[0]), toFloat(act1[1])
    act2[0], act2[1] = toFloat(act2[0]), toFloat(act2[1])

    if act1[1] < act2[0] or act2[1] < act1[0]:
        return []

    # initalize start and end time for both person's and change duration to float
    interval = [max(act1[0], act2[0]), min(act1[1], act2[1])]
    duration =  duration / 100

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
    start, end = interval[0], interval[1]
    temp1, temp2 = [], []
    prev_start1, prev_start2 = start, start
    for i in range(len(input1)-1):
        curr_end1 = input1[i][1]
        nxt_start1 = input1[i+1][0]
        # use max function to take care of intervals not being after agreed start time edge case
        prev_start1 = max(prev_start1, curr_end1)
        # check if (start + duration) < nxt_start -> if (nxt_start - duration) <= (prev_staart + duration) -> only 1 meeting allowed
        shortest_meeting = timeAddition(prev_start1, duration)
        if shortest_meeting <= nxt_start1:
            temp1.append([prev_start1, nxt_start1])

    for i in range(len(input2)-1):
        curr_end2 = input2[i][1]
        nxt_start2 = input2[i+1][0]
        # use max function to take care of intervals not being after agreed start time edge case
        prev_start2 = max(prev_start2, curr_end2)
        # check if (start + duration) < nxt_start
        shortest_meeting = timeAddition(prev_start2, duration)
        if shortest_meeting <= nxt_start2:
            temp2.append([prev_start2, nxt_start2])


    # consider edge case of last activity end time and add to lists
    last_sched1, last_sched2 = input1[-1][1], input2[-1][1]
    if timeAddition(last_sched1, duration) <= end:
        temp1.append([last_sched1, end])

    if timeAddition(last_sched2, duration) <= end:
        temp2.append([last_sched2, end])

    # check for overlaps
    res = []
    for start1,end1 in temp1:
        for start2,end2 in temp2:
            if (start1 <= end2) and (end1 >= start2):
                begin, stop = max(start1,start2), min(end1,end2)
                res.append([begin,stop])

    print(res)


greedy([['16:00', '18:00'], ['7:00', '8:30'], ['12:00', '13:00']], ['9:00', '19:00'], [['9:00', '10:30'], ['16:00', '17:00'], ['12:20', '13:30'], ['14:00', '15:00']], ['9:00', '18:30'], 30)
