import curses
from curses import wrapper
from typing import Pattern

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

def splitBlocks(FinputPolymer, Fblocksize):
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

def pattern_detection(FinputPair, FinputPolymer, Fdict, Fstep):
    # try and detect pattern
    # step 0 =  2 elems
    # step 1 =  3 elems (2^1 +1)
    # step 2 =  5 elems (2^2 +1), start_elem, 3 elems, end_elem
    # step 3 =  9 elems (2^3 +1), 3 * 3 elems
    # step 4 = 17 elems         , start_elem, 5*3 elems, end_elem
    # step 5 = 33 elems         , 11 * 3 elems
    # step 6 = 65 elems         , start_elem, 21 * 3, end
    # step 7 = 129              , 43 * 3
    # step 8 = 257              , start_elem, 85 * 3, end_elem
    patternFound = False

    if Fstep < 3:
        # nothing to do
        pass
    elif Fstep % 2 == 0: #even step
        # let's see if the pattern matches
        # split the string between start_elem and end_elem in blocks of 3
        elem_Blocks = []
        for i in range(1, len(FinputPolymer)-2, 3):
            elem_Blocks.append(FinputPolymer[i:i+3])
        print('h')
    elif Fstep % 2 == 1: #odd step
        # let's see if the pattern matches
        # split the string between start_elem and end_elem in blocks of 3
        elem_Blocks = []
        for i in range(0, len(FinputPolymer)-2, 3):
            elem_Blocks.append(FinputPolymer[i:i+3])
        print('h')



    if patternFound:
        # update the dictionary with the found repetition
        Fdict[FinputPair]['repetition_freq'] = Fstep
        Fdict[FinputPair]['repetition_string'] = FinputPolymer
        Fdict[FinputPair]['element_count'] = {}
        for element in sorted(set(list(FinputPolymer))):
            Fdict[FinputPair]['element_count'][element] = FinputPolymer.count(element)
    return(patternFound, Fdict)


def main(stdscr):
    day = 14
    f = open(f'input/{day}_sampleA.txt', 'r+')
    # f = open(f'input/{day}.txt', 'r+')
    inputFile = f.read().splitlines()
    f.close()

    rec, element_count = {}, {}
    # create dict that holds the recipe
    polymer = inputFile[0]
    for recipe in list(filter(lambda x: x.count(' -> ') > 0, inputFile)):
        input, insert = recipe.split(' -> ')
        rec[input] = {'output': input[0] + insert + input[1]}

    # after how many steps does a polymer pair repeat itself?
    # count the number of elements, steps and use that to calculate
    
    for pair in list(rec.keys()):
        polymer_tmp, patternFound,step = pair, False, 0
        print(pair.center(277))
        while not patternFound and step < 10:
            step += 1
            polymer_tmp = updatePolymer(polymer_tmp, rec)
            patternFound, rec = pattern_detection(pair, polymer_tmp, rec, step)
            if False: print(' '.join(splitBlocks(polymer_tmp, 3))[:260].center(277))
        if polymer_tmp[0:2] == pair:
            rec[pair]['repetition_freq'] = step
            rec[pair]['repetition_string'] = polymer_tmp
            rec[pair]['element_count'] = {}
            for element in sorted(set(list(polymer_tmp))):
                rec[pair]['element_count'][element] = polymer_tmp.count(element)
        else:
            print('no default repetition found for', pair)
            rec[pair]['repetition_freq'] = -1
            rec[pair]['repetition_string'] = polymer_tmp

    # run 10 steps of pair insertion
    step = 0
    polymer ='CH'
    print(polymer)
    while step <= 40:
        step += 1
        polymer_new = ''
        for i in range(0, len(polymer)-1):
            polymer_new += polymer[i:i+2].replace(polymer[i:i+2], rec[polymer[i:i+2]]['output'][:-1])
        polymer = polymer_new + polymer[-1]
        # count all elements
        for element in sorted(set(list(polymer))):
            element_count[element] = polymer.count(element)
        max_elem = max(element_count, key=element_count.get)
        min_elem = min(element_count, key=element_count.get)
        # print(f'max ', max_elem, ': ', element_count[max_elem] , f'min ', min_elem, ': ', element_count[min_elem] )
        print(f'Step {step} - polymer: {" ".join(splitBlocks(polymer, 3))[:130].center(132)}') #, element_count[max_elem]-element_count[min_elem])






        
   
    print('The answer to part 1 is (sample should be 1588)', element_count[max_elem]-element_count[min_elem])


# stdscr = curses.initscr()
# curses.start_color()
# curses.use_default_colors()
# wrapper(main)

main(None)