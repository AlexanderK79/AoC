import argparse

def calc(fDesResult: int, fStart: int, fNumbers: tuple, fOpList: list) -> bool:
    if len(fNumbers) == 1: # at the end
        return fDesResult == fStart * fNumbers[0] or fDesResult == fStart + fNumbers[0]
    else:
        return ( calc(fDesResult=fDesResult, fStart=fStart * fNumbers[0], fNumbers=fNumbers[1:], fOpList=fOpList+'*') or
        calc(fDesResult=fDesResult, fStart=fStart + fNumbers[0], fNumbers=fNumbers[1:], fOpList=fOpList+'+') )
    pass

def main(stdscr):
    with open(fName, 'r+') as f:
        fContent = f.read().splitlines()

    myCal = list()
    for line in fContent:
        r, i = line.split(': ')
        r = int(r)
        i = tuple(map(int, i.split(' ')))
        myCal.append([r, i, None])
    del r, i, line, f, stdscr, fContent

    for cal in myCal:
        print('processing cal', cal[:2])
        cal[2] = calc(fDesResult=cal[0], fStart=cal[1][0], fNumbers=tuple(cal[1][1:]), fOpList='')
    pass
    del cal


    result = sum([r[0] for r in myCal if r[2]])
    message = f'The answer to part 1 is (sample should be 3749, answer should be 6392012777720): {result}\n'
    print(message)
    pass


# globals
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose"   , action="store_true", default=False, help="Add this to enable verbose output")
parser.add_argument("-p", "--production", action="store_true", default=False, help="Add this to try the puzzle input")
args = parser.parse_args()

day = '07'
fName = f'2024/input/{day}_sample.txt'
if args.production: fName = f'2024/input/{day}.txt'

debug = args.verbose

main(None)