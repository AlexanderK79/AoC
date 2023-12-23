import argparse
import pandas as pd

class gameLog:
    def __init__(self, ) -> None:
        self.gamelist = list()
        pass
    def build(self, fContent):
        self.content = fContent
        # self.df = pd.DataFrame(columns=['id', 'game'])
        for line in fContent:
            thisLine = line.split(':')
            thisTurns = thisLine[1].split(';')
            thisTurnlist = [i for i in thisTurns]
            thisTurndetails = list()
            for i in thisTurnlist:
                thisTurnLog = {'red': 0, 'green': 0, 'blue': 0}
                for j in i.split(','):
                    thisTurnLog[j.strip().split(' ')[1]] = int(j.strip().split(' ')[0])
                thisTurndetails.append(thisTurnLog)

            self.gamelist.append({'game': int(thisLine[0].split(' ')[1]), 'turns': thisTurns, 'turnlog': thisTurndetails })
        return self
    def checkValid(self, fLimit):
        for i in self.gamelist:
            validGame = True
            for j in i['turnlog']:
                for color in fLimit.keys():
                    if j[color] > fLimit[color]:
                        validGame = False
                        break
                if not validGame: break
            i['valid'] = validGame
    def sumValid(self):
        return sum([i['game']  for i in self.gamelist if i['valid']])
    def calcPower(self):
        for i in self.gamelist:
            i['power'] = 1
            for x in [max([k[colored] for k in i['turnlog']]) for colored in i['turnlog'][0].keys()]:
                i['power'] *= x
    def sumPower(self):
        return sum([i['power']  for i in self.gamelist])


def main(stdscr):
    with open(fName, 'r+') as f:
        fContent = f.read().splitlines()

    myGames = gameLog()
    result = myGames.build(fContent=fContent)
    result = myGames.checkValid({'red': 12, 'green': 13, 'blue': 14})
    result = myGames.sumValid()

    message = f'The answer to part 1 is (sample should be 8, answer should be 2449): {result}'
    print(message)

    print(20 * '*')

    result = myGames.calcPower()
    result = myGames.sumPower()

    message = f'The answer to part 2 is (sample should be 2286, answer should be 63981): {result}'
    print(message)


# globals
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose"   , action="store_true", default=False, help="Add this to enable verbose output")
parser.add_argument("-d", "--draw"      , action="store_true", default=False, help="Add this to enable drawing")
parser.add_argument("-i", "--drawinterval", type=int, default=1, help="Add the value in ms for drawing interval")
parser.add_argument("-p", "--production", action="store_true", default=False, help="Add this to try the puzzle input")
args = parser.parse_args()

day = '02'
fName = f'2023/input/{day}_sample.txt'
if args.production: fName = f'2023/input/{day}.txt'

debug = args.verbose
draw = args.draw

main(None)