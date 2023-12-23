import argparse
import curses
from curses import wrapper
import re

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
        self.width, self.minwidth = 0, float('inf')
        self.height, self.minheight = 0, float('inf')
        for fLine in fContent:
            matches = re.match('^Sensor at (x=(-*\d+)), (y=(-*\d+)): closest beacon is at (x=(-*\d+)), (y=(-*\d+))$', fLine).groups()
            xS, yS, valS, xB, yB, valB = int(matches[1]), int(matches[3]), 'S', int(matches[5]), int(matches[7]), 'B'
            self.map[self.costring((xB, yB))] = {'x': xB, 'y': yB, 'val': valB, 'node': Beacon(self, (xB, yB))}
            self.map[self.costring((xS, yS))] = {'x': xS, 'y': yS, 'val': valS, 'node': Sensor(self, (xS, yS), self.map[self.costring((xB, yB))]['node'])}
            self.updateMapDimension((xS,yS))
            self.updateMapDimension((xB,yB))
            if debug:
                for thisSensor in [s['node'] for s in self.map.values() if s['val'] == 'S']:
                    for co in thisSensor.get_radius():
                        self.updateMapDimension(co)
                        thisCo = self.map.get(self.costring(co), None)
                        if thisCo is None:
                            self.map[self.costring(co)] = {'x': co[0], 'y': co[1], 'val': '#'}
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

    def updateMapDimension(self, fCo):
        self.width     = max(self.width, fCo[0])
        self.height    = max(self.height, fCo[1])
        self.minwidth  = min(self.minwidth, fCo[0])
        self.minheight = min(self.minheight, fCo[1])

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

class Sensor():
    def __init__(self, fParent, fCo, fBeacon) -> None:
        self.parent = fParent
        self.beacon = fBeacon
        self.beacon.sensor = self
        self.co = fCo
        self.x, self.y = fCo[0], fCo[1]
        self.radius = abs(self.x-fBeacon.x) + abs (self.y-fBeacon.y)
        pass
    def co_in_sensor_range(self, fCo):
        # check if a coordinate is in range of the sensor
        (x, y) = fCo
        xdist = abs(x-self.x)
        ydist = abs(y-self.y)
        if xdist + ydist > self.radius:
            # out of range
            return False
        else:
            # in range
            return True

    def y_range(self, fY):
        # returns the range of x co's on the specific y co
        if abs(self.y - fY) > self.radius:
            #fY out of range
            return None
        else:
            y = fY
            xdist = abs(abs(self.y - y) - self.radius)
            return (self.x-xdist, self.x+xdist)

    def get_radius(self):
        # return al co's in the radius of fCo
        co_list = []
        for y in range(self.y - self.radius, self.y + self.radius + 1):
            xdist = abs(abs(self.y - y) - self.radius)
            co_list += self.parent.path((self.x-xdist, y), (self.x+xdist, y))
            pass
        co_list.remove(self.co)
        return co_list

class Beacon():
    def __init__(self, fParent,fCo) -> None:
        self.parent = fParent
        self.co = fCo
        self.x, self.y = fCo[0], fCo[1]
        self.sensor = None
        pass

def main(stdscr):
    with open(fName, 'r+') as f:
        fContent = f.read().splitlines()
        myMap = MapGrid(fContent)

    if debug: myMap.printMap()

    ymark = 10 if debug else 2000000
    ranges = sorted(list(filter(lambda x: x is not None, [s['node'].y_range(ymark) for s in myMap.map.values() if s['val'] == 'S'])))
    result_ranges = [ranges[0]]

    for r in ranges[1::]:
        (s,e) = r
        for rr in result_ranges:
            (rrs, rre) = rr
            if (s <= rrs-1 <= e+1 <= rre ) or (rrs <= s-1 <= rre+1 <= e):
                # current range partially overlaps, adjust it
                result_ranges[result_ranges.index(rr)] = (min(s, rrs), max(e, rre))
                pass
            elif s > rre or e < rrs:
                # current range outside of examined range
                result_ranges.append((s,e))
                pass
            elif rrs <= s <= e <= rre:
                # current range contained
                pass
            else:
                # why do we get here
                pass
    
    #result = len([i for i in myMap.map.values() if i['y'] == 10 and i['val'] == '#'])
    result = sum([e-s for (s,e) in result_ranges])
    del s, e, r, rr, f, fContent, rrs, rre, result_ranges, ranges, ymark

    message = f'The answer to part 1 is (sample should be 26, answer should be 5125700): {result}'
    print(message)


    print(20 * '*')
    # move around the edges of each sensor and check if the
    # is in range of one of the other sensors
    lstSensors = [i['node'] for i in myMap.map.values() if i['val']=='S']

    search_square = range(0, 21) if debug else range(0, 4000001)
    coFound = False
    for s in lstSensors:
        if coFound: break
        startCo = (s.x, s.y - s.radius -1) # travel around edge
        curCo = startCo
        blFirst = True
        (x, y) = (None, None)
        while blFirst or (not coFound and curCo != startCo):
            blFirst = False
            if curCo[0] in search_square and curCo[1] in search_square:
                result = set([othS.co_in_sensor_range(curCo) for othS in lstSensors])
                if result == set([False]):
                    #we've got him
                    (x, y) = curCo
                    coFound = True
                    break
            if curCo[0] >= s.x and curCo[1] < s.y: # top-right
                x_incr, y_incr = 1,1
            elif curCo[0] > s.x and curCo[1] >= s.y: # bottom-right
                x_incr, y_incr = -1,1
            elif curCo[0] <= s.x and curCo[1] > s.y: # bottom-left
                x_incr, y_incr = -1,-1
            elif curCo[0] < s.x and curCo[1] <= s.y: # top-left
                x_incr, y_incr = 1,-1
            else:
                pass # why do we get here
            curCo = (curCo[0]+x_incr, curCo[1]+y_incr)

    result = (x * 4000000 ) + y

    message = f'The answer to part 2 is (sample should be 56000011, answer should be 11379394658764): {result}'
    print(message)


# globals
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose"   , action="store_true", default=False, help="Add this to enable verbose output")
parser.add_argument("-d", "--draw"      , action="store_true", default=False, help="Add this to enable drawing")
parser.add_argument("-i", "--drawinterval", type=int, default=1, help="Add the value in ms for drawing interval")
parser.add_argument("-p", "--production", action="store_true", default=False, help="Add this to try the puzzle input")
args = parser.parse_args()

day = '15'
fName = f'2022/input/{day}_sample.txt'
if args.production: fName = f'2022/input/{day}.txt'

debug = args.verbose
draw = args.draw

stdscr = curses.initscr()
curses.start_color()
curses.use_default_colors()
wrapper(main)

# main(None)