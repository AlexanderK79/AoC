import argparse
import numpy as np
import pandas as pd

def main(stdscr):
    myDF = pd.read_table(fName, names=['List A', 'List B'], sep='\s+')
    myDF.sort_values(by='List A', inplace=True)
    myDF = myDF.reset_index(drop=True)
    myDF['List B']=myDF['List B'].sort_values().values
    # myDF['diff'] = abs(myDF['List B'] - myDF['List A'])
    result = myDF.apply(np.diff, axis=1).abs().sum()[0]
    message = f'The answer to part 1 is (sample should be ?, answer should be 1603498): {result}\n'
    print(message)

    tmpDF = myDF.groupby(['List B'])['List B'].size().to_frame('size')
    result = myDF['List A'].apply(lambda x: x*tmpDF['size'].get(x, 0)).sum()
    del tmpDF
    message = f'The answer to part 2 is (sample should be ?, answer should be 25574739): {result}\n'
    print(message)
    pass


# globals
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose"   , action="store_true", default=False, help="Add this to enable verbose output")
parser.add_argument("-p", "--production", action="store_true", default=False, help="Add this to try the puzzle input")
args = parser.parse_args()

day = '01'
fName = f'2024/input/{day}_sample.txt'
if args.production: fName = f'2024/input/{day}.txt'

debug = args.verbose

main(None)