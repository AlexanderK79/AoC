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
    # initialize dict
    # key level_index
    #            0_0
    #    1_0           1_1
    # 2_0   2_1     2_2   2_3
    # even indexes are left, odd indexes are right
    # attributes: data (number or list of values)
    #             parentcount (==level)
    #             parent (reference to dict[key_index])
    #             type (node | leaf)
    treeDict = {}
    level, index = 0, 0
    treeDict = addNode(treeDict, level, index, inputList, None)
    return(treeDict)

def addNode(FtreeDict, Flevel, Findex, Fdata, Fparent):
    if isinstance(Fdata, int):
        FtreeDict[str(Flevel) + '_' + str(Findex)] = {'data': Fdata, 'parentcount': Flevel, 'index': Findex, 'parent': Fparent, 'type': 'leaf'}
    else:
        myIndex = Findex
        Findex = 2 * Findex
        FtreeDict[str(Flevel) + '_' + str(myIndex)] = {'data': Fdata, 'parentcount': Flevel, 'index': myIndex, 'parent': Fparent, 'type': 'node'}
        for item in Fdata:
            FtreeDict = addNode(FtreeDict, Flevel+1, Findex, item, f'{str(Flevel)}_{str(myIndex)}')
            Findex += 1

    return(FtreeDict)

def explodeNode(FtreeDict, node):
    #this function returns the new version of the tree dictionary where the specified node has been exploded
        # explode the left-most pair; return the new tree
        # To explode a pair, the pair's left value is added to the first regular number to the left of the exploding pair (if any),
        #  and the pair's right value is added to the first regular number to the right of the exploding pair (if any). 
        # Exploding pairs will always consist of two regular numbers. 
        # Then, the entire exploding pair is replaced with the regular number 0.
        
        # traverse tree; until a pair is found with parentPairCount >= 4
    pass


    return(FtreeDict)

def nextValue(FtreeDict, Fnode, hor_direction, vert_direction):
    # this function will return the location of the pair containing the first nextValue to the {direction} of the Fnode

    # unless we start at the root, move upward until there is a path in the desired direction
    # then keep moving in the opposite of the desired direction until we find a value
    
    nextValuePair = FtreeDict[Fnode]['parent'] # now moving upward

    # now try to move sideways
    if nextValuePair is None and vert_direction == 'down': # we are at the root of the tree and starting down
        # if we start here, let's pretend we already made the upward move and set the nextValuePair to the Fnode
        nextValuePair = Fnode
        pass
    elif nextValuePair is not None or (nextValuePair is None and vert_direction == 'up'): 
        # we are at the root of the tree and went up:  or we are not at the root of the tree
        # now find a way in the desired direction
        foundPath = False
        while not foundPath:
            nextValuePair = Fnode if nextValuePair is None else nextValuePair # we reached the top of the dict
            myIndex = FtreeDict[nextValuePair]['index']
            if hor_direction == 'left':
                nextValuePair = str(FtreeDict[nextValuePair]['parentcount']) + '_' + str(myIndex) # we are looking for the even side of the pair
            elif hor_direction == 'right':
                nextValuePair = str(FtreeDict[nextValuePair]['parentcount']) + '_' + str(myIndex+1) # we are looking for the odd side of the pair
            else:
                exit('we should have found a valid type nextValuePair by now')
            if FtreeDict.get(nextValuePair):
                if nextValuePair == Fnode:
                    # we arrived at the top, but a move in the desired direction, results in an endless loop; return None
                    nextValuePair = None
                foundPath = True
            else:
                # move up one pair and try again; if we are not at the top...
                if FtreeDict[Fnode]['parent'] is None:
                    # there is no pair found in the desired direction
                    nextValuePair = '0_0'
                    foundPath = True
                else:
                    nextValuePair = nextValue(FtreeDict, FtreeDict[Fnode]['parent'], hor_direction, 'up')
    else:
        exit('we should not get here')

    if  FtreeDict[nextValuePair]['parent'] is None and nextValuePair == Fnode and vert_direction == 'up':
        # we arrived at the top, but a move in the desired direction, results in an endless loop; return None
        nextValuePair = None
    elif  FtreeDict[nextValuePair]['parent'] is None and nextValuePair == Fnode and vert_direction == 'down' and hor_direction == 'left':
        # we start at the top, but there is no left side; return None
        nextValuePair = None
    elif FtreeDict[nextValuePair]['parent'] is not None and nextValuePair == Fnode:
        # this is the same as where we came from and we are not at the root, try one up again from this node
        nextValuePair = nextValue(FtreeDict, nextValuePair, hor_direction, 'up')
    else:
        # we have moved one step in the correct (not necessarily right) direction
        # now keep going in the opposite direction until we find a value
        foundValue = None
        while foundValue is None:
            if FtreeDict[nextValuePair]['type'] == 'leaf':
                foundValue = FtreeDict[nextValuePair]['data']
                nextValuePair = FtreeDict[nextValuePair]['parent']
            else: # recurse down in the direction
                myIndex = 2 * FtreeDict[nextValuePair]['index']
                if hor_direction == 'left':
                    nextValuePair = str(FtreeDict[nextValuePair]['parentcount']+1) + '_' + str(myIndex+1) # we are now looking for the 1 side of the pair
                elif hor_direction == 'right':
                    nextValuePair = str(FtreeDict[nextValuePair]['parentcount']+1) + '_' + str(myIndex) # we are now looking for the 0 side of the pair
                
    return(nextValuePair)



def traverseTree(self, mode):
    newValue = None
    if mode[0] == 'nextValue':
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
    for line in inputFile[4:5]:
        print(line)
        SFnumber, SFnumberResult = line.split(' becomes ')
        SFnumber = createStruct(SFnumber)
        
        # SFnumber.PrintTree()
        
        # first explode
        SFnumber_in = None
        while SFnumber_in != SFnumber: # keep splitting
            SFnumber_in = None
            while SFnumber_in != SFnumber: # keep exploding (and try exploding again after a split occurs)
                SFnumber_in = SFnumber
                node = nextValue(SFnumber, '0_0', 'right', 'down')
                print('no node found to the right') if node is None else print('right: ', node, ':', SFnumber[node]['data'], SFnumber[node])
                node = nextValue(SFnumber, '0_0', 'left', 'down')
                print('no node found to the left') if node is None else print('left:  ', node, ':', SFnumber[node]['data'], SFnumber[node])
                nextValue(SFnumber, '4_15', 'right', 'down')

                # SFnumber = SFnumber.explode()



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