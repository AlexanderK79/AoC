import argparse
import itertools
import heapq

class Line:
    def __init__(self) -> None:
        self.content = list()
        self.steps = list()
        self.cos = list()
        self.cos_with_distance = list()
        pass
    def build(self, fInitCo, fContent):
        self.__init__
        self.content = fContent
        for thisStep in fContent.split(','):
            self.steps.append({'direction': thisStep[0], 'value': int(thisStep[1:]), 'value.x': int, 'value.y': int, 'co.start': co, 'co.end': co, 'cos': list() , 'cos_with_distance': list() })
            lastStep = self.steps[-1]
            lastStep['co.start'] = self.steps[-2]['co.end'] if len(self.steps) > 1 else fInitCo
            startDist = self.steps[-2]['cos_with_distance'][-1]['distance'] if len(self.steps) > 1 else 0
            match (lastStep['direction']):
                case ('L'): lastStep['value.x'], lastStep['value.y'] = -lastStep['value'], 0
                case ('R'): lastStep['value.x'], lastStep['value.y'] = lastStep['value'], 0
                case ('U'): lastStep['value.x'], lastStep['value.y'] = 0, lastStep['value']
                case ('D'): lastStep['value.x'], lastStep['value.y'] = 0, -lastStep['value']
            pass
            lastStep['co.end'] = co(lastStep['co.start'].x + lastStep['value.x'], lastStep['co.start'].y + lastStep['value.y'])
            lastStep['cos'] = lastStep['co.start'].betweenCos(lastStep['co.end'])
            lastStep['cos_with_distance'] = lastStep['co.start'].betweenCosWithDistance(lastStep['co.end'], startDist)
            assert len(lastStep['cos']) == lastStep['value']+1, "Error: invalid number of cos"
        tmpCos = [d['cos'] for d in self.steps]
        self.cos = list(itertools.chain(*tmpCos))
        tmpCos = [d['cos_with_distance'] for d in self.steps]
        self.cos_with_distance = list(itertools.chain(*tmpCos))
        return self
    

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
    def betweenCosWithDistance(self, fDestCo, fDist) -> None:
        # return the list of coordinates between two points if it is horizontal or vertical
        thisList = list()
        if not (self.x == fDestCo.x or self.y == fDestCo.y):
            quit()
        else:
            # 75,0   75,-30
            step_x, step_y = 1 if fDestCo.x > self.x else -1, 1 if fDestCo.y > self.y else -1
            for x in range(self.x, fDestCo.x + step_x, step_x):
                for y in range(self.y, fDestCo.y + step_y, step_y):
                    thisList.append({'co': co(x, y), 'distance': fDist + abs(x - self.x) + abs(y - self.y)})
            return thisList


def main(stdscr):
    with open(fName, 'r+') as f:
        fContent = f.read().splitlines()
    
    thisLines = list()

    for thisLine in fContent:
        thisLines.append(Line.build(Line(), co(0, 0), thisLine))
    
    intersectingCos = set([thisCo.co for thisCo in thisLines[0].cos]).intersection(set([thisCo.co for thisCo in thisLines[1].cos]))
    result = min([co(thisCo[0], thisCo[1]).calcDist(co(0,0)) for thisCo in intersectingCos if thisCo != (0,0)])

    message = f'The answer to part 1 is (sample should be 159, answer should be 855): {result}\n'
    print(message)

    print(20 * '*')

    intersectingCos = set([thisCo["co"].co for thisCo in thisLines[0].cos_with_distance]).intersection(set([thisCo["co"].co for thisCo in thisLines[1].cos_with_distance if thisCo["co"].co != (0,0)]))

    a = [(thisCo["co"].co, thisCo["distance"]) for thisCo in sorted(thisLines[0].cos_with_distance, key=lambda d: d["co"].co) if thisCo["co"].co in intersectingCos]
    b = [(thisCo["co"].co, thisCo["distance"]) for thisCo in sorted(thisLines[1].cos_with_distance, key=lambda d: d["co"].co) if thisCo["co"].co in intersectingCos]
    result = min([i[0][1] + i[1][1] for i in zip(a,b)])

    message = f'The answer to part 2 is (sample should be 610, answer should be 11238): {result}\n'
    print(message)
    pass


# globals
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose"   , action="store_true", default=False, help="Add this to enable verbose output")
parser.add_argument("-d", "--draw"      , action="store_true", default=False, help="Add this to enable drawing")
parser.add_argument("-i", "--drawinterval", type=int, default=1, help="Add the value in ms for drawing interval")
parser.add_argument("-p", "--production", action="store_true", default=False, help="Add this to try the puzzle input")
args = parser.parse_args()

day = '03'
fName = f'2019/input/{day}_sample.txt'
if args.production: fName = f'2019/input/{day}.txt'

debug = args.verbose
draw = args.draw

main(None)