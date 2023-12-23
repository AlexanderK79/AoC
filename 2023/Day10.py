import argparse

class pipeMap:
    def __init__(self) -> None:
        self.content = list()
        self.drawContent = list()
        self.map = dict() # x_y mapping of neighboors, co's of connection
        self.validnb = {
             'W': ['╚', '═', '╔']
            ,'N': ['╔', '║', '╗']
            ,'E': ['╗', '═', '╝']
            ,'S': ['╚', '║', '╝']
        }
        self.nb2chk = {
             'S': ['W', 'N', 'E', 'S']
            ,'═': ['W', 'E']
            ,'║': ['N', 'S']
            ,'╚': ['N', 'E']
            ,'╔': ['E', 'S']
            ,'╗': ['S', 'W']
            ,'╝': ['N', 'W']
        }
        self.nboffset = {'W': (-1, 0), 'N': (0, -1), 'E': (1, 0), 'S': (0, 1)}
        pass
    def build(self, fContent):
        self.content = fContent
        y = 0
        for thisLine in fContent:
            if thisLine == '#quit': break
            y += 1
            thisLine = thisLine.replace('F', '╔').replace('7', '╗').replace('|', '║').replace('-', '═')
            thisLine = thisLine.replace('L', '╚').replace('J', '╝')
            self.drawContent.append(thisLine)
            x = 0
            for char in thisLine:
                x += 1
                self.map['_'.join(map(str, (x,y)))] = {'co': (x, y), 'x': x, 'y': y, 'char': char, 'connected': bool, 'enclosed': bool, 'pairs': list(), 'steps_from_S': int(999999999)}
            pass
        pass
        # calculate connections and steps from S
        startCo = [i for i,j in self.map.items() if j['char'] == 'S'][0]
        self.map[startCo]['steps_from_S'] = 0
        thisCo = startCo
        thisCoPairNew = [startCo]
        while len(thisCoPairNew) > 0:
            thisCoPair = [i for i in thisCoPairNew]
            thisCoPairNew = list()
            for (thisCo, edge) in zip(thisCoPair, [self.findConnNeighboors(i) for i in thisCoPair]):
                pass
                for nb in edge:
                    if self.map[nb]['steps_from_S'] > self.map[thisCo]['steps_from_S'] + 1 :
                        self.map[nb]['steps_from_S'] = self.map[thisCo]['steps_from_S'] + 1
                        thisCoPairNew.append(nb)
                    pass
            pass

        return self
    
    def findConnNeighboors(self, fCo):
        # sets the co's of connected neighboors
        myX, myY = self.map[fCo]['co']
        myChar = self.map[fCo]['char']
        self.map[fCo]['pairs'] = list()
        for drctn in self.nb2chk[myChar]:
            thisX, thisY = myX + self.nboffset[drctn][0], myY + self.nboffset[drctn][1]
            if self.map.get('_'.join(map(str,(thisX, thisY))), {'char': None})['char'] in self.validnb[drctn]:
                self.map[fCo]['pairs'].append('_'.join(map(str,(thisX, thisY))))
                pass 
            pass

        if len(self.map[fCo]['pairs']) > 0: self.map[fCo]['connected'] = True
        pass
        return self.map[fCo]['pairs']
    
    def calcFreeTiles(self):
        # calculates if a tile is enclosed within a loop
        # tiles that are enclosed have an odd number of active vertical pipe elements to the left and right of them
        thisVertHookParts = ['╚', '╗', '╔', '╝']
        thisVertStraightParts = ['║']
        thisPipeLine = [i for i in self.map.values() if i['connected'] == True ]
        startCo = [i for i in thisPipeLine if i['char']=='S'][0]
        # reverse engineer the part
        drctn = list()
        for p in startCo['pairs']:
            oX, oY = startCo['x'] - self.map[p]['x'] , startCo['y'] - self.map[p]['y']
            drctn.append([k for k,v in self.nboffset.items() if v == (oX, oY)][0])
        pass
        startCo['char'] = ''.join(set.intersection(*[set(v) for k,v in self.validnb.items() if k in drctn]))
        for thisTile in [i for i in self.map.values() if i['connected'] != True]:
            # number of vert parts to the right
            Rh = [i for i in thisPipeLine if thisTile['x'] < i['x'] and thisTile['y'] == i['y'] and i['char'] in thisVertHookParts]
            Rhs = min((len([i for i in Rh if i['char'] == '╚']), len([i for i in Rh if i['char'] == '╗']))) # these parts become 1 straight
            Rhs += min((len([i for i in Rh if i['char'] == '╝']), len([i for i in Rh if i['char'] == '╔']))) # these parts become 1 straight
            Rs = Rhs + len([i for i in thisPipeLine if thisTile['x'] < i['x'] and thisTile['y'] == i['y'] and i['char'] in thisVertStraightParts])
            Rh = len(Rh) - (2*Rhs)
            Lh = [i for i in thisPipeLine if i['x'] < thisTile['x'] and thisTile['y'] == i['y'] and i['char'] in thisVertHookParts]
            Lhs = min((len([i for i in Lh if i['char'] == '╚']), len([i for i in Lh if i['char'] == '╗']))) # these parts become 1 straight
            Lhs += min((len([i for i in Lh if i['char'] == '╝']), len([i for i in Lh if i['char'] == '╔']))) # these parts become 1 straight
            Lh = len(Lh) - (2*Lhs)
            Ls = Lhs + len([i for i in thisPipeLine if i['x'] < thisTile['x'] and thisTile['y'] == i['y'] and i['char'] in thisVertStraightParts])

            if (Rh % 2 + Rs % 2 ) == 1 and (Lh % 2 + Ls % 2 ) == 1: thisTile['enclosed'] = True
            pass
        pass

