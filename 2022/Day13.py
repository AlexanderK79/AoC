import argparse
from curses import wrapper
import json

class Message:
    def __init__(self) -> None:
        self.valid_indices = [] # list of valid Pairs
        self.pairs = []
        self.packets = []
        self.packets += [[[2]], [[6]]]
        self.ordered_packets = [None]
        pass
    def parse(self, fContent):
        i = 1
        for p in fContent.split('\n\n'):
            self.pairs.append(Pair(self, i, p.split('\n')))
            i+=1
        pass
    def validate(self):
        for p in self.pairs:
            p.validate()
        pass
    def orderpacket(self):
        # set the first packet
        self.ordered_packets[0] = self.packets[0] # place the first packet
        for thisPacket in (self.packets[1::]): # start from the second packet
            valid = None
            for placedPacket in self.ordered_packets[::-1]: #move backwards through list until we hit invalid
                valid = self.pairs[0].compareLists(thisPacket, placedPacket)
                if not valid:
                    break
            if valid:
                self.ordered_packets.insert(self.ordered_packets.index(placedPacket), thisPacket)
            else:
                self.ordered_packets.insert(1+self.ordered_packets.index(placedPacket), thisPacket) #we hit false put it just after the placedPacket
            pass

class Pair:
    def __init__(self, fParent, fIndex, fItems) -> None:
        self.parent = fParent
        self.index = fIndex
        self.left = json.loads(fItems[0])
        self.right = json.loads(fItems[1])
        self.parent.packets += [self.left, self.right]
        pass
    def validate(self):
        i = 0
        valid = None
        while valid is None:
            L = self.left[i] if i < len(self.left) else None 
            R = self.right[i] if i < len(self.right) else None 
            valid = self.compareLists(L, R)
            i+=1
            del L, R
            pass
        self.valid = valid
        if valid: self.parent.valid_indices.append(self)
        pass

    def compareLists(self, L, R):
        i, valid = 0, None
        while valid is None and ( ( type(L) in (int, type(None)) or type(R) in (int, type(None)) or i < len(L) or i < len(R) ) ):
            # compare type and recurse
            if ( type(L) in (int, list) ) and ( type(R) in (int, list) ) and type(L) != type(R):
                if type(L) == int: L = list([L])
                elif type(L) == type(None): L = list([None])
                if type(R) == int: R = list([R])
                elif type(R) == type(None): R = list([None])
                valid = self.compareLists(L, R)
            elif type(L) == type(R) == list:
                if len(L) == i: L.append(None)
                if len(R) == i: R.append(None)
                valid = self.compareLists(L[i], R[i])
            # compare int
            elif type(L) == type(R) == int:
                if L < R: valid = True
                elif L > R: valid = False
                return valid
            # compare run out of list items
            elif type(L) == type(None) or type(R) == type(None):
                if type(L) == type(None): valid = True
                elif type(R) == type(None): valid = False
                else:
                    pass
            if type(L) == list: L = list(filter(lambda item: item is not None, L))
            if type(R) == list: R = list(filter(lambda item: item is not None, R))
            i+=1
        return valid
        pass

def main(stdscr):
    myMessage = Message()
    with open(fName, 'r+') as f:
        myMessage.parse(f.read())

    #validate the pairs
    myMessage.validate()

    result = sum([p.index for p in myMessage.valid_indices])

    message = f'The answer to part 1 is (sample should be 13, answer should be x): {result}'
    print(message)

    myMessage.orderpacket()

    result = (1+myMessage.ordered_packets.index([[2]])) * (1+myMessage.ordered_packets.index([[6]]))

    # wrong 26800 too high
    message = f'The answer to part 2 is (sample should be 140, answer should be x): {result}'
    print(message)


# globals
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose"   , action="store_true", default=False, help="Add this to enable verbose output")
parser.add_argument("-d", "--draw"      , action="store_true", default=False, help="Add this to enable drawing")
parser.add_argument("-i", "--drawinterval", type=int, default=1, help="Add the value in ms for drawing interval")
parser.add_argument("-p", "--production", action="store_true", default=False, help="Add this to try the puzzle input")
args = parser.parse_args()

day = '13'
fName = f'2022/input/{day}_sample.txt'
if args.production: fName = f'2022/input/{day}.txt'

debug = args.verbose
draw = args.draw

""" stdscr = curses.initscr()
curses.start_color()
curses.use_default_colors()
wrapper(main)
 """
main(None)