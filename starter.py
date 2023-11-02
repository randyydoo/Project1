def toFloat(time: str) -> float:
    time = time.replace(':', '.')
    return float(time)

def timeAddition(time: float, duration: float) -> float:
    remainder = (time - int(time)) + duration
    time = int(time)
    while remainder >= .60:
        time = round(time+1, 2)
        remainder -= .60
     
    return round(time + remainder, 2)

def getMaxEnd(time: float, duration: float, end: float, interval_end: float) -> float:
    if timeAddition(time, duration) > end or timeAddition(time, duration) > interval_end:
        return time

    time = timeAddition(time, duration)
    return getMaxEnd(time, duration, end, interval_end)

def toString(res: list[list[float, float]]):
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
    return res

def printCases(input1: list[list[str, str]], act1: list[str,str], input2: list[list[str,str]], act2: list[str, str], duration: int, interval: list[str]) -> None:
    print(f'Person 1 Activities: {input1}')
    print(f'Person 2 Activities: {input2}')
    print(f'Person 1 Daily Activities: {act1} ')
    print(f'Person 2 Daily Activities: {act2}')
    print(f'Duration: {duration} minutes')
    print(f'Interval: {interval}')
    return



def greedy(input1: list[list[str, str]], act1: list[str,str], input2: list[list[str,str]], act2: list[str, str], duration: int) -> None:
    # check if daily activties have an open interval
    temp_act1, temp_act2 = act1.copy(), act2.copy()
    act1[0], act1[1] = toFloat(act1[0]), toFloat(act1[1])
    act2[0], act2[1] = toFloat(act2[0]), toFloat(act2[1])

    # get latest start time and earliest end time
    interval = [max(act1[0], act2[0]), min(act1[1], act2[1])]
    start1, start2 = str(interval[0]), str(interval[1])
    start1, start2 = start1.replace('.', ':'), start2.replace('.', ':')
    if (start1[1] == ':' and len(start1) == 3) or (start1[2] == ':' and len(start1) == 4):
        start1 += '0'
    if (start2[1] == ':' and len(start2) == 3) or (start2[2] == ':' and len(start2) == 4):
        start2 += '0'

    # print test cases
    printCases(input1, temp_act1, input2, temp_act2, duration, [start1, start2])


    # check edge case if activites have no slots in common
    if interval[0] > interval[1]:
        print(f'Output: {[]} \n')
        return

    # check edge case of both persons free all day
    if not input1 and not input2:
        print(f'Output: {[start1, start2]}\n')
        return

    # initalize start and end time for both person's and change duration to float
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

    # check for edge case if input is None
    if not input1:
        temp1.append([start,end])
    elif timeAddition(start, duration) <= input1[0][0]:
        temp1.append([start, input1[0][0]])

    if not input2:
        temp2.append([start, end])
    elif timeAddition(start, duration) <= input2[0][0]:
        temp2.append([start, input2[0][0]])


    for i in range(len(input1)-1):
        curr_end1 = input1[i][1]
        nxt_start1 = input1[i+1][0]
        # check if shortest meeting is less than next start time and less than end
        shortest_meeting = timeAddition(curr_end1, duration)
        if start <= curr_end1 <= end and nxt_start1 >= shortest_meeting <= end:
            temp1.append([curr_end1, nxt_start1])


    for i in range(len(input2)-1):
        curr_start2, curr_end2 = input2[i][0], input2[i][1]
        nxt_start2 = input2[i+1][0]
        shortest_meeting = timeAddition(curr_end2, duration)
        # check if shortest meeting is less than next start time and less than end 
        if start <= curr_end2 <= end and nxt_start2 >= shortest_meeting <= end:
            temp2.append([curr_end2, nxt_start2])


    # consider edge case of last activity end time and add to lists
    if input1 and start <= input1[-1][1] <= end and start <= timeAddition(input1[-1][1], duration) <= end:
        temp1.append([input1[-1][1], end])

    if input2 and start <= input2[-1][1] <= end and start <= timeAddition(input2[-1][1], duration) <= end:
        temp2.append([input2[-1][1], end])

    # join and sort both lists containing avaliable slots for both individuals
    joined = temp1 + temp2
    joined = sorted(joined, key=lambda x: x[1])

    # check for overlaps
    i, res = 0, []
    while i < len(joined):
        curr_start, curr_bound = joined[i][0], joined[i][1]
        max_meeting_time = getMaxEnd(curr_start, duration, curr_bound, end)

        if i < len(joined)-1:
            next_start, next_bound = joined[i+1][0], joined[i+1][1]
            max_meeting_time2 = getMaxEnd(next_start, duration, next_bound, end)
        else:
            next_start, next_bound = None, None

        if next_start and curr_bound > next_start:
            max_start, min_bound = max(curr_start, next_start), min(curr_bound,next_bound)
            max_end = getMaxEnd(max_start, duration, min_bound, end)
            # check if minimum duration is valid
            if max_end > max_start:
                res.append([max_start,max_end])
            i += 2
        else:
            res.append([curr_start, max_meeting_time])
            i += 1

    # convert back to time
    res = toString(res)
    print(f'Output: {res} \n')



