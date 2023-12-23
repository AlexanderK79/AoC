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
        polymer_tmp, polymer_new,step = pair, '', 0
        while (polymer_tmp[0:2] != pair and step <= 10) or step == 0:
            step += 1
            polymer_new = ''
            for i in range(0, len(polymer_tmp)-1):
                polymer_new += polymer_tmp[i:i+2].replace(polymer_tmp[i:i+2], rec[polymer_tmp[i:i+2]]['output'][:-1])
            polymer_tmp = polymer_new + polymer_tmp[-1]
            if polymer_tmp[-2:] == pair and step == 1: break
        if polymer_tmp[-2:] == pair and step == 1: # infinite repetition via right side
            rec[pair]['repetition_freq'] = step
            rec[pair]['repetition_string'] = polymer_tmp
            rec[pair]['element_count'] = {}
            for element in sorted(set(list(polymer_tmp))):
                rec[pair]['element_count'][element] = polymer_tmp.count(element)
        elif polymer_tmp[0:2] == pair:
            rec[pair]['repetition_freq'] = step
            rec[pair]['repetition_string'] = polymer_tmp
            rec[pair]['element_count'] = {}
            for element in sorted(set(list(polymer_tmp))):
                rec[pair]['element_count'][element] = polymer_tmp.count(element)
        else:
            print('no default repetition found for', pair)
            rec[pair]['repetition_freq'] = -1
            rec[pair]['repetition_string'] = polymer_tmp
    # check if the pairs without repetition change into parts that do repeat themselves
    for pair in list(rec.keys()):
        if rec[pair]['repetition_freq'] != -1: continue
        polymer_tmp, polymer_new,step,allRepPairs = pair, '', 0, []
        while allRepPairs.count(False) > 0 or step == 0:
            step += 1
            polymer_new = ''
            for i in range(0, len(polymer_tmp)-1):
                polymer_new += polymer_tmp[i:i+2].replace(polymer_tmp[i:i+2], rec[polymer_tmp[i:i+2]]['output'][:-1])
            polymer_tmp = polymer_new + polymer_tmp[-1]
            allRepPairs = []
            for i in range(0, len(polymer_tmp)-1):
                # check if each pair is repetitive
                allRepPairs.append(rec[polymer_tmp[i:i+2]]['repetition_freq'] != -1)
        print('This pair repeated itself to a block consisting of other blocks')
        rec[pair]['repetition_freq'] = step
        rec[pair]['repetition_string'] = polymer_tmp

    # run 10 steps of pair insertion
    step = 0
    polymer ='CB'
    print(polymer)
    while step < 10:
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
        print(f'Step {step} - polymer: {polymer[:130]}', element_count[max_elem]-element_count[min_elem])






        
   
    print('The answer to part 1 is (sample should be 1588)', element_count[max_elem]-element_count[min_elem])


# stdscr = curses.initscr()
# curses.start_color()
# curses.use_default_colors()
# wrapper(main)

main(None)