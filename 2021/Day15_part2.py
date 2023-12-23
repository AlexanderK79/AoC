import argparse
import curses
from curses import wrapper

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
    stdscr.timeout(args.drawinterval)
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


def xy_to_costr(Fx, Fy):
    return('_'.join(list(map(str, [Fx, Fy]))))
def costr_to_colist(Fco):
    return(list(map(int, Fco.split('_'))))
def matrix_as_list(Fmatrix):
    matrix_list = []
    matrix_list = [[None] * Fmatrix['width'] for _ in range(Fmatrix['height'])]
    for key in filter(lambda k: k.count('_') == 1, Fmatrix):
        matrix_list[Fmatrix[key]['y']][Fmatrix[key]['x']] = Fmatrix[key]['weight']
    return(matrix_list)


def adjTiles(x, y, Fdict):
    if (x % 2 == 0 and y % 2 == 0) or (x % 2 == 1 and y % 2 == 1): possibleCos = ((x+1, y), (x, y+1), (x-1, y), (x,y-1)) # E, S, W, N
    else: possibleCos = ((x, y+1), (x+1, y), (x-1, y), (x,y-1)) # S, E, W, N

    possibleCos = tuple(filter(lambda co: co[0] >= 0 and co[1] >= 0 and co[0] < Fdict['width'] and co[1] < Fdict['height'], possibleCos )) # remove co's outside of bounds
    possibleTiles = tuple(map(lambda co: (xy_to_costr(co[0], co[1]), Fdict[xy_to_costr(co[0], co[1])]['path_weight']), possibleCos))

    return(possibleTiles)

def getCheapestPath(co, Fdict):
    # this function will return the tile with the cheapest path to follow
    # if two or more tiles have the same value, recurse until there is a difference
    pass


def main(stdscr):
    inputFile = f.read().splitlines()
    f.close()

    # read file into dict with co [x,y] as key
    matrix = {}
    for y in range(0, len(inputFile)):
        for x in range(0, len(inputFile[y])):
            matrix[xy_to_costr(x,y)] = {'weight': int(inputFile[y][x]), 'x': x, 'y': y, 'path_weight': float('inf') }
    matrix['width'], matrix['height'] = len(inputFile[0]), len(inputFile)

    # enlarge the matrix right 5 times and then down 5 times
    # adding 1 to each weight; 9's become 1
    for rep in range(1,5):
        for y in range(matrix['height']):
            for x in range(matrix['width']):
                srcVertex = matrix[xy_to_costr(((rep-1) * matrix['width']) + x, y)]
                srcWeight = srcVertex['weight']
                new_x, new_y = (rep * matrix['width']) +x, y
                dstVertexCo = xy_to_costr(new_x, new_y)
                matrix[dstVertexCo] = {'weight': max(1, (srcWeight+1) % 10), 'x': new_x, 'y': new_y, 'path_weight': float('inf') }
    matrix['width'] *= rep+1
    for rep in range(1,5):
        for y in range(matrix['height']):
            for x in range(matrix['width']):
                srcVertex = matrix[xy_to_costr(x, ((rep-1) * matrix['height']) + y)]
                srcWeight = srcVertex['weight']
                new_x, new_y = x, (rep * matrix['height']) + y
                dstVertexCo = xy_to_costr(new_x, new_y)
                matrix[dstVertexCo] = {'weight': max(1, (srcWeight+1) % 10), 'x': new_x, 'y': new_y, 'path_weight': float('inf') }
    matrix['height'] *= rep+1


    # start top, left
    startCo = '0_0'
    matrix[startCo]['path_weight'] = 0
    destCo = xy_to_costr(matrix['width']-1, matrix['height']-1)

    for co in list(filter(lambda co: co.count('_') > 0, matrix)):
        # get each adjacent tile and calculate weight
        for adjTile, p_w in adjTiles(costr_to_colist(co)[0], costr_to_colist(co)[1], matrix):
            matrix[adjTile]['path_weight'] = min (p_w, matrix[co]['path_weight'] + matrix[adjTile]['weight'])
    # follow the path along the lightest weight
    shortestPath = [destCo]
    while shortestPath[0] != startCo:
        co = shortestPath[0]
        sortedAdj = [k[1] for k in (sorted((value, key) for (key,value) in adjTiles(costr_to_colist(co)[0], costr_to_colist(co)[1], matrix)))]
        shortestPath = [sortedAdj[0]] + shortestPath

    status, message = None, None
    message = f"the answer to part 2 is *** {matrix[destCo]['path_weight']} *** sample should be 315, solution should 2835"
    if draw: draw_Screen([status, message], 'full', '#', matrix_as_list(matrix), shortestPath)


    print(message)   


# globals
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose"   , action="store_true", default=False, help="Add this to enable verbose output")
parser.add_argument("-d", "--draw"      , action="store_true", default=False, help="Add this to enable drawing")
parser.add_argument("-i", "--drawinterval", type=int, default=1, help="Add the value in ms for drawing interval")
parser.add_argument("-p", "--production", action="store_true", default=False, help="Add this to try the puzzle input")
args = parser.parse_args()

day = 15
f = open(f'input/{day}_sampleA.txt', 'r+')
if args.production: f = open(f'input/{day}.txt', 'r+')

debug = args.verbose
draw = args.draw

stdscr = curses.initscr()
curses.start_color()
curses.use_default_colors()
stdscr.scrollok(True)
winHeader = curses.newwin(1,1,1,1)
winMatrix_1 = curses.newwin(1,1,2,1)

wrapper(main)

# main(None)