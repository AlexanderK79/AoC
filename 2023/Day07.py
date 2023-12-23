import argparse

class Hands:
    def __init__(self) -> None:
        self.allHands = list()
        self.cardVals = dict()
        self.cardVals = dict(map(lambda i,j : (i,j) , ['2', '3','4','5','6','7','8','9','T','J','Q','K','A'],[2,3,4,5,6,7,8,9,10,11,12,13,14]))
        self.scoreOrder = dict()
        self.scoreOrder = {
            '5'           : 7 # Five of a kind, where all five cards have the same label: AAAAA
            , '4_1'       : 6 # Four of a kind, where four cards have the same label and one card has a different label: AA8AA
            , '3_2'       : 5 # Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
            , '3_1_1'     : 4 # Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
            , '2_2_1'     : 3 # Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
            , '2_1_1_1'   : 2 # One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
            , '1_1_1_1_1' : 1 # High card, where all cards' labels are distinct: 23456
            }
        self.mFactor = 10**14
        self.sFactor = [10**j for j in range(12, -3, -3)]
        pass
    def build(self, fContent):
        self.example = fContent
        for thisLine in fContent:
            self.allHands.append(Hand(self, thisLine.split(' ')[0], thisLine.split(' ')[1]))
        return self
    def calcScore(self):
        thisSorted = sorted(self.allHands, key=lambda item: item.hand.get('total_score'))
        return sum([i*j for i,j in zip(list(range(1, len(self.allHands)+1)), [i.hand.get('bid') for i in thisSorted])])
    def evolve(self):
        [h.evolve() for h in self.allHands]
        return self

class Hand:
    def __init__(self, fParent, fHand, fBid) -> None:
        self.parent = fParent
        self.hand = dict()
        self.hand['handLine'] = fHand
        self.hand['bid'] = int(fBid)
        thisPattern = {i: fHand.count(i) for i in fHand}
        thisHandVals = [self.parent.cardVals[i] for i in fHand]
        self.hand['main_score'] = self.parent.mFactor * self.parent.scoreOrder['_'.join(map(str, sorted(thisPattern.values(), reverse=True)))]
        self.hand['sub_score'] = sum([i * j for i, j in zip(self.parent.sFactor,thisHandVals)])
        self.hand['total_score'] = self.hand['main_score'] + self.hand['sub_score']
        pass
    def evolve(self):
        fHand = self.hand['handLine']
        thisPattern = {i: fHand.count(i) for i in fHand}
        thisHandVals = [self.parent.cardVals[i] for i in fHand]
        if list(thisPattern.keys()) == ['J']:
            pass
        else:
            thisKey = sorted([i for i in thisPattern.items() if i[0] != 'J'], key= lambda item: item[1], reverse=True)[0][0]
            thisPattern[thisKey] += thisPattern.get('J') if thisPattern.get('J') else 0
            thisPattern.pop('J') if thisPattern.get('J') else None
        pass

        self.hand['main_score'] = self.parent.mFactor * self.parent.scoreOrder['_'.join(map(str, sorted(thisPattern.values(), reverse=True)))]
        self.hand['sub_score'] = sum([i * j for i, j in zip(self.parent.sFactor,thisHandVals)])
        self.hand['total_score'] = self.hand['main_score'] + self.hand['sub_score']
        
def main(stdscr):
    with open(fName, 'r+') as f:
        fContent = f.read().splitlines()
    

    myHand = Hands()
    result = myHand.build(fContent=fContent)
    result = myHand.calcScore()

    message = f'The answer to part 1 is (sample should be 6440, answer should be 250347426, 5385 is too low): {result}'
    print(message)

    print(20 * '*')

    myHand.cardVals['J'] = 1 # for compare in weak cards
    # evolve: add the J to the largest stack
    result = myHand.evolve()
    result = myHand.calcScore()

    message = f'The answer to part 2 is (sample should be 5905, answer should be x): {result}'
    print(message)
    pass

# globals
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose"   , action="store_true", default=False, help="Add this to enable verbose output")
parser.add_argument("-d", "--draw"      , action="store_true", default=False, help="Add this to enable drawing")
parser.add_argument("-i", "--drawinterval", type=int, default=1, help="Add the value in ms for drawing interval")
parser.add_argument("-p", "--production", action="store_true", default=False, help="Add this to try the puzzle input")
args = parser.parse_args()

day = '07'
fName = f'2023/input/{day}_sample.txt'
if args.production: fName = f'2023/input/{day}.txt'

debug = args.verbose
draw = args.draw

main(None)