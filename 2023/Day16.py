import argparse

class contraption:
    def __init__(self) -> None:
        self.content = list()
        self.mirroraction = {
            '|': { #key = incoming direction this mirror, #val = incoming direction next mirror
                'V': ['V'],
                '^': ['^'],
                '>': ['V', '^'],
                '<': ['V', '^']
            },
            '-': {
                'V': ['>', '<'],
                '^': ['>', '<'],
                '>': ['>'],
                '<': ['<']
            },
            '/': {
                'V': ['<'],
                '^': ['>'],
                '>': ['^'],
                '<': ['V']
            },
            '\\': {
                'V': ['>'],
                '^': ['<'],
                '>': ['V'],
                '<': ['^']
            }
        }
        self.mirrors = []
        self.path = []
        self.pathWorklist = [None]
        pass
    def build(self, fContent):
        self.content = fContent
        for (y, thisLine) in enumerate(fContent):
            for (x,thisC) in enumerate(thisLine):
                if thisC == '.': continue
                self.mirrors.append(self.mirror(x, y, thisC))
            pass
        self.width = len(self.content[0])
        self.height = len(self.content)
        return self
    def buildPath(self, fX, fY, fDirection):
        # returns the path of every co
        self.path = []
        self.pathWorklist = [(co(fX, fY), fDirection)]

        while len(self.pathWorklist) > 0: # keep exploring until we get on the same tile, in the same direction
            thisCo_dir = self.pathWorklist[0]
            self.path.append(thisCo_dir)
            print('processing', thisCo_dir[0].id, thisCo_dir[1]) if args.verbose else None
            thisM = [m for m in self.mirrors if m.co.id == thisCo_dir[0].id] 
            if len(thisM) > 0:
                thisM = thisM[0]
                # if we are arriving at the mirror, possibly changing direction
                fDirection = self.mirroraction[thisM.val][thisCo_dir[1]]
            else:
                thisM = thisCo_dir[0]
                # not at a mirror
                # check if we are outside of the bounds
                if thisM.x in (-1, len(self.content[0])) or thisM.y in (-1, len(self.content)):
                    self.path.remove(thisCo_dir)
                    self.pathWorklist.remove(thisCo_dir)
                    continue

            # find the next mirror in the possible directions
            nextMirrors = []
            if 'V' in fDirection:
                nextM = [m for m in self.mirrors if m.co.x == thisCo_dir[0].x and m.co.y >  thisCo_dir[0].y]
                if len(nextM) == 0:
                    nextM = (self.mirror(thisCo_dir[0].x, len(self.content), ''), 'V')
                    nextMirrors.append(nextM)
                else:
                    nextMirrors.append((sorted(nextM, key=lambda item:(item.co.x, item.co.y))[0], 'V'))
            if '^' in fDirection:
                nextM = [m for m in self.mirrors if m.co.x == thisCo_dir[0].x and m.co.y <  thisCo_dir[0].y]
                if len(nextM) == 0:
                    nextM = (self.mirror(thisCo_dir[0].x, -1, ''), '^')
                    nextMirrors.append(nextM)
                else:
                    nextMirrors.append((sorted(nextM, key=lambda item:(item.co.x, item.co.y))[-1], '^'))
            if '<' in fDirection:
                nextM = [m for m in self.mirrors if m.co.x <  thisCo_dir[0].x and m.co.y == thisCo_dir[0].y]
                if len(nextM) == 0:
                    nextM = (self.mirror(-1,thisCo_dir[0].y, ''), '<')
                    nextMirrors.append(nextM)
                else:
                    nextMirrors.append((sorted(nextM, key=lambda item:(item.co.x, item.co.y))[-1], '<'))
                pass
            if '>' in fDirection:
                nextM = [m for m in self.mirrors if m.co.x >  thisCo_dir[0].x and m.co.y == thisCo_dir[0].y]
                if len(nextM) == 0:
                    nextM = (self.mirror(len(self.content[0]),thisCo_dir[0].y, ''), '>')
                    nextMirrors.append(nextM)
                else:
                    nextMirrors.append((sorted(nextM, key=lambda item:(item.co.x, item.co.y))[0], '>'))
                pass
            self.pathWorklist.remove(thisCo_dir)
            for (m,d) in nextMirrors: # add the paths to explore, if we have not already been there
                if (m.co, d) not in self.path:
                    print('Adding', m.co.id, d,'to pathWorklist') if args.verbose else None
                    self.pathWorklist.append((m.co, d))
                    # add every co between this mirror and the next, to the path
                    p =  thisCo_dir[0].calcPath(m.co)
                    if p != None: [self.path.append((fCo, d)) for fCo in p]
                    pass
                # self.printPath()
        pass
    def printPath(self, keepMirrors=False):
        for (y, thisLine) in enumerate(self.content):
            if keepMirrors:
                print(''.join(['#' if co(x,y).id in [p[0].id for p in self.path] and c =='.' else c for (x,c) in enumerate(thisLine)]))
            else:
                print(''.join(['#' if co(x,y).id in [p[0].id for p in self.path] else '.' for (x,c) in enumerate(thisLine)]))
            

    class mirror:
        def __init__(self, fX, fY, fVal):
            self.co = co(fX, fY)
            self.val = fVal
            pass

