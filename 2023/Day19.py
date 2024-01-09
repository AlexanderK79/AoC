import argparse
import re
import math
from copy import deepcopy
from functools import reduce
import itertools

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

def ranges(i):
    for a, b in itertools.groupby(enumerate(i), lambda pair: pair[1] - pair[0]):
        b = list(b)
        yield b[0][1], b[-1][1]

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

    # possible number of combinations to end up in the 'A'
    # walk the pipelines, like they are paths/maze/graph

    paths, paths2explore = [], []
    limits = (1,4001)
    thisPath = [thisStartPL]
    paths2explore.append([thisPath, dict(zip('xmas', [list(), list(), list(), list()]))])
    while len(paths2explore) > 0:
        thisPath, thisVals = paths2explore.pop()
        thisPath = deepcopy(thisPath)
        newPath = deepcopy(thisPath)
        thisPL = thisPath[-1]
        for r in myPipelines[thisPL].rules:
            newVals = deepcopy(thisVals)
            if r.op == None:
                newPath = thisPath + [r.dest]
            if r.op == '<':
                newVals[r.name].append(range(limits[0],r.val))
                thisVals[r.name].append(range(r.val, limits[1]))
                newPath = thisPath + [r.dest]
            if r.op == '>':
                newVals[r.name].append(range(r.val+1, limits[1]))
                thisVals[r.name].append(range(limits[0], r.val+1))
                newPath = thisPath + [r.dest]
            if r.dest in ('R', 'A'):
                paths.append((newPath, newVals))
            else:
                paths2explore.append((newPath, newVals))
        pass
    pass
    del paths2explore, myParts, f, fContent, regex, stdscr, thisDest, thisLine, thisParm
    del message, newPath, newVals, p, r, thisPL, thisPath, thisStartPL, thisVals

    # count combinations
    totalNumCombis = 0
    knownCombis = []
    for p in [i for i in paths if i[0][-1] == 'A']:
        thisPath = p[0]
        thisCombi = [reduce((lambda x, y: set(x).intersection(y)), s) for s in [[range(limits[0], limits[1]), range(limits[0], limits[1])] if v == [] else [range(limits[0], limits[1])] + v for v in p[1].values()]]

        totalNumCombis += math.prod([len(i) for i in thisCombi])
        # subtract the intersections with knownCombis

        duplicates = sum([math.prod([len(c[i].intersection(thisCombi[i])) for i in range(len(c))]) for c in knownCombis if c != thisCombi])
        print('processing', p[0], [list(ranges(i)) for i in thisCombi]) if args.verbose else None
        [print ([len(c[i].intersection(thisCombi[i])) for i in range(len(c))]) for c in knownCombis if c != thisCombi]  if args.verbose else None
        totalNumCombis -= duplicates
        knownCombis.append(thisCombi)

        pass
    del p
    
    result = totalNumCombis

    message = f'The answer to part 2 is (sample should be 167409079868000, answer should be 123972546935551, 123950345737372 is too low):\n167409079868000\n{result}'
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