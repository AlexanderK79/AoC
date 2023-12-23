import argparse
import re

class SectionPair:
    def __init__(self, fLine):
        regex = re.match('(((\d+)-(\d+)),((\d+)-(\d+)))', fLine.strip() )
        if regex is None:
            pass
        else:
            self.sectionsA = list(range(int(regex.groups()[2]),(1+int(regex.groups()[3]))))
            self.sectionsB = list(range(int(regex.groups()[5]),(1+int(regex.groups()[6]))))
            self.intersection = list(set(list(self.sectionsA)) & set(list(self.sectionsB)))


def main(stdscr):
    with open(fName, 'r+') as f:
        data = list(map(SectionPair, f.read().splitlines()))
    result = len([i.intersection for i in data if len(i.intersection) in [len(i.sectionsA), len(i.sectionsB)]])
    message = f'The answer to part 1 is (sample should be 2, answer should be 509): {result}'
    print(message)
     # process groups of three
    result = len([i.intersection for i in data if len(i.intersection) > 0])
    message = f'The answer to part 2 is (sample should be 4, answer should be 870): {result}'
    print (message) 

# globals
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose"   , action="store_true", default=False, help="Add this to enable verbose output")
parser.add_argument("-d", "--draw"      , action="store_true", default=False, help="Add this to enable drawing")
parser.add_argument("-i", "--drawinterval", type=int, default=1, help="Add the value in ms for drawing interval")
parser.add_argument("-p", "--production", action="store_true", default=False, help="Add this to try the puzzle input")
args = parser.parse_args()

day = '04'
fName = f'2022/input/{day}_sample.txt'
if args.production: fName = f'2022/input/{day}.txt'

debug = args.verbose
draw = args.draw

main(None)