import argparse
import matplotlib.pyplot as plt
import numpy as np

class pile:
    def __init__(self) -> None:
        self.x, self.y, self.z = None, None, None
        self.blocks = list()
        self.content = list()
        self.dims = None
        self.dims_true = None
    def build(self, fContent):
        for (i, thisBlock) in enumerate(fContent):
            thisBlock = thisBlock.split('~')
            coB = tuple(map(int, thisBlock[0].split(',')))
            coE = tuple(map(int, thisBlock[1].split(',')))
            self.content.append((coB, coE))

        # calc max co's
        maxCo = [[max((S,E)) for S,E in zip(b[0], b[1])] for b in self.content]
        self.x = 1+ max([c[0] for c in maxCo])
        self.y = 1+ max([c[1] for c in maxCo])
        self.z = 1+ max([c[2] for c in maxCo])
        self.x, self.y, self.z = np.indices((self.x, self.y, self.z))

        # create the blocks
        colors = iter([plt.cm.Dark2(i % len(plt.cm.Dark2.colors)) for i in range(50)])
        colors = iter(len(self.content) * ['red', 'green', 'blue', 'yellow'])
        names  = iter(max(1, (len(self.content)//20)) * [chr(i) for i in range(65, 65+26)])
        if args.production: names  = iter(range(len(self.content)))
        self.blocks.append(block(self, 'FLOOR', (0,0,0), self.x.shape[:2]+((0,)), 'grey'))
        for thisBlock in self.content:
            coB, coE = thisBlock
            self.blocks.append(block(self, next(names), coB, coE, next(colors)))
        pass
        # update the support info for each block
        for thisBlock in self.blocks:
            thisBlock.update_support()
    
    def drop_pile(self):
        # keep dropping the blocks until they all are supported
        free_blocks = [b for b in self.blocks if len(b.supportedby) == 0 and False in (b.dims[:,:,0])]
        while len(free_blocks) > 0:
            if args.verbose: print('Stacked', len(self.blocks)-len(free_blocks), 'of', len(self.blocks), 'blocks')
            # sort along the Z-axis
            free_blocks = [b for b in sorted(free_blocks, key=lambda thisB: min(np.where(thisB.dims)[2]), reverse=False)]
            thisB = free_blocks[0]
            # thisBlock Z-axis
            # Z-axis of the next block with a shared x and y coordinate: number of drops to move
            thisZ = min(np.where(thisB.dims)[2])
            nextZ = max([max(np.where(b.dims)[2]) for b in self.blocks if np.logical_and(b.dims[:,:,:thisZ].max(axis=2), thisB.dims.max(axis=2)).any() and b != thisB])
            while len(thisB.supportedby) == 0:
                thisB.move(0,0,nextZ-thisZ+1)
            del thisZ, nextZ
            free_blocks = [b for b in self.blocks if len(b.supportedby) == 0 and False in (b.dims[:,:,0])]
            pass


    def draw(self):
        voxelarray = np.logical_or.reduce([b.dims for b in self.blocks])
        colors = np.empty(voxelarray.shape, dtype=object)
        for b in self.blocks:
            colors[b.dims] = b.color
            pass
        # and plot everything
        ax = plt.figure().add_subplot(projection='3d')
        ax.voxels(voxelarray, facecolors=colors, edgecolor='k')

        # Set the axis labels
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        plt.gca().set_aspect('equal', adjustable='box')
        plt.show()

        pass

class block:
    def __init__(self, fParent, fName, fCoB, fCoE, fColor) -> None:
        self.parent = fParent
        self.name = fName
        self.co_begin = fCoB
        self.co_end = fCoE
        self.color = fColor
        x,y,z = self.parent.x, self.parent.y, self.parent.z
        self.dims = [np.logical_and(S <= axis, axis <= E) for axis, S, E in zip([x,y,z], fCoB, fCoE)]
        self.dims = self.dims[0] & self.dims[1] & self.dims[2]
        self.supports = list()
        self.supportedby = list()
        pass
    def update_support(self):
        pass
        # find all blocks with a z that is exactly 1 higher: update or add to supports
        [b.supportedby.remove(self) for b in self.supports]
        self.supports = [b for b in self.parent.blocks if np.logical_and(b.dims[:,:,1:], self.dims[:,:,:-1]).any() and b != self]
        [b.supportedby.append(self) for b in self.supports if b not in b.supportedby]
        pass
        # find all blocks with a z that is exactly 1 lower: update or add to supportedby
        [b.supports.remove(self) for b in self.supportedby]
        self.supportedby = [b for b in self.parent.blocks if np.logical_and(b.dims[:,:,:-1], self.dims[:,:,1:]).any() and b != self]
        [b.supports.append(self) for b in self.supportedby if b not in b.supports]
        if args.verbose: print(self.name, 'supports', [b.name for b in self.supports], 'supportedby', [b.name for b in self.supportedby])

    def move(self, fX=0, fY=0, fZ=0):
        assert fX != 0 or fY != 0 or fZ !=0
        if args.verbose: print('Moving', self.name, 'Steps', fX, fY, fZ)
        if fX != 0: self.dims = np.roll(self.dims, fX, axis=0)
        if fY != 0: self.dims = np.roll(self.dims, fY, axis=1)
        if fZ != 0: self.dims = np.roll(self.dims, fZ, axis=2)
        pass
        self.update_support()

def main(stdscr):
    with open(fName, 'r+') as f:
        fContent = f.read().splitlines()
    

    myPile = pile()
    result = myPile.build(fContent=fContent)
    # if args.verbose and not args.production: myPile.draw()

    # drop every block by 1 z, until the pile stabilizes
    myPile.drop_pile()
    if args.verbose and args.production: pass
    myPile.draw()
    [b.update_support() for b in myPile.blocks]
    pass
    safe_blocks = [thisB for thisB in [(b.name, 1 not in [len(bs.supportedby) for bs in b.supports]) for b in myPile.blocks if b.name != 'FLOOR'] if thisB[1] == True]
    result = len(safe_blocks)
    print([thisB for thisB in [(b.name, 1 not in [len(bs.supportedby) for bs in b.supports], len(b.supports), [len(bs.supportedby) for bs in b.supports]) for b in myPile.blocks if b.name != 'FLOOR'] if thisB[1] == True])

    message = f'The answer to part 1 is (sample should be 5, answer should be 459, 1139, 1130, 1000 is too high): {result}'
    print(message)

    print(20 * '*')

    result = result

    message = f'The answer to part 2 is (sample should be x, answer should be x): {result}'
    print(message)
    pass


# globals
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose"   , action="store_true", default=False, help="Add this to enable verbose output")
parser.add_argument("-d", "--draw"      , action="store_true", default=False, help="Add this to enable drawing")
parser.add_argument("-i", "--drawinterval", type=int, default=1, help="Add the value in ms for drawing interval")
parser.add_argument("-p", "--production", action="store_true", default=False, help="Add this to try the puzzle input")
args = parser.parse_args()

day = '22'
fName = f'2023/input/{day}_sample.txt'
if args.production: fName = f'2023/input/{day}.txt'

debug = args.verbose
draw = args.draw

main(None)