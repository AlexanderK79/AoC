blTesting = False
Debug = True
day='18'
part='2'

if blTesting:
    with open(f'{day}-sample-input{part}.txt', 'r') as file: data = file.read().split('\n')
    # with open(f'{day}-sample-input2.txt', 'r') as file: data = file.read().split('\n')
else:
    with open(f'{day}-Alexander-input.txt', 'r') as file: data = file.read().split('\n')


def AoCMath(inputstr):
    # process the string left to right
    if '(' in inputstr or ")" in inputstr:
        print ("Something's wrong")
        quit
    answer = 0
    op='+'
    num=''
    for c in inputstr:
        if c in ('+', '*'):
            # process the prev operation
            if op == '+':
                answer += int(num)
            elif op == '*':
                answer *= int(num)
            op = c
            num = ''
        else:
            num += c
    # process the last operation
    if op == '+':
        answer += int(num)
    elif op == '*':
        answer *= int(num)
    
    return(answer)

def AoCMathPart2(inputstr):
    # process the string left to right, but process the additions first
    # split at the * put brackets around the other parts and then do a normal evaluation
    inputstr = inputstr.split('*')
    inputstr = '(' +')*('.join(inputstr)+')'
    answer = eval(inputstr)
    return(answer)



assignment = {}

# process each line
for linenum, line in enumerate(data):
    if blTesting:
        instruction, result = line[:-1].split(' becomes ')
        result = int(result)
    else:
        instruction=line
        result = 0
    # split the instruction to separate factors
    # example     =5 +       (8 * 3 + 9  + 3 * 4 * 3)
    # will become =5 + (((((((8 * 3)+ 9) + 3)* 4)* 3 )))
    # 5+((8*3) + 9  + 3 * 4 * 3)
    # 5+(((8*3) + 9)  + 3 * 4 * 3)
    # 5+((((8*3) + 9)  + 3) * 4 * 3)
    # 5+(((((8*3) + 9)  + 3) * 4) * 3)
    # 5+((((((8*3) + 9)  + 3) * 4) * 3))
    # 
    # or find the innermost () and work your way out
    # how to make python interpret a math string
    # eval('string2eval') # unsafe for unclean input
    # https://stackoverflow.com/questions/2371436/evaluating-a-mathematical-expression-in-a-string

    # create an entry in the dict per line
    assignment[linenum] = {'orgstring': line, 'instruction': instruction, 'result': None}
    # create a function to split the instruction in parts of "( )" called a level
    level = 0 # https://stackoverflow.com/questions/524548/regular-expression-to-detect-semi-colon-terminated-c-for-while-loops/524624#524624
    if not assignment[linenum].get(level): assignment[linenum][level] = {'instruction': "", 'result': None}
    for c in assignment[linenum]['instruction']:
        if c == ' ': continue
        if c =='(':
            level += 1
            assignment[linenum][level] = {'instruction': "", 'result': None}
        elif c ==')':
            #calculate the result for the level and append it to the current level instruction
            assignment[linenum][level]['result'] = AoCMathPart2(assignment[linenum][level]['instruction'])
            level -= 1
            assignment[linenum][level]['instruction'] += str(assignment[linenum][level+1]['result'])
        else: assignment[linenum][level]['instruction'] += c
    # back at level 0... calc the result!
    assignment[linenum]['result'] = AoCMathPart2(assignment[linenum][level]['instruction'])


    # create a function that calculates each level "( )" or traverses into a new one
    # loop through the dict from the deepest it's way up

    

answer = sum(assignment[x]['result'] for x in assignment.keys())
print (f'The answer to part {part} of day {day} is: {answer} and in test should be 693942')


