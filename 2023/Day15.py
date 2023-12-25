import argparse

class HHA:
    def __init__(self) -> None:
        self.content = list()
        self.sequence = list()
        self.boxes = [[[None, None]] for i in range(256)]
        pass
    def build(self, fContent):
        self.content = fContent
        for thisLine in fContent:
            self.sequence = [{'id':s, 'label': '','operation': s[-1], 'hash': 0, 'box': 0} for s in thisLine.strip().split(',')]
        pass
        return self
    def storeHash(self):
        for s in self.sequence:
            thisSeq    = s['id']
            thisLabel  = s['label']
            thisHash   = s['hash']
            thisBox    = s['box']
            thisBoxFound = False
            for c in thisSeq:
                thisHash += ord(c)
                thisHash *= 17
                thisHash %= 256
                thisBoxFound = True if c in ('-', '=') else thisBoxFound
                if thisBoxFound == False:
                    thisLabel += c
                    thisBox += ord(c)
                    thisBox *= 17
                    thisBox %= 256
                else:
                    pass
            s['label'] = thisLabel
            s['hash']  = thisHash
            s['box']   = thisBox
            pass
        self.hash = sum([s['hash'] for s in self.sequence])
        return self.hash
        pass

    def processBoxes(self):
        for s in self.sequence:
            op, box = s['operation'], int(s['box'])
            thisBox = self.boxes[box]
            if op == '-':
                [thisBox.remove(b) for b in thisBox if b[0] == s['label']]
            else:
                if s['label'] in [l[0] for l in thisBox if l[0] == s['label']]:
                    thisIndex = min([i for i,l in enumerate(thisBox) if l[0] == s['label']])
                    thisBox[thisIndex][1] = int(op)
                else:
                    thisBox.append([s['label'], int(op)])
        pass
        sumL = 0
        for (ib,b) in [b for b in enumerate(self.boxes)]:
            for (i,l) in enumerate(b):
                if i == 0: continue
                product = (ib+1) * i * l[1]
                sumL += product
                pass
        return sumL

def main(stdscr):
    with open(fName, 'r+') as f:
        fContent = f.read().splitlines()
    

    myHHA = HHA()
    result = myHHA.build(fContent=fContent)
    result = myHHA.storeHash()

    message = f'The answer to part 1 is (sample should be 1320, answer should be 506437): {result}'
    print(message)

    print(20 * '*')

    result = myHHA.processBoxes()

    message = f'The answer to part 2 is (sample should be 145, answer should be 288521): {result}'
    print(message)
    pass


# globals
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose"   , action="store_true", default=False, help="Add this to enable verbose output")
parser.add_argument("-d", "--draw"      , action="store_true", default=False, help="Add this to enable drawing")
parser.add_argument("-i", "--drawinterval", type=int, default=1, help="Add the value in ms for drawing interval")
parser.add_argument("-p", "--production", action="store_true", default=False, help="Add this to try the puzzle input")
args = parser.parse_args()

day = '15'
fName = f'2023/input/{day}_sample.txt'
if args.production: fName = f'2023/input/{day}.txt'

debug = args.verbose
draw = args.draw

main(None)