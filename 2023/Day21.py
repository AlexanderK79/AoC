import argparse

class gardenMap:
    def __init__(self) -> None:
        self.content = list()
        self.height, self.width = 0, 0
        self.startingCo = None
        self.matrix = {}
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
        # set all neighboors
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
        return self

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
        pass
    def calcDist(self, fCo) -> None:
        return abs(self.x - fCo.x) + abs(self.y - fCo.y)

def main(stdscr):
    with open(fName, 'r+') as f:
        fContent = f.read().splitlines()
    

    myMap = gardenMap()
    result = myMap.build(fContent=fContent)
    if args.verbose: myMap.printmap()
    # find path
    possibleDests = [c for c in myMap.matrix[myMap.startingCo].neighboors.values() if c.val in ('.', 'S')]
    if args.verbose:
        print('step:', 1)
        myMap.printmap(fReversed=False, fPath={c.id: 'O' for c in possibleDests})
    for step in range(2,65):
        if not args.production and step > 6: break
        possibleDests = set([item for sublist in [[c for c in d.neighboors.values() if c.val in ('.', 'S')] for d in possibleDests] for item in sublist])
        if args.verbose:
            print('step:', step)
            myMap.printmap(fReversed=False, fPath={c.id: 'O' for c in possibleDests})
    result = len(possibleDests)

    message = f'The answer to part 1 is (sample should be 16, answer should be 3814): {result}'
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

day = '21'
fName = f'2023/input/{day}_sample.txt'
if args.production: fName = f'2023/input/{day}.txt'

debug = args.verbose
draw = args.draw

main(None)