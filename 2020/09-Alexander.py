

blTesting = False

if blTesting:
    with open('09-sample-input.txt', 'r') as file: data = file.read().split('\n')
    preAmbleLen = 5
else:
    with open('09-Alexander-input.txt', 'r') as file: data = file.read().split('\n')
    preAmbleLen = 25

i = 0
inputList = []

# build our inputList
for line in data:
    inputList.append([int(line),[]])
    for j in range(max(0, i-preAmbleLen), i):
        inputList[i][1].append(inputList[i][0] + inputList[j][0])
    i += 1

for i in range(preAmbleLen, len(inputList)):
    possibleNums = []
    for item in inputList[i-preAmbleLen:i]:
        possibleNums += item[1]
    if inputList[i][0] not in possibleNums:
        culpritNum = inputList[i][0]
        print(f'we found the culprit:  {culpritNum:>15}')
        break

# find a list of contiguous numbers that sums up to culpritNum; the weakness is the sum of the smallest and the largest

for i in range(0, len(inputList)):
    curSum = inputList[i][0]
    j = i
    while curSum <= culpritNum:
        j += 1
        curSum += inputList[j][0]
        if curSum == culpritNum:
            weaknessNums = []
            for k in inputList[i:j]:
                weaknessNums.append(k[0])
            weaknessNum = min(weaknessNums) + max(weaknessNums)
            print(f'we found the weakness: {weaknessNum:>15}')
            break



print ('hoi')
