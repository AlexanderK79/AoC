from itertools import product 

blTesting = False
Debug = True
day='19'
part='1'

if blTesting:
    with open(f'2020/{day}-sample-input{part}.txt', 'r') as file: data = file.read().split('\n')
    # with open(f'{day}-sample-input2.txt', 'r') as file: data = file.read().split('\n')
else:
    with open(f'2020/{day}-Alexander-input.txt', 'r') as file: data = file.read().split('\n')


# parse the input file into a dict of rules and values
# parse the messages into a list
rulebase = {}
rulebase['posVals'] = []
messages = []
for line in data:
    if ':' in line:
        rulenum, item = map(str.strip, line.split(':'))
        if '"' in item:
            rulebase[rulenum]= {'value': item.replace('"', '')}
        else:
            rulebase[rulenum]= {'rule': item}
    else:
        message = line.strip()
        if message == '': continue
        messages.append(message)

# Your goal is to determine the number of messages that completely match rule 0.

def productListOfLists (LoL):
    # this function takes a list of lists as it's input and returns a unique list of every product as joined strings
    result = False
    for L in LoL:
        if not result:
            result = L
            if not type(L) is list:
                return(LoL)
        else:
          result = product(result, L)
          result = list(set(map(''.join, result)))
    return (result)

def calc_posVals(d, rule):
    posVals = d[rule].get('posVals', [])
    value = d[rule].get('value', False)
    if len(posVals) > 0:
        # there are posVals, append them to the main posVals
            # how do I know if all the posVals for this rule are completed?
        d['posVals'].append(posVals)
        d['posVals'] = list(set(d['posVals']))
    elif value:
        # this is a value, but I don't know why I get here actually
        #return (d)
        pass
    elif len(posVals) < 0 and d[rule].get('rule', False):
        #impossible to get here
        pass
    
    if d[rule].get('rule', False):
        # we are in a rule
        # now process it into the elements Rule (R), RulePart (RP), RPI (RPI), RuleValues (RV), RulePartValues (RPV), RPIValues (RPIV)
        if not d[rule].get('posVals', False): d[rule]['posVals'] = [] # init an empty list if it does not exist
        RV = d[rule]['posVals']
        RPV = [] # before processing every rulepart value, make sure we have an empty list
        for RP in d[rule]['rule'].split('|'):
            RPIV = [] # before processing every RPI value, make sure we have an empty list
            for RPI in map(str.strip, RP.strip().split(' ')):
                RPIV_vals = d[RPI].get('value', d[RPI].get('posVals', False))
                while not RPIV_vals:
                    # recurse any further down the rabbit hole from this RPI onward
                    calc_posVals(d, RPI)
                    RPIV_vals = d[RPI].get('value', d[RPI].get('posVals', False))
                RPIV.append(list(RPIV_vals)) # add the value or a list possible values to this RPIV; a list of values for every RPI
                pass
            # calc the product of the list of RPIV's to get the RPV
            RPV += productListOfLists(RPIV) # this should be a list of possible values for this part
            #RPV = list(set(RPV))
        # calc the product of the list of RPV's to get the RV
        RV += productListOfLists(RPV)
        RV = list(set(RV))
        d[rule]['posVals'] = RV
    return (d)

# build a list of possible valid messages (hopefully it fits in memory)
rulebase = calc_posVals(rulebase, '0')

answer = len(set(messages).intersection(rulebase['0']['posVals']))
print (f'The answer to part {part} of day {day} is: {answer} and in test should be 2')


