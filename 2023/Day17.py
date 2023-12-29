import argparse
import itertools

class CrucibleMap:
    def __init__(self) -> None:
        self.content = list()
        self.map = {}
        self.height, self.width = 0,0
        pass
    def build(self, fContent):
        self.content = fContent
        for (y, thisLine) in enumerate(fContent):
            for (x,thisC) in enumerate(thisLine):
                p = pathPoint(x+1, y+1, thisC)
                self.map[p.co.id] = p
                pass
        self.height, self.width = y+1, x+1
        # now give each pathPoint the path to it's neighboors
        for p in self.map.values():
            thisX, thisY = p.co.x, p.co.y
            for relX, relY in itertools.product((-1, 0, 1), repeat=2):
                if abs(relX + relY) != 1: continue
                if self.map.get(co(thisX + relX, thisY + relY).id):
                    match (relX, relY): # d = direction to get to this tile
                        case (-1,  0): d = '<'
                        case ( 1,  0): d = '>'
                        case ( 0, -1): d = '^'
                        case ( 0,  1): d = 'v'
                    destP = self.map[co(thisX + relX, thisY + relY).id]
                    p.destinations[destP.co.id] = {'id': destP.co.id, 'd': d, 'val': destP.val, 'p': destP}
                    pass
            pass
        return self
    

    def cheapestPath(self, fStartCo, fEndCo, fMaxConsecMoves):
        self.allPaths = self.recursePath((fStartCo.id, '.', self.map[fStartCo.id].val), fEndCo.id, [], fMaxConsecMoves)
        return sorted(self.allPaths,  key=lambda item: item[0])[0]
        
        
    def recursePath(self, fStartNode, fEndNode, fAllPaths, fMaxConsecMoves, fMyPath=()):
        # returns a list of allPaths
        """
        Recursive function. Finds all paths through the specified
        graph from start node to end node. For cyclical paths, this stops
        at the end of the first cycle.
        """
        fMyPath += tuple([fStartNode])
        minPathVal = 10**10 if len(fAllPaths) == 0 else min([j[0] for j in fAllPaths])
        for nextNode in sorted(self.map[fStartNode[0]].destinations.values(), key=lambda item: (item['p'].co.calcDist(self.map[fEndNode].co), item['val'])): # sort by shorted distance to fEndNode
            # only move forward, avoid loops
            if nextNode['id'] in [i[0] for i in fMyPath]: continue
            # skip if path contains more than fMaxConsecMoves consecutive moves
            fMyNewPath = fMyPath + ((nextNode['id'], nextNode['d'], nextNode['val']),)
            fMyNewPathVal = sum([i[2] for i in fMyNewPath[1::]])
            # check if we have been at this point before and if that was a cheaper path, continue
            if self.map[fMyNewPath[-1][0]].pathFrom.get(fMyNewPath[0][0], {'val': 10**21})['val'] <= fMyNewPathVal:
                continue
            else:
                # this is the cheapest way to get here
                self.map[fMyNewPath[-1][0]].pathFrom[fMyNewPath[0][0]] = {'path': fMyNewPath, 'val': fMyNewPathVal}

            if len(fMyNewPath) > fMaxConsecMoves and len(set([i[1] for i in fMyNewPath[-(fMaxConsecMoves+1)::]])) == 1:
                # print('aborting', ' '.join([i[1] for i in fMyNewPath]))
                continue
            # skip if path is more expensive than existing path
            # if len(fAllPaths) > 0 and len(fMyNewPath) > max([len(i) for i in fAllPaths]):
            if len(fAllPaths) > 0 and fMyNewPathVal > minPathVal:
                # print('skipping, because minPathVal ==', minPathVal, 'sum fMyNewPath', fMyNewPathVal)
                continue
            if len(fAllPaths) > 0 and fMyNewPathVal+nextNode['p'].co.calcDist(self.map[fEndNode].co) > minPathVal:
                # print('impossible to be shorter, thisVal', fMyNewPathVal, ' '.join([i[0] for i in fMyNewPath]))
                continue

            # print(' '.join([i[0] for i in fMyNewPath]))


            # check if we are at the fEndNode
            if nextNode['id'] == fEndNode:
                fAllPaths.append((fMyNewPathVal, fMyNewPath))
                minPathVal = min([j[0] for j in fAllPaths])
                print('found path of', fMyNewPathVal, 'min', minPathVal)
                print(' '.join([i[0] for i in fMyNewPath]))

                pass
            else:
                self.recursePath((nextNode['id'], nextNode['d'], nextNode['val']), fEndNode, fAllPaths, fMaxConsecMoves, fMyPath)
        return fAllPaths

    def printMap(self):
        for y in range(1, self.height+1):
            print(''.join([self.map['_'.join(map(str, (x,y)))].val for x in range(1, self.width+1)]))

class pathPoint:
    def __init__(self, fX, fY, fVal) -> None:
        self.co  = co(fX, fY)
        self.val = int(fVal)
        self.destinations = {}
        self.pathFrom = {}
        pass

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
    

    myMap = CrucibleMap()
    result = myMap.build(fContent=fContent)
    result = myMap.cheapestPath(co(1,1), co(myMap.width, myMap.height), 3)

    message = f'The answer to part 1 is (sample should be 102, answer should be x): {result[0]}\n'
    message += ' '.join([i[0] for i in result[1]])
    print(message)

    print(20 * '*')

    result = result

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

day = '17'
fName = f'2023/input/{day}_sample.txt'
if args.production: fName = f'2023/input/{day}.txt'

debug = args.verbose
draw = args.draw

main(None)