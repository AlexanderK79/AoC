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
    vlist = [(v.name) for k,v in reversed(sorted(myMap.map.items(), key=lambda x: x[1].potential)) if v.potential>0]
    # create permutations of a; calculate the realised + potential; stop once it is over the best result
    #a_perms = list(permutations(a))
    # a = [['DD'], ['BB'],['JJ'],['HH'],['EE'],['CC']]
    best_result = 0
    #for a in a_perms:
    failedPath = None
    # create a permutation set of max 5 items
    perm_length = 5
    queue = []
    for i in range(0, len(vlist), perm_length):
        queue += [list(permutations(vlist[i:i+perm_length]))]
    pass
    # numOfqparts = 3
    queue.append(((3 - len(queue)) * [tuple()]))

    a, deadendsq1, deadends= [], [], []
    for q0 in queue[0]:
        if q0 in deadendsq1:
            deadendsq1.remove(q0)
            continue
        for q1 in queue[1]:
            exitloop1, nextloop1 = False, False
            for q2 in queue[2]:
                exitloop2, nextloop2 = False, False
                a = q0 + q1 + q2
                myMap = copy.deepcopy(myMap_initial) # reset the map and timer
                for x in a:
                    if myMap.Timer.value == 0:
                        exitloop1, exitloop2 = True, True
                        break # break out of for x in a
                    if a[0:a.index(x)+1] in deadends:
                        if perm_length <= a.index(x) < 2 * perm_length:
                            exitloop2 = True
                            nextloop1 = True
                        if 2 * perm_length <= a.index(x):
                            nextloop1 = True
                            nextloop2 = True
                        break # break out of for x in a
                    failedPath = None
                    if myMap.travel_check(x):
                        myMap.travel_and_open(x)
                        thisResult = sum([(i.released) for i in myMap.map.values()])
                        potential_result = sum([(i.potential) for i in myMap.map.values() if i.potential > 0])
                        pass
                    else:
                        # we cannot travel here...store it as failed path and store the result of the last successfull attempt
                        failedPath = a[0:a.index(x)+1]
                        a = a[:a.index(x)]
                        x = a[-1]
                        potential_result = 0
                        myMap.Timer.countdown(myMap.Timer.value) # let the timer run out to 0
                        thisResult = sum([(i.released) for i in myMap.map.values()])
                        pass

                    if failedPath or ((thisResult + potential_result) < best_result):
                        if (thisResult + potential_result) < best_result:
                            thisResult = -1000000 - thisResult - potential_result
                        if not failedPath: failedPath = a[0:a.index(x)+1]
                        # remove the dead ends from q1
                        if len(failedPath) <= perm_length:
                            for deadend in list(filter(lambda p: p[0:len(failedPath)] == failedPath, queue[0])):
                                deadendsq1.append(deadend)
                                pass
                            exitloop1, exitloop2 = True, True
                        if perm_length < len(failedPath) <= 2* perm_length:
                            deadends.append(failedPath)
                            nextloop1 = True
                            exitloop2 = True
                        if 2* perm_length < len(failedPath):
                            nextloop1 = True
                            nextloop2 = True
                        break # break out for x in a
                if thisResult > -1000000:
                    myMap.Timer.countdown(myMap.Timer.value) # let the timer run out to 0 if we have a valid result
                    thisResult = sum([(i.released) for i in myMap.map.values()])
                    pass
                result_list += [(thisResult, ('-').join(a))]
                result_list = list(reversed(sorted(result_list, key=lambda x: x[0])))[:100]
                if best_result < max([r[0] for r in result_list]):
                    best_result = max([r[0] for r in result_list])
                    print(list(filter(lambda k: k[0] == best_result, result_list)))
                del thisResult, potential_result
                if exitloop2: break
                if nextloop2: continue
            if exitloop1: break
            if nextloop1: continue
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