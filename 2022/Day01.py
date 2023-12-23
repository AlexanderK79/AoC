import argparse
#import curses
#from curses import wrapper
import functools
import pandas as pd  # importing pandas module 
from io import StringIO # Importing the StringIO module. 
import re # import regular expressions

def main(stdscr):
    inputFile = f.read().splitlines()
    f.close()

    for line in inputFile:
    #for line in inputFile[-1:]:
        #print(line)
        pass
    df = file2df(fName)
    result = df.groupby('name').sum().sort_values('calories').iloc[-1:]['calories'].values[0]
    print('The answer to part 1 is (sample should be 24000)', result)
    result = df.groupby('name').sum().sort_values('calories').iloc[-3:]['calories'].sum()
    print('The answer to part 2 is (sample should be 45000)', result)

def file2df(fTxtFile):
    fileContent = open(fTxtFile).read()
    fDF = pd.DataFrame(columns=['name', 'calories'])

    i = 0
    for line in fileContent.splitlines():
        if line.strip() == '':
            i += 1
            pass
        else: 
            names, items = list(), list()
            for item in line.split ( ' '):
                #print (i, item)
                names.append(i)
                items.append(int(item))
            fDF = pd.concat([fDF, pd.DataFrame.from_dict({'name': names , 'calories': items})], ignore_index=True)
    return fDF

# globals
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose"   , action="store_true", default=False, help="Add this to enable verbose output")
parser.add_argument("-d", "--draw"      , action="store_true", default=False, help="Add this to enable drawing")
parser.add_argument("-i", "--drawinterval", type=int, default=1, help="Add the value in ms for drawing interval")
parser.add_argument("-p", "--production", action="store_true", default=False, help="Add this to try the puzzle input")
args = parser.parse_args()

day = '01'
fName = f'2022/input/{day}_sample.txt'
if args.production: fName = f'2022/input/{day}.txt'
f = open(fName, 'r+')

debug = args.verbose
draw = args.draw

# stdscr = curses.initscr()
# curses.start_color()
# curses.use_default_colors()
# stdscr.scrollok(True)
# winHeader = curses.newwin(1,1,1,1)
# winMatrix_1 = curses.newwin(1,1,2,1)

# wrapper(main)

main(None)