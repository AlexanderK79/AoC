blTesting = False
Debug = True
day='17'
part='1'

if blTesting:
    with open(f'{day}-sample-input{part}.txt', 'r') as file: data = file.read().split('\n')
    # with open(f'{day}-sample-input2.txt', 'r') as file: data = file.read().split('\n')
else:
    with open(f'{day}-Alexander-input.txt', 'r') as file: data = file.read().split('\n')


# all change at the same time in three dimensions
# we can do the same as a few days before, but this would require a bitstream in 3D (and we have an infinite grid now)
# or... we create a class that on update compares and processes

class fullgrid:
    def __init__(self, grid={}):
        self.grid = {0: {0: {0:  {'current_state': None, 'future_state': None, 'activeNeighbors': None}}}}

    def addco(self, x, y, z, current_state='.', future_state='.', activeNeighbors=None):
        # if a co does not exist, create it
        if self.grid.get(x) is None:
            self.grid[x] = {} # initialize if it does not exist
        if self.grid[x].get(y) is None:
            self.grid[x][y] = {}
        if self.grid[x][y].get(z) is None:
            self.grid[x][y][z] = {}
        if not self.grid[x][y][z].get('current_state'):
            self.grid[x][y][z] = {'current_state': current_state, 'future_state': future_state,  'activeNeighbors': activeNeighbors}
    
    def enumGrid(self, type='default'):
        # this returns a tuple of tuples
        # tuples are ordered
        allX, allY, allZ = set(), set(), set()
        for x in (self.grid.keys() - allX):
            allX.add(x)
            for y in (self.grid[x].keys() - allY):
                allY.add(y)
                for z in (self.grid[x][y].keys() - allZ):
                    allZ.add(z)
        if type=='default':
            return((sorted(allX)), (sorted(allY)), (sorted(allZ)))
        elif type=='print':
            return((sorted(allX)), list(reversed(sorted(allY))), (sorted(allZ)))
        else:
            return((sorted(allX)), (sorted(allY)), (sorted(allZ)))

    def expandGrid(self):
        enumGrid = self.enumGrid(type='default')
        for x in range(min(enumGrid[0])-1, max(enumGrid[0])+1+1):
            for y in range(min(enumGrid[1])-1, max(enumGrid[1])+1+1):
                for z in range(min(enumGrid[2])-1, max(enumGrid[2])+1+1):
                    self.addco(x, y, z)


    def calculateGrid(self):
        enumGrid = self.enumGrid(type='default')
        for x in enumGrid[0]:
            for y in enumGrid[1]:
                for z in enumGrid[2]:
                    numOfActiveNeighbors = self.calculateNeighbors(x, y, z)
                    if self.grid[x][y][z]['current_state'] == '.' and numOfActiveNeighbors == 3:
                        # If a cube is inactive but exactly 3 of its neighbors are active, the cube becomes active.
                        # Otherwise, the cube remains inactive.
                        self.grid[x][y][z]['future_state'] = '#'
                    elif self.grid[x][y][z]['current_state'] == '#' and numOfActiveNeighbors in (2, 3):  
                        # If a cube is active and exactly 2 or 3 of its neighbors are also active, the cube remains active.
                        # Otherwise, the cube becomes inactive.
                        self.grid[x][y][z]['future_state'] = '#'
                    else:
                        self.grid[x][y][z]['future_state'] = '.'

    def calculateNeighbors(self, x, y, z):
        numOfActiveNeighbors = 0
        for xCo in (x-1, x, x+1):
            for yCo in (y-1, y, y+1):
                for zCo in (z-1, z, z+1):
                    if (xCo == x and yCo == y and zCo == z):
                        continue
                    # process every adjacent coordinate
                    val = self.grid.get(xCo, {}).get(yCo, {}).get(zCo, {}).get('current_state', 'create')
                    if val == 'create':
                        self.addco(xCo, yCo, zCo)
                    else:
                        numOfActiveNeighbors += val.count('#')
        return(numOfActiveNeighbors)

    def updateGrid(self):
        enumGrid = self.enumGrid(type='default')
        allZwithoutLife = list(tuple(enumGrid[2]))
        for x in enumGrid[0]:
            for y in enumGrid[1]:
                for z in enumGrid[2]:
                    # update the co current_state to it's future_state
                    self.grid[x][y][z]['current_state'] = self.grid[x][y][z]['future_state'] 
                    self.grid[x][y][z]['future_state'] = '.'
                    if self.grid[x][y][z]['current_state'] == '#':
                        if z in allZwithoutLife: allZwithoutLife.remove(z)
        # only keep 1 outermost empty z layer
        while len(allZwithoutLife) >= 4 and len(allZwithoutLife) % 2 == 0:
            for z in min(allZwithoutLife), max(allZwithoutLife):
                allZwithoutLife.remove(z)
                for x in enumGrid[0]:
                    for y in enumGrid[1]:
                        self.grid[x][y].pop(z)
    
    def countActiveCubes(self):
        activeCubes = 0
        enumGrid = self.enumGrid(type='default')
        for x in enumGrid[0]:
            for y in enumGrid[1]:
                for z in enumGrid[2]:
                    activeCubes += self.grid[x][y][z]['current_state'].count('#')
        return activeCubes
    
    def printGrid(self):
        enumGrid = self.enumGrid(type='print')
        for z in enumGrid[2]:
            print(f"\nLevel: {z:>5}")
            for y in enumGrid[1]:
                line = ""
                xaxis = ""
                if y == 0: yaxis = f"\n"
                for x in enumGrid[0]:
                    if x == 0 and y == 0: 
                        xaxis += f"\u253C\u2500"
                        line += f"\u2502"
                    elif y == 0: xaxis += f"\u2500"
                    elif x == 0: line += f"\u2502"
                    line += self.grid[x][y][z]['current_state']
                print(line)
                if y == 0: print(xaxis)

myGrid = fullgrid()

# initialize the grid with 3 layers and a blank around it
for y, line in enumerate(data[::-1]): # read backwards, so it matches a regular math grid
    for x, char in enumerate(line):
        myGrid.addco(x, y, 0, current_state=char)
myGrid.expandGrid()

# Now do 6 boot cycles and calculate the grid
myGrid.printGrid()
for i in range(1, 7):
    print (f"\nRun: {i:>5}")
    myGrid.calculateGrid()
    myGrid.updateGrid()
    myGrid.printGrid()

# How many cubes are left in the active state after the sixth cycle?

answer= myGrid.countActiveCubes()
print (f'The answer to part {part} of day {day} is: {answer}')


