import argparse
import curses
from curses import wrapper

class Clock:
    def __init__(self) -> None:
        self.cycle = 0
        self.cpu = CPU()
        self.screen = Screen(6, 40)
        self.signal_strength = self.cycle * self.cpu.X
        self.cycle_log = [(self.signal_strength, self.cycle, self.cpu.X)]
    def execute(self, fA):
        if fA[0] == 'noop':
            self.noop()
        elif fA[0] == 'addx':
            fInt = int(fA[1])
            self.addX(fInt)
        else:
            pass
    def addCycle(self):
        self.screen.drawPixel(self)
        self.cycle += 1
        self.signal_strength = self.cycle * self.cpu.X
        self.cycle_log.append((self.signal_strength, self.cycle, self.cpu.X))
    def noop(self):
        self.addCycle()
    def addX(self, fInt):
        self.addCycle()
        self.addCycle()
        self.cpu.X += fInt
        self.signal_strength = self.cycle * self.cpu.X

class CPU:
    def __init__(self) -> None:
        self.X = 1
        pass

class Screen:
    def __init__(self, fH, fW) -> None:
        self.matrix = []
        for i in range(0, fH): self.matrix.append(fW * [' '])
        self.H = fH
        self.W = fW
        self.size = fH * fW
        pass
    def drawPixel(self, fClock):
        curPixel = fClock.cycle % (self.size)
        curSprite = fClock.cpu.X
        curSprite = [curSprite-1, curSprite, curSprite+1]
        curSprite = [i for i in curSprite if i>=0]
        myH = curPixel // self.W
        myW = curPixel % self.W
        self.matrix[myH][myW] = '#' if myW in curSprite else '.'
        if debug:
            debugLine = self.matrix[myH].copy()
            for i in curSprite:
                if debugLine[i] != '#': debugLine[i] = '_'
            print('cycle', str(fClock.cycle+1).rjust(4, '0'), 'cpu',  str(fClock.cpu.X).rjust(4, '0'), ''.join(debugLine))
            del debugLine

def main(stdscr):
    myClock = Clock()
    with open(fName, 'r+') as f:
        for line in f.read().splitlines():
            myClock.execute(fA=line.split())
    
    # Find all of the directories with a total size of at most 100000. 
    # What is the sum of the total sizes of those directories?
    result = sum([ i[0] for i in myClock.cycle_log if i[1] == 20 or (i[1]-20) % 40 == 0])

    message = f'The answer to part 1 is (sample should be 13140, answer should be 13680): {result}'
    print(message)

    for line in myClock.screen.matrix:
        print(''.join(line).replace('.', ' ').replace('#', '█'))

    # Find all of the directories with a total size of at most 100000. 
    # What is the sum of the total sizes of those directories?
    result = 0

    message = f'The answer to part 2 is (sample should be x, answer should be PZGPKPEB): {result}'
    print(message)


# globals
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose"   , action="store_true", default=False, help="Add this to enable verbose output")
parser.add_argument("-d", "--draw"      , action="store_true", default=False, help="Add this to enable drawing")
parser.add_argument("-i", "--drawinterval", type=int, default=1, help="Add the value in ms for drawing interval")
parser.add_argument("-p", "--production", action="store_true", default=False, help="Add this to try the puzzle input")
args = parser.parse_args()

day = '10'
fName = f'2022/input/{day}_sample.txt'
if args.production: fName = f'2022/input/{day}.txt'

debug = args.verbose
draw = args.draw

""" stdscr = curses.initscr()
curses.start_color()
curses.use_default_colors()
wrapper(main)
 """
main(None)