def runTests() -> None:
    # tests will contain all the parameters to the greedy function in order with a length of 10

    tests = [
    [[], ['10:00', '20:00'], [], ['9:00', '21:00'], 90],
    [[['16:00', '18:00'], ['7:00', '8:30'], ['12:00', '13:00']], ['9:00', '13:00'], [['9:00', '10:30'], ['16:00', '17:00'], ['12:20', '13:30'], ['14:00', '15:00']], ['13:40', '18:30'], 100],
    [[], ['10:00', '20:00'], [['13:00', '16:00'], ['18:00', '18:45']], ['9:00', '21:00'], 90],
    [[['16:00', '18:00'], ['7:00', '8:30'], ['12:20', '13:00']], ['9:00', '19:00'], [['9:00', '10:30'], ['16:00', '17:00'], ['12:20', '13:30'], ['14:00', '15:00']], ['9:00', '18:30'], 60],
    [[['9:00', '12:00']], ['7:00', '23:00'], [['12:30', '13:00']], ['8:00', '23:30'], 60],
    [[], ['10:00', '20:00'], [['13:00', '16:00'], ['18:00', '18:45']], ['9:00', '21:00'], 90],
    [[['10:20', '12:45'], ['0:10', '2:40'], ['3:00','3:45'], ['6:25','8:20']], ['2:00', '20:00'], [['13:00', '16:00'], ['18:00', '18:45'], ['1:00','3:45'], ['6:25','8:20']], ['3:00', '21:00'], 240],
    [[['1:00', '3:59'], ['4:12', '5:30']], ['1:32', '5:00'], [['2:00', '4:01'], ['16:23', '18:53']], ['2:30', '5:00'], 1],
    [[['12:00', '13:30'], ['14:30', '15:00'], ['3:00', '5:00'], ['8:30','10:00']], ['0.00', '23:59'], [['16:12', '19:00']], ['0:00', '23:59'], 150],
    [[['11:00', '13:30'], ['20:00', '23:00'], ['7:00','8:30']], ['6.00', '17:00'],[['12:30', '14:45'], ['6:30', '9:00'],  ['16:16', '22:00']],['4:00', '16:30'], 90],
    [[['11:26', '13:13'], ['8:50', '10:37'], ['16:11', '16:58']], ['10:19', '17:32'], [['8:20', '9:10'], ['9:48', '10:32'], ['11:12', '12:17'], ['13:12', '14:00']], ['7:05', '14:33'], 37],
    [[['10:12', '11:13'], ['12:19', '12:45'], ['13:39', '13:50'], ['14:14','15:00'] , ['16:12', '17:00'], ['17:53', '18:11'], ['19:23', '19:51']], ['11:18', '20:12'], [['9:22', '9:55'], ['10:12', '12:31'], ['13:40', '14:09'], ['16:00', '16:21']],  ['8:22', '17:56'], 53],
[[['9:02', '11:19'], ['12:13', '13:51'], ['14:33', '15:52'], ['16.36','17:36'], ['17:52', '18:20']], ['7:31', '19:18'],[['8:18', '10:19'], ['11:09', '12:11'], ['13:12', '14:08'], ['16:50', '17:32'], ['18:12', '19:05']],['6:32', '19:32'], 43]
    ]

    for i in range(len(tests)):
        input1, act1, input2, act2, duration = tests[i][0], tests[i][1], tests[i][2], tests[i][3], tests[i][4]
        greedy(input1,act1,input2,act2,duration)

runTests()
