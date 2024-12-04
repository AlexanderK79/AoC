import argparse
import itertools
import heapq

class AocMap:
    def __init__(self) -> None:
        self.content = list()
        self.map = {}
        self.height, self.width = 0,0
        self.pq = []
        self.history = set()
        self.allPaths = []
        self.validEntries = []
        self.validEntries_p2 = []
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
                # if abs(relX + relY) != 1: continue
                if relX == 0 and relY == 0: continue
                if self.map.get(co(thisX + relX, thisY + relY).id):
                    match (relX, relY): # d = direction to get to this tile
                        case (-1, -1): d = 1
                        case (0,  -1): d = 2
                        case (1,  -1): d = 3
                        case (-1,  0): d = 4
                        case (0,  0) : d = 5 # self
                        case (1,  0) : d = 6
                        case (-1,  1): d = 7
                        case (0,  1) : d = 8
                        case (1,  1) : d = 9
                    destP = self.map[co(thisX + relX, thisY + relY).id]
                    p.destinations[destP.co.id] = {'id': destP.co.id, 'd': d, 'val': destP.val, 'p': destP}
                    pass
            pass
        return self
    

    def findWord(self, fStartNode, fDir, fThisPath, fWord, fWordPart):
        if fDir == 5 and fStartNode.val != fWord[0]:
            return

        # this function takes the current path and moves on in the same direction to find fWord
        # add the starting point to the queue
        self.pq = []
        fThisNode, fDir, fThisPath, fWord, fWordPart, fMyNewPath = fStartNode, fDir, [(fDir, fStartNode)], fWord, fWordPart, list()
        heapq.heappush(self.pq, ( (fThisNode, fDir), fThisPath, fWord, fWordPart, fMyNewPath ))
        while len(self.pq) > 0: # keep going, until the queue is empty
            thisP  = heapq.heappop(self.pq)
            (fThisNode, fDir), fThisPath, fWord, fWordPart, fMyNewPath = thisP
            del thisP
            # if we are at the end node, break(?)
            if fWordPart == fWord:
                # we are at the end
                self.validEntries.append(fThisPath)
                # break
                continue
            
            for nextNode in [nN for nN in fThisNode.destinations.values() if nN['val'] == fWord[len(fWordPart)] and (fDir == 5 or nN['d'] == fDir)]:
                fMyNewPath = fThisPath + [(nextNode['d'], nextNode['p'])]
                heapq.heappush(self.pq, ((nextNode['p'], nextNode['d']), fMyNewPath, fWord, fWord[:len(fWordPart)+1], fMyNewPath))

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
        self.val = fVal
        self.destinations = {}
        self.pathFrom = {}
        pass
    def __lt__(self, other):
        return self.co.x < other.co.x and self.co.y < other.co.y

    def __le__(self,other):
        return self.co.x <= other.co.x and self.co.y <= other.co.y

class co:
    def __init__(self, fX, fY) -> None:
        self.x, self.y = fX, fY
        self.co = (self.x, self.y)
        self.id = '_'.join(map(str, (self.co)))
        pass
    def __eq__(self, other):
        return self.co == other.co
    def calcDist(self, fCo) -> None:
        return abs(self.x - fCo.x) + abs(self.y - fCo.y)
    def betweenCos(self, fDestCo) -> None:
        # return the list of coordinates between two points if it is horizontal or vertical
        thisList = list()
        if not (self.x == fDestCo.x or self.y == fDestCo.y):
            quit()
        else:
            # 75,0   75,-30
            step_x, step_y = 1 if fDestCo.x > self.x else -1, 1 if fDestCo.y > self.y else -1
            for x in range(self.x, fDestCo.x + step_x, step_x):
                for y in range(self.y, fDestCo.y + step_y, step_y):
                    thisList.append(co(x, y))
            return thisList
        
def main(stdscr):
    with open(fName, 'r+') as f:
        fContent = f.read().splitlines()
    

    myMap = AocMap()
    myMap.build(fContent=fContent)

    word2Find = 'XMAS'

    for co in [co for co in myMap.map.values() if co.val == word2Find[0]]:
        myMap.findWord(fStartNode=co, fDir=5, fThisPath=[], fWord=word2Find, fWordPart=word2Find[0])
        pass

    result = len(myMap.validEntries)
    message = f'The answer to part 1 is (sample should be 18, answer should be x): {result}\n'
    # result = myMap_P2.cheapestPath(co(1,1), co(myMap_P2.width, myMap_P2.height), 4, 10)
    # message = f'The answer to part 2 is (sample should be 94, answer should be x): {result[0]}\n'
    print(message)

    # this is very custom for part 2
    for i in [co for co in myMap.map.values() if co.val == 'A']:
        dest_1 = ([{'val': ''}] + [dest for dest in i.destinations.values() if dest['d'] == 1])[-1]['val']
        dest_3 = ([{'val': ''}] + [dest for dest in i.destinations.values() if dest['d'] == 3])[-1]['val']
        dest_7 = ([{'val': ''}] + [dest for dest in i.destinations.values() if dest['d'] == 7])[-1]['val']
        dest_9 = ([{'val': ''}] + [dest for dest in i.destinations.values() if dest['d'] == 9])[-1]['val']
        if dest_1 + dest_9 in ('SM', 'MS') and dest_3 + dest_7 in ('SM', 'MS'):
            myMap.validEntries_p2.append(i.co.id)

    result = len(myMap.validEntries_p2)
    message = f'The answer to part 2 is (sample should be 9, answer should be x): {result}\n'
    print(message)
    pass

# globals
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose"   , action="store_true", default=False, help="Add this to enable verbose output")
parser.add_argument("-d", "--draw"      , action="store_true", default=False, help="Add this to enable drawing")
parser.add_argument("-i", "--drawinterval", type=int, default=1, help="Add the value in ms for drawing interval")
parser.add_argument("-p", "--production", action="store_true", default=False, help="Add this to try the puzzle input")
args = parser.parse_args()

day = '04'
fName = f'2024/input/{day}_sample.txt'
if args.production: fName = f'2024/input/{day}.txt'

debug = args.verbose
draw = args.draw

main(None)