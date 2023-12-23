import argparse
import re

class keyPair:
    def __init__(self, fLine):
        subjectNumber = 7
        self.pubKey = int(fLine)
        self.pubKeyList = list(map(self.executeLoop, 16 * [subjectNumber], range(0,16)))
        #self.loopSize = self.pubKeyList.index(self.pubKey)
        """ i = 0
        while self.executeLoop(subjectNumber, i) != self.pubKey:
            i+=1
            if i % 10 == 0:
                pass """
        self.loopSize = self.findLoopSize(subjectNumber)
    def executeLoop(self, fSubjectNumber, numLoops):
        # The handshake used by the card and the door involves an operation that transforms a subject number. 
        # To transform a subject number, start with the value 1. Then, a number of times called the loop size, 
        # perform the following steps:
        value = 1
        i = 1
        while i <= numLoops:
            # Set the value to itself multiplied by the subject number.
            # Set the value to the remainder after dividing the value by 20201227.
            value = value * fSubjectNumber % 20201227
            i+=1
        return value
    def findLoopSize(self, fSubjectNumber):
        value, i = 1, 0
        while value != self.pubKey:
            value = value * fSubjectNumber %20201227
            i+=1
        return i
            
            # The card always uses a specific, secret loop size when it transforms a subject number. 
            # The door always uses a different, secret loop size.
            # For example, suppose you know that the card's public key is 5764801. 
            # With a little trial and error, you can work out that the card's loop size must be 8, 
            # because transforming the initial subject number of 7 with a loop size of 8 produces 5764801.
        



def main(stdscr):
    with open(fName, 'r+') as f:
        data = list(map(keyPair, f.read().splitlines()))
    result = data[0].executeLoop(data[0].pubKey, data[1].loopSize)
    message = f'The answer to part 1 is (sample should be 14897079, answer should be 11288669): {result}'
    print(message)
     # process groups of three
    #result = len([i.intersection for i in data if len(i.intersection) > 0])
    message = f'The answer to part 2 is (sample should be 4, answer should be 870): {result}'
    print (message) 

# globals
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose"   , action="store_true", default=False, help="Add this to enable verbose output")
parser.add_argument("-d", "--draw"      , action="store_true", default=False, help="Add this to enable drawing")
parser.add_argument("-i", "--drawinterval", type=int, default=1, help="Add the value in ms for drawing interval")
parser.add_argument("-p", "--production", action="store_true", default=False, help="Add this to try the puzzle input")
args = parser.parse_args()

day = '25'
fName = f'2020/input/{day}_sample.txt'
if args.production: fName = f'2020/input/{day}.txt'

debug = args.verbose
draw = args.draw

main(None)