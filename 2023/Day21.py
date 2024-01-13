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
            # y += 1 # make it 1-based instead of 0-based
            self.matrix
            for (x,thisChar) in enumerate(thisLine):
                # x += 1 # make it 1-based instead of 0-based
                thisCo = co(x, y, thisChar)
                self.matrix[thisCo.id] = thisCo
        self.height, self.width = y, x
        self.startingCo = [i.id for i in self.matrix.values() if i.val == 'S'][0]
        # set all neighboors
        for p in self.matrix.values():
            thisX, thisY = p.x, p.y
            for relX, relY in ((-1,0), (1,0), (0,-1), (0,1)):
                thisNb = self.matrix.get(co(thisX + relX, thisY + relY).id, self.matrix.get(co((thisX + relX ) % self.width, (thisY + relY) % self.height).id, 'why'))
                thisNb = self.matrix.get(co(thisX + relX, thisY + relY).id)
                if thisNb == 'why': 
                    print('error opening', (thisX + relX ) % self.width, (thisY + relY) % self.height)
                    quit()
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

def calcMaps(fCycles):
    # returns a tuple with (#even maps, #odd maps)
    p = fCycles % 2 
    if p == 0:
        full_odd_maps  = sum([(i-1)*4 for i in range (fCycles-1,0,-2)] + [1])
        full_even_maps = sum([(i-1)*4 for i in range (fCycles, 0,-2)])
    elif p == 1:
        full_odd_maps  = sum([(i-1)*4 for i in range (fCycles,0,-2)] + [1])
        full_even_maps = sum([(i-1)*4 for i in range (fCycles-1, 0,-2)])
    return(full_even_maps, full_odd_maps)

