# read instructions
# ordered list of instruction quarters instruction, num, step, acc

import copy

with open('08-sample-input.txt', 'r') as file: data = file.read().split('\n')
with open('08-Alexander-input.txt', 'r') as file: data = file.read().split('\n')

def runCode(inputListProg):
    acc, pos, step = 0, 0, 0
    validProgram  = True
    while validProgram and pos < len(inputListProg):

        if inputListProg[pos][3] is not None:
            print(f'infinite loop! with accumulator at {acc}')
            validProgram = False
        elif(inputListProg[pos][0] == 'acc'):
            acc += inputListProg[pos][1]
            inputListProg[pos][2] = step
            inputListProg[pos][3] = acc
            pos += 1
            step += 1
        elif(inputListProg[pos][0] == 'jmp'):
            inputListProg[pos][2] = step
            inputListProg[pos][3] = acc
            pos += inputListProg[pos][1]
            step += 1
        elif(inputListProg[pos][0] == 'nop'):
            inputListProg[pos][2] = step
            inputListProg[pos][3] = acc
            pos += 1
            step += 1
        else:
            print ('Why do we get here?')

    return (acc, validProgram)


orgListProg = []

for line in data:
    orgListProg.append([line.split()[0]] + [int(line.split()[1])] + [None] + [None])

# accumulator = stepcount

# run through the list
listProgTmp = copy.deepcopy(orgListProg)

curReplace = 0
while not runCode(copy.deepcopy(listProgTmp))[1]:
    listProgTmp = copy.deepcopy(orgListProg)
    # find every occurence of nop or jmp
    while curReplace < len(listProgTmp):
        if listProgTmp[curReplace][0] == 'nop' and listProgTmp[curReplace][1] != 0:
            listProgTmp[curReplace][0] = 'jmp'
            curReplace += 1
            break
        elif listProgTmp[curReplace][0] == 'jmp':
            listProgTmp[curReplace][0] = 'nop'
            curReplace += 1
            break
        else:
            curReplace += 1

if runCode(copy.deepcopy(listProgTmp))[1]:
    print(f'Found a succesfull program that exited with accumulator at {runCode(copy.deepcopy(listProgTmp))[0]}')
else:
    print ('No valid program found')

# print('hoi')