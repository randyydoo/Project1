def toFloat(time: str) -> float:
    time = time.replace(':', '.')
    return float(time)

def timeAddition(time: float, duration: float) -> float:
    remainder = (time - int(time)) + duration
    time = int(time)
    while remainder >= .60:
        time += 1
        remainder -= .60
     
    return round(time + remainder, 2)

def getMaxEnd(time: float, duration: float, end: float, interval_end: float) -> float:
    next_time = timeAddition(time, duration)

    if next_time > end or next_time > interval_end:
        return time 

    return getMaxEnd(next_time, duration, end, interval_end)

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
         
    # combine and sort by end time
    joined = input1 + input2
    joined = sorted(joined, key=lambda x: x[1])

    # check for overlaps
    start, end = interval[0], interval[1]
    i, res = 0, []
    # check for start -> earliest
    if timeAddition(start, duration) <= joined[0][0]:
        res.append([start, getMaxEnd(start, duration, joined[0][0], end)])

    while i < len(joined)-1:
        curr_start, curr_bound = joined[i][0], joined[i][1]
        max_meeting_time = getMaxEnd(curr_start, duration, curr_bound, end)

        next_start, next_bound = joined[i+1][0], joined[i+1][1]
        max_meeting_time2 = getMaxEnd(next_start, duration, next_bound, end)
        
        max_start, min_bound, max_bound = max(curr_start, next_start), min(curr_bound,next_bound), max(curr_bound, next_bound)
        max_end = getMaxEnd(max_start, duration, min_bound, end)
        
        shortest = timeAddition(curr_bound, duration)
        # check for overlap
        if curr_bound > next_start and max_end > max_start and not min_bound <= max_end <= max_bound and start <= max_end <= end and start <= max_start <= end:
                res.append([max_start,max_end])
                i += 2
        # check for next range with minumum duration
        elif shortest <= next_start and  shortest > curr_bound and start <= shortest <= end and start <= max_start <= end:
            res.append([curr_bound, getMaxEnd(curr_bound, duration, next_start, end)])
            i += 1
        else:
            i += 1

    # check for last -> end
    if timeAddition(joined[-1][1], duration) <= end:
        res.append([joined[-1][1], getMaxEnd(joined[-1][1], duration, end, end)])

    # convert back to time
    res = toString(res)
    print(f'Output: {res} \n')



def runTests() -> None:
    # tests will contain all the parameters to the greedy function in order with a length of 10
    
    tests = [
    [[], ['10:00', '20:00'], [], ['9:00', '21:00'], 90],
    [[['16:00', '18:00'], ['7:00', '8:30'], ['12:00', '13:00']], ['9:00', '13:00'], [['9:00', '10:30'], ['16:00', '17:00'], ['12:20', '13:30'], ['14:00', '15:00']], ['13:40', '18:30'], 100],
    [[], ['10:00', '20:00'], [['13:00', '16:00'], ['18:00', '18:45']], ['9:00', '21:00'], 90],
    [[['9:00', '12:00']], ['7:00', '23:00'], [['12:30', '13:00']], ['8:00', '23:30'], 60],
    [[], ['10:00', '20:00'], [['13:00', '16:00'], ['18:00', '18:45']], ['9:00', '21:00'], 90],
    [[['10:20', '12:45'], ['0:10', '2:40'], ['3:00','3:45'], ['6:25','8:20']], ['2:00', '20:00'], [['13:00', '16:00'], ['1:00','3:45'], ['6:25','8:20']], ['3:00', '21:00'], 210],
    [[['1:00', '3:59'], ['4:12', '5:30']], ['1:32', '5:00'], [['2:00', '4:01'], ['16:23', '18:53']], ['2:30', '5:00'], 1],
    [[['12:00', '13:30'], ['14:30', '15:00'], ['3:00', '5:00'], ['8:30','10:00']], ['0.00', '23:59'], [['16:12', '19:00']], ['0:00', '23:59'], 150],
    [[['11:00', '13:30'], ['20:00', '23:00'], ['7:00','8:30']], ['6.00', '17:00'],[['12:30', '14:45'], ['6:30', '9:00'],  ['16:16', '22:00']],['4:00', '16:30'], 90],
    [[['10:12', '11:13'], ['12:19', '12:45'], ['13:39', '13:50'], ['14:14','15:00'] , ['16:12', '17:00'], ['17:53', '18:11'], ['19:23', '19:51']], ['11:18', '20:12'], [['9:22', '9:55'], ['10:12', '12:31'], ['13:40', '14:09'], ['16:00', '16:21']],  ['8:22', '17:56'], 53]
    ]
    for i in range(len(tests)):
        if i == 0:
            print("EDGE CASE: NO INPUTS")
        if i == 1:
            print("EDGE CASE: DAILY ACTIVITES NOT VALID")
        input1, act1, input2, act2, duration = tests[i][0], tests[i][1], tests[i][2], tests[i][3], tests[i][4]
        greedy(input1,act1,input2,act2,duration)

runTests()
