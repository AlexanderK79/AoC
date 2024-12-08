import argparse
import itertools as it

def main(stdscr):
    with open(fName, 'r+') as f:
        fContent = f.read().splitlines()

    myCal = list()
    for line in fContent:
        r, i = line.split(': ')
        r = int(r)
        i = tuple(map(int, i.split(' ')))
        myCal.append([r, i, [x for x in it.product(('*','+'), repeat=len(i)-1)], list(), dict()])
    del r, i, line, f, stdscr, fContent

    for cal in myCal:
        print('processing cal', cal[:2])
        cal[4] = dict() # dictionary of previous calculations
        for oplist in cal[2]:
            # check if part of this calc is already done
            for j in range(len(oplist)+1):
                r = cal[4].get(oplist[:-j])
                if r is not None:
                    # calculation already done, continue from there
                    # print ('already know', oplist[:-j], '=', r)
                    pass
                else:
                    # calculation does not exist... do it from the start
                    r = cal[1][0]
                    assert(j == 0, 'this should be 0 now')
                    pass
            
            while r < cal[0] and r > 0:
                for i,n in enumerate(cal[1][1:]):
                    match oplist[i]:
                        case '+': r += n
                        case '*': r *= n
                    cal[4][oplist[:i+1]] = r
            # we broke out, now check the result
            if r == cal[0] and i+1 == len(cal[1][1:]):
                cal[3].append(True)
                break
            else:
                cal[3].append(False)
                # remove all entries from oplist that have the same start
                [cal[2].remove(o) for o in cal[2] if o[:i+1] == oplist[:i+1] and o != oplist]
                pass
    pass
    del cal, i, n, r, oplist


    result = sum([r[0] for r in myCal if True in r[3]])
    message = f'The answer to part 1 is (sample should be 3749, answer should be ?): {result}\n'
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