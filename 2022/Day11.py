import argparse
import curses
from curses import wrapper
import re
from decimal import Decimal
from decimal import getcontext
import math
from copy import deepcopy

class Monkey:
    def __init__(self, fMode, fMonkeyGroup, fName, fItems, fOp, fTest, fDestTrue, fDestFalse) -> None:
        self.name = fName
        self.group = fMonkeyGroup
        self.items = [Item(int(i.strip())) for i in fItems.split(',')] # list of items, currently owned by
        self.operation = fOp
        self.test = fTest
        regex = re.match('(divisible by )(\d+)$', fTest)
        self.modulus = int(regex.groups()[1])
        self.destname = [fDestTrue[-1], fDestFalse[-1]] # true name, false name
        self.inspection_counter = 0
        self.LCM = int()
        pass
    def turn(self, fMode):
        if draw: print(f'Monkey {self.name}:')
        if len(self.items) >  0:
            # op, inspect, bore, test, throw
            itemlist = self.items.copy()
            for i in itemlist:
                if draw: print (f'  Monkey inspects a item with a worry level of {i.value}')
                self.inspect_item(i)
                if fMode == 'A': self.bored_with_item(i)
                self.reduce_with_modulo(i)
                fDestName = self.test_item(i)
                if draw: print(f'    Item with worry level {i.value} is thrown to monkey {fDestName}.')
                self.throw_item(i, self.group[fDestName])
            pass
        pass
    def inspect_item(self, fItem):
        self.inspection_counter += 1
        self.op_item(fItem)
        pass
    def op_item(self, fItem):
        regex = re.match('(new = )(.+)( (\+|\-|\*) )(.+)$', self.operation)
        op = regex.groups()[3]
        factor1 = fItem.value if regex.groups()[1] == 'old' else Decimal(regex.groups()[1])
        factor2 = fItem.value if regex.groups()[4] == 'old' else Decimal(regex.groups()[4])
        if op == '+':
            fItem.value = factor1 + factor2
        elif op == '-':
            fItem.value = factor1 - factor2
        elif op == '*':
            fItem.value = factor1 * factor2
        pass
    def test_item(self, fItem):
        if pow(fItem.value, 1, self.modulus) == 0:
            fDest = self.destname[0]
        else:
            fDest = self.destname[1]
        return fDest
        pass
    def reduce_with_modulo(self, fItem):
        fItem.value = fItem.value % self.LCM

    def bored_with_item(self, fItem):
        fItem.value = fItem.value // 3
        pass
    def throw_item(self,fItem, fDest):
        self.items.remove(fItem)
        fDest.items.append(fItem)
        pass

class Item:
    def __init__(self, fVal) -> None:
        self.value = Decimal(fVal)
        pass

def main(stdscr):
    MonkeyGroup = dict()
    with open(fName, 'r+') as f:
        for line in f.read().splitlines():
            DestFalse = None
            regex = re.match('((^Monkey )((\d):$))', line.strip())
            if regex and regex.groups()[1] == 'Monkey ': MonkeyName = regex.groups()[3]
            regex = re.match('((^Starting items: )(.*$))', line.strip())
            if regex and regex.groups()[1] == 'Starting items: ': StartingItems = regex.groups()[2]
            regex = re.match('((Operation: )(.*$))', line.strip())
            if regex and regex.groups()[1] == 'Operation: ': Op = regex.groups()[2]
            regex = re.match('((Test: )(.*$))', line.strip())
            if regex and regex.groups()[1] == 'Test: ': Test = regex.groups()[2]
            regex = re.match('((If true: )(.*$))', line.strip())
            if regex and regex.groups()[1] == 'If true: ': DestTrue = regex.groups()[2]
            regex = re.match('((If false: )(.*$))', line.strip())
            if regex and regex.groups()[1] == 'If false: ': DestFalse = regex.groups()[2]

            if DestFalse: 
                MonkeyGroup[MonkeyName] = Monkey('A', MonkeyGroup, MonkeyName, StartingItems, Op, Test, DestTrue, DestFalse)
                del MonkeyName, StartingItems, Op, Test, DestTrue, DestFalse
    
    # determine the number of operations when a value is back in it's original form
    myLCM = 1
    for i in MonkeyGroup.values():
        myLCM = math.lcm(myLCM, i.modulus)
    for i in MonkeyGroup.values():
        i.LCM = myLCM
    del myLCM
    MonkeyGroupB = deepcopy(MonkeyGroup)

    if not skipA:
        for i in range(numRoundsA):
            for m in MonkeyGroup.values():
                m.turn('A')
                pass

    # Find all of the directories with a total size of at most 100000. 
    # What is the sum of the total sizes of those directories?
    result = sorted([i.inspection_counter for i in MonkeyGroup.values()])[-2::]
    result = result[0] * result[1]
#    if debug and not skipA and result not in (10605, 55216): quit(f'incorrect result: {result}')
    message = f'The answer to part 1 is (sample should be 10605, answer should be 55216/113220): {result}'
    print(message)


    for i in range(numRoundsB):
        for m in MonkeyGroupB.values():
            m.turn('B')
    result = sorted([i.inspection_counter for i in MonkeyGroupB.values()])[-2::]
    result = result[0] * result[1]

    message = f'The answer to part 2 is (sample should be 2713310158, answer should be 12848882750): {result}'
    print(message)


# globals
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose"   , action="store_true", default=False, help="Add this to enable verbose output")
parser.add_argument("-d", "--draw"      , action="store_true", default=False, help="Add this to enable drawing")
parser.add_argument("-i", "--drawinterval", type=int, default=1, help="Add the value in ms for drawing interval")
parser.add_argument("-ra", "--roundsA", type=int, default=20, help="Add the numbe of rounds you want")
parser.add_argument("-rb", "--roundsB", type=int, default=10000, help="Add the numbe of rounds you want")
parser.add_argument("-s", "--skipA", action="store_true", default=False, help="Add the numbe of rounds you want")
parser.add_argument("-p", "--production", action="store_true", default=False, help="Add this to try the puzzle input")
args = parser.parse_args()

day = '11'
fName = f'2022/input/{day}_sample.txt'
if args.production: fName = f'2022/input/{day}.txt'

debug = args.verbose
draw = args.draw
numRoundsA = args.roundsA
numRoundsB = args.roundsB
skipA = args.skipA

""" stdscr = curses.initscr()
curses.start_color()
curses.use_default_colors()
wrapper(main)
 """
main(None)