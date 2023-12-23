f = open('input/10_sample.txt', 'r+')
f = open('input/10.txt', 'r+')
inputFile = f.read().splitlines()
f.close()

debug = True

tagChars = {
    '(': {'counterpart': ')', 'type': 'open' }, 
    ')': {'counterpart': '(', 'type': 'close', 'errorpoints': 3, 'acpoints': 1}, 
    '[': {'counterpart': ']', 'type': 'open' }, 
    ']': {'counterpart': '[', 'type': 'close', 'errorpoints': 57, 'acpoints': 2}, 
    '{': {'counterpart': '}', 'type': 'open' }, 
    '}': {'counterpart': '{', 'type': 'close', 'errorpoints': 1197, 'acpoints': 3}, 
    '<': {'counterpart': '>', 'type': 'open' }, 
    '>': {'counterpart': '<', 'type': 'close', 'errorpoints': 25137, 'acpoints': 4}
    }


errorScore = 0
acScore = []
for line in inputFile:
    corruptLine = False
    acLineScore = 0
    acString = ''
    i, level = 0, 0
    lineLevel = ['start']
    for char in list(line):
        # print(char)
        if tagChars[char]['type'] == 'open':
            level += 1
            if len(lineLevel)-1 < level:
                lineLevel.append(char)
            else:
                lineLevel[level] = char
        elif tagChars[char]['type'] == 'close':
            # if debug: print('closing', char, 'position', i, 'stringpart', line[:i])
            if tagChars[char]['counterpart'] == lineLevel[level]:
                # if debug: print('correct closing tag')
                pass
            else:
                print('incorrect tag... expected:', tagChars[lineLevel[level]]['counterpart'], ', but found: ', char)
                errorScore += tagChars[char]['errorpoints']
                corruptLine = True
                break
            lineLevel.pop(level)
            level -= 1

        i += 1
    # end of line reached, now close
    if not corruptLine:
        if debug: print(level)
        while level > 0:
            acString += tagChars[lineLevel[level]]['counterpart']
            acLineScore = (5*acLineScore) + tagChars[tagChars[lineLevel[level]]['counterpart']]['acpoints']
            lineLevel.pop(level)
            level -= 1
        acScore.append(acLineScore)


print('The answer to part 1 is: ', errorScore, 'expecting: 26397')
# Autocomplete tools are an odd bunch: the winner is found by sorting all of the scores and then taking the middle score. (There will always be an odd number of scores to consider.)

print('The answer to part 2 is', sorted(acScore)[len(acScore)//2])