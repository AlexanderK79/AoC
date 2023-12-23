import argparse
import re
import math
class engineSchema:
    def __init__(self) -> None:
        self.numbers = dict()
        self.symbols = dict()
        self.validCos = list()
        pass
    def build(self, fContent):
        linenum = 0
        for line in fContent:
            linenum += 1
            regex = re.finditer('(\d+)', line.strip() )
            for match in regex:
                self.numbers['_'.join((str(match.start()), str(linenum)))] = ({'number': match.group(), 'coords': set(co.listCoords(None, match.start(), linenum, match.end(), linenum+1)), 'value': int(match.group())})
            regex = re.finditer('[^\d\.]', line.strip() )
            for match in regex:
                self.symbols['_'.join((str(match.start()), str(linenum)))] = ({'symbol': match.group(), 'coord': (match.start(), linenum), 'adj_coords': co.listCoords(None, match.start()-1, linenum - 1, match.end()+1, linenum+2)})
            pass
        # add every valid coordinate
        [self.validCos.extend(co['adj_coords']) for co in self.symbols.values()]
        self.validCos = set(self.validCos)
        # check if the number is an engine part, by checking if it is adjacent to a symbol
        for part in self.numbers.values():
             if self.validCos.intersection(part['coords']):
                  part['validNumber'] = True
             else:
                  part['validNumber'] = False
        
        # check all * symbols to see if it has exactly two parts connected
        for gear in [i for i in self.symbols.values() if i['symbol'] == '*'] :
            myParts = [i for i in self.numbers.values() if set(gear['adj_coords']).intersection(i['coords'])]
            if len(myParts) == 2:
                gear['ratio'] = math.prod([i['value'] for i in myParts])
            pass
        
        return self
    def sumValidParts(self):
         return sum([part['value'] for part in self.numbers.values() if part['validNumber'] == True])
    def sumGearRatios(self):
         return sum([gear['ratio'] for gear in self.symbols.values() if gear['symbol'] == '*' and gear.get('ratio') ])

class co:
        def __init__(self, fX, fY) -> None:
             return (fX, fY)
             pass
        def listCoords(self, fX, fY, fXrange, fYrange):
            thisListCoords = list()
            for y in range(fY, fYrange):
                  for x in range(fX, fXrange):
                       thisListCoords.append((x, y))
                       pass
            return thisListCoords

def main(stdscr):
    with open(fName, 'r+') as f:
        fContent = f.read().splitlines()
    
    mySchema = engineSchema()
    result = mySchema.build(fContent=fContent)
    result = mySchema.sumValidParts()

    message = f'The answer to part 1 is (sample should be 4361, answer should be 556367): {result}'
    print(message)
    print(20 * '*')

    result = mySchema.sumGearRatios()

    message = f'The answer to part 2 is (sample should be 467835, answer should be 89471771): {result}'
    print(message)
    pass


# globals
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose"   , action="store_true", default=False, help="Add this to enable verbose output")
parser.add_argument("-d", "--draw"      , action="store_true", default=False, help="Add this to enable drawing")
parser.add_argument("-i", "--drawinterval", type=int, default=1, help="Add the value in ms for drawing interval")
parser.add_argument("-p", "--production", action="store_true", default=False, help="Add this to try the puzzle input")
args = parser.parse_args()

day = '03'
fName = f'2023/input/{day}_sample.txt'
if args.production: fName = f'2023/input/{day}.txt'

debug = args.verbose
draw = args.draw

main(None)