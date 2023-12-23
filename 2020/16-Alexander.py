import pandas as pd

blTesting = False
Debug = True
day='16'
part='2'

if blTesting:
    with open(f'{day}-sample-input{part}.txt', 'r') as file: data = file.read().split('\n')
    # with open(f'{day}-sample-input2.txt', 'r') as file: data = file.read().split('\n')
else:
    with open(f'{day}-Alexander-input.txt', 'r') as file: data = file.read().split('\n')

# parse the input 
# determine the type of line
allValidNumbers = set()
ValidTickets = []
ValidClasses = {}
ScanningErrorRate = 0
for line in data:
    if len(line)==0: continue
    items = line.split(':')
    if len(items)>1:
        className = items[0].strip()
        ValidClasses[className] = {'ranges': [], 'possibleCols': []}
        ranges = items[1].split(' or ')
        if len(ranges)>1:
            for itemRange in ranges:
                LowLimit = int(itemRange.split('-')[0])
                UpperLimit = int(itemRange.split('-')[1])
                allValidNumbers.update(range(LowLimit, UpperLimit+1))
                ValidClasses[className]['ranges'].append({'L': LowLimit, 'U': UpperLimit, 'nums': range(LowLimit, UpperLimit+1)})

    elif className == 'your ticket':
        myTicket = tuple(map(int, line.split(',')))
    elif className == 'nearby tickets':
        curTicket = tuple(map(int, line.split(',')))
        invalidNums = set(curTicket) - allValidNumbers
        if len(invalidNums) == 0:
            ValidTickets.append((curTicket))
        else:
            ScanningErrorRate += sum(invalidNums)

    else:
        pass
ValidClasses.pop('your ticket')
ValidClasses.pop('nearby tickets')

answer = ScanningErrorRate
print (f'The answer to part {part} of day {day} is: {answer}')

# part 2
# find the correct field order
# create pandas df from ValidTickets
# process every className; count the number of rows that fit between the upper and lowerbound of the class
# if this the same as the total number of rows, we have a (possible?!) hit; change the column accordingly
dfValidTickets = pd.DataFrame(ValidTickets)
totalcount = dfValidTickets.shape[0]
foundCols = []
for item in ValidClasses:
    totalRange = set()
    for curRange in ValidClasses[item]['ranges']:
        #print (item, curRange['nums'])
        totalRange.update(set(curRange['nums']))

    possibleCols = []
    validCols = 0
    for col in dfValidTickets:
        if totalcount == dfValidTickets[dfValidTickets[col].isin(list(totalRange))].shape[0]:
            if not col in foundCols:
                ValidClasses[item]['possibleCols'].append(col)
            validCols += 1
            validCol = col
            print(f"Possible match for {item:>20} = {col:>8}")
    if validCols == 1:
        print (f"one match for {item} {validCol}")
        ValidClasses[item]['possibleCols'] = [validCol]
        # remove the entry from other possibleCols and put it in the foundCols
        foundCols.append(validCol)
        for i in ValidClasses:
            if validCol in ValidClasses[i]['possibleCols']:
                if not i == item: ValidClasses[i]['possibleCols'].remove(validCol) 

while len(foundCols) < dfValidTickets.shape[1]:
    for i in ValidClasses:
        if len(ValidClasses[i]['possibleCols']) > 1:
            ValidClasses[i]['possibleCols'] = [j for j in ValidClasses[i]['possibleCols'] if j not in foundCols]
        if len(ValidClasses[i]['possibleCols']) == 1:
            if not ValidClasses[i]['possibleCols'][0] in foundCols:
                foundCols.append(ValidClasses[i]['possibleCols'][0])


answer = 1
print(myTicket)
for i in ValidClasses:
    if i[:len('departure')] == 'departure':
    #if 'a' in i:
        print(i, ValidClasses[i]['possibleCols'][0], myTicket[ValidClasses[i]['possibleCols'][0]])
        answer *= myTicket[ValidClasses[i]['possibleCols'][0]]


print('hoi', answer)
# dfValidTickets[((dfValidTickets >= 0) & (dfValidTickets<=1)|(dfValidTickets >=4) & (dfValidTickets<=19))]



