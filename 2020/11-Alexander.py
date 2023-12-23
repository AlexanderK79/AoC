import pandas as pd
from io import StringIO
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

def AdjacentItems(FFloorplan, FOccupiedSeats, FGridWidth, FGridLength):
    # a item on the rightside edge is not a neighbor to the item on the next position in the string:
    #     ....L
    #     L....
    # let's remove those on the next line from the source using a mask
    # the mask is modulo FGridWidth 
    # direction in the variablename is the direction of the shift
    FGrid_leftMask = int((FGridLength // FGridWidth) * format(2**(FGridWidth-1),'b'), 2)
    FGrid_left = FOccupiedSeats >> 1
    FGrid_left = (FGrid_left^(FGrid_left & FGrid_leftMask ))

    # the item on the leftside edge is not a neighbor to the item on the previous position in the string:
    #     ....L
    #     L....
    # let's remove those on the previous line from the source using a mask
    # the mask is modulo FGridWidth
    FGrid_rightMask = BinMask(FGrid_leftMask << 1, FGridWidth, FGridLength)
    FGrid_right = BinMask(FOccupiedSeats << 1, FGridWidth, FGridLength)
    FGrid_right = (FGrid_right^(FGrid_right & FGrid_rightMask ))
     

    FGrid_down = BinMask(FOccupiedSeats << FGridWidth, FGridWidth, FGridLength)
    FGrid_top = FOccupiedSeats >> FGridWidth


    FGrid_topleft = FGrid_left >> FGridWidth
    FGrid_topright = FGrid_right >> FGridWidth

    FGrid_downleft = BinMask(FGrid_left << FGridWidth, FGridWidth, FGridLength)
    FGrid_downright = BinMask(FGrid_right << FGridWidth, FGridWidth, FGridLength)

    return (FGrid_topleft, FGrid_top, FGrid_topright, FGrid_left, FGrid_right, FGrid_downleft, FGrid_down, FGrid_downright)

def Step1(FFloorplan, FOccupiedSeats, FAdjacentItems, FGridWidth, FGridLength):
    # This function returns the seats that become empty,  because they have 4 or more occupied neighboors
    # If a seat is occupied (#) and four or more seats adjacent to it are also occupied, the seat becomes empty.
    # It returns the filled seats that will become empty
    GridTL, GridT, GridTR, GridL, GridR, GridDL, GridD, GridDR = FAdjacentItems

    # situations that make a seat go empty
    # divide the 8 adjacent tiles in two groups: A (=GridTL, GridT, GridTR, GridL) and B (GridR, GridDL, GridD, GridDR)
    # A = 4 | B = 4
    FStep1a = (FFloorplan & OccupiedSeats ) & ( (GridTL & GridT & GridTR & GridL) | (GridR & GridDL & GridD & GridDR) ) 
    # A >= 3 & B >= 1   
    FStep1b = (FFloorplan & OccupiedSeats ) & ( ((GridTL & GridT) & (GridTR | GridL)) & (GridR | GridDL | GridD | GridDR) ) 
    FStep1c = (FFloorplan & OccupiedSeats ) & ( ((GridTL | GridT) & (GridTR & GridL)) & (GridR | GridDL | GridD | GridDR) ) 
    # A >= 2 & B >= 2
    FStep1d = (FFloorplan & OccupiedSeats ) & ( ((GridTL ^ GridT) & (GridTR ^ GridL)) & ((GridR ^ GridDL) & (GridD ^ GridDR)) ) 
    FStep1e = (FFloorplan & OccupiedSeats ) & ( ((GridTL & GridT) ^ (GridTR & GridL)) & ((GridR ^ GridDL) & (GridD ^ GridDR)) ) 
    FStep1f = (FFloorplan & OccupiedSeats ) & ( ((GridTL ^ GridT) & (GridTR ^ GridL)) & ((GridR & GridDL) ^ (GridD & GridDR)) ) 
    FStep1g = (FFloorplan & OccupiedSeats ) & ( ((GridTL & GridT) ^ (GridTR & GridL)) & ((GridR & GridDL) ^ (GridD & GridDR)) ) 
    # A >= 1 & B >= 3
    FStep1h = (FFloorplan & OccupiedSeats ) & ( (GridTL | GridT | GridTR | GridL) & ( (GridR & GridDL) & (GridD | GridDR) ) )  
    FStep1i = (FFloorplan & OccupiedSeats ) & ( (GridTL | GridT | GridTR | GridL) & ( (GridR | GridDL) & (GridD & GridDR) ) )  

    FStep1 = (FFloorplan & OccupiedSeats ) & (FStep1a | FStep1b | FStep1c | FStep1d | FStep1e | FStep1f | FStep1g | FStep1h | FStep1i)

    return (FStep1)

def BinMask(FBase, FGridWidth, FGridLength):
    # chop of the bits that are longer than the FGridLength
    # we use binary masking for this
    # working syntax 6^(6&4) means 6 is the string, 4 is the mask i.e. remove the 4 if it exists

    BitLenFBase = int(FBase).bit_length() # determine the length of the input number
    # create the mask 
    Mask = max(0,((2**BitLenFBase)-1) - ((2**FGridLength)-1))
    # PrintBinDec('Mask', Mask, FGridWidth, FGridLength)

    # apply the mask
    return(FBase^(FBase&Mask))

def PrintBinDec (prefix, Fint, FGridWidth, FGridLength):
    GridString = format(Fint, f'0{FGridLength}b') # make the binary string FGridLength positions long with padding zeroes
    GridStringFormatted = ''

    for i in range(len(GridString)): # group the binary by GridWidth
        if i % FGridWidth == 0: GridStringFormatted += ' '
        GridStringFormatted += GridString[i]

    print (prefix.ljust(20), str(Fint).rjust(10), GridStringFormatted)

def PrintGrid (FFloorplan, FOccupiedSeats, FGridWidth, FGridLength):
    #if Debug: PrintBinDec ('\nGrid value', FOccupiedSeats, FGridWidth, FGridLength)
    # convert the FOccupiedSeats to a binary string, reverse it and replace a 1 by a # and a 0 by .
    GridFloorplan = format(FFloorplan, f'0{FGridLength}b')[::-1].replace('1', 'L').replace('0', '.')
    GridOccupiedSeats = format(FOccupiedSeats, f'0{FGridLength}b')[::-1].replace('1', '#').replace('0', '.')
    GridFormatted = ''
    for i in range(len(GridFloorplan)):
        if i % FGridWidth == 0 and i > 0: GridFormatted += '\n'
        # if the seat is occupied, return that character, else use one from the floorplan
        GridFormatted +=  GridOccupiedSeats[i] if GridOccupiedSeats[i] == '#' else GridFloorplan[i]

    print(GridFormatted)

def ClearScreen():
    if name == 'nt': # windows
        _ = system('cls')
    else:     # for mac and linux(here, os.name is 'posix') 
        _ = system('clear')



# If a seat is empty (L) and there are no occupied seats adjacent to it, the seat becomes occupied.
# If a seat is occupied (#) and four or more seats adjacent to it are also occupied, the seat becomes empty.
# Otherwise, the seat's state does not change.

# Turn data into datastream (and include a padding of empty seats)
# stream 0 = possible seats (1's)
# stream 1 = occupied seats to the top-left of the current seat, by shifting the datastream 

# 1 2 3        A B C    0 0 0
# 4 5 6        D E F    0 A B
# 7 8 9        G H I    0 G H
# 00000 01230 04560 07890 00000 basic stream
# 00000 00000 00120 00780 00000 shifted stream

print ('starting...')

# the solution is based on bitwise operators
# https://www.tutorialspoint.com/python/bitwise_operators_example.htm
# kind of cool, I think :-)

# first read our input and convert it to a binary string and print the biodiversity rating
# which is the decimal representation of the grid

MultiF = 1
InputFile = data
GridWidth = MultiF*len(InputFile[0])
InputFile = ''.join(InputFile)
InputFile = InputFile[::-1].replace('L', '1').replace('.', '0')
GridLength = MultiF*MultiF*len(InputFile)
GridHeight = GridLength // GridWidth

Floorplan = int(InputFile, 2) # 2 is the base
# Floorplan = 1106406491103142594639952740205
#    return (FGrid_topleft, FGrid_top, FGrid_topright, FGrid_left, FGrid_right, FGrid_downleft, FGrid_down, FGrid_downright)

OccupiedSeats = 0 # initial situation
if Debug:
    print(f"\n*****************Initial situation")
    PrintGrid(Floorplan, OccupiedSeats, GridWidth, GridLength)
i = 0
prevOccupiedSeats = -1
while True and i < 10000:
    sleep(1/6)
    ClearScreen()
    i += 1
    print(f"\n*****************Run number {i}")
    # If a seat is empty (L) and there are no occupied seats adjacent to it, the seat becomes occupied.
    GridTL, GridT, GridTR, GridL, GridR, GridDL, GridD, GridDR = AdjacentItems(Floorplan, OccupiedSeats, GridWidth, GridLength)

    # If a seat is occupied (#) and four or more seats adjacent to it are also occupied, the seat becomes empty.
    # Remove the seats that will become empty from the occupiedseats
    OccupiedSeats = OccupiedSeats ^ Step1(Floorplan, OccupiedSeats, (GridTL, GridT, GridTR, GridL, GridR, GridDL, GridD, GridDR ), GridWidth, GridLength)

    # Fill the seats where all adjacents seats are zero; this is the new OccupiedSeats
    # in words: new occupiedseats must be already occupied seat OR they must be in the floorplan AND there should not be any occupied adjacent seats
    OccupiedSeats = OccupiedSeats | (Floorplan & (Floorplan ^ (GridTL | GridT | GridTR | GridL | GridR | GridDL | GridD | GridDR) ) )
    if (OccupiedSeats == prevOccupiedSeats): break
    if Debug: PrintGrid(Floorplan, OccupiedSeats, GridWidth, GridLength)
    prevOccupiedSeats = OccupiedSeats


# if we compare the seating with the 


answer = format(OccupiedSeats, f'0{GridLength}b')[::-1].replace('1', '#').count('#')
if Debug:
    PrintGrid(Floorplan, OccupiedSeats, GridWidth, GridLength)

print (f'The answer to part 1 is: {answer} after {i} runs')
