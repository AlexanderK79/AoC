import argparse
import curses
from curses import wrapper


class mapgrid:
    def __init__(self) -> None:
        self.grid = {} # coordinates in x_y
        self.h, self.w = 0, 0
        self.zdict = {} # height
        i=0
        for c in map(chr, range(ord('a'), ord('z')+1)):
            self.zdict[c] = i
            i+=1
        self.zdict['S'] = self.zdict['a']
        self.zdict['E'] = self.zdict['z']
        pass
    def addRow(self, fY, fLine):
        self.h = max(fY, self.h)
        self.w = max(len(fLine), self.w)
        fX = 0
        for n in fLine:
            self.grid['_'.join(map(int.__str__, (fX, fY)))] = node(self, n, fX, fY)
            fX += 1

    def calcDist(self, fSrc):
        #self.grid[fSrc].update_distToS_recursive(0)
        for n in self.grid.values():
            n.distToS = float('inf')
        self.grid[fSrc].update_distToS(0)
        i = 0
        old_nodes_set = len([v for v in self.grid.values() if v.distToS < float("inf")])
        cur_nodes_set = 2
        while cur_nodes_set > old_nodes_set:
            i+=1
            old_nodes_set = cur_nodes_set
            if draw: print (f'Round number {i:5} Number of nodes set: {cur_nodes_set}')
            for thisNode in self.grid.values():
                thisNode.distToS = min([thisNode.distToS]+ [1+n.distToS for n in thisNode.src_neighboors()])
                #if draw and thisNode.distToS < float('inf'): print (f'{thisNode.x:5}{thisNode.y:5}{thisNode.z:5}{thisNode.val:>5}{thisNode.distToS:5}')
                pass
            cur_nodes_set = len([v for v in self.grid.values() if v.distToS < float("inf")])
            #print ([n.distToS for n in self.grid.values() if n.val == 'E'][0])
        return [n.distToS for n in self.grid.values() if n.val == 'E'][0]

    def printGrid(self):
        for y in range(self.h):
            fLine =[]
            fLinePath =[]
            for x in range(self.w):
                fLine.append(self.grid['_'.join(map(int.__str__, (x, y)))].val)
                fLinePath.append(self.grid['_'.join(map(int.__str__, (x, y)))].distToS)
            print(fLine)
            #print(fLinePath)
            del fLine, fLinePath

class node:
    def __init__(self, fParent, fVal, fX, fY) -> None:
        self.parent = fParent
        self.val = fVal
        self.distToS = float('inf')
        self.x, self.y, self.z = fX, fY, fParent.zdict[fVal]
        self.neighboors = {} # "NESW"
        for k,v in {'N': (0, -1, 'S'), 'E': (1, 0, 'W'), 'S': (0, 1, 'N'), 'W': (-1, 0, 'E')}.items():
            n = fParent.grid.get('_'.join(map(int.__str__, (self.x + v[0], self.y + v[1]))))
            self.neighboors[k] = n
            if n: n.neighboors[v[2]] = self
        pass

    def dest_neighboors(self):
        return [n for n in self.neighboors.values() if n and ( (n.z - self.z) in (0,1) or (self.z > n.z) )]

    def src_neighboors(self):
        return [n for n in self.neighboors.values() if n and ( (n.z - self.z) in (0,-1) or (self.z < n.z) )]

    def update_distToS(self, fDist):
        self.distToS = fDist

    def update_distToS_recursive(self, fDist):
        self.distToS = fDist
        for n in self.neighboors.values():
            if n and n.z - self.z in (0,1) and fDist + 1 < n.distToS:
                n.update_distToS_recursive(fDist+1)


        pass


def main(stdscr):
    myMap = mapgrid()
    y = 0
    with open(fName, 'r+') as f:
        for line in f.read().splitlines():
            myMap.addRow(y, line)
            y+=1
        del line
    Sco = '_'.join(map(int.__str__, [(n.x, n.y) for n in myMap.grid.values() if n.val == 'S'][0]))
    result = myMap.calcDist(Sco)
    if draw: myMap.printGrid()

    #result = [n.distToS for n in myMap.grid.values() if n.val == 'E'][0]

    message = f'The answer to part 1 is (sample should be 31, answer should be 481): {result}'
    print(message)

    Sco_list = [(n.x, n.y) for n in myMap.grid.values() if n.val == 'a']
    results = {}
    for co in Sco_list:
        print (f'Processing {Sco_list.index(co)}/{len(Sco_list)}')
        Sco = '_'.join(map(int.__str__, co))
        result = myMap.calcDist(Sco)
        results[Sco] = result
    pass
    result = min(v for v in results.values())

    message = f'The answer to part 2 is (sample should be 29, answer should be y): {result}'
    print(message)


# globals
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose"   , action="store_true", default=False, help="Add this to enable verbose output")
parser.add_argument("-d", "--draw"      , action="store_true", default=False, help="Add this to enable drawing")
parser.add_argument("-i", "--drawinterval", type=int, default=1, help="Add the value in ms for drawing interval")
parser.add_argument("-p", "--production", action="store_true", default=False, help="Add this to try the puzzle input")
args = parser.parse_args()

day = '12'
fName = f'2022/input/{day}_sample.txt'
if args.production: fName = f'2022/input/{day}.txt'

debug = args.verbose
draw = args.draw

""" stdscr = curses.initscr()
curses.start_color()
curses.use_default_colors()
wrapper(main)
 """
main(None)