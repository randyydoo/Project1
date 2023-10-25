def toFloat(time: str) -> float:
    time = time.replace(':', '.')
    return float(time)

def timeAddition(time: float, duration: float) -> float:
    remainder = (time - int(time)) + duration
    time = int(time)
    while remainder >= .60:
        time += 1
        remainder -= .60
     
    return float(time + remainder)

def greedy(input1: list[list[str, str]], act1: list[str,str], input2: list[list[str,str]], act2: list[str, str], duration: int) -> None:
    print(f'Person 1 Activities: {input1} ')
    print(f'Person 1 Daily Activies: {act1} ')
    print(f'Person 2 Activities: {input2} ')
    print(f'Person 2 Daily Activies: {act2}')
    print(f'Duration: {duration}')

    # check if daily activties have an open interval
    act1[0], act1[1] = toFloat(act1[0]), toFloat(act1[1])
    act2[0], act2[1] = toFloat(act2[0]), toFloat(act2[1])
    

    # check edge case if activites have no slots in common
    if act1[0] >= act2[1] or act2[0] > act1[1]:
        print(f'Output: {[]} \n')
        return

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

    # compare prev_start with 0th index to check for edge case of input activities being length 1
    # check for edge case if input is None
    if not input1:
        temp1.append([start,end])
    elif timeAddition(start, duration) <= input1[0][0]:
        temp1.append([start, input1[0][0]])

    if not input2:
        temp2.append([start,end])
    elif timeAddition(start, duration) <= input2[0][0]:
        temp2.append([start, input2[0][0]])

    for i in range(len(input1)-1):
        curr_end1 = input1[i][1]
        nxt_start1 = input1[i+1][0]
        # check if (start + duration) < nxt_start -> if (nxt_start - duration) <= (prev_staart + duration) -> only 1 meeting allowed
        shortest_meeting = timeAddition(curr_end1, duration)
        if shortest_meeting <= nxt_start1:
            temp1.append([curr_end1, nxt_start1])

    for i in range(len(input2)-1):
        curr_end2 = input2[i][1]
        nxt_start2 = input2[i+1][0]
        # check if (start + duration) < nxt_start
        shortest_meeting = timeAddition(curr_end2, duration)
        if shortest_meeting <= nxt_start2:
            temp2.append([curr_end2, nxt_start2])


    # consider edge case of last activity end time and add to lists
    if input1 and timeAddition(input1[-1][1], duration) <= end:
        last_sched1 = timeAddition(input1[-1][1], duration)
        temp1.append([input1[-1][1], end])

    if input2 and timeAddition(input2[-1][1], duration) <= end:
        last_sched2 = timeAddition(input2[-1][1], duration)
        temp2.append([input2[-1][1], end])

    # check for overlaps
    res = []
    for start1,end1 in temp1:
        for start2,end2 in temp2:
            if (start1 <= end2) and (end1 >= start2):
                begin, stop = max(start1,start2), min(end1,end2)
                if stop - begin >= duration: 
                    res.append([begin,stop])

    # convert back to string
    for i in range(len(res)):
        start, end = res[i][0], res[i][1]
        start, end = str(start), str(end)
        start, end = start.replace('.', ':'), end.replace('.', ':')
        if start[1] == ':' and len(start) <= 3 or start[2] == ':' and len(start) <= 4:
            start += '0'
        if end[1] == ':' and len(end) <= 3 or end[2] == ':' and len(end) <= 4:
            end += '0'

        res[i][0], res[i][1] = start,end

    print(f'Output: {res} \n')



def runTests() -> None:
    # tests will contain all the parameters to the greedy function in order with a length of 10

    tests = [
    [[['16:00', '18:00'], ['7:00', '8:30'], ['12:00', '13:00']], ['9:00', '13:00'], [['9:00', '10:30'], ['16:00', '17:00'], ['12:20', '13:30'], ['14:00', '15:00']], ['13:40', '18:30'], 100],
    [[['16:00', '18:00'], ['7:00', '8:30'], ['12:00', '13:00']], ['9:00', '19:00'], [['9:00', '10:30'], ['16:00', '17:00'], ['12:20', '13:30'], ['14:00', '15:00']], ['9:00', '18:30'], 30],
    [[['9:00', '12:00']], ['7:00', '23:00'], [['12:30', '13:00']], ['8:00', '23:30'], 60],
    [[], ['10:00', '20:00'], [['13:00', '16:00'], ['18:00', '18:45']], ['9:00', '21:00'], 90]
    ]

    for i in range(4):
        input1, act1, input2, act2, duration = tests[i][0], tests[i][1], tests[i][2], tests[i][3], tests[i][4]
        greedy(input1,act1,input2,act2,duration)

runTests()
