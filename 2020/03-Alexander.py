# read the text file
# the width of the text file is the mod for the x coord
# the top-left coord is 1, 1

def travelSlope(inputDict, startX, startY, moveX, moveY, maxX, maxY):
    print ('Travelling from ', startX, ', ', startY)
    d = inputDict
    curX, curY = startX, startY
    iMod, iMaxY = maxX, maxY
    curTrees = 0

    while curY <= iMaxY:
        if d[curX, curY] == '#':
            print ('Tree at ', curX, ',', curY)
            curTrees += 1
        # move next line and 3 to the right
        curY += moveY
        curX = (curX + moveX) % iMod
    print ('We met ', curTrees , ' trees')
    return curTrees


# read the text-file into a dict 
d = {}
iLineNumber = 0
with open("03-Alexander-input.txt") as f:
    for line in f:
        iCharNumber = 0
        for char in line.strip():
            (y, x, val) = iLineNumber, iCharNumber, char
            d[int(x), int(y)] = val
            iCharNumber += 1
        iLineNumber += 1

iMod = iCharNumber
iMaxY = iLineNumber-1

result = 1
for move in ((1,1), (3,1), (5,1), (7,1), (1,2)):
    result *= travelSlope(d, 0, 0, move[0], move[1], iMod, iMaxY)

print (result)
print (d)