def calcDest(fCycles, fSteps, full, quarter):
    p = fSteps % 2 
    restPaths, thisQuar = 4197 + ((fCycles-1) * 30945), quarter[p]
    maps = calcMaps(fCycles)
    fResult = (maps[0] * full[p-1]) + (maps[1] * full[p] ) + restPaths + thisQuar
    print('Calculation: based on (', maps[0], 'even submaps *', full[p-1], ') + (', maps[1], 'odd submaps *', full[p], ') + (restPaths = ', restPaths, ') + ', thisQuar,' quarter =',  fResult, '\n')
    return fResult


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
    # it will take 26501365 steps
    # the map is a square of 131 x 131; S is in the center on 65,65
    # there are highways without blocking rocks from the center to each edge and around the edges
    # it takes 65 steps to reach the edge and 131 steps to reach a corner
    # in that many steps, some submaps of the map will always be completely filled, we can just count the odd and even numbers for those maps and multiply
    # the submaps around the edge that are about to be filled have to be simulated
    # how to determine which maps to simulate?
    # each map that can be reached within // 131 steps
    # check if after 130/131/132 steps the filling of a single map changes; 132 should be the same as 130 or we're screwed
    # Processed step: 130 Possibledests 7747
    # Processed step: 131 Possibledests 7702
    # Processed step: 132 Possibledests 7747
    # Processed step: 133 Possibledests 7702

    # cycle	full	half	q							5				
    # 1	    1	    0	    4						5	4	5			
    # 2	    5	    4	    4					5	4	3	4	5		
    # 3	    13  	8	    4				5	4	3	2	3	4	5	
    # 4	    25  	12	    4			5	4	3	2	1	2	3	4	5
    # 5	    41  	16	    4				5	4	3	2	3	4	5	
    # 	    		        					5	4	3	4	5		
    # 	    		        						5	4	5			
    # 	    		        							5				
    # calculation:
    # full_odd  = sum([(i-1)*4 for i in range (cycles-1,1,-2)])
    # full_even = sum([(i-1)*4 for i in range (cycles,1,-2)] + [1])
    # half = (cycles-1) * 4
    # quar = 4
    #
    # a cycle reaches a maximum:
    # the inside corner or the center of a horizontal/vertical adjacent map (taking out a quarter, including the edge itself)
    # check for every quarter how much is filled after 131 steps
    # idem for every half type (both halves \, both halves / )
    # create a 15x15 map of submaps
    # count number of filled of each type after 4 cycles (answer in the end needs to be after odd steps, but even cycles) and subtract the full maps
    # 4 cycles, means 1 odd parity, 4 even, 8 odd, 12 even
    # 26501365 steps // 131 = 202300 cycles + 65 steps
    # then process for 2, 8, 12 cycles and count the number and calculate the number and see if it matches

    myMap = gardenMap()
    maxCycles = args.cycles
    myMap.build(fContent=((2*maxCycles)+1) * [((2*maxCycles)+1) * line for line in fContent])
    #adjust startCo to be in the center
    submap_h = len(fContent)
    sCo = myMap.matrix[myMap.startingCo]
    myMap.startingCo = co((maxCycles * submap_h) + sCo.x, (maxCycles * submap_h) + sCo.y).id
    sCo = myMap.matrix[myMap.startingCo]
    baseRange = (range(sCo.x-(submap_h//2)+1, sCo.x+(submap_h//2)))
    print (myMap.startingCo, baseRange)
    pass

    # count number of filled of each type after 4 cycles (answer in the end needs to be after odd steps, but even cycles) and subtract the full maps
    # 4 cycles, means 1 odd parity, 4 even, 8 odd, 12 even
    # even = Possibledests 7747
    # odd  = Possibledests 7702
    allSteps = 26501365
    allCycles, remainingSteps = allSteps // submap_h, allSteps % submap_h

    possibleDests = [c for c in myMap.matrix[myMap.startingCo].neighboors.values() if c.val in ('.', 'S')]
    full = (7747, 7702) # even PossibleDests = 7747, odd = 7702
    for step in range(2,allSteps+1):
        possibleDests = set([item for sublist in [[c for c in d.neighboors.values() if c.val in ('.', 'S')] for d in possibleDests] for item in sublist])
        if args.verbose:
            print('step:', step)
            myMap.printmap(fReversed=False, fPath={c.id: 'O' for c in possibleDests})
        cycles     = step // submap_h
        if cycles > maxCycles: break
        quarter    = [0, 0]
        rest_small = [0, 0]
        rest_big   = [0, 0]
        if cycles > 0 and step % submap_h == remainingSteps:
            print('Processed cycle:', cycles, 'step:', step, 'Possibledests', len(possibleDests))
            # depending on the parity of the steps (even or odd), the value of each submap switches
            # in odd number of steps, submap 1 has 7702 destinations, in even number of steps it is 7747
            p = step % 2 # even = 0, odd = 1

            if True: #cycles in (1, 2, 3):
                distToOut = (cycles * submap_h) - (submap_h//2)
                quarter[p] = len([c for c in possibleDests if (c.y in baseRange and abs(sCo.x - c.x) >= distToOut) or (c.x in baseRange and abs(sCo.y - c.y) >= distToOut)])
                maps = calcMaps(cycles)
                rest_small[p] = ( len(possibleDests) - quarter[p] - (maps[0] * full[p-1]) - (maps[1] * full[p]) )
                rest_big[p]   = 0
            print ('maps:', maps, 'full:', full)
            print ('parity', 'odd' if p == 1 else 'even', 'rest_small', rest_small[p], 'rest_big', rest_big[p], 'quarter', quarter[p])

            result = calcDest(cycles, step, full, quarter)
            result = calcDest(allCycles, allSteps, full, quarter)

    result = calcDest(allCycles, allSteps, full, quarter, rest_small, rest_big)
    message = f'The answer to part 2 is (sample should be x, answer should be 632.257.949.158.206, 3.153.435.759, 12.722.503.990, 632.254.851.334.401 are too low, 632.257.938.881.841 incorrect): {result}'
    print(message)
    pass


# globals
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose"   , action="store_true", default=False, help="Add this to enable verbose output")
parser.add_argument("-d", "--draw"      , action="store_true", default=False, help="Add this to enable drawing")
parser.add_argument("-i", "--drawinterval", type=int, default=1, help="Add the value in ms for drawing interval")
parser.add_argument("-p", "--production", action="store_true", default=False, help="Add this to try the puzzle input")
parser.add_argument("-c", "--cycles", type=int, default=3, help="Add this to try the puzzle input")
args = parser.parse_args()

day = '21'
fName = f'2023/input/{day}_sample.txt'
if args.production: fName = f'2023/input/{day}.txt'

debug = args.verbose
draw = args.draw

main(None)