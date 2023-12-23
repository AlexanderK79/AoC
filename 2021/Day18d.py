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

    bintree = Node(inputList, None)
    bintree.expandNode(bintree.data)
    return(bintree)

class Node:
    def __init__(self, data, parent):
        self.parent          = parent
        self.data            = data
        self.left            = None
        self.right           = None
        self.side            = None
        self.level           = 0 if parent is None else parent.level + 1
        self.horIndex        = None
        self.magnitude       = None
        
    def get(self, property):
        # returns the value of the property
        return(getattr(self, property))

    def expandNode(self, data):
        self.horIndex = 0 if self.parent is None else self.horIndex
        if self.data:
            #store or recurse left side
            if isinstance(data[0], int):
                self.left = data[0]
            else:
                self.left = Node(data[0], self)
                self.left.side = 'left'
                self.left.horIndex = ( 2 * self.horIndex if isinstance(self.horIndex, int) else 0 ) + 0
                self.left.expandNode(self.left.data)

            #store or recurse right side
            if isinstance(data[1], int):
                self.right = data[1]
            else:
                self.right = Node(data[1], self)
                self.right.side = 'right'
                self.right.horIndex = ( 2 * self.horIndex if isinstance(self.horIndex, int) else 0 ) + 1
                self.right.expandNode(self.right.data)
            
            # expand added node

        else:
            exit("why do we get here")

    def PrintTree(self, width):
        charLeft, charRight = ' \u2571', '\u2572  '
        sepLine = width//2 * '* '
        print(sepLine)
        print(f'{"ROOT":^{width}}')
        print(f'{str(self.data):^{width}}')
        for line in self.buildPrintTree(None, width)[1:]:
            width //= 2
            lineHeader = map(lambda x: f"{charLeft if x[1] != ' ' else ' ':^{width}}" if x[0] %2 == 0 else f"{charRight if x[1] != ' ' else ' ':^{width}}" , enumerate(line))
            lineResult = map(lambda x: f'{x[1]:^{width}}' if x[0] %2 == 0 else f'{x[1]:^{width}}' , enumerate(line))
            print(''.join(lineHeader))
            print(''.join(lineResult))
        print(sepLine)

    def buildPrintTree(self, result, width):
        result = [] if result is None else result
        while len(result) <= self.level+1:
            result.append((2**(self.level+1)) * [' '])
        
        # add the left side to the result
        if isinstance(self.left, int):
            horIndex = (2 * self.horIndex) + 0
            result[self.level+1][horIndex] = str(self.left)
        else:
            result[self.left.level][self.left.horIndex] = str(self.left.data)

        # add the right-hand side to the result
        if isinstance(self.right, int):
            horIndex = (2 * self.horIndex) + 1
            result[self.level+1][horIndex] = str(self.right)
        else:
            result[self.right.level][self.right.horIndex] = str(self.right.data)

        # keep recursing
        if isinstance(self.left, Node):
            self.left.buildPrintTree(result, width)
        if isinstance(self.right, Node):
            self.right.buildPrintTree(result, width)


        return(result)

    def explodeNode(self):
        #this function returns the new version of the tree dictionary where the specified node has been exploded
        # explode the left-most pair; return the new tree
        # To explode a pair, the pair's left value is added to the first regular number to the left of the exploding pair (if any),
        #  and the pair's right value is added to the first regular number to the right of the exploding pair (if any). 
        # Exploding pairs will always consist of two regular numbers. 
        # Then, the entire exploding pair is replaced with the regular number 0.
        
        # move left part to
        if self.nextValuePair('left', None) is not None:
            if self.nextValuePair('left', None) == self.parent:
                self.nextValuePair('left', None).left += self.left
                self.nextValuePair('left', None).data[0] += self.left
            else:
                self.nextValuePair('left', None).right += self.left
                self.nextValuePair('left', None).data[1] += self.left
        # move right part to
        if self.nextValuePair('right', None) is not None:
            if self.nextValuePair('right', None) == self.parent:
                self.nextValuePair('right', None).right += self.right
                self.nextValuePair('right', None).data[1] += self.right
            else:
                self.nextValuePair('right', None).left += self.right
                self.nextValuePair('right', None).data[0] += self.right
        # change this pair to a 0
        if self.side == 'left':
            self.parent.data[0] = 0
            self.parent.left = 0
        else:
            self.parent.data[1] = 0
            self.parent.right = 0

        return(self)

    def firstValuePair(self):
        # to find the firstValuePair; imagine you're outside the node; the first pair is then at your right hand (but in the tree it's most left)
        return(self.nextValuePair('right', 'first'))

    def nextValuePair(self, hor_direction, vert_direction):
        # vert_direction == None for the initial function call ; vert_direction is only used once recursing
        # this function will return the location of the pair containing the first nextValuePair to the {direction} of the Fnode

        # unless we start at the root, move upward until there is a path in the desired direction
        # then keep moving in the opposite of the desired direction until we find a value
        opp_hor_direction = 'left' if hor_direction == 'right' else 'right'

        if self.side is None and self.parent is None and vert_direction is None: 
            # we start at the top node
            # at the top node, without a vert_direction... there is no left or right node
            nextValuePair = None
        elif self.side is None and self.parent is None and vert_direction == 'first':
            # special case, where we look for the first node
            # start searching in the left direction immediately
            if isinstance(self.get('left'), int): # left side of the first node is an int, firstNode = root
                nextValuePair = self
            else:
                # recurse down in the left direction from the pair in the opposite direction, until we find a value
                nextValuePair = self.left.nextValuePair('left', 'down')
        elif self.side is None and self.parent is None and vert_direction == 'up': # we reached the top node, coming from the direction we're looking for; return None
            nextValuePair = None
        elif self.side == hor_direction:
            # the pair itself is at the side we're looking for; 
            if vert_direction in (None, 'up'):
                # recurse in the vertical direction where we came from 
                nextValuePair = self.parent.nextValuePair(hor_direction, 'up')
            elif vert_direction == 'down':
                if isinstance(self.get(hor_direction), int):
                    # return this pair as result
                    nextValuePair = self
                else:
                    # recurse further down in the desired direction
                    nextValuePair = self.get(hor_direction).nextValuePair(hor_direction, vert_direction)
        elif self.side == opp_hor_direction:
            if vert_direction is None:
                # the pair itself is at the opposite side we're looking for; change over to the other side of the node
                nextValuePair = self.parent.get(hor_direction)
            else:
                # we are moving down or up and the pair itself is at the opposite side we're looking for (which is not really relevant)
                nextValuePair = self
            # now we found a valid nextValuePair; recurse down until there is a value on the opposite side of the hor_direction
            if isinstance(nextValuePair, int):
                nextValuePair = self.parent
            else:
                # recurse down in the opposite direction
                nextValuePair = nextValuePair.nextValuePair(opp_hor_direction, 'down')

        return(nextValuePair)

    def testSearch(self):
        FirstNode = self.firstValuePair()
        print('FirstNode:    ', FirstNode.left  if isinstance(FirstNode.left, int)  else FirstNode.left.data
        ,'   '     , FirstNode.right if isinstance(FirstNode.right, int) else FirstNode.right.data
        ,'FirstNode is ROOT' if FirstNode == self else '')

        for d in ('left', 'right'):
            d_node = FirstNode.nextValuePair(d, None)
            if d_node is None:
                print('search', f'{d:>5}', d_node)
            else:
                # if the nextValuePair and the FirstNode are the same, 
                # we find the nextValue on the search direction
                # if it's a different node, it is on the opposite side of the search direction
                if d == 'left':
                    d_value = d_node.get(d)
                else:
                    d_value = d_node.get('right')
                    
                print ('search', f'{d:>5}', d_value if isinstance(d_value, int) else d_node.data)


    def traverseTree(self, mode):
        newValue = None
        if mode[0] == 'nextValuePair':
            # traverse through the tree, returning a reference to the first nodepair in the specified direction that has not yet been visited
            # left and right are seen from the node you're working on
            # keep going down until we find a value; go up until we change direction, then keep going down in the opposite direction until we find a value; return that pair
            # if we are at the top node: skip the first to steps
            # mode is tuple (mode, direction (left|right))
            direction = mode[1]

        return(self)


