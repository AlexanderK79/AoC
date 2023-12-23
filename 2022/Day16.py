import argparse
import curses
from curses import wrapper
import re
from itertools import permutations
import copy

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
    def __init__(self, fContent, fTimer) -> None:
        self.Timer = fTimer
        self.position = None
        self.map = dict()
        self.paths = dict()
        self.failedpaths = []
        for fLine in fContent:
            matches = re.match('^(Valve (\w\w)) has (flow rate=(\d+)); (tunnel(s){0,1} lead(s){0,1} to valve(s){0,1} (.+))$', fLine).groups()
            name, flowrate, dest = matches[1], matches[3], matches[8]
            self.map[name] = Valve(self, name, flowrate, dest)
            del name, flowrate, dest
        del fContent, fLine, matches
        # process tunnels
        for v in self.map.values():
            for d in v.destLine.split(', '):
                self.map[d].dests.append(v)
                pass
            del d
        del v
        # set all initial distances
        for v in self.map.values():
            for d in self.map.keys():
                v.distance[d] = 0 if v.name == d else float('inf')
            del d
        del v
        pass

    def calc_distances(self):
        #calculate the shortest distance for every valve to every other valve
        while sum([len([j for j in i.distance.values() if j == float('inf')]) for i in self.map.values()])>0:
            for v in self.map.values():
                self.update_distance(v)
        pass

    def update_distance(self, fSrc):
        # dive down until there is no going back, return next position or False
        for d in [d for d in fSrc.dests if d.name != fSrc.name]:
            fSrc.distance[d.name], d.distance[fSrc.name] = 1, 1 # update each other's distance
            # check all other known distances and update those 
            for k, v in dict(filter(lambda v: v[1] != float('inf'), fSrc.distance.items())).items(): # take the items with a distance set
                # these are the valves with a distance to me that is known
                # let's check it's item for other known distances and add those to mine
                for oth_k, oth_v in dict(filter(lambda v: v[1] != float('inf'), self.map[k].distance.items())).items():
                    fSrc.distance[oth_k] = min(fSrc.distance[oth_k], v+oth_v)
                    self.map[oth_k].distance[k] = min(self.map[oth_k].distance[k], v+oth_v)
                del oth_k, oth_v
                pass
            del k, v
        del d
        pass
    def travel_check(self, fDest):
        if self.position.distance[fDest] < self.Timer.value:
            return True
        else:
            return False
    def travel(self, fDest):
        self.Timer.countdown(self.position.distance[fDest])
        self.position = self.map[fDest]
    def travel_and_open(self, fDest):
        self.travel(fDest)
        self.map[fDest].open()


    def calcPath(self, fStart, fPath, fTimer):
        # fPath = tuple of valves by name
        # fPosition = initial position
        # fTimer = initial value of timer
        # stores the result of the path that is reachable within fTimer
        # self.paths['path-path-path'] = value
        # return ('path-path-path', value)
        # permutation of valves where sum(traveltime)+numofitems (=traveltime) <= 30
        # result for each permutation: sum (opentime of prev - traveltime from prev - actiontime)*myFlowRate

        bestresult = 0 if len(self.paths) == 0 else max(self.paths.values())
        fPath = tuple([fStart]) + tuple(filter(lambda x: x is not None, fPath))
        # build new_path while (travel + n) < fTimer
        traveltime, i, total_released = 0, 1, 0
        pathParts = ['-'.join(j) for j in [fPath[0:i] for i in range(1,len(fPath)+1)]]
        if set(pathParts).intersection(set(self.failedpaths)):
            return (False, False)
        if set(pathParts).intersection(set(self.paths)):
            thispath = list(set(pathParts).intersection(set(self.paths)))[0]
            return (thispath, self.paths[thispath])
        while i < len(fPath) and ((traveltime + self.map[fPath[i-1]].distance[fPath[i]]) < fTimer):
            if i < len(fPath)-1 and total_released + sum(v.potential for v in self.map.values() if v.name in fPath[i:]) < bestresult:
                break # exit out of this while loop
            traveltime += self.map[fPath[i-1]].distance[fPath[i]] + 1
            total_released += (fTimer - traveltime) * self.map[fPath[i]].flowrate
            i += 1
        if i < len(fPath):
            # this might be a failed path
            i = i+1
            self.failedpaths.append('-'.join(fPath[0:i]))
            self.failedpaths.sort()
        thispath = '-'.join(fPath[0:i])
        self.paths[thispath] = total_released
        return (thispath, total_released)

    def nextStep(self, fTimer, fSrc, fList):
        bestResult = 0 if len(self.paths) == 0 else max(self.paths.values())
        if type(fSrc[0]) in (tuple, list):
            return [self.nextStep(fTimer, i, fList) for i in fSrc]
        elif type(fSrc[0]) == str:
            fPath = fSrc[1]
            fList = fList.copy()
            if len(fPath) > 0: [fList.remove(i) for i in fPath]
            result = (lambda x,y: [(z, x[1] + tuple([z]), x[2] + self.map[x[0]].distance[z]+1) for z in y])(fSrc, fList)
            result = [i for i in result if i[2] <= fTimer]

            if len(result) == 0: # no further paths to explore
                traveltime, total_released = 0,0
                for i in range(1,len(fPath)):
                    traveltime += self.map[fPath[i-1]].distance[fPath[i]] + 1
                    total_released += (fTimer - traveltime) * self.map[fPath[i]].flowrate
                result = [fPath, total_released]
                self.paths['-'.join(fPath)]= total_released

            return result

    def printMap(self):
        fResult = [(i[1].name, i[1].potential, i[1].opentime, i[1].released, self.position.distance[i[1].name]) for i in sorted(self.map.items(), key=lambda k: k[0])]
        print(f'Timer: {self.Timer.value} Position: {self.position.name}')
        for fLine in fResult:
            oTime = 'None' if fLine[2] is None else fLine[2]
            print(f'{fLine[0]:<5}{fLine[1]:8}{oTime:>8}{fLine[3]:8}{fLine[4]:8}')
