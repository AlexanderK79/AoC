import argparse
import itertools
import heapq

class CrucibleMap:
    def __init__(self) -> None:
        self.content = list()
        self.map = {}
        self.height, self.width = 0,0
        self.pq = []
        self.history = set()
        self.allPaths = []
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
        fEndCo = co(9,1) if not args.production and not args.verbose else fEndCo
        self.explorePathClean(fStartCo.id, fEndCo.id, fMaxConsecMoves)
        return sorted(self.allPaths,  key=lambda item: item[0])[0]

    def explorePathClean(self, fStartNode, fEndNode, fMaxConsecMoves):
        # add the starting point to the queue
        self.pq = []
        minPathVal = 9*(self.width+self.height)
        fEstimatedCost, fCost, fThisNode, fDir, fNumConsecMoves, fMyNewPath = 9*(self.width+self.height), 0, fStartNode, '.', 0, tuple(((fStartNode, '.', 0),))
        heapq.heappush(self.pq, (fEstimatedCost, fCost, fThisNode, fDir, fNumConsecMoves, fMyNewPath))
        # provide sort order of points to explore that will be unique, making sure to try the best first
        while len(self.pq) > 0: # keep going, until the queue is empty
            # print('size of history: ', len(self.history), 'queue', len(self.pq))
            # [print('queue:',i[0], i[3], i[4], i[1]) for i in self.pq[:5]]
            thisP  = heapq.heappop(self.pq)
            fEstimatedCost, fCost, fThisNode, fDir, fNumConsecMoves, fThisPath = thisP
            del thisP
            # if we are at the end node, break(?)
            if fThisNode == fEndNode:
                # we are at the end
                self.allPaths.append((fCost, fThisPath))
                minPathVal = min([j[0] for j in self.allPaths])
                print('found path of', fCost, 'min', minPathVal)
                self.printMap({i[0]: i[1] for i in fThisPath})
                pass
                break
                # continue
            
            # maintain a list of all points, direction and consecmoves already visited
            fHistEntry = (fThisNode, fDir, fNumConsecMoves)
            if fHistEntry in self.history:
                pass
                continue
            else:
                self.history.add(fHistEntry)
            del fHistEntry

            for nextNode in self.map[fThisNode].destinations.values():
                if len(fThisPath) > 1 and nextNode['id'] == fThisPath[-2][0]:
                    continue # don't return to the previous node
                fMyNewPath = fThisPath + ((nextNode['id'], nextNode['d'], fCost+nextNode['val']),)
                fMyNewPathVal = fMyNewPath[-1][2]
                if fMyNewPath[-2][1] == fMyNewPath[-1][1]:
                    fNewNumConsecMoves = fNumConsecMoves + 1
                else:
                    fNewNumConsecMoves = 1
                
                #check if it fits the constraint of fMaxConsecMoves
                if fNewNumConsecMoves > fMaxConsecMoves:
                    pass
                    continue

                fEstimatedCost = fMyNewPathVal + (1*nextNode['p'].co.calcDist(self.map[fEndNode].co))
                heapq.heappush(self.pq, (fEstimatedCost, fMyNewPathVal, nextNode['id'], nextNode['d'], fNewNumConsecMoves, fMyNewPath))
                # remove duplicates and sort the queue
                # a = [];[a.append(i) for i in self.pq if (i not in a) and max((i[1], i[1]+(1*self.map[i[3]].co.calcDist(self.map[fEndNode].co)))) < minPathVal];self.pq = sorted(a);del a
                # a = [];[a.append(i) for i in self.pq if (i not in a)];self.pq = sorted(a);del a
                # self.pq = list(filter(lambda item: item[1] <= minPathVal, self.pq))
                pass
                

            pass
            
            


    def printMap(self, fPath={}):
        for y in range(1, self.height+1):
            if fPath == {}:
                print(''.join(map(str,[self.map['_'.join(map(str, (x,y)))].val for x in range(1, self.width+1)])))
            else:
                print(''.join(map(str,[fPath.get('_'.join(map(str, (x,y))), self.map['_'.join(map(str, (x,y)))].val) for x in range(1, self.width+1)])))


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

    message = f'The answer to part 1 is (sample should be 102/29 to 9_1, answer should be 1076): {result[0]}\n'
    # message += ' '.join([i[0] for i in result[1]]) + '\n'
    # message += '   '.join([i[1] for i in result[1]])
    print(message)
    # myMap.printMap({i[0]: i[1] for i in result[1]})

    print(20 * '*')
    quit()

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