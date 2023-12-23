import argparse
import re

class Forest:
    # consists of trees
    def __init__(self, fContent):
        self.grid = dict() # grid with x, y and 0,0 bottom left
        y = 0
        for line in fContent.splitlines()[::-1]:
            x = 0
            for h in line:
                self.grid['_'.join(map(int.__str__,(x, y)))] = Tree(self, x, y, int(h))
                x += 1
            del h
            y+=1
        del x, y, line

        # now update each neighboor
        for t in self.grid.values():
            t.update_neighboors()
            pass

        # now set the visibility and scenic score of each tree
        for t in self.grid.values():
            for d in  ['N', 'E', 'S', 'W']:
                cur_t = t
                t.visible[d] = True
                vis_trees = 0
                while t.visible and cur_t:
                    cur_t = cur_t.neighboors[d]
                    if cur_t:
                        vis_trees += 1
                        if t.height <= cur_t.height:
                            t.visible[d] = False
                            t.scenic_vals[d] = vis_trees
                            break
                t.scenic_vals[d] = vis_trees
                pass
            if True in set(t.visible.values()):
                t.visible_anydir = True
            else:
                t.visible_anydir = False
            
            scenic_score = 1
            for i in t.scenic_vals.values():
                scenic_score *= i
            t.scenic_score = scenic_score
        pass

class Tree:
    # consists of trees
    def __init__(self, fForest, fX, fY, fH):
        self.forest = fForest
        self.height = fH 
        self.neighboors = dict() # {'N': ref to Tree, 'NE', ref to Tree, etc.}
        self.visible = dict() # direction from what side it is visible
        self.visible_anydir = None
        self.scenic_vals = dict ()
        self.scenic_score = None
        self.X, self.Y = fX, fY
        pass
    def update_neighboors(self):
        nb = [['N', [0, 1]], ['E', [1, 0]], ['S', [0,-1]], ['W', [-1,0]]]
        for pair in nb:
            x, y = self.X + pair[1][0], self.Y + pair[1][1]
            self.neighboors[pair[0]] = self.forest.grid.get('_'.join(map(int.__str__, (x, y))), None)
            pass
        pass


def main(stdscr):
    with open(fName, 'r+') as f:
        data = Forest(f.read())

    result = len([t for t in data.grid.values() if t.visible_anydir])
    message = f'The answer to part 1 is (sample should be 21, answer should be 1812): {result}'
    print(message)

    print(20 * '*')
    result = max([t.scenic_score for t in data.grid.values()])
    message = f'The answer to part 2 is (sample should be 8, answer should be 315495): {result}'
    print(message)


# globals
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose"   , action="store_true", default=False, help="Add this to enable verbose output")
parser.add_argument("-d", "--draw"      , action="store_true", default=False, help="Add this to enable drawing")
parser.add_argument("-i", "--drawinterval", type=int, default=1, help="Add the value in ms for drawing interval")
parser.add_argument("-p", "--production", action="store_true", default=False, help="Add this to try the puzzle input")
args = parser.parse_args()

day = '08'
fName = f'2022/input/{day}_sample.txt'
if args.production: fName = f'2022/input/{day}.txt'

debug = args.verbose
draw = args.draw

main(None)