def main(stdscr):
    fName = f'2023/input/{day}_sample.txt'
    if args.production: fName = f'2023/input/{day}.txt'

    with open(fName, encoding = 'utf-8', mode = 'r+') as f:
        fContent = f.read().splitlines()

    myMap = pipeMap()
    result = myMap.build(fContent=fContent)
    result = max([i['steps_from_S'] for i in myMap.map.values() if i['connected'] == True ])

    message = f'The answer to part 1 is (sample should be 8, answer should be 7086): {result}'
    print(message)

    print(20 * '*')

    fName = f'2023/input/{day}_sample_part2.txt'
    if args.production: fName = f'2023/input/{day}.txt'

    with open(fName, encoding = 'utf-8', mode = 'r+') as f:
        fContent = f.read().splitlines()

    myMapP2 = pipeMap()
    result = myMapP2.build(fContent=fContent)
    result = myMapP2.calcFreeTiles()
    result = len([i for i in myMapP2.map.values() if i['enclosed'] == True ])

    message = f'The answer to part 2 is (sample should be 4, answer should be x): {result}'
    print(message)

    if args.production: quit()
    fName = f'2023/input/{day}_sample_part2b.txt'
    with open(fName, encoding = 'utf-8', mode = 'r+') as f:
        fContent = f.read().splitlines()

    myMapP2 = pipeMap()
    result = myMapP2.build(fContent=fContent)
    result = myMapP2.calcFreeTiles()
    result = len([i for i in myMapP2.map.values() if i['enclosed'] == True ])

    message = f'The answer to part 2 is (sample should be 8, answer should be x): {result}'
    print(message)

    pass


# globals
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose"   , action="store_true", default=False, help="Add this to enable verbose output")
parser.add_argument("-d", "--draw"      , action="store_true", default=False, help="Add this to enable drawing")
parser.add_argument("-i", "--drawinterval", type=int, default=1, help="Add the value in ms for drawing interval")
parser.add_argument("-p", "--production", action="store_true", default=False, help="Add this to try the puzzle input")
args = parser.parse_args()

day = '10'

debug = args.verbose
draw = args.draw

main(None)