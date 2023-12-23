import argparse
import re
import math

class sampleClass:
    def __init__(self, fParent) -> None:
        self.attr = fParent
        self.list = []
        pass
    def build(self, fContent):
        self.example = fContent
        return self

def calcDist(fRaceLen, fHold):
    return (fRaceLen-fHold) * fHold if fHold < fRaceLen else 0

def quadform(a, b, c):
  return [(-b + s * math.sqrt(b*b - 4*a*c)) / (2*a) for s in (-1, 1)]

def main(stdscr):
    with open(fName, 'r+') as f:
        fContent = f.read().splitlines()
    
    myRaces = zip(re.split('\s+', fContent[0])[1::], re.split('\s+', fContent[1])[1::])
    bestResults = dict()
    myRaces = [list(map(int, i)) for i in myRaces]
    for i in myRaces:
        bestResults[str(i[0])] = list()
        for j in range(0, i[0]):
            thisResult = calcDist(i[0], j)
            bestResults[str(i[0])] .append((j, thisResult)) if thisResult > i[1] else None
            pass
        pass

    result = math.prod([len(i) for i in bestResults.values()])


    message = f'The answer to part 1 is (sample should be 288, answer should be 500346): {result}'
    print(message)

    print(20 * '*')

    # part 2
    myRaces = list(map(int, (fContent[0].replace(' ', '').split(':')[1], fContent[1].replace(' ', '').split(':')[1])))

    # snijpunt van parabool en lijn; aantal punten op x tussen de twee is het antwoord
    # sample parabool (x = tijd, y = distance; x<=71530): y = (71530 - x) * x
    # sample lijn: y = 940200
    # 940200 = 71530x -x**2
    # -x**2 + 71530x - 940200 = 0
    # abc formule
    # x = ( -b +_ V(b**2 - 4ac) ) / 2a

    a,b,c = (-1, 51926890, -222203111261225) if args.production else (-1, 71530, -940200)
    result = quadform(a, b, c)
    result = list(map(int, reversed(sorted(result))))
    result = result[0] - result[1]
    message = f'The answer to part 2 is (sample should be 71503, answer should be 42515755): {result}'
    print(message)
    pass


# globals
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose"   , action="store_true", default=False, help="Add this to enable verbose output")
parser.add_argument("-d", "--draw"      , action="store_true", default=False, help="Add this to enable drawing")
parser.add_argument("-i", "--drawinterval", type=int, default=1, help="Add the value in ms for drawing interval")
parser.add_argument("-p", "--production", action="store_true", default=False, help="Add this to try the puzzle input")
args = parser.parse_args()

day = '06'
fName = f'2023/input/{day}_sample.txt'
if args.production: fName = f'2023/input/{day}.txt'

debug = args.verbose
draw = args.draw

main(None)