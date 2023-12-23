import argparse
import curses
from curses import wrapper
import functools

def draw_Screen(header, Fmatrix_1, Fmatrix_2, Fmatrix_3):
    max_y, max_x = stdscr.getmaxyx()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_YELLOW)
    begin_x, begin_y = 5, 1
    height, width = 3, 60
    winHeader = curses.newwin(height, width, begin_y, begin_x)

    begin_x, begin_y = 5, 5
    height, width = 25, 35
    ATTR = curses.color_pair(1)
    if debug: draw_Matrix(Fmatrix_1, begin_x, begin_y, height, width, ATTR)
    begin_x = 45
    if debug: draw_Matrix(Fmatrix_2, begin_x, begin_y, height, width, ATTR)
    begin_x = 85
    ATTR = curses.color_pair(2) + curses.A_BLINK
    draw_Matrix(Fmatrix_3, begin_x, begin_y, height, width, ATTR)

    winHeader.erase()
    winHeader.addstr(0, 0, header)
    winHeader.addstr(1, 0, 'Press any key for the next step...')
    winHeader.refresh()
    if not debug: stdscr.timeout(1000//500)
    keyInput = stdscr.getch()
    if keyInput in [0, 27]: exit()
    

def draw_Matrix(Fmatrix, begin_x, begin_y, height, width, ATTR):
    winMatrix = curses.newwin(height, width, begin_y, begin_x)
    winMatrix.erase()
    for y in range(0, len(Fmatrix)):
        conv = lambda i : i or '' # convert None to ''
        for x in range(0,len(Fmatrix[y])):
            winMatrix.addstr(2*y, 3*x, str(conv(Fmatrix[y][x])).strip(), ATTR)
    winMatrix.refresh()

def createStruct(Fline):
    # returns a binary tree
    inputList = eval(Fline)
    # initialize tree
    binTree = Node(inputList, None)

    return(binTree)

class Node:
    def __init__(self, data, parent):
        self.parent          = parent
        self.data            = data
        self.left            = None
        self.right           = None
        self.side            = None
        self.parentPairCount = 0 if parent is None else parent.parentPairCount + 1
        self.magnitude       = None
        self.unpack(data)

# Insert Node
    def unpack(self, data):
        if self.data:
            #store or recurse left side
            if isinstance(data[0], int):
                self.left = data[0]
            else:
                self.left = Node(data[0], self)
                self.left.side = 'left'

            #store or recurse right side
            if isinstance(data[1], int):
                self.right = data[1]
            else:
                self.right = Node(data[1], self)
                self.right.side = 'right'
        else:
            exit("why do we get here")

    def get(self, property):
        # returns the value of the property
        return(getattr(self, property))

    def traverseTree(self, mode):
        newValue = None
        if mode[0] == 'nextValue':
            # traverse through the tree, returning a reference to the first nodepair in the specified direction that has not yet been visited
            # left and right are seen from the node you're working on
            # keep going down until we find a value; go up until we change direction, then keep going down in the opposite direction until we find a value; return that pair
            # if we are at the top node: skip the first to steps
            # mode is tuple (mode, direction (left|right))
            direction = mode[1]

        return(foundPair)



    def explode(self):
        # explode the left-most pair; return the new tree
        # To explode a pair, the pair's left value is added to the first regular number to the left of the exploding pair (if any),
        #  and the pair's right value is added to the first regular number to the right of the exploding pair (if any). 
        # Exploding pairs will always consist of two regular numbers. 
        # Then, the entire exploding pair is replaced with the regular number 0.
        
        # traverse tree; until a pair is found with parentPairCount >= 4

        return(self)


# Print the Tree
    def PrintTree(self):
        leftStr  = str(self.left.data)  if isinstance(self.left, Node)  else str(self.left)
        rightStr = str(self.right.data) if isinstance(self.right, Node) else str(self.right)
        if self.side == None:
            print( str(self.data).center(80) )
            print( f"{' '.join((leftStr, rightStr)).center(80)}" )
        elif self.side == 'left':
            width = 40//self.parentPairCount
            print( f'{str(self.data).center(width):<}' )
            print( f"{' '.join((leftStr, rightStr)).center(40//self.parentPairCount):<40//self.parentPairCount}" )
        elif self.side == 'right':
            print( f'{str(self.data).center(40//self.parentPairCount):>40//self.parentPairCount}' )
            print( f"{'   '.join((leftStr, rightStr)).center(40//self.parentPairCount):>80}" )

        if isinstance(self.left, Node):
            self.left.PrintTree()
        if isinstance(self.right, Node):
            self.right.PrintTree()
# Inorder traversal
# Left -> Root -> Right
    def inorderTraversal(self, root):
        res = []
        if root:
            res = self.inorderTraversal(root.left)
            res.append(root.data)
            res = res + self.inorderTraversal(root.right)
        return res



def main(stdscr):
    inputFile = f.read().splitlines()
    f.close()

    # for line in inputFile[-1:]:
    for line in inputFile:
        print(line)
        SFnumber, SFnumberResult = line.split(' becomes ')
        SFnumber = createStruct(SFnumber)
        
        SFnumber.PrintTree()
        
        # first explode
        SFnumber_in = None
        while SFnumber_in != SFnumber: # keep splitting
            SFnumber_in = None
            while SFnumber_in != SFnumber: # keep exploding (and try exploding again after a split occurs)
                SFnumber_in = SFnumber
                SFnumber = SFnumber.explode()



        SFnumberResult = SFnumberResult.replace(',', ', ')
        # explodeSFnumber(SFnumber)
        # print('\n'.join((str(SFnumber.data), SFnumberResult)))

        



    print('The answer to part 1 is (sample should be XXX)', SFnumberResult)


# globals
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose"   , action="store_true", default=False, help="Add this to enable verbose output")
parser.add_argument("-d", "--draw"      , action="store_true", default=False, help="Add this to enable drawing")
parser.add_argument("-i", "--drawinterval", type=int, default=1, help="Add the value in ms for drawing interval")
parser.add_argument("-p", "--production", action="store_true", default=False, help="Add this to try the puzzle input")
args = parser.parse_args()

day = 18
f = open(f'input/{day}_sampleA.txt', 'r+')
if args.production: f = open(f'input/{day}.txt', 'r+')

debug = args.verbose
draw = args.draw

# stdscr = curses.initscr()
# curses.start_color()
# curses.use_default_colors()
# stdscr.scrollok(True)
# winHeader = curses.newwin(1,1,1,1)
# winMatrix_1 = curses.newwin(1,1,2,1)

# wrapper(main)

main(None)