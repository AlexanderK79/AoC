import curses
from curses import wrapper

debug = False
debug = True
draw = False
draw = True

def draw_Screen(header, Fmatrix_1, Fmatrix_2, Fmatrix_3):
    max_y, max_x = stdscr.getmaxyx()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_YELLOW)
    begin_x, begin_y = 5, 1
    height, width = 3, max_x - begin_x
    stdscr.erase()
    stdscr.refresh()
    winHeader = curses.newwin(height, width, begin_y, begin_x)

    begin_x, begin_y = 5, 5
    padding = 5
    matrix_height, matrix_width = len(Fmatrix_1), max(list(map(lambda x: len(x), Fmatrix_1)))
    height, width = matrix_height + 2, matrix_width+2
    ATTR = curses.color_pair(1)
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
    day = 13
    f = open(f'input/{day}_sampleA.txt', 'r+')
    f = open(f'input/{day}.txt', 'r+')
    inputFile = f.read().splitlines()
    f.close()

    matrix = []
    # create matrix that holds the representation
    for co in list(filter(lambda x: x.count(',') > 0, inputFile)):
        x,y = list(map(lambda x: int(x), co.split(',')))

        if len(matrix) <= y:
            matrix += [[] for n in range((y - len(matrix))+1)]
        if len(matrix[y]) <= x:
            matrix[y] += ['.' for n in range(x - len(matrix[y])+1)]
        matrix[y][x] = '#'
    matrix_height, matrix_width = len(matrix), max(list(map(lambda x: len(x), matrix)))
    for item in matrix:
        item += ['.' for n in range((matrix_width - len(item))+1 )]

    # draw it
    if draw: draw_Screen("Initial layout", matrix, [], [])

    # fold it along instructions
    foldCount = 0
    for instr in list(filter(lambda x: x.count('fold along ') > 0, inputFile)):
        direction, foldline = instr.replace('fold along ','').split('=')
        foldline = int(foldline)
        if direction == 'y':
            # folding up; move each # on a line larger then the fold line to a line as far away from the fold
            for y in range(foldline, len(matrix)):
                for x in range(0, len(matrix[y])):
                    if matrix[y][x] == '#':
                        if foldline+(foldline-y) < 0: exit('this is weird') 
                        matrix[foldline+(foldline-y)][x] = '#'
                # clear line
                matrix[y] = []
            # keep only non-empty lines
            matrix = [elem for elem in matrix if elem != []]
        elif direction == 'x':
            # folding left; move each # on a x larger then the fold line
            for y in range(0, len(matrix)):
                for x in range(foldline, len(matrix[y])):
                    if matrix[y][x] == '#':
                        if foldline+(foldline-x) < 0: exit('this is weird') 
                        matrix[y][foldline+(foldline-x)] = '#'
                # clear rest of the line
                matrix[y][foldline:] = []
            # keep only non-empty lines
            matrix = [elem for elem in matrix if elem != []]
        foldCount += 1
        totalDots = sum([elem.count('#') for elem in matrix])
        if draw: draw_Screen(f'After fold {foldCount} using {direction} {str(foldline)}: {totalDots} dots', matrix, [], [])
        # if foldCount == 1: break




        
   
    print('The answer to part 1 is (sample should be 17)', totalDots)


stdscr = curses.initscr()
curses.start_color()
curses.use_default_colors()
wrapper(main)

# main(None)