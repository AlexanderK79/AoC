import argparse

class Rucksack:
    def __init__(self, fLine):
        halfP = len(fLine)//2
        self.contents = fLine
        self.comp1 = fLine[:halfP]
        self.comp2 = fLine[halfP:]
        self.intersection = list(set(list(self.comp1)) & set(list(self.comp2)))[0]
        self.intersection_value = charvals[self.intersection]

class TeamOfElves:
    def __init__(self, fData, fI):
        self.badge = list(set(list(fData[fI].contents)) & set(list(fData[fI+1].contents)) & set(list(fData[fI+2].contents)))[0]
        self.badge_value = charvals[self.badge]

def main(stdscr):
    with open(fName, 'r+') as f:
        data = list(map(Rucksack, f.read().splitlines()))
    result = sum([i.intersection_value for i in data])
    message = f'The answer to part 1 is (sample should be 157, answer should be 8202): {result}'
    print(message)
    # process groups of three
    TeamOfElves_all = list(map(TeamOfElves, len(data)//3 * [data], [t for t in range(0, len(data)-1, 3)]))
    result = sum([i.badge_value for i in TeamOfElves_all])
    message = f'The answer to part 2 is (sample should be 70, answer should be 2864): {result}'
    print (message)

# globals
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose"   , action="store_true", default=False, help="Add this to enable verbose output")
parser.add_argument("-d", "--draw"      , action="store_true", default=False, help="Add this to enable drawing")
parser.add_argument("-i", "--drawinterval", type=int, default=1, help="Add the value in ms for drawing interval")
parser.add_argument("-p", "--production", action="store_true", default=False, help="Add this to try the puzzle input")
args = parser.parse_args()

day = '03'
fName = f'2022/input/{day}_sample.txt'
if args.production: fName = f'2022/input/{day}.txt'

debug = args.verbose
draw = args.draw

charvals = dict(zip(list(map(chr, range(65, 91))) + list(map(chr, range(97, 123))), list(range(27,53)) + list(range(1, 27)) ))

main(None)