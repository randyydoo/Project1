def toFloat(time: str) -> float:
    time = time.replace(':', '.')
    return float(time)

def timeAddition(time: float, duration: float) -> float:
    remainder = (time - int(time)) + duration
    if remainder >= .60:
        res = (1 + int(time)) + (remainder - .60)
        return res 

    return time + duration

def timeSubtraction(time: float, duration: float) -> float:
    remainder = time - int(time)
    if time - duration < int(time):
        return (int(time) - 1) + (.60 - duration) + (remainder)

    return time - duration

# def getLatest(time: float, duration: float, ceiling: float) -> float:
#     curr = time
#     while 1:
#         if timeAddition(curr, duration) >= ceiling:
            # return curr

        # curr = timeAddition(time, duration)

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
        # check if (start + duration) < nxt_start
        if timeAddition(prev_start1, duration) < nxt_start1:
            temp1.append([prev_start1, timeSubtraction(nxt_start1,duration)])

    for i in range(len(input2)-1):
        curr_end2 = input2[i][1]
        nxt_start2 = input2[i+1][0]
        # use max function to take care of intervals not being after agreed start time edge case
        prev_start2 = max(prev_start2, curr_end2)
        # check if (start + duration) < nxt_start
        if timeAddition(prev_start2, duration) < nxt_start2:
            temp2.append([prev_start2, timeSubtraction(nxt_start2,duration)])

    # consider edge case of last activity end time and add to lists
    temp1.append([input1[-1][1], timeSubtraction(end, duration)])
    temp2.append([input2[-1][1], timeSubtraction(end, duration)])
    print(temp1) 
    print(temp2)

     
greedy([['16:00', '18:00'], ['7:00', '8:30'], ['12:00', '13:00']], ['9:00', '19:00'], [['9:00', '10:30'], ['16:00', '17:00'], ['12:20', '13:30'], ['14:00', '15:00']], ['9:00', '18:30'], 30)

