from copy import deepcopy
import curses
from curses import wrapper

stdscr = curses.initscr()
curses.start_color()
curses.use_default_colors()
debug = False
debug = True
draw = False
# draw = True

def update_adj_fields(Fmatrix, x, y):
    ubound_X, ubound_Y = len(Fmatrix[0])-1, len(Fmatrix)-1
    coords2update = []
    for curY in range(max(0,y-1), min(ubound_Y, y+1)+1):
        for curX in range(max(0, x-1), min(ubound_X, x+1)+1):
            if curX == x and curY == y: continue
            coords2update.append([curX, curY])
    for curCo in coords2update:
        curVal = Fmatrix[curCo[1]][curCo[0]]
        if curVal is not None and curVal >= 0: Fmatrix[curCo[1]][curCo[0]] += 1
    return Fmatrix

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
    day = 11
    f = open(f'input/{day}_sample.txt', 'r+')
    f = open(f'input/{day}.txt', 'r+')
    inputFile = f.read().splitlines()
    f.close()

    # turn the file into a list of lists
    matrix, matrix_flash = [],[]
    for line in inputFile:
        matrix.append(list(map(lambda x: int(x), list(line))))

    step, iterFlashes, totalFlashes = 0, 1, 0

    while step < 1000000000:
        step += 1
        prev_matrix = deepcopy(matrix)
        if draw: draw_Screen('Displaying state at start of step: ' + str(step), prev_matrix, matrix, matrix_flash)
        # phase 1: every octo +1
        # First, the energy level of each octopus increases by 1.
        i = 0
        while i < len(matrix):
            matrix[i] = list(map(lambda x: x+1, matrix[i]))
            i += 1
        if draw: draw_Screen('Displaying after just updating every octopus energy in step: ' + str(step), prev_matrix, matrix, matrix_flash)

        # repeat while count this round > 0 or if prevmatrix == matrix
        # Then, any octopus with an energy level greater than 9 flashes. This increases the energy level of all adjacent octopuses by 1, including octopuses that are diagonally adjacent. If this causes an octopus to have an energy level greater than 9, it also flashes. This process continues as long as new octopuses keep having their energy level increased beyond 9. (An octopus can only flash at most once per step.)
        matrix_stable = False
        prev_matrix = deepcopy(matrix)
        j = 0 # iteration counter per step
        matrix_flash_end = list(len(matrix) * [list(len(matrix[0]) * ' ')]) # reset the flash list for this iteration
        while not matrix_stable: # run each iteration until there are no new flashes
        # while iterFlashes > 0:
            iterFlashes = 0 # set to 0, to detect if something happens this iteration
            # set up some defaults
            matrix_flash = list(len(matrix) * [list(len(matrix[0]) * ' ')]) # reset the flash list for this iteration
            j += 1
            i = 0
            # phase 2a: every octo > 9: fire  and set to -1; draw, count fired, 
            while i < len(matrix):  # count the new flashes ( >9) and set them to -1 to indicate it has just flashed
                matrix_flash[i]     = list(map(lambda x:  'X' if x is not None and x > 9 else ' ', matrix[i]))
                # count the total number of flashes in this iteration
                iterFlashes += matrix_flash[i].count('X')
                # set the energy level to -1 as a sign it has just flashed
                matrix[i] = list(map(lambda x: -1 if x is not None and x > 9 else x, matrix[i]))
                i += 1
            totalFlashes += iterFlashes

            # phase 2b: give a +1 to every positive-integer neighboor of an octo that just fired = -1
            y = 0 
            while y < len(matrix): # update the adjacent fields for every octopus that just flashed (-1 )
                for x in [m for m, x in enumerate(matrix[y]) if x is not None and (x == -1 )]:
                    matrix = update_adj_fields(matrix, x, y)
                y += 1

            # phase 2c: set the -1's to None
            y = 0
            while y < len(matrix): 
                # change the -1's in the matrix to None to prevent a second flash
                matrix[y] = list(map(lambda x: None if x is not None and x == -1 else x, matrix[y]))
                y += 1

            if draw: draw_Screen('Displaying in step: ' + str(step) + ' - iteration ' + str(j) + ' total flashes:' + str(totalFlashes), prev_matrix, matrix, matrix_flash)
            if matrix == prev_matrix: matrix_stable = True
            else: prev_matrix = deepcopy(matrix)

        # phase 3: set every octo that flashed (None) in the prev round to 0
        y = 0
        roundFlashes = 0
        while y < len(matrix):
            # Finally, any octopus that flashed during this step has its energy level set to 0, as it used all of its energy to flash.
            matrix[y] = list(map(lambda x: 0 if x is None else x, matrix[y]))
            roundFlashes += matrix[y].count(0)
            y += 1
        # count the 0's to see how many flashed




        if draw: draw_Screen('Displaying after step: ' + str(step) + ' round flashes:' + str(roundFlashes) + ' total flashes:' + str(totalFlashes), prev_matrix, matrix, matrix_flash)
        if roundFlashes == 100: exit('Sync flash in step ' + str(step))
        
    #After 100 steps, there have been a total of 1656 flashes.
    print('The answer to part 1 is (sample should be 1656)', totalFlashes)
    # Given the starting energy levels of the dumbo octopuses in your cavern, simulate 100 steps. How many total flashes are there after 100 steps?


wrapper(main)