class co:
    def __init__(self, fX, fY) -> None:
        self.x, self.y = fX, fY
        self.co = (self.x, self.y)
        self.id = '_'.join(map(str, (self.co)))
    def calcPath(self, fCodest):
        # returns all co's between (but not including) fCo1 en fCo2
        fCo1, fCo2 = self, fCodest
        x_range = [x for x in range(fCo1.x + (1 if fCo1.x < fCo2.x else -1), fCo2.x, 1 if fCo1.x < fCo2.x else -1)]
        y_range = [y for y in range(fCo1.y + (1 if fCo1.y < fCo2.y else -1), fCo2.y, 1 if fCo1.y < fCo2.y else -1)]
        if len(x_range) == 0: x_range = len(y_range) * [self.x]
        if len(y_range) == 0: y_range = len(x_range) * [self.y]
        pass
        if len(x_range) == len(y_range) and len(x_range) > 0:
            result = [co(x,y) for (x,y) in zip(x_range, y_range)]
        else:
            result = None
            pass
        return result



def main(stdscr):
    with open(fName, 'r+') as f:
        fContent = f.read().splitlines()
    

    myContraption = contraption()
    result = myContraption.build(fContent=fContent)
    result = myContraption.buildPath(0, 0, '>')
    myContraption.printPath(keepMirrors=True) if args.verbose else None
    result = len(set([p[0].id for p in myContraption.path]))

    message = f'The answer to part 1 is (sample should be 46, answer should be 7728, 7736 is too high): {result}'
    print(message)

    print(20 * '*')

    result = result

    results = []
    for x in (0, myContraption.width):
        for y in range(0, myContraption.height):
            d = '>' if x == 0 else '<'
            myContraption.buildPath(x,y,d)
            results.append(len(set([p[0].id for p in myContraption.path])))
            print (x, y, d, results[-1])
    for y in (0, myContraption.height):
        for x in range(0, myContraption.width):
            d = 'V' if y == 0 else '^'
            myContraption.buildPath(x,y,d)
            results.append(len(set([p[0].id for p in myContraption.path])))
            print (x, y, d, results[-1])

    result = max(results)

    message = f'The answer to part 2 is (sample should be 51, answer should be x): {result}'
    print(message)
    pass


# globals
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose"   , action="store_true", default=False, help="Add this to enable verbose output")
parser.add_argument("-d", "--draw"      , action="store_true", default=False, help="Add this to enable drawing")
parser.add_argument("-i", "--drawinterval", type=int, default=1, help="Add the value in ms for drawing interval")
parser.add_argument("-p", "--production", action="store_true", default=False, help="Add this to try the puzzle input")
args = parser.parse_args()

day = '16'
fName = f'2023/input/{day}_sample.txt'
if args.production: fName = f'2023/input/{day}.txt'

debug = args.verbose
draw = args.draw

main(None)