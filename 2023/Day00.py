import argparse

class sampleClass:
    def __init__(self) -> None:
        self.content = list()
        pass
    def build(self, fContent):
        self.content = fContent
        for thisLine in fContent:
            pass
        return self

def main(stdscr):
    with open(fName, 'r+') as f:
        fContent = f.read().splitlines()
    

    myMap = sampleClass()
    result = myMap.build(fContent=fContent)

    message = f'The answer to part 1 is (sample should be x, answer should be x): {result}'
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

day = '01'
fName = f'2023/input/{day}_sample.txt'
if args.production: fName = f'2023/input/{day}.txt'

debug = args.verbose
draw = args.draw

main(None)