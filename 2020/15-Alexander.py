blTesting = False
Debug = True
day='15'

if blTesting:
    with open(f'{day}-sample-input1.txt', 'r') as file: data = file.read().split('\n')
    # with open(f'{day}-sample-input2.txt', 'r') as file: data = file.read().split('\n')
else:
    with open(f'{day}-Alexander-input.txt', 'r') as file: data = file.read().split('\n')

# just take the index of a list
def part1(NumList, endTurn):
    if Debug:
        for curTurn in range(1, 4): print(f"Turn: {curTurn:>6}: {NumList[curTurn]:>8}")
    for curTurn in range(len(NumList), endTurn+1):
        lastCalledNumber = NumList[curTurn-1]
        if lastCalledNumber in NumList[1:-1]: # the number was spoken before
            lastCall_1 = len(NumList)-1 - NumList[::-1].index(lastCalledNumber) # x rounds ago for the last time
            diff       = 1 + NumList[:lastCall_1][::-1].index(lastCalledNumber) # y rounds ago the time before
            # it was called in a previous turn, call out the difference
            NumList.append(diff)
        else:
            NumList.append(0)
        if Debug: print(f"Turn: {curTurn:>6}: {NumList[-1]:>8}")
    return(NumList[endTurn])

def updatenumHist(numHist):
    # this function will take the current number and return a new numHist
    # numHist has the structure of a dict: numHist[number]=lastPos
    curNum = numHist['curNum']
    curTurn = numHist['curTurn']
    if curNum in numHist:
        numHist[curNum] = curTurn - numHist[curNum]
    else:
        numHist[curNum] = 0
    return numHist


def part2(NumList, startIndex, endTurn):
    numHist = {} # this stores in which turn the specified number was called 
    for i, n in enumerate(NumList[1:startIndex]):
        numHist[n] = {'t': i+1, 'pt': 0}
    del (i,n)

    for turn in range(startIndex, endTurn+1):
        lastCalledNumber = NumList[turn-1]
        # the number is in the dict, check if prevturn > 0
        if numHist[lastCalledNumber]['pt'] == 0:
            # the call in the previous turn was the first time it was called
            CallNumber = 0
        else:
            CallNumber = turn-1 - numHist[lastCalledNumber]['pt']

        if CallNumber in numHist:
            numHist[CallNumber] = {'t': turn, 'pt': numHist[CallNumber]['t']}
        else: numHist[CallNumber] = {'t': turn, 'pt': 0}

        NumList[turn] = CallNumber

        
    return(NumList[endTurn])

for line in data:
    NumList = [None]+[int(x) for x in line.split(',')]
    # answer = part1(NumList, 100)
    # print (f'The answer to part 1 of day {day} for {NumList[1:4]} is: {answer}')

# part 2
maxTurn = 2020
maxTurn = 30000000
for line in data:
    NumList = [None]+[int(x) for x in line.split(',')]
    startIndex = len(NumList)
    # redimension the NumList, to fit the maxTurn
    NumList = NumList + (maxTurn - len(NumList)+1) * [None]
    answer = part2(NumList, startIndex, maxTurn)
    print (f'The answer to part 2 of day {day} for {NumList[1:4]} is: {answer}')

