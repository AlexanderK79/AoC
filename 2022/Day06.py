import argparse
import re

class Buffer:
    def __init__(self, fMessage):
        for c in (4, 14):
            i = 0
            while len(set(list(fMessage)[i:i+c])) < c: 
                i+=1
                if c == 4: self.StartOfPacketMarker = i + c
                if c == 14: self.StartOfMessageMarker = i + c
        pass

def main(stdscr):
    with open(fName, 'r+') as f:
        data = list(map(Buffer, list(f.read().splitlines())))

    for i in data:    
        result = i.StartOfPacketMarker
        message = f'The answer to part 1 is (sample should be 7, answer should be 1855): {result}'
        print(message)

    print(20 * '*')
    for i in data:    
        result = i.StartOfMessageMarker
        message = f'The answer to part 2 is (sample should be 7, answer should be 1855): {result}'
        print(message)


# globals
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose"   , action="store_true", default=False, help="Add this to enable verbose output")
parser.add_argument("-d", "--draw"      , action="store_true", default=False, help="Add this to enable drawing")
parser.add_argument("-i", "--drawinterval", type=int, default=1, help="Add the value in ms for drawing interval")
parser.add_argument("-p", "--production", action="store_true", default=False, help="Add this to try the puzzle input")
args = parser.parse_args()

day = '06'
fName = f'2022/input/{day}_sample.txt'
if args.production: fName = f'2022/input/{day}.txt'

debug = args.verbose
draw = args.draw

main(None)