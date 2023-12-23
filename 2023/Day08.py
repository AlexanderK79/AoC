import argparse
import math

class DesertMap:
    def __init__(self) -> None:
        self.directions = list()
        self.nodes = dict()
        pass
    def build(self, fContent):
        self.directions = [i for i in fContent[0]]
        for thisLine in fContent[2::]:
            thisNode, thisDests = thisLine.split(' = ')
            thisDests = thisDests[1:-1].split(', ')
            self.nodes[thisNode] = {'node': thisNode, 'L': thisDests[0], 'R': thisDests[1], 'steps_from': dict()}
            pass
        return self
    def findPath(self, fSource, fDest):
        thisNode = fSource
        thisDirections = self.directions
        i = 0
        while thisNode != fDest:
            while i <= len(thisDirections) and thisNode != fDest:
                i = 0 if i == len(thisDirections) else i
                thisSteps = self.nodes[thisNode]['steps_from'].get(fSource, 0)
                thisNode = self.nodes[thisNode][thisDirections[i]]
                self.nodes[thisNode]['steps_from'][fSource] = thisSteps + 1
                i += 1
                pass
            pass
        return self
    def findGhostPath(self, fSource, fDest):
        thisNodes = [i['node'] for i in self.nodes.values() if i['node'][-1] == fSource[-1]]
        destNodes = [i['node'] for i in self.nodes.values() if i['node'][-1] == fDest[-1]]
        thisDirections = self.directions
        i, thisSteps = 0, 0

        # while len(thisNodes) != len([i for i in thisNodes if i[-1] == fDest[-1]]):
        #     while i <= len(thisDirections) and len(thisNodes) != len([i for i in thisNodes if i[-1] == fDest[-1]]):
        #         i = 0 if i == len(thisDirections) else i
        #         thisNodes = [self.nodes[n][thisDirections[i]] for n in thisNodes]
        #         thisSteps += 1
        #         i += 1
        #         print(thisSteps) if thisSteps % 1000000 == 0 else None
        #     pass
        # pass
        return thisSteps
    def findPattern(self, fSource, fDest):
        thisNodes = [i['node'] for i in self.nodes.values() if i['node'][-1] == fSource[-1]]
        destNodes = [i['node'] for i in self.nodes.values() if i['node'][-1] == fDest[-1]]
        # find the repetition pattern in from 
        thisDirections = self.directions
        i, thisSteps = 0, 0
        result = list()
        for thisNode in thisNodes:
            thisPath = [thisNode]
            while len([i for i in thisPath if i[-1] == 'Z']) < 1:
                pass
                for d in thisDirections:
                    thisNode = self.nodes[thisNode][d]
                    thisPath.append(thisNode)
                    result.append([thisPath[0], thisNode, len(thisPath)-1]) if thisNode[-1] == 'Z' else None
                    pass
        # there is a fixed interval when the Z items are reached (found by manually analyzing the result)
        return math.lcm(*[i[2] for i in result])


def main(stdscr):
    fName = f'2023/input/{day}_sample.txt'
    if args.production: fName = f'2023/input/{day}.txt'

    with open(fName, 'r+') as f:
        fContent = f.read().splitlines()

    myMap = DesertMap()
    result = myMap.build(fContent=fContent)
    result = myMap.findPath('AAA', 'ZZZ')
    result = myMap.nodes['ZZZ']['steps_from']['AAA']

    message = f'The answer to part 1 is (sample should be x, answer should be 21389): {result}'
    print(message)

    print(20 * '*')

    fName = f'2023/input/{day}_sample_part2.txt'
    if args.production: fName = f'2023/input/{day}.txt'
    with open(fName, 'r+') as f:
        fContent = f.read().splitlines()
    myMapP2 = DesertMap()
    result = myMapP2.build(fContent=fContent)
    # result = myMapP2.findGhostPath('..A', '..Z')
    result = myMapP2.findPattern('..A', '..Z')

    message = f'The answer to part 2 is (sample should be 6, answer should be 21083806112641): {result}'
    print(message)
    pass


# globals
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose"   , action="store_true", default=False, help="Add this to enable verbose output")
parser.add_argument("-d", "--draw"      , action="store_true", default=False, help="Add this to enable drawing")
parser.add_argument("-i", "--drawinterval", type=int, default=1, help="Add the value in ms for drawing interval")
parser.add_argument("-p", "--production", action="store_true", default=False, help="Add this to try the puzzle input")
args = parser.parse_args()

day = '08'

debug = args.verbose
draw = args.draw

main(None)