def main(stdscr):
    inputFile = f.read().splitlines()
    f.close()

    # for line in inputFile[-1:]:
    for line in inputFile[3:4]:
    # for line in inputFile[0:6]:
        print('\n', line)
        SFnumber, SFnumberResult = line.split(' becomes ')
        SFnumber = createStruct(SFnumber)
        
        SFnumber.PrintTree(130)

        # first explode
        SFnumber_in = None
        while SFnumber_in != SFnumber: # keep splitting
            SFnumber_in = None
            while SFnumber_in != SFnumber: # keep exploding (and try exploding again after a split occurs)
                SFnumber_in = SFnumber

                if debug: SFnumber.testSearch()
                CurrentNode = SFnumber.firstValuePair()
                # loop through, starting at FirstNode, checking if it needs to explode
                while CurrentNode is not None:
                    if CurrentNode == SFnumber:
                        # we are ROOT, so recurse down the right side
                        CurrentNode = CurrentNode.right.firstValuePair()
                    elif CurrentNode.level >= 4:
                        CurrentNode.explodeNode()
                        CurrentNode = CurrentNode.firstValuePair()
                    else:
                        CurrentNode = CurrentNode.firstValuePair()
                SFnumber.PrintTree(130)

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
f = open(f'2021/input/{day}_sampleA.txt', 'r+')
if args.production: f = open(f'2021/input/{day}.txt', 'r+')

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