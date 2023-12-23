import argparse
import re

class Stack:
    def __init__(self, fStack):
        self.id = int(fStack.strip())
        self.location = (self.id * 4) - 3
        self.crates = list()
    def move(self, fDest, fCount):
        i=0
        while i < fCount:
            fDest.place(self.take())
            i+=1
    def moveB(self, fDest, fCount):
        for c in self.crates[-fCount:]:
            fDest.place(c)
            self.take()
    def place(self, fName):
        self.crates.append(fName)
    def take(self):
        crate = self.crates[-1]
        self.crates.pop()
        return crate



def main(stdscr):
    with open(fName, 'r+') as f:
        fileContent = f.read().splitlines()
        stacks = [line.split() for line in fileContent if re.match('^ (\d+ +)+$', line)][0]
        AllStacks = dict(zip(stacks, list(map(Stack, stacks))))
        AllStacksB = dict(zip(stacks, list(map(Stack, stacks))))
        del stacks
        
        crates = [line for line in fileContent[::-1] if re.match(' *(\[[A-Z]\] *)+ *$', line)]
        for line in crates:
            for m in re.finditer('(\[[A-Z]{1,1}\])', line):
                i = (m.span()[1]+1+3)//4
                AllStacks[str(i)].place(m.group()[1])
                AllStacksB[str(i)].place(m.group()[1])
        del crates

        instructions = [line for line in fileContent if re.match('^move .*$', line)]
        for line in instructions:
            m = re.findall('(\d+)', line)
            AllStacks[m[1]].move(AllStacks[m[2]], int(m[0]))
            AllStacksB[m[1]].moveB(AllStacksB[m[2]], int(m[0]))
        del instructions

    result = ''.join([AllStacks[i].crates[-1] for i in AllStacks.keys()])
    message = f'The answer to part 1 is (sample should be CMZ, answer should be BWNCQRMDB): {result}'
    print(message)
    result = ''.join([AllStacksB[i].crates[-1] for i in AllStacksB.keys()])
    message = f'The answer to part 2 is (sample should be MCD, answer should be NHWZCBNBF): {result}'
    print (message) 

# globals
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose"   , action="store_true", default=False, help="Add this to enable verbose output")
parser.add_argument("-d", "--draw"      , action="store_true", default=False, help="Add this to enable drawing")
parser.add_argument("-i", "--drawinterval", type=int, default=1, help="Add the value in ms for drawing interval")
parser.add_argument("-p", "--production", action="store_true", default=False, help="Add this to try the puzzle input")
args = parser.parse_args()

day = '05'
fName = f'2022/input/{day}_sample.txt'
if args.production: fName = f'2022/input/{day}.txt'

debug = args.verbose
draw = args.draw

main(None)