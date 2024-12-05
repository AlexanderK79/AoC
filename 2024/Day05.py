import argparse
import re

def processUpdate(fReport):
    pass

def main(stdscr):
    with open(fName, 'r+') as f:
        fContent = f.read().splitlines()

    myRules = dict()
    myUpdates = dict()


    for i, line in enumerate(fContent[:fContent.index('')]):
        #process rules
        (x, y) = map(int, line.split('|'))
        thisX = myRules.setdefault(x, {'page': x, 'before': list(), 'after': list()})
        thisY = myRules.setdefault(y, {'page': y, 'before': list(), 'after': list()})
        thisX['before'].append(y) if y not in thisX['before'] else None
        thisY['after'].append(x) if x not in thisY['before'] else None
    del thisX, thisY, x, y
    pass

    for i, line in enumerate(fContent[1+fContent.index(''):]):
        #process updates
        thisUpdate = myUpdates.setdefault(i, {'update': list(map(int, line.split(','))), 'valid': True})['update']
        for j, pagenum in enumerate(thisUpdate):
            if set(myRules[pagenum]['after']).intersection(thisUpdate[j+1:]):
                myUpdates[i]['valid'] = False
                break
    del i, j, line
    pass

    result = sum([r['update'][len(r['update'])//2] for r in myUpdates.values() if r['valid']])
    message = f'The answer to part 1 is (sample should be 143, answer should be 5713): {result}\n'
    print(message)

    # fix ordering
    for thisUpdate in [r for r in myUpdates.values() if not r['valid']]:
        thisUpdate.setdefault('validUpdate', [p for p in thisUpdate['update']])
        while not thisUpdate['valid']:
            for j, pagenum in enumerate(thisUpdate['validUpdate']):
                if set(myRules[pagenum]['after']).intersection(thisUpdate['validUpdate'][j+1:]):
                    # not OK, move the page one to the right in the list and try again
                    thisUpdate['validUpdate'].append(pagenum)
                    thisUpdate['validUpdate'].pop(j)
                    break
            if j == len(thisUpdate['update'])-1:
                # we made it to the end of the for loop
                thisUpdate['valid'] = True
        pass

    result = sum([r['validUpdate'][len(r['validUpdate'])//2] for r in myUpdates.values() if r.get('validUpdate')])
    message = f'The answer to part 2 is (sample should be 123, answer should be 5180): {result}\n'
    print(message)

    pass


# globals
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose"   , action="store_true", default=False, help="Add this to enable verbose output")
parser.add_argument("-p", "--production", action="store_true", default=False, help="Add this to try the puzzle input")
args = parser.parse_args()

day = '05'
fName = f'2024/input/{day}_sample.txt'
if args.production: fName = f'2024/input/{day}.txt'

debug = args.verbose

main(None)