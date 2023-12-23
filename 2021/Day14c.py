import curses
from curses import wrapper
from typing import Pattern
import copy

debug = False
debug = True
draw = False
# draw = True

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

def splitBlocks_2(FinputPolymer):
    elem_Blocks = []
    # determine length
    for i in range(0, len(FinputPolymer)-1, 1):
        elem_Blocks.append(FinputPolymer[i:i+2])
    return (elem_Blocks)

def splitBlocks_3(FinputPolymer, Fblocksize):
    elem_Blocks = []
    # determine length
    if len(FinputPolymer) % Fblocksize == 0:
        startChar, s, e = 0, '',''
    else:
        startChar, s, e, = 1, FinputPolymer[0], FinputPolymer[-1]

    for i in range(startChar, len(FinputPolymer)-2, Fblocksize):
        elem_Blocks.append(FinputPolymer[i:i+Fblocksize])
    elem_Blocks = [s] + elem_Blocks + [e]
    
    return (elem_Blocks)


def insertElement(FinputPair, Fdict):
    return(Fdict[FinputPair]['output'])

def updatePolymer(FinputPolymer, Fdict):
    polymer_new = ''
    for i in range(0, len(FinputPolymer)-1):
        curPair = FinputPolymer[i:i+2]
        polymer_new += insertElement(curPair, Fdict)[:-1]
    polymer_new += FinputPolymer[-1]
    return(polymer_new)



def main(stdscr):
    day = 14
    f = open(f'input/{day}_sampleA.txt', 'r+')
    f = open(f'input/{day}.txt', 'r+')
    inputFile = f.read().splitlines()
    f.close()

    rec = {}
    # create dict that holds the recipe
    polymer = inputFile[0]
    for recipe in list(filter(lambda x: x.count(' -> ') > 0, inputFile)):
        input, insert = recipe.split(' -> ')
        rec[input] = {'output': input[0] + insert + input[1], 'output_pairs': (input[0] + insert, insert + input[1])}

    # run 10 steps of pair insertion
    step = 0
    # polymer ='CH'
    print(polymer)
    polymer_counter = {}
    for pair in list(rec.keys()):
        polymer_counter[pair] = 0
    for pair in splitBlocks_2(polymer):
        polymer_counter[pair] += 1
    while step < 40:
        step += 1
        polymer_counter_orig = copy.deepcopy(polymer_counter)
        for pair in list(polymer_counter_orig):
            if polymer_counter_orig[pair] == 0: continue
            for out_pair in rec[pair]['output_pairs']:
                polymer_counter[out_pair] += polymer_counter_orig[pair] 
            polymer_counter[pair] -= polymer_counter_orig[pair] # reduce with the pairs it originated from

        # polymer = updatePolymer(polymer, rec)
        # print(f'Step {step} - polymer: {" ".join(splitBlocks_3(polymer, 3))[:130].center(132)}') #, element_count[max_elem]-element_count[min_elem])

        # count elements
        element_count = {}
        # add the start and end element of the original polymer
        for element in (polymer[0], polymer[-1]):
            if element_count.get(element) is None: element_count[element] = 0
            element_count[element] += 1
        
        for pair in polymer_counter:
            for element in pair:
                if polymer_counter[pair] == 0: continue
                if element_count.get(element) is None: element_count[element] = 0
                element_count[element] += polymer_counter[pair]
        for element in element_count.keys():
            element_count[element] = element_count[element] // 2
        max_elem = max(element_count, key=element_count.get)
        min_elem = min(element_count, key=element_count.get)
        print(f'max ', max_elem, ': ', f'{element_count[max_elem]:>40}' , f'min ', min_elem, ': ', f'{element_count[min_elem]:>40}' )
        print(f'Step {step} - ', element_count[max_elem]-element_count[min_elem])
   
    print('The answer to part 1 is (sample should be 2188189693529)', element_count[max_elem]-element_count[min_elem])


# stdscr = curses.initscr()
# curses.start_color()
# curses.use_default_colors()
# wrapper(main)

main(None)