class Valve:
    def __init__(self, fParent, fName, fFlowRate, fDestLine) -> None:
        self.parent = fParent
        self.status = 'closed' # or 'open'
        self.flowrate = int(fFlowRate)
        self.name = fName
        self.destLine = fDestLine
        self.dests = []
        self.distance = dict()
        self.potential = -1
        self.opentime = None
        self.released = 0
        self.TimerObserver = TimerObserver(self, fParent.Timer) 
        pass
    def open(self):
        self.parent.Timer.countdown()
        self.opentime = self.parent.Timer.value
        self.status = 'open'
        self.parent.Timer.notify()
        #if debug: self.parent.printMap()

class Timer:
    # https://en.wikipedia.org/wiki/Observer_pattern
    # this is a timer where another class can register itself, so it will be updated when the timer is updated
    def __init__(self, fValue) -> None:
        self.value = fValue
        self.observers = []
        pass
    def register(self, fObj):
        self.observers.append(fObj)
    def update(self, fValue):
        self.value = fValue
        self.notify()
    def countdown(self, fValue=1):
        newVal = self.value-fValue
        if newVal < 0:
            #print('Negative counter is not possible...')
            self.update(max(0,newVal))
        else:
            self.update(newVal)
    def notify(self):
        for ob in self.observers:
            ob.update()
class TimerObserver:
    def __init__(self, fParent, fSubject) -> None:
        self.parent = fParent # parent class to update
        self.subject = fSubject # Timer to observe
        fSubject.register(self)
        self.update()
    def update(self):
        self.value = self.subject.value
        if self.parent.parent.position:
            tDist = self.parent.parent.map[self.parent.parent.position.name].distance[self.parent.name]
            openvalve = 1
            if self.parent.status == 'open': tDist,openvalve = 0,0
            self.parent.potential = max(0,(self.value - tDist - openvalve)) * self.parent.flowrate
            if self.parent.opentime: self.parent.released = (self.parent.opentime - self.value) * self.parent.flowrate
        pass

