import argparse
import matplotlib.pyplot as plt

class hailStorm:
    def __init__(self) -> None:
        self.content = list()
        self.hailstones = list()
        self.intersections = dict()
        self.minXY, self.maxXY = int(), int()

    def build(self, fContent):
        self.content = fContent
        for thisLine in fContent:
            (x,y,z),(dx,dy,dz) = [map(int, p.split(', ')) for p in thisLine.split(' @ ')]
            self.hailstones.append(line_2D(dy/dx, (y+(dy*(x/-dx))), fFuture=(y, -1 if dy < 0 else 1)))
        pass
        # with an X and Y position each at least 7 and at most 27, production 200000000000000, 400000000000000;
        if args.production:
            self.minXY, self.maxXY = 200000000000000, 400000000000000
        else:
            self.minXY, self.maxXY = 7, 27
        self.intersections = {thisL: [(nextL, line_intersect(thisL, nextL, self.minXY, self.maxXY)) for nextL in self.hailstones if nextL != thisL] for thisL in self.hailstones}
        pass

class line_2D:
    def __init__(self, fSlope, fConst, fFuture) -> None:
        self.slope = fSlope
        self.const = fConst
        self.future = fFuture # init y value and value of y shrinks (-1) or grows (+1) in the future
        pass

def line_intersect(L1, L2, fMin, fMax):
    if (L2.slope-L1.slope) == 0: # parallel lines
        return (0, (False, False))
    x=(L1.const-L2.const)/(L2.slope-L1.slope)
    y=L1.slope*x+L1.const
    # if y < const and slope > 0, it is in the past, then quit
    timing = 0
    for thisL in (L1, L2):
        if   (y > thisL.future[0] and thisL.future[1] ==  1) or (y < thisL.future[0] and thisL.future[1] == -1): timing += 1 # future
        elif (y > thisL.future[0] and thisL.future[1] == -1) or (y < thisL.future[0] and thisL.future[1] ==  1): timing -= 1 # past
        else: assert(timing != None)
    if args.verbose:
        X=[x for x in range(fMin,fMax)]
        Y1=[(L1.slope*x)+L1.const for x in X]
        Y2=[(L2.slope*x)+L2.const for x in X]
        plt.plot(X,Y1,'-r',label=f'L1 y={L1.slope}x+{L1.const}')
        plt.plot(X,Y2,'-b',label=f'L2 y={L2.slope}x+{L2.const}')
        plt.legend(loc='upper right', title=f'crosses at ({x}, {y})')
        plt.show()
    return (timing, (x,y))
    pass

def main(stdscr):
    with open(fName, 'r+') as f:
        fContent = f.read().splitlines()

    myHS = hailStorm()
    result = myHS.build(fContent=fContent)

    result = [[k[1] for k in [j[1] for j in i] if k[0] == 2 and myHS.minXY <= k[1][0] <= myHS.maxXY and myHS.minXY <= k[1][1] <= myHS.maxXY] for i in myHS.intersections.values()]

    result = sum(len(i) for i in result) // 2
    message = f'The answer to part 1 is (sample should be 2, answer should be 24627): {result}'
    print(message)

    print(20 * '*')

    result = result

    message = f'The answer to part 2 is (sample should be 2, answer should be x): {result}'
    print(message)
    pass


# globals
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose"   , action="store_true", default=False, help="Add this to enable verbose output")
parser.add_argument("-d", "--draw"      , action="store_true", default=False, help="Add this to enable drawing")
parser.add_argument("-i", "--drawinterval", type=int, default=1, help="Add the value in ms for drawing interval")
parser.add_argument("-p", "--production", action="store_true", default=False, help="Add this to try the puzzle input")
args = parser.parse_args()

day = '24'
fName = f'2023/input/{day}_sample.txt'
if args.production: fName = f'2023/input/{day}.txt'

debug = args.verbose
draw = args.draw

main(None)