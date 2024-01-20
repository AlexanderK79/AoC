import argparse
import heapq

class AoCmap:
    def __init__(self) -> None:
        self.content = list()
        self.height, self.width = 0, 0
        self.startingCo = None
        self.endingCo = None
        self.matrix = {}
        self.completePaths = []
        self.pathSegments = []
        pass
    def build(self, fContent):
        self.content = fContent
        for (y, thisLine) in enumerate(fContent):
            y += 1 # make it 1-based instead of 0-based
            self.matrix
            for (x,thisChar) in enumerate(thisLine):
                x += 1 # make it 1-based instead of 0-based
                thisCo = co(x, y, thisChar)
                self.matrix[thisCo.id] = thisCo
        self.height, self.width = y, x
        self.startingCo = [i.id for i in self.matrix.values() if i.val == 'S'][0]
        self.endingCo = [i.id for i in self.matrix.values() if i.val == 'E'][0]
        # set all neighboors and perimeter
        for p in self.matrix.values():
            thisX, thisY = p.x, p.y
            for relX, relY in ((-1,0), (1,0), (0,-1), (0,1)):
                thisNb = self.matrix.get(co(thisX + relX, thisY + relY).id)
                if thisNb:
                    match (relX, relY): # d = direction to get to this tile
                        case (-1,  0): direction = '<'
                        case ( 1,  0): direction = '>'
                        case ( 0, -1): direction = '^'
                        case ( 0,  1): direction = 'v'
                    p.neighboors[direction] = thisNb
            # if all p to an edge are # or none, store the perimeter
            if p.val != '#':
                if   set('#') == set(['#'] + [self.matrix['_'.join(map(str, (x, thisY)))].val for x in [x for x in range(1, thisX)]]): p.perimeter = 'L'
                elif set('#') == set(['#'] + [self.matrix['_'.join(map(str, (x, thisY)))].val for x in [x for x in range(thisX+1, self.width+1)]]): p.perimeter = 'R'
                elif set('#') == set(['#'] + [self.matrix['_'.join(map(str, (thisX, y)))].val for y in [y for y in range(1, thisY)]]): p.perimeter = 'T'
                elif set('#') == set(['#'] + [self.matrix['_'.join(map(str, (thisX, y)))].val for y in [y for y in range(thisY+1, self.height+1)]]): p.perimeter = 'D'
        pass
        return self

    def findLongestPath(self, p2=False):
        # do not return to tiles previously traveled, follow direction on <>v (^not used) tiles
        prioQ = [] # order by EstimatedCost, longest route first
        heapq.heapify(prioQ)
        maxPath = self.height * self.width
        thisPath = [self.startingCo]
        nextPath = [self.startingCo]
        nextSegment = [self.startingCo]
        nodePath = {}
        nodePath[self.startingCo] = 0
        self.pathSegments = [] # list of segments
        heapq.heappush(prioQ, (maxPath - len(nextPath), nextPath[-1], nextSegment, nextPath))
        while len(prioQ) > 0:
            thisN = heapq.heappop(prioQ)
            thisVal, thisN, thisSegment, thisPath = thisN
            thisCost = len(thisPath)-1
            # if nodePath.get(thisN, thisCost) > thisCost: continue # we have been here before, but more expensive
            nodePath[thisN] = thisCost
            if len(thisSegment) == 2 and thisSegment in [tS[:2] for tS in self.pathSegments]:
                continue # check if we already explored this segment
            

            if thisN == self.endingCo:
                # we are at the end
                if thisSegment not in self.pathSegments: self.pathSegments.append(thisSegment)
                if len(thisPath) == len(set(thisPath)):
                    self.completePaths.append((thisCost, thisPath))
                continue
                # break 

            # keep traveling a path until there is a choice
            nextN = [(k, v) for k,v in self.matrix[thisN].neighboors.items()]
            nextN = [(k, v) for k,v in nextN if v.val not in ('#')]
            a = len(nextN)
            nextN = [(k, v) for k,v in nextN if not (v.perimeter in ['R'] and k == '^')] # it is no use to move upward, if we are on the perimeter
            nextN = [(k, v) for k,v in nextN if not (v.perimeter in ['T'] and k == '<')] # it is no use to move left, if we are on the perimeter
            if len(nextN) < a:
                pass
            if not p2:
                nextN = [(k, v) for k,v in nextN if ''.join((k,v.val)) not in ('><', '<>', '^v', 'v^')] # to steep
            nextN = [(k,v) for k,v in nextN if v.id not in thisPath[-2:]] # already visited
            pass
            if len(nextN) > 1:
                # we've got a choice, end the segment
                if thisSegment not in self.pathSegments:
                    self.pathSegments.append(thisSegment)
                else:
                    pass # why do we get here
                thisSegment = [thisN]
            for k,v in nextN:
                nextSegment = thisSegment.copy() + [v.id]
                nextPath = thisPath.copy() + [v.id]
                heapq.heappush(prioQ, (maxPath - thisCost, nextPath[-1], nextSegment, nextPath))
        del thisPath, thisSegment, nextPath, nextSegment, thisCost, thisN, thisVal, nextN, k, v, nodePath
        pass
        if p2:
            [print(f' -- {len(i)-1} --> '.join((i[0], i[-1]))) for i in self.pathSegments]
            # now calculate the segments
            startingSegment = [i for i in self.pathSegments if i[0] == self.startingCo][0]
            thisSegment = startingSegment
            nextSegment = startingSegment
            nextPath = startingSegment
            heapq.heappush(prioQ, (len(nextPath), nextSegment[0], nextSegment, nextPath))
            while len(prioQ) > 0:
                thisVal, thisSegment_Start, thisSegment, thisPath = heapq.heappop(prioQ)
                thisCost = len(thisPath) - 1
                if thisPath[-1] == self.endingCo:
                    # we found an ending
                    self.completePaths.append((thisCost, thisPath))
                    print('Found path of ', thisCost, 'Maxpath', max([i[0] for i in self.completePaths]))
                    continue
                    # break
                
                for nextS in [S for S in self.pathSegments if S[0] == thisPath[-1]]:
                    # check if we are not returning to points, visited earlier
                    if True in [nS in [S for S in thisPath] for nS in nextS[1:]]:
                        continue
                    nextSegment = nextS
                    nextPath = thisPath + nextS[1:]
                    heapq.heappush(prioQ, (maxPath - len(nextPath), nextSegment[0], nextSegment, nextPath))
            pass

    def printmap(self, fReversed = False, fPath = dict()):
        for h in range(self.height, 0, -1) if fReversed else range(1, self.height+1):
            print(''.join([fPath.get(v.id, v.val) for v in sorted(self.matrix.values(), key=lambda item:(item.y, item.x)) if v.y == h]), f'{h:03}')
        print('\n')

