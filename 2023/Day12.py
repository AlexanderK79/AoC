import argparse
import re
import itertools
import math

class springsMap:
    def __init__(self) -> None:
        self.content = list()
        self.rows = dict()
        self.memory = {} # memoization function
        pass
    def build(self, fContent):
        self.content = fContent
        for i, thisLine in enumerate(fContent):
            thisLine = thisLine.split(' ')
            if thisLine[0] == '#': continue
            self.rows[str(i)] = {'rn': i, 'locations': thisLine[0], 'groups': list(map(int, thisLine[1].split(',')))}
            self.rows[str(i)]['result'] = thisLine[2] if not args.production else None
            pass
        return self
    def parse(self):
        for k in self.rows.keys():
            thisRow = self.rows[k]
            print(f'processing row {k} {thisRow}') if args.verbose else None
            matches = 0
            for (L, G) in self.buildWorklist(fLine=thisRow['locations'], fGroup=thisRow['groups']):
                matches += self.parseGroup(L, G, 'single')
            thisRow['matches'] = matches
            print (f"processed row {k}, result should be {thisRow['result']} and is {thisRow['matches']}", '\n') if args.verbose else None
            pass
        pass
    def buildWorklist(self, fLine, fGroup):
        # this will separate the fLine (one complete line of input) into groups to be processed
        # returns a fLine and the groups that can be in it
        # cut the line into pieces
        fLine = '^'+fLine+'$'
        thisWorklist = []
        thisStartGroupPos, thisEndGroupPos, overlap = 0, len(fLine), 0
        thisPat_lookback = '[\?^\.]+'+'[\?\.]+'.join([f'([#\?]{{{i}}})' for i in fGroup])+'[\?\.$]+'
        thisPat_lookahead = '[\?^\.]+?'+'[\?\.]+?'.join([f'([#\?]{{{i}}}?)' for i in fGroup])+'[\?\.$]+?'
        result = [m for m in re.finditer(thisPat_lookahead, fLine)] + [m for m in re.finditer(thisPat_lookback, fLine)] 
        result = [r.regs[1:] for r in result]
        for i,g in enumerate(fGroup): # fGroup is all items from fStart forward
            if i == 0:  # skip the first item; that one is covered by thisStartGroupPos
                thisWorklist.append((fLine[result[0][thisStartGroupPos][0]:result[1][thisStartGroupPos][1]], fGroup[thisStartGroupPos:i+1]))
                continue
            overlap = len(set(range(result[0][thisStartGroupPos][0],result[1][i-1][1])).intersection(range(result[0][i][0],result[1][i][1])))
            if overlap == 0: # overlap == 0 or at end of groups, add the groups up until this point to the worklist
                thisWorklist.append((fLine[result[0][thisStartGroupPos][0]:result[1][i-1][1]], fGroup[thisStartGroupPos:i]))
                thisStartGroupPos = i # set the startGroupPos
            elif overlap > 0: # overlap > 0 move to the next
                thisWorklist.append((fLine[result[0][thisStartGroupPos][0]:result[1][i][1]], fGroup[thisStartGroupPos:i+1]))
                thisStartGroupPos = i # set the startGroupPos
                if i < len(fGroup)-1: continue
            else:
                print('why do we get here')
                quit()
            if  i == len(fGroup)-1: # overlap at the end, now process it
                pass
                # thisWorklist.append((fLine[result[0][thisStartGroupPos][0]:result[1][i][1]], fGroup[thisStartGroupPos:]))
            print(thisWorklist) if args.verbose else None
        return thisWorklist


        pass
    def parseGroup(self, fLine, fGroup, fMode='single'):
        # print('fLine, fGroup', fLine, fGroup) if args.verbose else None
        if fMode in 'single':
            # check if parts have been calculated before:
            key = '__'.join((fLine, '_'.join(map(str, fGroup))))
            val = self.memory.get(key, None)
            if val != None:
                print('Returning', key, val, 'from self.memory') if args.verbose else None
                return val


            # use regex to find possible matches
            # 1,1,3 -> '\s*#{1}\s+#{1}\s+#{3}\s*'
            # ???.### -> '[#.]{3}.#{3}'
            re_str = fLine+ '.'
            # re_str = '^' + re_str + '$'

            thisLen = len(re_str)
            spaces = len(re_str) -sum(fGroup) - len(fGroup) + 1
            spaceCombi = [(i+1) * '.' for i in range(spaces)] if spaces > 0 else ['.']
            allElements = [[''] + spaceCombi]
            for thisG in [i * '#' for i in fGroup]:
                allElements.append([''.join(i) for i in itertools.product([thisG], spaceCombi)])
                pass
            re_pat_1 = '[\.]*' + '[\.]+'.join([f'([#.]{{{i}}}?)' for i in fGroup]) +'[\.]*'
            re_pat_2 = re_str.replace('$', '.$').replace('.', '\.').replace('?','[\.#]')
            possibleCombi = list(sorted(set([''.join(i) for i in itertools.product(*allElements) if len(''.join(i)) == thisLen ])))
            pass
            possibleCombi = [i[:-1] for i in possibleCombi if re.match(re_pat_1, i) and re.match(re_pat_2, i)]
            self.memory[key] = len(possibleCombi)
            return len(possibleCombi)

    def multiply(self, fMfactor):
        newContent = []
        for thisLine in self.content:
            newLine = '?'.join(fMfactor* [thisLine.split(' ')[0]]) + ' ' + ','.join(fMfactor * [thisLine.split(' ')[1]])
            newLine += '' if args.production == True else ' ' + thisLine.split(' ')[2]
            newContent.append(newLine)
        self.build(newContent)
        pass
        return self

    def calcRep(self, fMfactor):
        for k in self.rows.keys():
            thisRow = self.rows[k]
            pass
            # by adding a ? in between each string, does it create extra possibilities?
            if '#' in (thisRow['locations'][0], thisRow['locations'][-1] ) :
                # no extra possibilities
                thisRow['reps_'+ str(fMfactor)] = thisRow['matches'] * thisRow['matches']**(fMfactor-1)
            else:
                # see if extending the first part leads to new results:
                ext_bgn = self.parseGroup(thisRow['locations'] + '?', thisRow['groups'])
                ext_end = self.parseGroup('?' + thisRow['locations'], thisRow['groups'])
                if ext_bgn == thisRow['matches'] and ext_end == thisRow['matches']: # nodiff
                    thisRow['reps_'+ str(fMfactor)] = thisRow['matches']
                elif ext_bgn > thisRow['matches'] and ext_end == thisRow['matches'] : 
                    thisRow['reps_'+ str(fMfactor)] = ext_bgn**(fMfactor-1) * thisRow['matches']
                elif ext_bgn == thisRow['matches'] and ext_end > thisRow['matches'] : 
                    thisRow['reps_'+ str(fMfactor)] = thisRow['matches'] * ext_end**(fMfactor-1)
                elif ext_bgn > thisRow['matches'] and ext_end > thisRow['matches'] : 
                    # thisRow['reps_'+ str(fMfactor)] = ext_bgn**(fMfactor-1) * ext_end**(fMfactor-1) # wrong too high
                    # thisRow['reps_'+ str(fMfactor)] = ext_bgn * ext_end**(fMfactor-1) # too low
                    # thisRow['reps_'+ str(fMfactor)] = (ext_bgn**(fMfactor-1) * thisRow['matches'] ) + (thisRow['matches'] * ext_end**(fMfactor-1)) # too low
                    # thisRow['reps_'+ str(fMfactor)] = ext_bgn**(fMfactor) + ext_end**(fMfactor) # wrong
                    thisRow['reps_'+ str(fMfactor)] = ext_bgn**(fMfactor) + ext_end**(fMfactor) # 
                else:
                    print('why do we get here', thisRow)
        return self
        pass



def main(stdscr):
    with open(fName, 'r+') as f:
        fContent = f.read().splitlines()
    

    myMap = springsMap()
    result = myMap.build(fContent=fContent)
    result = myMap.parse()
    result = sum([i['matches'] for i in myMap.rows.values()])

    message = f'The answer to part 1 is (sample should be 21, answer should be 6827, 58105,  54999, 38318 are too high, 6183 is wrong): {result}'
    print(message)

    print(20 * '*')
    quit()

    reps = 5
    # result = myMap.calcRep(reps)
    result = myMap.multiply(reps)
    result = myMap.parse()
    # result = sum([i['reps_' + str(reps)] for i in myMap.rows.values()])

    message = f'The answer to part 2 is (sample should be 525152, answer should be x, 3098628954561320291 is too high, 633191595229 is too low, wrong: 1306268056875): {result}'
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
fName = f'2023/input/{day}_sample.txt'
if args.production: fName = f'2023/input/{day}.txt'

debug = args.verbose
draw = args.draw

main(None)