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

class Matrix(fWidth, fHeight):
    def __init__(self) -> None:
        self.matrix = 0
    def initial_setup(self) -> None:
        pass
    def place_piece(self, fPiece, fX, fY, fRotation):
        # check if it fits in the desired position; if not return False

        # place the piece, update the Matrix
        pass

    def remove_piece(self, fPiece):
        # check if the piece is on the board

        # remove the piece update the Matrix
        pass

class Pieces:
    def __init__(self) -> None:
        self.available_pieces = list # of pieces
        pass
    def add_piece(self, fPiece):
        self.available_pieces.add(fPiece)
        pass

class Piece:
    def __init__(self, fLayers, fColourCode, fColourName) -> None:
        self.colourCode = fColourCode
        self.colourName = fColourName
        self.shape = list # list of valid shapes
        self.size = list # list of the size of each possible
        # input is a binary represenation:
        # L1:
        # X
        # XXXX
        # L2:
        # 
        #   XX
        # binary rep:
        # 10001111, 11 valid, because max number of levels = 2



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


def main(stdscr):
    with open(fName, 'r+') as f:
        fContent = f.read().splitlines()
    del f, fContent

    result = 'hoi'

    message = f'The answer to part 2 is (sample should be x, answer should be ): {result}'
    print(message)

# globals
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose"   , action="store_true", default=False, help="Add this to enable verbose output")
parser.add_argument("-d", "--draw"      , action="store_true", default=False, help="Add this to enable drawing")
parser.add_argument("-i", "--drawinterval", type=int, default=1, help="Add the value in ms for drawing interval")
parser.add_argument("-p", "--production", action="store_true", default=False, help="Add this to try the puzzle input")
args = parser.parse_args()

day = 'IQFit'
fName = f'2023/input/{day}_sample.txt'
if args.production: fName = f'2023/input/{day}.txt'

debug = args.verbose
draw = args.draw

stdscr = curses.initscr()
curses.start_color()
curses.use_default_colors()

wrapper(main)