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


class Rope:
    def __init__(self, fX, fY, fNumKnots) -> None:
        self.knots = (fNumKnots) * [None]
        curKnot = None
        for i in range(0,fNumKnots):
            self.knots[i] = Knot(curKnot, fX, fY)
            curKnot = self.knots[i]
            pass
        pass
    def UpdatePos(self, fDir, fUnit):
        self.knots[0].UpdatePos(fDir, fUnit)
        pass

class Knot:
    def __init__(self, fParent, fX, fY) -> None:
        self.x, self.y = fX, fY
        self.history = [(fX, fY)]
        self.parent = fParent
        if fParent: self.parent.child = self
        self.child = None
        pass
    def UpdatePos(self, fDir, fUnit):
        for i in range(0, fUnit):
            if fDir == 'R': self.x += 1
            elif fDir == 'L': self.x -= 1
            elif fDir == 'U': self.y += 1
            elif fDir == 'D': self.y -= 1
            else: 
                print("why do we get here?")
                pass
            self.history.append((self.x, self.y))
            #update all children
            self.child.UpdateKnot()
            pass

    def UpdateKnot(self):
        #update tail pos
        xDist = self.parent.x - self.x
        yDist = self.parent.y - self.y

        if abs(xDist) > 1:
            self.x += xDist // 2
        elif abs(xDist) == 1 and abs(yDist) > 1:
            self.x = self.parent.x

        if abs(yDist) > 1:
            self.y += yDist // 2
        elif abs(yDist) == 1 and abs(xDist) > 1:
            self.y = self.parent.y

        #update history
        self.history.append((self.x, self.y))
        if self.child: self.child.UpdateKnot()
        pass

def main(stdscr):
    rope = Rope(0, 0, 2)
    with open(fName, 'r+') as f:
        for line in f.read().splitlines():
            rope.UpdatePos(line.split()[0], int(line.split()[1]))
    
    # Find all of the directories with a total size of at most 100000. 
    # What is the sum of the total sizes of those directories?
    result = len(set(rope.knots[-1].history))

    message = f'The answer to part 1 is (sample should be 13 / 88, answer should be 5683): {result}'
    print(message)

    print(20 * '*')
    rope = Rope(0, 0, 10)
    with open(fName, 'r+') as f:
        for line in f.read().splitlines():
            rope.UpdatePos(line.split()[0], int(line.split()[1]))
    
    # Find all of the directories with a total size of at most 100000. 
    # What is the sum of the total sizes of those directories?
    result = len(set(rope.knots[-1].history))

    message = f'The answer to part 2 is (sample should be 36, answer should be 2372): {result}'
    print(message)


# globals
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose"   , action="store_true", default=False, help="Add this to enable verbose output")
parser.add_argument("-d", "--draw"      , action="store_true", default=False, help="Add this to enable drawing")
parser.add_argument("-i", "--drawinterval", type=int, default=1, help="Add the value in ms for drawing interval")
parser.add_argument("-p", "--production", action="store_true", default=False, help="Add this to try the puzzle input")
args = parser.parse_args()

day = '09'
fName = f'2022/input/{day}_sampleB.txt'
if args.production: fName = f'2022/input/{day}.txt'

debug = args.verbose
draw = args.draw

stdscr = curses.initscr()
curses.start_color()
curses.use_default_colors()
wrapper(main)

# main(None)