def main(stdscr):
    myTimer = Timer(30)
    with open(fName, 'r+') as f:
        fContent = f.read().splitlines()
        myMap = MapGrid(fContent, myTimer)
    del f, fContent

    myMap.calc_distances() # calculate the distance between each valve

    myMap.position = myMap.map['AA']
    myMap.Timer.notify()
    if debug: myMap.printMap()

    myMap_initial = copy.deepcopy(myMap)
    result_list = [] # list of tuples each [value, path]
    # sort the valves top-down by potential
    vlist = [myMap.position.name] + [(v.name) for k,v in reversed(sorted(myMap.map.items(), key=lambda x: x[1].potential)) if v.potential>0]
    # create permutations of a; calculate the realised + potential; stop once it is over the best result
    #a_perms = list(permutations(a))
    # a = [['DD'], ['BB'],['JJ'],['HH'],['EE'],['CC']]

    # create a list of possible permutations of travel and open that fit within the length of the counter
    # permutation of valves where sum(traveltime)+numofitems (=traveltime) <= 30
    # result for each permutation: sum (opentime of prev - traveltime from prev - actiontime)*myFlowRate
    # also permutation for less than n elements (add n * [None] and strip those from the path; skip if )

    best_result, last_result, queue = 0, [], []
    #segment_size = 4
    #worklist_segments = (1+(len(vlist) // segment_size )) * [permutations(vlist, segment_size)]
    #worklist_counters = len(worklist_segments) * [0]
    #if len(vlist) % segment_size == 0: worklist_segments.pop()

    queue = [[] for i in vlist]

    # maintain a queue of items to process... while it exists, just take the first item... no need for tracking a counter
    # set up a queue

    # position, traveltime, path
    start = ['AA', ('AA',), 0]
    maxTimer = 30
    queue = myMap.nextStep(maxTimer, start, vlist)
    q1 = [myMap.nextStep(maxTimer, i, vlist) for i in queue]
    q2 = [myMap.nextStep(maxTimer, i, vlist) for i in q1]
    q3 = [myMap.nextStep(maxTimer, i, vlist) for i in q2]
    q4 = [myMap.nextStep(maxTimer, i, vlist) for i in q3]
    q5 = [myMap.nextStep(maxTimer, i, vlist) for i in q4]
    q6 = [myMap.nextStep(maxTimer, i, vlist) for i in q5]
    pass


    #for i in filter(lambda x: x[0:len(last_result)] != last_result, worklist): # not sure if it's faster with or without the filter
    for i in filter(lambda x: x[0:len(last_result)] != last_result, worklist): # not sure if it's faster with or without the filter
        result = myMap.calcPath('AA', i, 30)
        if best_result < result[1]:
            last_result = tuple(result[0].split('-'))[1:]
            best_result = result[1]
            print (f'New best result: {best_result:8}, path: {result[0]}')
        pass




    if False and not args.production:
        #replay of task
        myMap.travel_and_open('DD')
        myMap.travel_and_open('BB')
        myMap.travel_and_open('JJ')
        myMap.travel_and_open('HH')
        myMap.travel_and_open('EE')
        myMap.travel_and_open('CC')

    result = best_result
    # 1317 too low
    # 3000 too high
    # 1587 too low
    # 1641 1603 ?


    message = f'The answer to part 1 is (sample should be 1651, answer should be -it is not 1587!- ): {result}'
    print(message)


    print(20 * '*')
    message = f'The answer to part 2 is (sample should be x, answer should be ): {result}'
    print(message)

# globals
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose"   , action="store_true", default=False, help="Add this to enable verbose output")
parser.add_argument("-d", "--draw"      , action="store_true", default=False, help="Add this to enable drawing")
parser.add_argument("-i", "--drawinterval", type=int, default=1, help="Add the value in ms for drawing interval")
parser.add_argument("-p", "--production", action="store_true", default=False, help="Add this to try the puzzle input")
args = parser.parse_args()

day = '16'
fName = f'2022/input/{day}_sample.txt'
if args.production: fName = f'2022/input/{day}.txt'

debug = args.verbose
draw = args.draw

#stdscr = curses.initscr()
#curses.start_color()
#curses.use_default_colors()
#wrapper(main)

main(None)