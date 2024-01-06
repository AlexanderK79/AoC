import argparse
import heapq
import itertools
import matplotlib.pyplot as plt

class lagoon:
    def __init__(self) -> None:
        self.content = list()
        self.layout = list()
        self.width, self.height = int(), int()
        self.grid = []
        self.pq = []
        pass
    def build(self, fContent):
        self.content = fContent
        thisX, thisY = 0, 0
        for thisLine in fContent:
            thisDir, thisLen, thisColor = thisLine.split()
            thisLen = int(thisLen)
            thisColor = thisLine.partition('(')[-1].rpartition(')')[0]
            self.layout.append(lagoonEdge(thisX, thisY, thisDir, thisLen, thisColor))
            thisX, thisY = self.layout[-1].endCo.x, self.layout[-1].endCo.y
        self.width  = 1+max([max((i.startCo.x, i.endCo.x)) for i in self.layout])-min([min((i.startCo.x, i.endCo.x)) for i in self.layout])
        self.height = 1+max([max((i.startCo.y, i.endCo.y)) for i in self.layout])-min([min((i.startCo.y, i.endCo.y)) for i in self.layout])
        self.grid = [['.' for x in range(self.width)] for y in range(self.height)]
        self.grid_offset_xy = (-min([min((i.startCo.x, i.endCo.x)) for i in self.layout]), -min([min((i.startCo.y, i.endCo.y)) for i in self.layout]))
        print('Offset is:', self.grid_offset_xy) if args.verbose else None
        pass

    def build_p2(self, fContent):
        self.content = fContent
        thisX, thisY = 0, 0
        for thisLine in fContent:
            thisDir, thisLen, thisColor = thisLine.split()
            thisLen = int(thisLen)
            thisColor = thisLine.partition('(')[-1].rpartition(')')[0]
            #0 means R, 1 means D, 2 means L, and 3 means U.
            thisDir = ['R', 'D', 'L', 'U'][int(thisColor[-1])]
            thisLen = int(thisColor[1:6], 16)
            self.layout.append(lagoonEdge(thisX, thisY, thisDir, thisLen, thisColor))
            thisX, thisY = self.layout[-1].endCo.x, self.layout[-1].endCo.y
        self.width  = 1+max([max((i.startCo.x, i.endCo.x)) for i in self.layout])-min([min((i.startCo.x, i.endCo.x)) for i in self.layout])
        self.height = 1+max([max((i.startCo.y, i.endCo.y)) for i in self.layout])-min([min((i.startCo.y, i.endCo.y)) for i in self.layout])
        # self.grid = [['.' for x in range(self.width)] for y in range(self.height)]
        self.grid_offset_xy = (-min([min((i.startCo.x, i.endCo.x)) for i in self.layout]), -min([min((i.startCo.y, i.endCo.y)) for i in self.layout]))
        # print('Offset is:', self.grid_offset_xy) if args.verbose else None
        pass

    def dig(self):
        thisCursor = co(self.grid_offset_xy[0], self.grid_offset_xy[1])
        xyDir ={'R': (1, 0), 'L': (-1, 0), 'U': (0, -1), 'D': (0, 1)}
        for LE in self.layout:
            while thisCursor.co != co(LE.endCo.x+xyDir[LE.dir][0]+self.grid_offset_xy[0],LE.endCo.y+xyDir[LE.dir][1]+self.grid_offset_xy[1]).co:
                x, y = thisCursor.co
                self.grid[y][x] = '#'
                thisCursor = co(x+xyDir[LE.dir][0], y+xyDir[LE.dir][1])
            thisCursor = co(x, y)
            pass
        # loop should be closed
        [print(''.join([self.grid[y][x] for x in range(self.width)])) for y in range(self.height)]
        print('')
        # now do a flood fill
        thisCursor = co(self.grid_offset_xy[0], self.grid_offset_xy[1])
        thisCursor = co(thisCursor.x+1, thisCursor.y+1)
        heapq.heappush(self.pq, thisCursor.co)
        while len(self.pq) > 0:
            x, y = heapq.heappop(self.pq)
            for relX, relY in itertools.product((-1, 0, 1), repeat=2):
                if self.grid[y+relY][x+relX] == '.':
                    heapq.heappush(self.pq, co(x+relX, y+relY).co)
                    self.grid[y+relY][x+relX] = '#'
        [print(''.join([self.grid[y][x] for x in range(self.width)])) for y in range(self.height)]
        pass

    def calcArea(self):
        # https://en.wikipedia.org/wiki/Shoelace_formula
        # create a chain of polygon points
        # thisPolygonPoints = [(p.startCo.co, p.endCo.co) for p in self.layout] + [(self.layout[-1].endCo.co, self.layout[0].startCo.co)]

        #create perimeter in coordinates
        thisX, thisY = 1, 0
        for (i,LE) in enumerate(self.layout):
            thisXcorr, thisYcorr       = 0, 0
            thisXcorrPre, thisYcorrPre = 0, 0
            # clockwise directions (assuming clockwise ordering of the polygon)
            nextDir = 'R' if i == len(self.layout)-1 else self.layout[i+1].dir
            if (LE.dir, nextDir) == ('U', 'R') : thisXcorr = 1
            if (LE.dir, nextDir) == ('R', 'D') : thisYcorr = -1
            if (LE.dir, nextDir) == ('D', 'L') : thisXcorr = -1
            if (LE.dir, nextDir) == ('L', 'U') : thisYcorr = 1
            # counterclockwise directions
            if (LE.dir, nextDir) == ('U', 'L') : thisXcorr, thisYcorrPre = 0, -1
            if (LE.dir, nextDir) == ('L', 'D') : thisXcorrPre = 1
            if (LE.dir, nextDir) == ('D', 'R') : thisXcorrPre, thisYcorrPre = 0, 1
            if (LE.dir, nextDir) == ('R', 'U') : thisXcorrPre = -1

            thisX = thisX + ((LE.len if LE.dir in ('L', 'R') else 0) * (-1 if LE.dir in ('L', 'D') else 1))
            thisY = thisY + ((LE.len if LE.dir in ('U', 'D') else 0) * (-1 if LE.dir in ('L', 'D') else 1))

            thisX = thisX + thisXcorrPre
            thisY = thisY + thisYcorrPre

            LE.periCo = co(thisX, thisY)
            thisX = thisX + thisXcorr
            thisY = thisY + thisYcorr

            pass

        a=[p.periCo.co for p in self.layout]

        plt.plot([1]+[c.periCo.x for c in self.layout]+[1], [0]+[c.periCo.y for c in self.layout]+[0] )
        plt.show()

        thisPolygonPoints = list(zip([(1,0)] + a, a + [(1,0)]))
        return abs(0.5 * sum([p[0][0]*p[1][1] - (p[0][1]*p[1][0]) for p in thisPolygonPoints]))


