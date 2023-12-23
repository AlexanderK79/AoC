import argparse

class oasis:
    def __init__(self) -> None:
        self.input = list()
        self.source = list()
        self.result = list()
        pass
    def build(self, fContent):
        self.source = fContent
        for thisLine in fContent:
            self.input.append(list(map(int, thisLine.split(' '))))
            pass
    def predictSeq(self):
        for thisSet in self.input:
            mySet = [list(thisSet)]
            i = 0
            while set(thisSet) != set([0]):
                # for i in range(0,len(thisSet)-1):
                thisSet = [thisSet[i+1] - thisSet[i] for i in range(0,len(thisSet)-1)]
                mySet.append(thisSet)
                i += 1
                pass
            # now adjust the set
            for i in range(len(mySet)-2, -1, -1):
                mySet[i].append(mySet[i][-1] + mySet[i+1][-1])
                pass
            self.result.append(mySet)
        pass

    def predictPrevSeq(self):
        self.result = list()
        for thisSet in self.input:
            mySet = [list(thisSet)]
            i = 0
            while set(thisSet) != set([0]):
                # for i in range(0,len(thisSet)-1):
                thisSet = [thisSet[i+1] - thisSet[i] for i in range(0,len(thisSet)-1)]
                mySet.append(thisSet)
                i += 1
                pass
            # now adjust the set at the beginning
            for i in range(len(mySet)-2, -1, -1):
                mySet[i].insert(0, mySet[i][0] - mySet[i+1][0])
                pass
            self.result.append(mySet)
        pass

        return self

def main(stdscr):
    with open(fName, 'r+') as f:
        fContent = f.read().splitlines()
    

    myOasis = oasis()
    result = myOasis.build(fContent=fContent)
    result = myOasis.predictSeq()
    result = sum([i[0][-1] for i in myOasis.result])

    message = f'The answer to part 1 is (sample should be 114, answer should be x): {result}'
    print(message)

    print(20 * '*')

    result = myOasis.predictPrevSeq()
    result = sum([i[0][0] for i in myOasis.result])

    message = f'The answer to part 2 is (sample should be 2, answer should be x): {result}'
    print(message)
    pass


# globals
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose"   , action="store_true", default=False, help="Add this to enable verbose output")
parser.add_argument("-d", "--draw"      , action="store_true", default=False, help="Add this to enable drawing")
parser.add_argument("-i", "--drawinterval", type=int, default=1, help="Add the value in ms for drawing interval")
parser.add_argument("-p", "--production", action="store_true", default=False, help="Add this to try the puzzle input")
args = parser.parse_args()

day = '09'
fName = f'2023/input/{day}_sample.txt'
if args.production: fName = f'2023/input/{day}.txt'

debug = args.verbose
draw = args.draw

main(None)