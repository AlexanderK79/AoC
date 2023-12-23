import argparse
import re

class messages:
    def __init__(self, fMessages):
        self.maxLen = max([len(i) for i in fMessages])
        self.content = fMessages

class rulebase:
    possibleValues = list()
    def __init__(self, fRules, fMaxLen):
        self.maxLen = fMaxLen
        self.rules = len(fRules) * [None]
        self.rules = (list(map(rule, len(fRules) * [self], fRules)))
        pass

class rule():
    possibleValues = list()
    def __init__(self, parent, fLine):
        regex = re.match('(\d+):(.*)', fLine.strip() )
        self.id = int(regex.groups()[0])
        if re.match('.*"(.+)".*', regex.groups()[1]):
            self.value = re.match('.*"(.+)".*', regex.groups()[1]).groups()[0]
            parent.rules[self.id] = self
        else:
            #self.possibleValues.append()
            for i in regex.groups()[1].split('|'):
                for j in i.strip().split(' '):
                    print(parent.rules[int(j)].value)
                    pass
            pass
        pass

def main(stdscr):
    with open(fName, 'r+') as f:
        fileContent = f.read().splitlines()
        AllMessages = messages([line for line in fileContent if not re.match('(^\d+:)|(^$)', line.strip())])
        AllRules = rulebase([line for line in fileContent if re.match('(^\d+:)', line.strip())], AllMessages.maxLen)
        del fileContent

        #data = list(map(rulebase, [for line in f.read().splitlines()) if re.match('^\d+:', line.strip())] )
    result = 0
    message = f'The answer to part 1 is (sample should be 14897079, answer should be 11288669): {result}'
    print(message)
     # process groups of three
    message = f'The answer to part 2 is (sample should be 4, answer should be 870): {result}'
    print (message) 

# globals
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose"   , action="store_true", default=False, help="Add this to enable verbose output")
parser.add_argument("-d", "--draw"      , action="store_true", default=False, help="Add this to enable drawing")
parser.add_argument("-i", "--drawinterval", type=int, default=1, help="Add the value in ms for drawing interval")
parser.add_argument("-p", "--production", action="store_true", default=False, help="Add this to try the puzzle input")
args = parser.parse_args()

day = '19'
fName = f'2020/{day}-sample-input1.txt'
if args.production: fName = f'2020/{day}-Alexander-input.txt'

debug = args.verbose
draw = args.draw

main(None)