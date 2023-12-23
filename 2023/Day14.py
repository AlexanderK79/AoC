import argparse

class ParaRefDisc:
    def __init__(self) -> None:
        self.content = list()
        self.matrix = dict()
        self.width, self.height = 0, 0
        self.tiltHistory = {}
        self.cycleHistory = {}
        self.checksum = int()
        pass
    def build(self, fContent):
        self.content = fContent[::-1] # reverse
        self.width, self.height = len(fContent[0]), len(fContent)
        for (i, thisLine) in enumerate(self.content):
            i += 1 # make it 1-based instead of 0-based
            for (j, thisChar) in enumerate(thisLine):
                j += 1 # make it 1-based instead of 0-based
                thisCo = self.co(j, i, thisChar)
                self.matrix[thisCo.id] = thisCo
        pass
        self.calcChecksum()
        return self
    def calcChecksum(self):
        self.checksum = int(''.join([v.val for v in sorted(self.matrix.values(), key=lambda item:(item.y, item.x))]).replace('#', '0').replace('.', '0').replace('O','1'), 2)
        pass
    def cycle(self):
        for d in ('N', 'W', 'S', 'E'):
            self.tilt(fDirection=d)
        return self
    def findInterval(self, fInterval):
        orgChecksum = self.checksum
        cacheHit = self.cycleHistory.get(orgChecksum, None)
        if cacheHit != None:
            print(f'found interval: previous {cacheHit}, this {fInterval}, difference {fInterval-cacheHit}')
            return (cacheHit, fInterval-cacheHit)
        self.cycleHistory[orgChecksum] = fInterval
        self.cycle()
        return (None, None)


    def tilt(self, fDirection):
        cacheHit = self.tiltHistory.get(self.checksum, {}).get(fDirection, None)
        if cacheHit != None:
            pass
            # return cacheHit
        orgChecksum = self.checksum
        # move all 'O' until they reach the edge, another 'O' or  a '#'
        if fDirection=='N':
            thisStartLine, thisEndLine, thisVertStep = self.height, 0, -1
            thisStartPos, thisEndPos, thisHorStep = 1, self.width+1, 1
            nextX, nextY = 0, 1
        if fDirection=='S':
            thisStartLine, thisEndLine, thisVertStep = 1, self.height+1, 1
            thisStartPos, thisEndPos, thisHorStep = 1, self.width+1, 1
            nextX, nextY = 0, -1
        
        if fDirection=='W':
            thisStartLine, thisEndLine, thisVertStep = self.height, 0, -1
            thisStartPos, thisEndPos, thisHorStep = 1, self.width+1, 1
            nextX, nextY = -1, 0
        if fDirection=='E':
            thisStartLine, thisEndLine, thisVertStep = self.height, 0, -1
            thisStartPos, thisEndPos, thisHorStep = self.width, 0, -1
            nextX, nextY = 1, 0
        
        for y in range(thisStartLine, thisEndLine, thisVertStep):
            for x in range(thisStartPos, thisEndPos, thisHorStep):
                thisId = self.matrix['_'.join(map(str, (x,y)))]
                if thisId.val != 'O': continue
                thisVal, thisX, thisY = '.', thisId.x, thisId.y
                while thisVal == '.':
                    # move on up, until the edge or another val is hit
                    thisX, thisY = thisX+nextX,thisY+nextY
                    nextId = '_'.join(map(str, (thisX, thisY)))
                    thisVal = self.matrix.get(nextId, None)
                    thisVal = thisVal.val if thisVal != None else None
                thisX, thisY = thisX-nextX,thisY-nextY #reverse one step
                nextId = self.matrix['_'.join(map(str, (thisX, thisY)))]
                if thisId != nextId:
                    thisId.val = '.'
                    nextId.val = 'O'
                pass
        pass
        self.calcChecksum()
        if self.tiltHistory.get(orgChecksum) == None:
            self.tiltHistory[orgChecksum] = {} 
        self.tiltHistory[orgChecksum][fDirection] = self.checksum
        return self

    def calcWeight(self):
        pass
        return sum([v.y for v in self.matrix.values() if v.val == 'O'])

    def printmap(self, fReversed = True):
        for h in range(self.height, 0, -1) if fReversed else range(1, self.height+1):
            print(''.join([v.val for v in sorted(self.matrix.values(), key=lambda item:(item.y, item.x)) if v.y == h]), f'{h:03}')
        print('\n')

    class co:
        def __init__(self, fX, fY, fVal) -> None:
            self.x, self.y, self.val = fX, fY, fVal
            self.co = (self.x, self.y)
            self.id = '_'.join(map(str, (self.co)))
            pass

def main(stdscr):
    with open(fName, 'r+') as f:
        fContent = f.read().splitlines()
    

    myPRD = ParaRefDisc()
    result = myPRD.build(fContent=fContent)
    result = myPRD.tilt(fDirection='N')
    result = myPRD.calcWeight()

    message = f'The answer to part 1 is (sample should be 136, answer should be 106997): {result}'
    print(message)
    del myPRD

    print(20 * '*')

    # 1000000000 cycles
    myPRD = ParaRefDisc()
    result = myPRD.build(fContent=fContent)
    # find stabilization factor
    result, i = (None, None), 0
    while result == (None, None):
        i += 1
        result = myPRD.findInterval(fInterval=i)
    startpos, interval = result

    totalCycles = 1000000000
    remainingCycles = totalCycles - startpos # subtract the starpos
    remainingCycles %= interval
    for i in range(remainingCycles+1):
        myPRD.cycle()
        print(f'processing cycle {i:010}', myPRD.calcWeight())

    result = myPRD.calcWeight()

    message = f'The answer to part 2 is (sample should be 64, answer should be 99641): {result}'
    print(message)
    pass


# globals
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose"   , action="store_true", default=False, help="Add this to enable verbose output")
parser.add_argument("-d", "--draw"      , action="store_true", default=False, help="Add this to enable drawing")
parser.add_argument("-i", "--drawinterval", type=int, default=1, help="Add the value in ms for drawing interval")
parser.add_argument("-p", "--production", action="store_true", default=False, help="Add this to try the puzzle input")
args = parser.parse_args()

day = '14'
fName = f'2023/input/{day}_sample.txt'
if args.production: fName = f'2023/input/{day}.txt'

debug = args.verbose
draw = args.draw

main(None)