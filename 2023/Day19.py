import argparse
import re

class pipeLine:
    def __init__(self, fName, fParm) -> None:
        self.name = list()
        self.rules = []
        self.content = fParm
        for i, thisRule in enumerate(fParm.split(',')):
            regex = re.match('([xmas]{1})([<>]{1})(\d+):(.+)', thisRule)
            if regex is None:
                # this is the catch all rule
                self.rules.append(self.plRule(None, None, None, thisRule, i))
                pass
            else:
                thisAttr, thisOp, thisVal, thisDest = regex.groups()
                self.rules.append(self.plRule(thisAttr, thisOp, thisVal, thisDest, i))
    def process(self, fPart):
        thisResult = None
        while thisResult is None:
            for rule in self.rules:
                thisResult = rule.process(fPart)
                if thisResult is not None: break
            pass
        return thisResult

    class plRule:
        def __init__(self, fName, fOp, fVal, fDest, fOrder) -> None:
            self.name, self.op, self.dest, self.val, self.order = fName, fOp, fDest, fVal if fVal is None else int(fVal), fOrder
            pass
        def process(self, fPart):
            thisResult = None
            # return the name of the next queue
            if self.op == '<':
                if fPart.val[self.name] < self.val: thisResult = self.dest
            elif self.op == '>':
                if fPart.val[self.name] > self.val: thisResult = self.dest
            elif self.op is None:
                thisResult = self.dest
            if thisResult is not None: fPart.location = thisResult
            return thisResult

class part:
    def __init__(self, fAtrr) -> None:
        self.val = dict(zip('xmas', map(int, fAtrr)))
        self.location = 'heap'
        self.sum = sum(self.val.values())
        pass

def main(stdscr):
    with open(fName, 'r+') as f:
        fContent = f.read().splitlines()
    
    myPipelines = {}
    myParts = []
    for thisLine in fContent:
        regex = re.match('^(.*)\{(.+)(x=(\d+),m=(\d+),a=(\d+),s=(\d+))*\}$', thisLine.strip() )
        if regex is None: continue
        thisPL, thisParm = regex.groups()[0:2]

        if thisPL != '':
            # this is a pipeline
            myPipelines[thisPL] = pipeLine(thisPL, thisParm)

        if thisPL == '':
            # this is a part
            myParts.append(part(re.match('x=(\d+),m=(\d+),a=(\d+),s=(\d+)', thisParm).groups()))
    myPipelines['A'] = []
    myPipelines['R'] = []

    # now process all parts
    thisStartPL = 'in'
    for p in myParts:
        thisDest = thisStartPL
        while thisDest not in ('A', 'R'):
            thisDest = myPipelines[thisDest].process(p)
            pass
        myPipelines[thisDest].append(p)
        pass

    # sum xmas of parts in A
    result = sum([p.sum for p in myPipelines[ 'A']])

    message = f'The answer to part 1 is (sample should be 19114, answer should be 330820): {result}'
    print(message)

    print(20 * '*')

    result = 0

    message = f'The answer to part 2 is (sample should be x, answer should be x): {result}'
    print(message)
    pass


# globals
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose"   , action="store_true", default=False, help="Add this to enable verbose output")
parser.add_argument("-d", "--draw"      , action="store_true", default=False, help="Add this to enable drawing")
parser.add_argument("-i", "--drawinterval", type=int, default=1, help="Add the value in ms for drawing interval")
parser.add_argument("-p", "--production", action="store_true", default=False, help="Add this to try the puzzle input")
args = parser.parse_args()

day = '19'
fName = f'2023/input/{day}_sample.txt'
if args.production: fName = f'2023/input/{day}.txt'

debug = args.verbose
draw = args.draw

main(None)