import copy
from os import system, name
from time import sleep

blTesting = False
Debug = True
day=11

if blTesting:
    with open(f'{day}-sample-input1.txt', 'r') as file: data = file.read().split('\n')
    # with open(f'{day}-sample-input2.txt', 'r') as file: data = file.read().split('\n')
else:
    with open(f'{day}-Alexander-input.txt', 'r') as file: data = file.read().split('\n')

def AdjacentItemsInRange(FOccupiedSeats, FcurY, FcurX, FGridHeight, FGridWidth):
    # this function returns the status of the first visible seat for the specified FcurY, FcurX in each direction
    # NW  N  NE
    # W  cur E
    # SW  S  SE
    #    travelPath(FOccupiedSeats, FGridHeight, FGridWidth, FcurY, FcurX, FendY, FstepY,  FstepX)

    NW = travelPath(FOccupiedSeats, FGridHeight, FGridWidth, FcurY, FcurX, -1, -1)
    N  = travelPath(FOccupiedSeats, FGridHeight, FGridWidth, FcurY, FcurX, -1,  0)
    NE = travelPath(FOccupiedSeats, FGridHeight, FGridWidth, FcurY, FcurX, -1,  1)
    W  = travelPath(FOccupiedSeats, FGridHeight, FGridWidth, FcurY, FcurX,  0, -1)
    E  = travelPath(FOccupiedSeats, FGridHeight, FGridWidth, FcurY, FcurX,  0,  1)
    SW = travelPath(FOccupiedSeats, FGridHeight, FGridWidth, FcurY, FcurX,  1, -1)
    S  = travelPath(FOccupiedSeats, FGridHeight, FGridWidth, FcurY, FcurX,  1,  0)
    SE = travelPath(FOccupiedSeats, FGridHeight, FGridWidth, FcurY, FcurX,  1,  1)

    return (NW, N, NE, W, E, SW, S, SE)

def travelPath (FOccupiedSeats, FGridHeight, FGridWidth, FcurY, FcurX, FstepY, FstepX):
    # this function returns the status of the found seat, or "." for an empty seat
    curY, curX = FcurY, FcurX
    result ='.'
    curY += FstepY
    curX += FstepX

    while result=='.' and (0 <= curY < FGridHeight) and (0 <= curX < FGridWidth) :
        result = FOccupiedSeats[curY][curX]
        curY += FstepY
        curX += FstepX
        
    return(result)

def ClearScreen():
    if name == 'nt': # windows
        _ = system('cls')
    else:     # for mac and linux(here, os.name is 'posix') 
        _ = system('clear')


# create a grid with the floorplan
# x -> 
# y   0 1 2 3 4 5 6
# | 0 L . L L . L
# v 1 L L L L L L
#   2 L . L . L .

GridHeight = len(data)
GridWidth = len(data[0])
FloorPlan, OccupiedSeats = {}, {}
y = 0
for y in range(GridHeight):
    x = 0
    FloorPlan[y] = {}
    for x in range(GridWidth):
        FloorPlan[y][x] = data[y][x]

OccupiedSeats = copy.deepcopy(FloorPlan)

curGrid, curLine = "", ""
for line in FloorPlan:
    curLine = ""
    for char in FloorPlan[line]:
        curLine += FloorPlan[line][char]
    curGrid += curLine + '\n'
print (f"Initial floorplan:\n{curGrid}")

# keep calculating the new OccupiedSeats
runNumber = 0
GridHistory = list()
while not curGrid in GridHistory[:-1]:
    runNumber += 1
    NewOccupiedSeats = copy.deepcopy(OccupiedSeats)
    curGrid, curLine = "", ""
    for line in OccupiedSeats:
        curLine = ""
        for char in OccupiedSeats[line]:
            if OccupiedSeats[line][char] == '.': 
                curLine += OccupiedSeats[line][char]
            else:
                # watch for the first seat in each of the eight directions and check if it is occupied or empty
                scanresult = tuple(AdjacentItemsInRange(OccupiedSeats, line, char, GridHeight, GridWidth))
                # if all 8 seats in view are empty, occupy seat
                if OccupiedSeats[line][char]=='L' and (scanresult.count('.')+scanresult.count('L')) == 8: NewOccupiedSeats[line][char] = '#'
                # if there are five or more occupied seats in view, then leave your seat
                if  OccupiedSeats[line][char]=='#' and scanresult.count('#') >= 5: NewOccupiedSeats[line][char] = 'L'
                curLine += NewOccupiedSeats[line][char]
        curGrid += curLine + '\n'
    OccupiedSeats = copy.deepcopy(NewOccupiedSeats)
    GridHistory.append(curGrid)
    # ClearScreen()
    # print (f"Result of run number {runNumber}:\n{curGrid}")


answer = curGrid.count('#')
print (f"The answer to part 2 of day {day} is {answer} after {runNumber} runs")