class co:
    def __init__(self, fX, fY, fVal=None) -> None:
        self.x, self.y = fX, fY
        self.co = (self.x, self.y)
        self.id = '_'.join(map(str, (self.co)))
        self.val = fVal
        self.neighboors = dict()
        self.perimeter = ''
        pass
    def calcDist(self, fCo) -> None:
        return abs(self.x - fCo.x) + abs(self.y - fCo.y)
def main(stdscr):
    with open(fName, 'r+') as f:
        fContent = f.read().splitlines()
    

    myMap = AoCmap()
    result = myMap.build(fContent=fContent)
    if args.verbose: myMap.printmap()
    myMap.findLongestPath()
    result = max([p[0] for p in myMap.completePaths])

    message = f'The answer to part 1 is (sample should be 94, answer should be 2086): {result}'
    print(message)

    print(20 * '*')
    myMap.findLongestPath(p2=True)
    result = max([p[0] for p in myMap.completePaths])


    message = f'The answer to part 2 is (sample should be 154, answer should be 6526, 4778, 6222 too low): {result}'
    print(message)
    pass


# globals
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose"   , action="store_true", default=False, help="Add this to enable verbose output")
parser.add_argument("-d", "--draw"      , action="store_true", default=False, help="Add this to enable drawing")
parser.add_argument("-i", "--drawinterval", type=int, default=1, help="Add the value in ms for drawing interval")
parser.add_argument("-p", "--production", action="store_true", default=False, help="Add this to try the puzzle input")
args = parser.parse_args()

day = '23'
fName = f'2023/input/{day}_sample.txt'
if args.production: fName = f'2023/input/{day}.txt'

debug = args.verbose
draw = args.draw

main(None)