import argparse
import curses
from curses import wrapper
import turtle

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

def sumVals(start, step):
    # returns the value of the individual values after # steps
    # in Xco mode: don't go below 0
    # in Yco mode: go below 0
    # ( (highest val + lowest val) * number of elements) // 2
    val = ( (start + (start - step+1) ) * (1+ (step-1)) ) // 2
    return (val)

def calculateX(startX, Vx, step):
    # returns the new X after # steps
    X = startX
    X += max(sumVals(Vx, min(step, Vx+1)), sumVals(Vx, step))  # stabilizes in step Vx + 1
    return(X)

def calculateY(startY, Ay, step):
    # returns the new Y after # steps
    Y = startY
    Y = sumVals(Ay, step)
    return(Y)

def calculateXY(startX, startY, Vx, Ay, step):
    return((calculateX(startX, Vx, step), calculateY(startY, Ay, step)))

def main(stdscr):
    day = 17
    inputFile = f.read().splitlines()
    f.close()

    targetArea = list(map(lambda item: item.strip().replace('x=', '').replace('y=','').split('..'), inputFile[0].replace('target area: ','').split(',')))
    targetArea = list(map(lambda co: list(map(lambda insideco: int(insideco), co)), targetArea))
    # check how many cos of the trajectory overlap with targetAreaCos
    TAminX, TAmaxX = min(targetArea[0][0], targetArea[0][1]), max(targetArea[0][0], targetArea[0][1])
    TAminY, TAmaxY = min(targetArea[1][0], targetArea[1][1]), max(targetArea[1][0], targetArea[1][1])

    if False:
        for i in range(5, 7):
            for j in range(1, 20):
                # print(f'Vx: {i} Ay: {i} Step: {j} X: {calculateX(0, i, j)} Y: {calculateY(0, i, j)}')
                print(f'Vx: {i} Ay: {i} Step: {j} X: {calculateXY(0, 0, i, i, j)[0]} Y: {calculateXY(0, 0, i, i, j)[1]}')

    # now check if this probe hits the target area
    # create tuple of all possible coordinates in target area
    targetAreaCos = tuple((x, y)for y in range(TAminY, TAmaxY+1) for x in range(TAminX, TAmaxX+1)  )

    startCoX, startCoY, x, y, step = 5 * [0]
    HittingPaths, HitVA = {}, []
    for Vx in range(0, TAmaxX+1):
        # x, y = calculateXY(startCoX, startCoY, Vx, 1, Vx +1)
        # if x < TAminX: 
        #     continue  # stabilizes in step Vx + 1, so if this is lower than TAminX, it's no use in looking any further
        for Ay in range(TAminY,500):
            step, x, y, maxY = 3 * [0] + [-999]

            while x <= TAmaxX and y >= TAminY: # keep stepping if we are not yet in and not past the target zone
                step += 1
                x, y = calculateXY(startCoX, startCoY, Vx, Ay, step)
                maxY = max(maxY, y)
                # print(f'Vx: {Vx} Ay: {Ay} Step: {step}, X: {x} Y: {y}')
                if set(tuple(((x, y), (0,0)))) & set(targetAreaCos):
                    # print(f'found a hit, max reached height ', maxY)
                    if (Vx, Ay) not in HitVA: HitVA += [(Vx,Ay)]
                    HittingPaths['_'.join(list(map(lambda item: str(item), [startCoX, startCoY, Vx, Ay, step])))] = {
                        'startCoX': startCoX, 'startCoY': startCoY,
                        'Vx': Vx, 'Ay': Ay, 'step': step,
                        'hit': (x,y), 'maxY': maxY
                    }

    # find the highest maxY in the dict HittingPaths
    best_shot = sorted(HittingPaths.items(), key=lambda item: item[1]['maxY'], reverse=True)[0]
    print(best_shot)

    if draw:
        T = turtle.Turtle()
        T.screen.bgcolor('#005EB8')
        T.penup()
        T.goto(targetArea[0][0], targetArea[1][0])
        T.pendown()
        T.goto(targetArea[0][1], targetArea[1][0])
        T.goto(targetArea[0][1], targetArea[1][1])
        T.goto(targetArea[0][0], targetArea[1][1])
        T.goto(targetArea[0][0], targetArea[1][0])
        T.penup()
        T.home()
        T.forward(200)
        T.dot(10)
        T.forward(200)


    # The probe's x position increases by its x velocity.
    # The probe's y position increases by its y velocity.
    # Due to drag, the probe's x velocity changes by 1 toward the value 0; that is, it decreases by 1 if it is greater than 0, increases by 1 if it is less than 0, or does not change if it is already 0.
    # Due to gravity, the probe's y velocity decreases by 1.



    print('The answer to part 1 is (sample should be 45)', best_shot[1]['maxY'])
    print('The answer to part 2 is (sample should be 112)', len(HitVA))


# globals
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose"   , action="store_true", default=False, help="Add this to enable verbose output")
parser.add_argument("-d", "--draw"      , action="store_true", default=False, help="Add this to enable drawing")
parser.add_argument("-i", "--drawinterval", type=int, default=1, help="Add the value in ms for drawing interval")
parser.add_argument("-p", "--production", action="store_true", default=False, help="Add this to try the puzzle input")
args = parser.parse_args()

day = 17
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