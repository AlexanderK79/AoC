import argparse
import re

class pileOfScratchCards:
    def __init__(self) -> None:
        self.cards = dict()
        pass
    def build(self, fContent, fNumOfWinningNumbers):
        linenum = 0
        fNumOfWinningNumbers += 1
        for line in fContent:
            linenum += 1
            regex = re.finditer('(\d+ *)', line.strip() )
            myMatches = [m for m in regex]
            thisCard = int(myMatches[0].group()) 
            self.cards[thisCard] = { 
                'id': thisCard
                , 'count': 1
                , 'winning': set([int(b.group().strip()) for b in myMatches[1:fNumOfWinningNumbers]])
                , 'mynumbers': set([int(b.group().strip()) for b in myMatches[fNumOfWinningNumbers::]])
                }
            self.cards[thisCard]['mywinningnumbers'] = self.cards[thisCard]['winning'].intersection(self.cards[thisCard]['mynumbers'])
            self.cards[thisCard]['value'] = 0 if len(self.cards[thisCard]['mywinningnumbers']) == 0 else 2 ** (len(self.cards[thisCard]['mywinningnumbers'])-1)
            pass
        return self
    def sumPart1(self):
        return sum([c['value'] for c in self.cards.values() if c['value'] > 0])
    
    def processPart2(self):
        # add a counter for each card
        for thisCard in self.cards.values():
            thisId = thisCard['id']
            for i in range(thisId+1, thisId+1+len(self.cards[thisId]['mywinningnumbers'])):
                self.cards[i]['count'] += self.cards[thisId]['count']
        pass
    def countCards(self):
        return sum([c['count'] for c in self.cards.values()])

def main(stdscr):
    with open(fName, 'r+') as f:
        fContent = f.read().splitlines()

    myPile = pileOfScratchCards()
    myNumOfWinningNumbers = 10 if args.production else 5
    result = myPile.build(fContent=fContent, fNumOfWinningNumbers=myNumOfWinningNumbers)
    result = myPile.sumPart1()

    message = f'The answer to part 1 is (sample should be 13, answer should be 20107): {result}'
    print(message)

    print(20 * '*')

    result = myPile.processPart2()
    result = myPile.countCards()

    message = f'The answer to part 2 is (sample should be 30, answer should be 8172507): {result}'
    print(message)


# globals
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose"   , action="store_true", default=False, help="Add this to enable verbose output")
parser.add_argument("-d", "--draw"      , action="store_true", default=False, help="Add this to enable drawing")
parser.add_argument("-i", "--drawinterval", type=int, default=1, help="Add the value in ms for drawing interval")
parser.add_argument("-p", "--production", action="store_true", default=False, help="Add this to try the puzzle input")
args = parser.parse_args()

day = '04'
fName = f'2023/input/{day}_sample.txt'
if args.production: fName = f'2023/input/{day}.txt'

debug = args.verbose
draw = args.draw

main(None)