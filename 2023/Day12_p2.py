import argparse
import re
import math

class AoCmap:
    def __init__(self) -> None:
        self.content = list()
        self.input = {}
        self.mySolutions = {} # memoization of solutions to reduce calculation time
        pass
    def build(self, fContent):
        self.content = fContent
        for i, thisLine in enumerate(self.content):
            item = thisLine.split(' ')
            self.input[i] = {'string': item[0], 'groups': item[1].split(','), 'solutions_check': [0,0] if args.production else [item[2], item[3]] }


    def multiply(self, fMfactor):
        newContent = []
        for thisLine in self.content:
            newLine = '?'.join(fMfactor* [thisLine.split(' ')[0]]) + ' ' + ','.join(fMfactor * [thisLine.split(' ')[1]])
            newLine += '' if args.production == True else ' ' + ' '.join(thisLine.split(' ')[2:])
            newContent.append(newLine)
        self.build(newContent)
        pass

    def calcNumSolutions(self):
        for tV in self.input.values():
            tStr, tGrps, tChk = tV.values()
            # ? can be a . or a #
            # a group is always surrounded by a . or a ?
            # remove double '.' from the string
            tStr = re.sub('\.+', '.', tStr)
            tStr = re.sub('^\.|\.$', '', tStr)
            tGrps = tuple(map(int, tGrps))
            tChk = tuple(map(int, tChk))
            thisResult_all = []
            for i, tGrp in enumerate(tGrps):
                fpp = sum(tGrps[:i])+len(tGrps[:i]) # first possible position for this group
                if fpp>0 and tStr[fpp-1] == '#': fpp += 1
                lpp = len(tStr) - sum(tGrps[i+1:])-len(tGrps[i+1:]) # last possible position for this group
                tStr2Chk = tStr[fpp:lpp]
                del fpp, lpp
                for tStrGrp in tStr2Chk.split('.'):
                    if len(tStrGrp) == 0: continue
                    thisResult = self.mySolutions.get((tStrGrp, tGrp), None)
                    if thisResult == None:
                        thisResult = self.calcNumPerGroup((tStrGrp, tGrp))
                    thisResult_all.append(thisResult)
                    pass
            thisResult = math.prod([i for i in thisResult_all if i>0])
            thisResult = 1 + sum([i for i in thisResult_all if i>1])
            tChk = tChk[0] if reps == 1 else tChk[1]
            print(tStr, tGrps, tChk, thisResult, thisResult_all)
            if thisResult != tChk:
                pass
            del thisResult, thisResult_all

    def calcNumPerGroup(self, fInput):
        fStr, fGrp = fInput
        # fStr = re.sub('^\.|\.$', '', fStr)
        assert fStr.count('.') == 0 # there should not be any . characters
        if len(fStr) == fGrp and fStr.count('.') == 0:
            fResult = 1
        if len(fStr) < fGrp or fStr.count('#') > fGrp :
            fResult = 0
        elif fStr.count('#') == fGrp:
            fResult = 1
        elif fStr.count('?') == fGrp and fStr.count('#') == 0:
            fResult = 1
        elif fStr.count('?') + fStr.count('#') == fGrp:
            fResult = 1
        elif fStr.count('?') + fStr.count('#') == fGrp:
            fResult = 1
        elif fStr.count('?') == len(fStr):
            fResult = 1 + len(fStr) - fGrp
        elif fStr.count('?') + fStr.count('#') > fGrp:
            # more possibilities, but how many
            # a # limits the number of possibilities ('???#', 3 has only one solution)
            # ('??#?', 2 has two solutions)
            # ('??#?', 3 has two solutions)
            # ('??#??', 2 has two solutions)
            # ('??#??', 3 has three solutions); min (fstr.index('#')
            # ('?????', 3 has three solutions; len(fStr) - fGrp + 1
            # ('????#??', 3 has three solutions); min (fStr.index('#')
            # the number of possibilities is determined by the minimum distance from the outer # to the edge
            posB = len(fStr) - fStr[::-1].index('#') - fGrp
            posE = fStr.index('#') + fGrp
            fResult = 1 + posE - posB -fGrp
            pass
        pass
        self.mySolutions[fInput] = fResult
        return fResult



def main(stdscr):
    with open(fName, 'r+') as f:
        fContent = f.read().splitlines()

    myMap = AoCmap()
    result = myMap.build(fContent=fContent)

    message = f'The answer to part 1 is (sample should be 21, answer should be 6827): {result}'
    print(message)

    print(20 * '*')

    myMap.multiply(reps)
    myMap.calcNumSolutions()
    result = result

    message = f'The answer to part 2 is (sample should be x, answer should be x): {result}'
    print(message)
    pass


# globals
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose"   , action="store_true", default=False, help="Add this to enable verbose output")
parser.add_argument("-d", "--draw"      , action="store_true", default=False, help="Add this to enable drawing")
parser.add_argument("-i", "--drawinterval", type=int, default=1, help="Add the value in ms for drawing interval")
parser.add_argument("-p", "--production", action="store_true", default=False, help="Add this to try the puzzle input")
args = parser.parse_args()

day = '12'
reps = 5
fName = f'2023/input/{day}_sample.txt'
if args.production: fName = f'2023/input/{day}.txt'

debug = args.verbose
draw = args.draw

main(None)