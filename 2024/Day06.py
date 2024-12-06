import argparse
import re

class AocMap:
    def __init__(self) -> None:
        self.content = list()
        self.map = list()
        self.dirs = tuple()
        self.height, self.width = 0,0
        self.pos = list()
        self.path = list()
        pass
    def build(self, fContent, fDirs):
        self.content = fContent
        self.dirs = fDirs
        for y, line in enumerate(reversed(fContent)):
            for x, value in enumerate(line):
                if value == '#':
                    self.map.append((x,y))
                elif value in self.dirs:
                    self.pos = [(x, y), value]
                else:
                    pass
        self.path.append(((self.pos[0]), self.pos[1]))
        self.width, self.height = x, y
        return self
    def move(self):
        # return new position and direction and if it has hit the edge
        hitEdge = False
        if self.pos[1] in ('^', 'v'):
            # move vertically
            thisX = self.pos[0][0]
            thisY = [-1] + [co[1] for co in self.map if co[0] == self.pos[0][0]] + [self.height+1]
            if self.pos[1] == '^':
                thisY = min([y for y in thisY if y > self.pos[0][1]])
                hitEdge, thisY = (True, thisY) if thisY == self.height+1 else (False, thisY - 1)
            elif self.pos[1] == 'v':
                thisY = max([y for y in thisY if y < self.pos[0][1]])
                hitEdge, thisY = (True, thisY) if thisY == -1 else (False, thisY + 1)
            else:
                quit()
        elif self.pos[1] in ('>', '<'):
            # move horizontally
            thisX = [-1] + [co[0] for co in self.map if co[1] == self.pos[0][1]] + [self.width+1]
            thisY = self.pos[0][1]
            if self.pos[1] == '>':
                thisX = min([x for x in thisX if x > self.pos[0][0]])
                hitEdge, thisX = (True, thisX) if thisX == self.width+1 else (False, thisX - 1)
            elif self.pos[1] == '<':
                thisX = max([x for x in thisX if x < self.pos[0][0]])
                hitEdge, thisX = (True, thisX) if thisX == -1 else (False, thisX + 1)
            else:
                quit()
        else:
            quit('why do get here')
        if not hitEdge:
            # turn right
            self.pos[1] = self.dirs[(self.dirs.index(self.pos[1])+1) % 4]
        self.pos[0] = (thisX, thisY)
        return hitEdge
    def distinctPositions(self):
        # returns a set of distinct positions
        visitedCos = list()
        for i, co in enumerate(self.path[:-1]):
            startX, endX, startY, endY =  self.path[i][0][0], self.path[i+1][0][0], self.path[i][0][1], self.path[i+1][0][1]
            if startX == endX:
                for j in range(min(startY, endY), max(startY, endY)+1):
                    visitedCos.append((startX, j))
            elif startY == endY:
                for j in range(min(startX, endX), max(startX, endX)+1):
                    visitedCos.append((j, startY))
        return set(visitedCos)


def main(stdscr):
    with open(fName, 'r+') as f:
        fContent = f.read().splitlines()

    myMap = AocMap().build(fContent=fContent, fDirs = ('^', '>', 'v', '<'))

    # find next obstacle until we hit the edge of the map
    hitEdge = False
    while not hitEdge:
        hitEdge = myMap.move()
        myMap.path.append(tuple(myMap.pos))
    
    # find the distinct positions
    result = len(myMap.distinctPositions()) - 1 # remove the point that's over the edge

    message = f'The answer to part 1 is (sample should be 41, answer should be 4890): {result}\n'
    print(message)

    # create a copy of the map and place an object in one of the visited points
    # if we have been there already in the same direction, we found a loop
    result = 0
    for c in [c for c in myMap.distinctPositions() if c != myMap.path[0][0]]:
        myMap_2 = AocMap().build(fContent=fContent, fDirs = ('^', '>', 'v', '<'))
        myMap_2.map.append(c)
        # find next obstacle until we hit the edge of the map or revisit
        hitEdge, pVisited = False, False
        while not hitEdge and not pVisited:
            hitEdge = myMap_2.move()
            pVisited = tuple(myMap_2.pos) in myMap_2.path
            myMap_2.path.append(tuple(myMap_2.pos))
        result += 1 if pVisited else 0
        pass

    message = f'The answer to part 2 is (sample should be 6, answer should be ?): {result}\n'
    print(message)
    pass


# globals
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose"   , action="store_true", default=False, help="Add this to enable verbose output")
parser.add_argument("-p", "--production", action="store_true", default=False, help="Add this to try the puzzle input")
args = parser.parse_args()

day = '06'
fName = f'2024/input/{day}_sample.txt'
if args.production: fName = f'2024/input/{day}.txt'

debug = args.verbose

main(None)