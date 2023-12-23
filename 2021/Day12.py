import curses
from curses import wrapper

debug = False
debug = True
draw = False
# draw = True

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

def main(stdscr):
    day = 12
    f = open(f'input/{day}_sampleA.txt', 'r+')
    f = open(f'input/{day}_sampleB.txt', 'r+')
    f = open(f'input/{day}_sampleC.txt', 'r+')
    f = open(f'input/{day}.txt', 'r+')
    inputFile = f.read().splitlines()
    f.close()
    
    nodes = {}
    # turn the file into a dict: key = cave, properties: neighboors
    for line in inputFile:
        nodeA, nodeB = line.split('-')
        for nodePair in [[nodeA, nodeB,], [nodeB, nodeA]]:
            nodeA, nodeB = nodePair
            if nodes.get(nodeA) is None:
                nodes[nodeA] = {}
                nodes[nodeA]['neighboors'] = []
            else:
                pass
            if nodes[nodeA]['neighboors'].count(nodeB) == 0:
                nodes[nodeA]['neighboors'].append(nodeB)
            else:
                pass

    # Your goal is to find the number of distinct paths that start at start, end at end, and don't visit small caves more than once. 
    possiblePaths = []
    explorablePaths = []
    # start at start
    curPath = []
    startNode, endNode = 'start', 'end'
    explorablePaths.append([startNode])
    while len(explorablePaths) > 0:
        for curPath in explorablePaths:
            curNode = curPath[-1]
            for node in nodes[curNode]['neighboors']:
                if not node in [startNode, endNode]: # do not add start as a possible dest
                    if node.isupper() or (node.islower() and not node in curPath): # visit a small cave only if it is not already visited
                        explorablePaths.append(list(curPath) + [node])
                if node == endNode: # when end is reached add curPath to possiblePaths
                    possiblePaths.append(list(curPath) + [node])
                # iterate through each possible neighboor
            explorablePaths.remove(curPath)


    print('The answer to part 1 is (sample should be 10)', len(possiblePaths))


# stdscr = curses.initscr()
# curses.start_color()
# curses.use_default_colors()
# wrapper(main)

main(None)