class lagoonEdge:
    def __init__(self, fX, fY, fDir, fLen, fColor) -> None:
        xyDir ={'R': (1, 0), 'L': (-1, 0), 'U': (0, -1), 'D': (0, 1)}
        fLen = fLen
        colorEdge ={'R': 'N', 'L': 'S', 'U': 'W', 'D': 'E'}
        self.startCo  = co(fX, fY)
        self.endCo = co(fX + (fLen * xyDir[fDir][0]), fY + (fLen * xyDir[fDir][1]))
        self.color = {colorEdge[fDir]: fColor}
        self.dir = fDir
        self.len = fLen

class co:
    def __init__(self, fX, fY) -> None:
        self.x, self.y = fX, fY
        self.co = (self.x, self.y)
        self.id = '_'.join(map(str, (self.co)))
        pass
    def calcDist(self, fCo) -> None:
        return abs(self.x - fCo.x) + abs(self.y - fCo.y)

def main(stdscr):
    with open(fName, 'r+') as f:
        fContent = f.read().splitlines()
    

    myMap = lagoon()
    result = myMap.build(fContent=fContent)
    result = myMap.dig()
    result = sum([[myMap.grid[y][x] for x in range(myMap.width)].count('#') for y in range(myMap.height)])

    message = f'The answer to part 1 is (sample should be 62, answer should be 62365): {result}'
    print(message)

    print(20 * '*')

    result = myMap.calcArea()
    print(result)

    myMap_p2 = lagoon()
    result = myMap_p2.build_p2(fContent=fContent)
    result = myMap_p2.calcArea()

    message = f'The answer to part 2 is (sample should be 952408144115, answer should be 159485361249806): {result}'
    print(message)
    pass


# globals
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose"   , action="store_true", default=False, help="Add this to enable verbose output")
parser.add_argument("-d", "--draw"      , action="store_true", default=False, help="Add this to enable drawing")
parser.add_argument("-i", "--drawinterval", type=int, default=1, help="Add the value in ms for drawing interval")
parser.add_argument("-p", "--production", action="store_true", default=False, help="Add this to try the puzzle input")
args = parser.parse_args()

day = '18'
fName = f'2023/input/{day}_sample.txt'
if args.production: fName = f'2023/input/{day}.txt'

debug = args.verbose
draw = args.draw

main(None)