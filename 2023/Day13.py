import argparse

class notebook:
    def __init__(self) -> None:
        self.content = list()
        self.pages = []
        pass
    def build(self, fContent):
        self.content = fContent
        for thisPage in fContent.split('\n\n'):
            self.pages.append(self.page(thisPage))
            pass
        return self
    def find_sym_axis(self, fOrientation= 'both'):
        if fOrientation in ( 'both', 'vertical'):
            [p.find_sym_axis(fOrientation='vertical') for p in self.pages]
        if fOrientation in ( 'both', 'horizontal'):
            [p.find_sym_axis(fOrientation='horizontal') for p in self.pages]
        pass
    def clean_spots(self, fOrientation= 'both'):
        if fOrientation in ( 'both', 'vertical'):
            [p.clean_spots(fOrientation='vertical') for p in self.pages]
        if fOrientation in ( 'both', 'horizontal'):
            [p.clean_spots(fOrientation='horizontal') for p in self.pages]
        pass

    class page:
        def __init__(self, fContent) -> None:
            self.content = fContent
            self.lines = {}
            self.sym_axis_vert = {}
            self.sym_axis_hor = {}
            for (i, thisLine) in enumerate(fContent.split()):
                self.lines[i] = {'i': i, 'line': thisLine}
            pass
        def find_sym_axis(self, fOrientation='vertical'):
            thisPage = [l['line'] for l in self.lines.values()]
            if fOrientation == 'horizontal':
                # transpose
                thisPage = [''.join([fLine[x] for fLine in thisPage]) for x in range(len(thisPage[0]))] # transpose the list
                pass
            # parse through all lines on thisPage and note the possible axis
            for (i, thisLine) in enumerate(thisPage):
                if fOrientation == 'vertical':
                    thisAxis = self.sym_axis_vert
                elif fOrientation == 'horizontal':
                    thisAxis = self.sym_axis_hor
                thisAxis[i] = []
                
                for j in range(1,len(thisLine)):
                    mirrorRange = min((j-0, len(thisLine)-j))
                    if thisLine[j-mirrorRange:j][::-1] == thisLine[j:j+mirrorRange]:
                        thisAxis[i].append(j)
                pass
            # find the common position
            thisCommon = set(thisAxis[0])
            for v in thisAxis.values():
                thisCommon = thisCommon.intersection(set(v))
            thisAxis['common'] = list(thisCommon)
            pass
            # look which axis is shared by all
        def clean_spots(self, fOrientation='vertical'):
            # the spot to clean misses just one position
            # check horizontal
            thisSpots, thisSpotsDict = list(), dict()
            if fOrientation == 'vertical':
                thisAxis = self.sym_axis_vert
            elif fOrientation == 'horizontal':
                thisAxis = self.sym_axis_hor
            
            for v in [v for (k,v) in thisAxis.items() if k != 'common']:
                thisSpots += v
            for j in set(thisSpots):
                thisSpotsDict[j] = thisSpots.count(j)
            thisSpotsDict = {k: v for k, v in sorted(thisSpotsDict.items(), key=lambda item: item[1], reverse=True)}
            hotSpot = [k for (k,v) in thisSpotsDict.items() if v == len(thisAxis)-2]
            thisAxis['hotSpot'] = [hotSpot[0]] if len(hotSpot) > 0  else [0]

            del thisSpots, thisSpotsDict, thisAxis
            pass


def main(stdscr):
    with open(fName, 'r+') as f:
        fContent = f.read()
    

    myNotebook = notebook()
    result = myNotebook.build(fContent=fContent)
    result = myNotebook.find_sym_axis(fOrientation='both')
    result = sum([sum(v.sym_axis_vert['common']) for v in myNotebook.pages]) + (100 * sum([sum(v.sym_axis_hor['common']) for v in myNotebook.pages]))

    message = f'The answer to part 1 is (sample should be 405, answer should be 37025): {result}'
    print(message)

    print(20 * '*')

    result = myNotebook.clean_spots()
    result = sum([sum(v.sym_axis_vert['hotSpot']) for v in myNotebook.pages]) + (100 * sum([sum(v.sym_axis_hor['hotSpot']) for v in myNotebook.pages]))

    message = f'The answer to part 2 is (sample should be 400, answer should be 32854): {result}'
    print(message)
    pass


# globals
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose"   , action="store_true", default=False, help="Add this to enable verbose output")
parser.add_argument("-d", "--draw"      , action="store_true", default=False, help="Add this to enable drawing")
parser.add_argument("-i", "--drawinterval", type=int, default=1, help="Add the value in ms for drawing interval")
parser.add_argument("-p", "--production", action="store_true", default=False, help="Add this to try the puzzle input")
args = parser.parse_args()

day = '13'
fName = f'2023/input/{day}_sample.txt'
if args.production: fName = f'2023/input/{day}.txt'

debug = args.verbose
draw = args.draw

main(None)