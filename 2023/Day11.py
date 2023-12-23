import argparse

class galaxyMap:
    def __init__(self) -> None:
        self.content = list()
        self.glxs = dict()
        pass
    def build(self, fContent):
        self.content = [i for i in fContent]
        # add extra space in empty rows
        posEmptyRows = [i for i, item in enumerate(fContent) if set(item) == set('.')]
        [fContent.insert(i, fContent[i]) for i in reversed(posEmptyRows)]
        TfContent = [[fLine[x] for fLine in fContent] for x in range(len(fContent[0]))] # transpose the list
        posEmptyCols = [i for i, item in enumerate(TfContent) if set(item) == set('.')]
        [TfContent.insert(i, TfContent[i]) for i in reversed(posEmptyCols)]
        self.emptyRows, self.emptyCols = posEmptyRows, posEmptyCols
        fContent = [''.join([''.join(fLine[x]) for fLine in TfContent]) for x in range(len(TfContent[0]))]
        del TfContent, posEmptyRows, posEmptyCols
        self.contentParsed = fContent
        for (y, item) in enumerate(self.content):
            for x in [pos for pos, thisChar in enumerate(item) if thisChar == '#']:
                thisCo = co(x, y)
                self.glxs[thisCo.id] = {'co': thisCo}
                pass
            pass
        self.glxs_keys = [k for k in self.glxs.keys()]
        return self

class co:
    def __init__(self, fX, fY) -> None:
        fX, fY = map(int, ((fX, fY)))
        self.x, self.y = fX, fY
        self.co = (self.x, self.y)
        self.id = '_'.join(map(str, (self.co)))
    def calcDist(self, fCo, fMap, fMultiplier):
        # count how many empty cols there are and add these to the result
        thisMc = len([i for i in fMap.emptyCols if min(self.x, fCo.x) < i < max(self.x, fCo.x) ])
        thisMr = len([i for i in fMap.emptyRows if min(self.y, fCo.y) < i < max(self.y, fCo.y) ])
        return abs(self.x - fCo.x) - thisMc + (fMultiplier*thisMc) + abs(self.y - fCo.y) - thisMr + (fMultiplier * thisMr)

def main(stdscr):
    with open(fName, 'r+') as f:
        fContent = f.read().splitlines()

    myMap = galaxyMap()
    result = myMap.build(fContent=fContent)
    # calc the distance of every galaxy with the next
    fMultiplier = 2
    result = [[myMap.glxs[myMap.glxs_keys[i]]['co'].calcDist(myMap.glxs[myMap.glxs_keys[j]]['co'], myMap, fMultiplier) for j in range(i+1, len(myMap.glxs_keys))] for i in range(len(myMap.glxs_keys))]
    result = sum([sum(rr) for rr in [r for r in result]])

    message = f'The answer to part 1 is (sample should be 374, answer should be 9599070): {result}'
    print(message)

    print(20 * '*')

    fMultiplier = 10
    fMultiplier = 1000000 if args.production else fMultiplier
    result = [[myMap.glxs[myMap.glxs_keys[i]]['co'].calcDist(myMap.glxs[myMap.glxs_keys[j]]['co'], myMap, fMultiplier) for j in range(i+1, len(myMap.glxs_keys))] for i in range(len(myMap.glxs_keys))]
    result = sum([sum(rr) for rr in [r for r in result]])

    message = f'The answer to part 2 is (sample should be 1030, answer should be 842645913794): {result}'
    print(message)
    pass


# globals
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose"   , action="store_true", default=False, help="Add this to enable verbose output")
parser.add_argument("-d", "--draw"      , action="store_true", default=False, help="Add this to enable drawing")
parser.add_argument("-i", "--drawinterval", type=int, default=1, help="Add the value in ms for drawing interval")
parser.add_argument("-p", "--production", action="store_true", default=False, help="Add this to try the puzzle input")
args = parser.parse_args()

day = '11'
fName = f'2023/input/{day}_sample.txt'
if args.production: fName = f'2023/input/{day}.txt'

debug = args.verbose
draw = args.draw

main(None)