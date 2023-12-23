import argparse
import curses
from curses import wrapper

class ScreenMatrix:
    def __init__(self) -> None:
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_YELLOW)
        ATTR = curses.color_pair(1)
        max_y, max_x = stdscr.getmaxyx()
        begin_x, begin_y = 5, 1
        begin_x, begin_y = 5, 5
        padding = 5
        self.matrix = []
        self.height, self.width = 3, max_x - begin_x
        matrix_height, matrix_width = len(Fmatrix_1), max(list(map(lambda x: len(x), Fmatrix_1)))
        height, width = matrix_height + 2, matrix_width+2
        self.winHeader = curses.newwin(height, width, begin_y, begin_x)
        pass

def draw_Screen(header, Fmatrix_1, Fmatrix_2, Fmatrix_3):
    stdscr.erase()
    stdscr.refresh()

    if draw: draw_Matrix(Fmatrix_1, begin_x, begin_y, height, width, ATTR)
    # begin_x = 45
    # if draw: draw_Matrix(Fmatrix_2, begin_x, begin_y, height, width, ATTR)
    # begin_x = 85
    # ATTR = curses.color_pair(2) + curses.A_BLINK
    # if draw: draw_Matrix(Fmatrix_3, begin_x, begin_y, height, width, ATTR)

    winHeader.erase()
    winHeader.addstr(0, 0, header)
    winHeader.addstr(1, 0, 'Press any key for the next step...')
    winHeader.refresh()
    if not debug: stdscr.timeout(1000//500)
    keyInput = stdscr.getch()
    if keyInput in [0, 27]: exit()
    

def draw_Matrix(Fmatrix, begin_x, begin_y, height, width, ATTR):
    # winMatrix = curses.newwin(height, width, begin_y, begin_x)
    max_y, max_x = stdscr.getmaxyx()
    winMatrix = curses.newpad(height, width)
    winMatrix.scrollok(True)
    winMatrix.erase()
    winMatrix.border()
    for y in range(0, len(Fmatrix)):
        conv = lambda i : i or '' # convert None to ''
        for x in range(0,len(Fmatrix[y])):
            winMatrix.addstr(y+1, x+1, str(conv(Fmatrix[y][x])).strip(), ATTR)
    # winMatrix.refresh()
    winMatrix.refresh(0, 0, begin_y, begin_x, max_y-begin_y, max_x-begin_x)


class MapGrid:
    def __init__(self, fContent) -> None:
        self.map = dict() # costring: {x: x, y: y, val: (# = rock, o = sand, . = air, + = start)}
        self.width, self.minwidth = 0, 99999
        self.height, self.minheight = 0, 99999
        for fLine in fContent:
            dS = fLine.split(' -> ')[:-1]
            dE = fLine.split(' -> ')[1:]
            for coPair in zip(dS, dE):
                coPair = [self.coint(i) for i in coPair]
                for co in self.path(coPair[0], coPair[1]):
                    self.map[self.costring(co)] = {'x': co[0], 'y': co[1], 'val': '#'}
                    self.updateMapDimension(co)
                    pass
                pass
        pass
    def costring(self, fCo):
        if type(fCo) == str: fCo = self.coint(fCo)
        if type(fCo) == tuple: fCo = tuple(map(int.__str__, fCo))
        return '_'.join(fCo)
    def coint(self, fCo):
        if type(fCo) == str: fCo = tuple(map(int, fCo.split(',')))
        return tuple(map(int, fCo))

    def path(self, fCoS, fCoE):
        # return al co's between and including two co's
        x_range = range(min(fCoS[0], fCoE[0]), max(fCoS[0], fCoE[0])+1)
        y_range = range(min(fCoS[1], fCoE[1]), max(fCoS[1], fCoE[1])+1)
        if len(x_range) == 1: x_range = len(y_range) * list(x_range)
        if len(y_range) == 1: y_range = len(x_range) * list(y_range)
        return zip(list(x_range), list(y_range))
        pass
    def addFloor(self, fY):
        # add # at y = fY
        for x in range(self.minwidth-10, self.width+11):
            self.map[self.costring((x, fY))] = {'x': x, 'y': fY, 'val': '#'}
            self.updateMapDimension((x,fY))
    def expandFloor(self, fX):
            y = self.height
            self.map[self.costring((fX, y))] = {'x': fX, 'y': y, 'val': '#'}
            self.updateMapDimension((fX,y))


    def updateMapDimension(self, fCo):
        self.width     = max(self.width, fCo[0])
        self.height    = max(self.height, fCo[1])
        self.minwidth  = min(self.minwidth, fCo[0])
        self.minheight = min(self.minheight, fCo[1])
    def setStart(self, fCo):
        self.start = fCo
        self.map[self.costring(fCo)]= {'x': fCo[0], 'y': fCo[1], 'val': '+'}
        self.updateMapDimension(fCo)

    def printMap(self):
        fResult = []
        for y in range(self.minheight, self.height+1):
            fLine = []
            for x in range(self.minwidth ,self.width+1):
                c = self.map.get(self.costring((x,y)), ' ')
                if c != ' ': c = c['val']
                fLine.append(c)
            fResult.append(''.join(fLine))
            del fLine
        for fLine in fResult:
            print(fLine)


class Sand:
    def __init__(self,fStartCo) -> None:
        self.start = fStartCo # tuple with (x, y)
        pass

class SandPile:
    def __init__(self, fParent) -> None:
        self.parent = fParent # MapGrid of cave
        self.flowpath = []
        pass
    def drop(self):
        if len(self.flowpath) > 0:
            self.flowpath = self.flowpath[:-1]
        else:
            self.flowpath = [self.parent.start]
        if self.parent.map[self.parent.costring(self.parent.start)]['val'] == 'o':
            return # we have reached the starting point
        rest = None
        thisCo = self.flowpath[-1]
        while rest is None:
            while rest is None:
                # next co-order: (x, y+1), (x-1, y+1), (x+1, y+1)
                for destCo in ((thisCo[0], thisCo[1]+1),(thisCo[0]-1, thisCo[1]+1),(thisCo[0]+1, thisCo[1]+1) ):
                    # check if destCo is on the map
                    if destCo[0] not in range(self.parent.minwidth, self.parent.width+1) or destCo[1] not in range(self.parent.minheight, self.parent.height+1) :
                        rest = False
                        break
                    destResult = self.parent.map.get(self.parent.costring(destCo), ' ')
                    if destResult == ' ': # if val not in ('#', 'o')
                        self.flowpath.append(destCo)
                        thisCo = destCo
                        break
                if rest is None and destResult != ' ':
                    self.parent.map[self.parent.costring(thisCo)] = {'x': thisCo[0], 'y': thisCo[1], 'val': 'o'}
                    self.parent.updateMapDimension(thisCo)
                    rest = True
                pass
            pass
        pass

def main(stdscr):
    with open(fName, 'r+') as f:
        fContent = f.read().splitlines()
        myMap = MapGrid(fContent)
        myMapTwo = MapGrid(fContent)

    myMap.setStart((500,0))
    myMapTwo.setStart((500,0))
    myPile = SandPile(myMap)
    prev_result, result = -1, 0
    while prev_result < result:
        prev_result = result
        myPile.drop()
        result = len([i for i in myMap.map.values() if i['val'] == 'o'])
        pass
    myMap.printMap()
    

    message = f'The answer to part 1 is (sample should be 24, answer should be x): {result}'
    print(message)

    print(20 * '*')

    myMap = myMapTwo
    myMap.addFloor(myMap.height+2)
    myPile = SandPile(myMap)

    prev_result, result = -1, 0
    while prev_result < result:
        prev_result = result
        # expand the floor if there is a drop of sand on or near the edge
        Lco, Rco = (myMap.minwidth+1, myMap.height-1), (myMap.width-1, myMap.height-1)
        if (myMap.map.get(myMap.costring(Lco), {'val': ' '})['val'] == 'o'): myMap.expandFloor(Lco[0]-2)
        if (myMap.map.get(myMap.costring(Rco), {'val': ' '})['val'] == 'o'): myMap.expandFloor(Rco[0]+2)
        myPile.drop()
        result = len([i for i in myMap.map.values() if i['val'] == 'o'])
        pass

    myMap.printMap()

    result = result

    message = f'The answer to part 2 is (sample should be 93, answer should be x): {result}'
    print(message)


# globals
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose"   , action="store_true", default=False, help="Add this to enable verbose output")
parser.add_argument("-d", "--draw"      , action="store_true", default=False, help="Add this to enable drawing")
parser.add_argument("-i", "--drawinterval", type=int, default=1, help="Add the value in ms for drawing interval")
parser.add_argument("-p", "--production", action="store_true", default=False, help="Add this to try the puzzle input")
args = parser.parse_args()

day = '14'
fName = f'2022/input/{day}_sample.txt'
if args.production: fName = f'2022/input/{day}.txt'

debug = args.verbose
draw = args.draw

stdscr = curses.initscr()
curses.start_color()
curses.use_default_colors()
wrapper(main)

# main(None)