import curses
from curses import wrapper

day = 15
f = open(f'input/{day}_sampleA.txt', 'r+')
# f = open(f'input/{day}.txt', 'r+')

debug = False
debug = True
draw = False
draw = True

def draw_Screen(header, Fco, Fvalue, Fmatrix, Fpath):
    max_y, max_x = stdscr.getmaxyx()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_YELLOW)

    begin_x, begin_y = 5, 5
    height, width = len(Fmatrix)+5, len(Fmatrix[0])+5
    
    if Fco == '0_0':
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
    if debug: stdscr.timeout(1000//1*10)
    else: stdscr.timeout(1000//3)
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
        matrix_list[Fmatrix[key]['y']][Fmatrix[key]['x']] = Fmatrix[key]['value']
    return(matrix_list)


def adjTiles(x, y, Fdict, Fpath, FpathLength):
    # only return tiles that have not been visited before
    
    if (x % 2 == 0 and y % 2 == 0) or (x % 2 == 1 and y % 2 == 1): possibleCos = ((x+1, y), (x, y+1), (x-1, y), (x,y-1)) # E, S, W, N
    else: possibleCos = ((x, y+1), (x+1, y), (x-1, y), (x,y-1)) # S, E, W, N

    possibleCos = tuple(filter(lambda co: co[0] >= 0 and co[1] >= 0 and co[0] < Fdict['width'] and co[1] < Fdict['height'], possibleCos )) # remove co's outside of 
    possibleCos = tuple(filter(lambda co: (co[0] < Fdict['width'] -1 and co [1] < Fdict['height'] -1) or ( co[0] == Fdict['width'] -1 and co[1] >= y) or ( co[1] == Fdict['height'] -1 and co[0] >= x) , possibleCos ) ) # it's useless to search in a part that is locked in by the edges; destCO = max of width and height
    possibleTiles = tuple(map(lambda co: xy_to_costr(co[0], co[1]), possibleCos))
    possibleTiles = list(filter(lambda co: co not in Fpath, possibleTiles))
    # possibleTiles = list(filter(lambda co: co[1] not in Fpath, [k[1] for k in (sorted((value, key) for (key,value) in validCos.items()))]))
    validCos = {}

    for coStr in possibleTiles:
        coVal =  Fdict[coStr]['value']
        coDist = Fdict[coStr]['costToGetHereFrom_0_0']

        if (FpathLength + coVal) <= coDist:
            # update the weight of each adjacent tile if it's lower than the currentValue
            Fdict[coStr]['costToGetHereFrom_0_0'] = FpathLength + coVal
            Fdict[coStr]['path'] = Fpath + [coStr]

        validCos[coStr] = Fdict[coStr]['costToGetHereFrom_0_0']

    possibleTiles = [k[1] for k in (sorted((value, key) for (key,value) in validCos.items()))] # order tiles by distance from 0_0

    if Fdict[possibleTiles[0]]['costToGetHereFrom_0_0'] < FpathLength:
        status = None
        message = 'Found shorter path, redrawing'
        if draw: draw_Screen([status, message], 'full', '#', matrix_as_list(Fdict), Fdict[coStr]['path'])

    return(possibleTiles, Fdict, Fdict[possibleTiles[0]]['path'], Fdict[possibleTiles[0]]['costToGetHereFrom_0_0'])

def onestepback(FcurCo, Fdict, Fpath, FpathLength):
    prevCo = Fpath[-2]
    newPath = Fpath[:-1]
    status = None
    message = f'Moving back from {FcurCo} to {prevCo}' #; changing path from {Fpath[-5:]} to {newPath[-5:]}'
    if debug: print (message)
    Fdict[prevCo]['possiblePaths'].remove(FcurCo)
    # FpathLength -= Fdict[prevCo]['value'] # before going back, subtract the value of the prev co
    FpathLength -= Fdict[FcurCo]['value'] # before going back, subtract the value of the cur  co
    if draw: draw_Screen([status, message], FcurCo, 'full', matrix_as_list(Fdict), Fpath)
    FcurCo = prevCo # go back one step
    return(FcurCo, Fdict, newPath, FpathLength)

def main(stdscr):
    inputFile = f.read().splitlines()
    f.close()

    # read file into dict with co [x,y] as key
    matrix = {}
    for y in range(0, len(inputFile)):
        for x in range(0, len(inputFile[y])):
            matrix[xy_to_costr(x,y)] = {'value': int(inputFile[y][x]), 'x': x, 'y': y, 'costToGetHereFrom_0_0': float('inf') }
    matrix['width'], matrix['height'] = len(inputFile[0]), len(inputFile)

    # start top, left
    curCo = '0_0'
    destCo = xy_to_costr(matrix['width']-1, matrix['height']-1)
    ShortestPathLength = matrix['width'] * matrix['height'] * 9
    ExplorablePaths, PossiblePaths, curPathLength = [], [], 0
    curPath, curPathLength, message = [curCo], 0, 'Starting...'
    while message == 'Starting...' or curCo != '0_0' : # until there are no more paths to explore....
        status, message = None, None
        if curCo != '0_0':
            if curPath[-1] != curCo: # we are here, because we explored this for the first time (not stepped back)
                curPath += [curCo] # add the current coordinate to the path
                curPathLength += matrix[curCo]['value']
                if matrix[curCo].get('costToGetHereFrom_0_0') is None:
                    matrix[curCo]['costToGetHereFrom_0_0'] = curPathLength
                elif curPathLength > matrix[curCo]['costToGetHereFrom_0_0']:
                    # useless to continue searching from here
                    PossiblePaths.append({'path': curPath, 'value': curPathLength, 'status': 'expensive_point'})
                    curCo, matrix, curPath, curPathLength = onestepback(curCo, matrix, curPath, curPathLength)
                    message = 'Found expensive point'
                    continue
                else:
                    matrix[curCo]['costToGetHereFrom_0_0'] = curPathLength
                    status = f'Current shortestPathLength: {ShortestPathLength} Paths disdovered: {len(PossiblePaths)}'
                    message = f'Exploring {curCo}; last 5 steps {curPath[-5:]}'
        if debug: print (message)
        if draw: draw_Screen([status, message], curCo, '#', matrix_as_list(matrix), curPath)

        if curPathLength >= ShortestPathLength and curCo != destCo: # stop exploring this route if it is longer than the shortest existing route
            PossiblePaths.append({'path': curPath, 'value': curPathLength, 'status': 'expensive'})
            status = None
            message = f'Found expensive path with value of: {curPathLength} and {len(curPath)} steps; last 5 steps {curPath[-5:]}'
            if draw: draw_Screen([status, message], curCo, '#', matrix_as_list(matrix))
            curCo, matrix, curPath, curPathLength = onestepback(curCo, matrix, curPath, curPathLength)
            continue

        if curCo == destCo:
            ShortestPathLength = min(ShortestPathLength, curPathLength)
            PossiblePaths.append({'path': curPath, 'value': curPathLength, 'status': 'completed'})
            # if debug: 
            status = None
            message = (f'Found path with value of: {curPathLength} and {len(curPath)} steps ; {len(PossiblePaths)} paths scanned')
            curCo, matrix, curPath, curPathLength = onestepback(curCo, matrix, curPath, curPathLength)

            continue
        if curPathLength > ShortestPathLength: # stop exploring this route if it is longer than the shortest existing route
            PossiblePaths.append({'path': curPath, 'value': curPathLength, 'status': 'expensive'})
            if debug: print(f'Found expensive path with value of: {curPathLength} and {len(curPath)} steps; last 5 steps {curPath[-5:]}')
            curCo, matrix, curPath, curPathLength = onestepback(curCo, matrix, curPath, curPathLength)
            continue

        # start exploring, stop the path when you reach a path already visited; stop the path when the destCo is reached
        # find adjacent tiles
        if matrix[curCo].get('possiblePaths') is None: # we are a first time visitor here
            matrix[curCo]['possiblePaths'], matrix, curPath, curPathLength = adjTiles(matrix[curCo]['x'], matrix[curCo]['y'], matrix, curPath, curPathLength)
        if matrix[curCo].get('possiblePaths') == []: # no more paths to explore, because we have been here before and explored everything
            while matrix[curCo].get('possiblePaths') == [] and curCo != '0_0':
                # check if the current path has already been explored and remove that from the list of possible tiles
                matrix[curCo]['possiblePaths'], matrix, curPath, curPathLength = adjTiles(matrix[curCo]['x'], matrix[curCo]['y'], matrix, curPath, curPathLength)
                if matrix[curCo].get('possiblePaths') == []: # no possible continuation for this path
                    PossiblePaths.append({'path': curPath + [None], 'value': curPathLength, 'status': 'dead-end'})
                # for path in filter(lambda x: curPath == x['path'][:len(curPath)], PossiblePaths):
                #     if matrix[curCo]['possiblePaths'].count(path['path'][len(curPath)]) > 0:
                #         matrix[curCo]['possiblePaths'].remove(path['path'][len(curPath)]) # remove this tile from the possible path
                if matrix[curCo].get('possiblePaths') == []: # if there are still no paths to explore; take one step back
                    curCo, matrix, curPath, curPathLength = onestepback(curCo, matrix, curPath, curPathLength)
                    if curCo == '0_0':
                        print('reached start co')
            # continue
        else: 
            pass
        # explore the next path

        if curCo == '0_0' and matrix[curCo]['possiblePaths'] == []:
            # finished!
            pass
        else:
            curCo = matrix[curCo]['possiblePaths'][0] # move to the next coordinate with the lowest value

    # now look through all PossiblePaths having a status completed and select the one with the lowest value
    shortestpath = sorted(filter(lambda p: p['status'] == 'completed' ,PossiblePaths), key=lambda d: d['value'])[0]

    status = f"{len(PossiblePaths)} paths scanned, {len(list(filter(lambda p: p['status'] == 'completed' ,PossiblePaths)))} paths completed"
    message = f"The answer to part 1 is (sample should be 40): {shortestpath['value']}"
    draw_Screen([status, message], curCo, 'full', matrix_as_list(matrix), shortestpath['path'])
    print(message)

stdscr = curses.initscr()
stdscr.scrollok(True)
winHeader = curses.newwin(1,1,1,1)
winMatrix_1 = curses.newwin(1,1,2,1)
# winMatrix_1 = curses.newpad(1,1)

curses.start_color()
curses.use_default_colors()
wrapper(main)

# main(None)