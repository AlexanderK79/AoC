import argparse
import re

class almanac:
    def __init__(self) -> None:
        self.mappings = dict()
        self.mapping_index = dict()
        pass
    def build(self, fContent):
        self.content = fContent
        for thisMap in '\n'.join(fContent[2::]).split('\n\n'):
            thisMap = thisMap.split('\n')
            thisMapType = thisMap[0].split(' map:')[0]
            # seed number 98 corresponds to soil number 50
            self.mappings[thisMapType] = mapping(thisMapType, thisMap)
            self.mapping_index[self.mappings[thisMapType].source] = self.mappings[thisMapType]
            pass
        pass

    def find_location(self, fType, fItem):
        myType, myItem = fType, fItem
        while self.mapping_index.get(myType):
            myItem = self.mapping_index[myType].getVal(myItem)
            myType = self.mapping_index[myType].destination
        return myItem

    def find_location_part2(self, fType, fSeedRange):
        myType = fType
        mySeedRanges = list()
        mySeedRanges.append(fSeedRange)
        while self.mapping_index.get(myType):
            mySeedRanges = self.mapping_index[myType].getValRange(mySeedRanges)
            myType = self.mapping_index[myType].destination
        return mySeedRanges

        return self

class mapping:
    def __init__(self, fType, fContent) -> None:
        self.type = fType
        self.content = fContent
        self.source, self.destination = fType.split('-to-')
        self.rules = list() # of dicts
        for thisLine in fContent[1::]:
            thisLine = [int(j) for j in thisLine.strip().split(' ')]
            thisSource, thisDest, thisRange = thisLine
            self.rules.append({'lower': thisDest, 'upper': thisDest + thisRange - 1, 'returnOffset': thisSource - thisDest})
            pass
    def getVal(self, fItem):
        result = [i for i in self.rules if i['lower'] <= int(fItem) <= i['upper']]
        return  int(fItem) + result[0]['returnOffset'] if result else fItem
    def getValRange(self, fSeedRange):
        # returns the lowest and highest number for each block per rule
        result = list()
        for thisRange in fSeedRange:
            blockStart, blockEnd = thisRange
            self.rules = sorted([r for r in self.rules], key=lambda item:item.get("lower"))
            for rule in self.rules:
                if blockEnd < rule['lower'] or blockStart > rule['upper'] or blockStart == blockEnd:
                    continue # no need to process this rule
                if blockStart < rule['lower'] and blockEnd >= rule['lower']: 
                    result.append(tuple((blockStart, rule['lower']-1))) # append a block from the start until the lower limit of this rule
                    blockStart = rule['lower'] # set the blockStart at the lower limit
                if rule['lower'] <= blockStart and blockEnd <= rule['upper']:
                    result.append(tuple((blockStart, blockEnd))) # this block falls entirely within the limits of this rule
                    blockStart = blockEnd  # reached the end of this block
                if rule['lower'] <= blockStart <= rule['upper'] and blockEnd <= rule['upper'] and blockStart < blockEnd:
                    result.append(tuple((blockStart, blockEnd)))
                    blockStart = blockEnd # reached the end of this block
                if rule['lower'] <= blockStart <= rule['upper'] and blockEnd > rule['upper']:
                    result.append(tuple((blockStart, rule['upper'])))
                    blockStart = rule['upper'] + 1
            # after processing all rules
            if blockStart < blockEnd:
                result.append(tuple((blockStart, blockEnd)))
        result
        result = [tuple((self.getVal(r[0]), self.getVal(r[1]))) for r in result]
        return result

def main(stdscr):
    with open(fName, 'r+') as f:
        fContent = f.read().splitlines()
    
    mySeeds = [int(i) for i in fContent[0].split(':')[1].strip().split(' ')]
    myAlmanac = almanac()
    result = myAlmanac.build(fContent=fContent)
    result = str(min([int(myAlmanac.find_location('seed', i)) for i in mySeeds]))

    message = f'The answer to part 1 is (sample should be 35, answer should be 1181555926, 22675169 is too low): {result}'
    print(message)

    print(20 * '*')

    mySeeds = [int(i) for i in fContent[0].split(':')[1].strip().split(' ')]
    thisResult = list()
    for i in range(0, len(mySeeds), 2):
        thisResult.append(myAlmanac.find_location_part2('seed', tuple((mySeeds[i], mySeeds[i] + mySeeds[i+1]-1))))
        pass
    result = min(min([min(i) for i in thisResult]))

    message = f'The answer to part 2 is (sample should be 46, answer should be 37806486, 100644325 is too high): {result}'
    print(message)
    pass

# globals
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose"   , action="store_true", default=False, help="Add this to enable verbose output")
parser.add_argument("-d", "--draw"      , action="store_true", default=False, help="Add this to enable drawing")
parser.add_argument("-i", "--drawinterval", type=int, default=1, help="Add the value in ms for drawing interval")
parser.add_argument("-p", "--production", action="store_true", default=False, help="Add this to try the puzzle input")
args = parser.parse_args()

day = '05'
fName = f'2023/input/{day}_sample.txt'
if args.production: fName = f'2023/input/{day}.txt'

debug = args.verbose
draw = args.draw

main(None)