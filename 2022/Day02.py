import argparse
#import curses
#from curses import wrapper
import functools
import pandas as pd  # importing pandas module 
from io import StringIO # Importing the StringIO module. 
import re # import regular expressions

def main(stdscr):
    df = file2df(fName)
    result = df['my_score'].sum()
    print('The answer to part 1 is (sample should be 15)', result)
    df = file2dfB(fName)
    result = df['my_score'].sum()
    print('The answer to part 2 is (sample should be 12)', result)

def file2df(fTxtFile):
    #The first column is what your opponent is going to play: A for Rock, B for Paper, and C for Scissors. 
    #The second column--" Suddenly, the Elf is called away to help with someone's tent.

    # The second column, you reason, must be what you should play in response: 
    # X for Rock, Y for Paper, and Z for Scissors. 
    # Winning every time would be suspicious, so the responses must have been carefully chosen

    # Your total score is the sum of your scores for each round. 
    # The score for a single round is the score for the shape you selected (1 for Rock, 2 for Paper, and 3 for Scissors) 
    # plus the score for the outcome of the round (0 if you lost, 3 if the round was a draw, and 6 if you won).

    # Anyway, the second column says how the round needs to end: 
    # X means you need to lose, Y means you need to end the round in a draw, and Z means you need to win.


    fileContent = open(fTxtFile).read()
    fDF = pd.DataFrame(columns=['opponent_hand', 'my_hand', 'result', 'opponent_score', 'my_score'])
    hand2val = {'A': 1, 'B': 2, 'C': 3,'X': 1, 'Y': 2, 'Z': 3}

    for line in fileContent.splitlines():
        if line.strip() == '':
            pass
        else: 
            fResult = dict()
            opp_hand, my_hand = line.split ( ' ')
            fResult = ''
            opp_score, my_score = 0, 0
            opp_val, my_val = hand2val[opp_hand], hand2val[my_hand]

            if (opp_val == my_val):
                fResult = 'draw'
                opp_score = opp_val + 3
                my_score = opp_score
            elif (my_val - opp_val in (1, -2) ):
                fResult = 'win'
                opp_score = opp_val
                my_score = my_val + 6
            elif (my_val - opp_val in (-1, 2)):
                fResult = 'loss'
                opp_score = opp_val + 6
                my_score = my_val
            else:
                pass
            
            fResultDict = {
                    'opponent_hand': (opp_hand) , 
                    'my_hand': (my_hand),
                    'result': (fResult),
                    'opponent_score': (opp_score),
                    'my_score': (my_score)
                    }

            fDF = pd.concat([fDF, pd.DataFrame(fResultDict, index=[0])])
    return fDF

def file2dfB(fTxtFile):
    #The first column is what your opponent is going to play: A for Rock, B for Paper, and C for Scissors. 
    #The second column--" Suddenly, the Elf is called away to help with someone's tent.

    # The second column, you reason, must be what you should play in response: 
    # X for Rock, Y for Paper, and Z for Scissors. 
    # Winning every time would be suspicious, so the responses must have been carefully chosen

    # Your total score is the sum of your scores for each round. 
    # The score for a single round is the score for the shape you selected (1 for Rock, 2 for Paper, and 3 for Scissors) 
    # plus the score for the outcome of the round (0 if you lost, 3 if the round was a draw, and 6 if you won).

    # Anyway, the second column says how the round needs to end: 
    # X means you need to lose, Y means you need to end the round in a draw, and Z means you need to win.


    fileContent = open(fTxtFile).read()
    fDF = pd.DataFrame(columns=['opponent_hand', 'my_hand', 'result', 'opponent_score', 'my_score'])
    hand2val = {'A': 1, 'B': 2, 'C': 3,'X': 1, 'Y': 2, 'Z': 3}
    for line in fileContent.splitlines():
        if line.strip() == '':
            pass
        else: 
            i += 1
            fResult = dict()
            opp_hand, my_result = line.split ( ' ')
            fResult = ''
            opp_score, my_score = 0, 0
            opp_val = hand2val[opp_hand]
            
            if my_result == 'X': # lose
                my_val = opp_val - 1
                if (my_val == 0): my_val = 3
            elif my_result == 'Y': # draw
                my_val = opp_val
            elif my_result == 'Z': # win
                my_val = (opp_val % 3) + 1
            else:
                my_val = 0
            my_hand = my_val

            if (opp_val == my_val):
                fResult = 'draw'
                opp_score = opp_val + 3
                my_score = opp_score
            elif (my_val - opp_val in (1, -2) ):
                fResult = 'win'
                opp_score = opp_val
                my_score = my_val + 6
            elif (my_val - opp_val in (-1, 2)):
                fResult = 'loss'
                opp_score = opp_val + 6
                my_score = my_val
            else:
                pass
            
            fResultDict = {
                    'opponent_hand': (opp_hand) , 
                    'my_hand': (my_hand),
                    'result': (fResult),
                    'opponent_score': (opp_score),
                    'my_score': (my_score)
                    }

            fDF = pd.concat([fDF, pd.DataFrame(fResultDict, index=[0])])
    return fDF


# globals
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose"   , action="store_true", default=False, help="Add this to enable verbose output")
parser.add_argument("-d", "--draw"      , action="store_true", default=False, help="Add this to enable drawing")
parser.add_argument("-i", "--drawinterval", type=int, default=1, help="Add the value in ms for drawing interval")
parser.add_argument("-p", "--production", action="store_true", default=False, help="Add this to try the puzzle input")
args = parser.parse_args()

day = '02'
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