import argparse
import curses
from curses import wrapper
import functools
import pandas as pd  # importing pandas module 
from io import StringIO # Importing the StringIO module. 
import re # import regular expressions

def draw_Screen(header, Fco, Fvalue, Fmatrix, Fpath):
    max_y, max_x = stdscr.getmaxyx()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_YELLOW)

    begin_x, begin_y = 5, 5
    height, width = len(Fmatrix)+5, len(Fmatrix[0])+5
    
    if Fco in ('0_0', 'full'):
        ATTR = curses.color_pair(1)
        winHeader.resize(3, max_x - 10)
        winHeader.mvwin(1, 1)

        winMatrix_1.resize(height, width)
        winMatrix_1.mvwin(begin_y, begin_x)
    if Fco in ['0_0', 'full']:
        ATTR = curses.color_pair(1)
        draw_Matrix(winMatrix_1, Fmatrix, begin_x, begin_y, height, width, ATTR)
    if Fvalue == ' ':
        ATTR = curses.color_pair(1)
    else:
        ATTR = curses.color_pair(2) + curses.A_BLINK
    if Fco == 'full':
        for co in Fpath:
            draw_Path(winMatrix_1, costr_to_colist(co)[0], costr_to_colist(co)[1], Fvalue, begin_x, begin_y, height, width, ATTR)
    else: 
        draw_Path(winMatrix_1, costr_to_colist(Fco)[0], costr_to_colist(Fco)[1], Fvalue, begin_x, begin_y, height, width, ATTR)
    winMatrix_1.refresh()

    # winHeader.erase()
    if header[0] is not None:
        winHeader.addstr(0, 0, header[0])
        winHeader.clrtoeol()
    if header[1] is not None: 
        winHeader.addstr(1, 0, header[1])
        winHeader.clrtoeol()
    winHeader.addstr(2, 0, 'Press any key for the next step...')
    winHeader.refresh()
    if debug: stdscr.timeout(1000//1*10)
    else: stdscr.timeout(1000//3)
    keyInput = stdscr.getch()
    if keyInput in [0, 27]: exit()
    
def draw_Path(winMatrix, x, y, Fvalue, begin_x, begin_y, height, width, ATTR):
    # winMatrix = curses.newwin(height, width, begin_y, begin_x)
    # winMatrix = curses.newwin(5, 5, begin_y+y, begin_x+x)
    winMatrix.chgat(y, x, 1, ATTR)
    # winMatrix.refresh()

def draw_Matrix(winMatrix, Fmatrix, begin_x, begin_y, height, width, ATTR):
    winMatrix.erase()
    for y in range(0, len(Fmatrix)):
        conv = lambda i : i or ' ' # convert None to ' '
        for x in range(0,len(Fmatrix[y])):
            winMatrix.addch(y, x, str(conv(Fmatrix[y][x])), ATTR)
    winMatrix.refresh()

class Rucksack:
    def __init__(self, fLine):
        halfP = len(fLine)//2
        self.contents = fLine
        self.comp1 = fLine[:halfP]
        self.comp2 = fLine[halfP:]
        self.intersection = list(set(list(self.comp1)) & set(list(self.comp2)))[0]
        self.intersection_value = charvals[self.intersection]

class TeamOfElves:
    def __init__(self, fData, fI):
        self.badge = list(set(list(fData[fI].contents)) & set(list(fData[fI+1].contents)) & set(list(fData[fI+2].contents)))[0]
        self.badge_value = charvals[self.badge]

def main(stdscr):
    with open(fName, 'r+') as f:
        data = list(map(Rucksack, f.read().splitlines()))
    result = sum([i.intersection_value for i in data])
    status = None
    message = f'The answer to part 1 is (sample should be 157, answer should be 8202): {result}'
    #draw_Screen([status, message], 'full', )
    print(message)
    # process groups of three
    TeamOfElves_all = list(map(TeamOfElves, len(data)//3 * [data], [t for t in range(0, len(data)-1, 3)]))
    result = sum([i.badge_value for i in TeamOfElves_all])

    message = f'The answer to part 2 is (sample should be 70, answer should be 2864): {result}'
    print (message)

def file2df(fTxtFile):
    fileContent = open(fTxtFile).read()
    fDF = pd.DataFrame(columns=['name', 'calories'])

    i = 0
    for line in fileContent.splitlines():
        if line.strip() == '':
            i += 1
            pass
        else: 
            names, items = list(), list()
            for item in line.split ( ' '):
                #print (i, item)
                names.append(i)
                items.append(int(item))
            fDF = pd.concat([fDF, pd.DataFrame.from_dict({'name': names , 'calories': items})], ignore_index=True)
    return fDF

# globals
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose"   , action="store_true", default=False, help="Add this to enable verbose output")
parser.add_argument("-d", "--draw"      , action="store_true", default=False, help="Add this to enable drawing")
parser.add_argument("-i", "--drawinterval", type=int, default=1, help="Add the value in ms for drawing interval")
parser.add_argument("-p", "--production", action="store_true", default=False, help="Add this to try the puzzle input")
args = parser.parse_args()

day = '03'
fName = f'2022/input/{day}_sample.txt'
if args.production: fName = f'2022/input/{day}.txt'

debug = args.verbose
draw = args.draw

stdscr = curses.initscr()
curses.start_color()
curses.use_default_colors()
stdscr.scrollok(True)
winHeader = curses.newwin(1,1,1,1)
winMatrix_1 = curses.newwin(1,1,2,1)

charvals = dict(zip(list(map(chr, range(65, 91))) + list(map(chr, range(97, 123))), list(range(27,53)) + list(range(1, 27)) ))


wrapper(main)

#main(None)