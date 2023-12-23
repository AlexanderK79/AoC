# basically these numbers are binary, where F=0, B=1 and L=0, R=1
# first 7 chars = row, last 3 chars = col
# seat id: (8 * row ) + col
# what is the highest seat ID?

# importing pandas module 
import pandas as pd 


def convertBP(row):
    R = row.input[:7].replace('F', '0').replace('B', '1')
    C = row.input[-3:].replace('L', '0').replace('R', '1')
    return [R, C, int(R, 2), int(C, 2), (8*int(R, 2)) + int(C, 2)]

strFileName = '05-Alexander-input.txt'
#strFileName = '05-sample-input.txt'

# Convert the dictionary into DataFrame   
df = pd.read_fwf(strFileName,  names=["input"])
df[['row', 'col', 'rowdec', 'coldec', 'seatID']]  = df.apply(convertBP, axis=1, result_type='expand')
df = df.sort_values(by=['seatID'])
df = df.reset_index(drop=True)

df['prevSeat'] = df.shift(1).seatID
df['nextSeat'] = df.shift(-1).seatID

#dfResult = df[(df.shift(-1).seatID +1 != df.seatID) & (df.shift(1).seatID -1 != df.seatID)]
dfResult = df[(df.prevSeat.notnull() & df.nextSeat.notnull()) & ((df.prevSeat +1 != df.seatID) | (df.nextSeat -1 != df.seatID))]

print ('Total number of boarding passes: ', int(df['seatID'].max()))
print ('Your seat is: ', int(dfResult['seatID'].mean()))

# for some fun... now draw the layout of the plane
#          seatnum  seatnum  seatnum              seatnum seatnum seatnum
# row num     X
# newline

offSet = int(df['seatID'].min())

rowWidth = 8
dfMap = pd.DataFrame(0, index=range(0, int(round(df['seatID'].max()/8)*8)), columns=[])

df.index.names = ['idx']
dfMap.index.names = ['idx']
dfMap = dfMap.join(df.set_index('seatID'), on='idx')
#dfMap = dfMap.fillna(0)
dfMap['validSeat'] = dfMap['input'].notnull()

colSep = '    '
for i in range(int(dfMap.index.min()), int(dfMap.index.max())):

    if i % rowWidth == 0:
        #print (f"{dfMap.loc[i].rowdec:<8.0f}{int(dfMap.loc[i+0].coldec):^5.0f}{dfMap.loc[i+1].coldec:^5.0f}{dfMap.loc[i+2].coldec:^5.0f}{dfMap.loc[i+3].coldec:^5.0f}   {dfMap.loc[i+4].coldec:^5.0f}{dfMap.loc[i+5].coldec:^5.0f}{dfMap.loc[i+6].coldec:^5.0f}{dfMap.loc[i+7].coldec:^5.0f}")
        #print (f"{' ':<6}{dfMap.loc[i+0].index::^5.0f}{dfMap.loc[i+1].index::^5.0f}{dfMap.loc[i+2].index::^5.0f}{dfMap.loc[i+3].index::^5.0f}{dfMap.loc[i+4].index::^5.0f}{dfMap.loc[i+5].index::^5.0f}{dfMap.loc[i+6].index::^5.0f}{dfMap.loc[i+7].index::^5.0f}")
        if i % (rowWidth*rowWidth) == 0:
            print(f"\n{'':<8}", f"{0:^5}", f"{1:^5}", f"{2:^5}", f"{3:^5}", colSep, f"{4:^5}", f"{5:^5}", f"{6:^5}", f"{7:^5}")
        print(f"{i/rowWidth:<8.0f}"
                ,"{val:^5}".format(val=i   if dfMap.loc[i].validSeat else '')
                ,"{val:^5}".format(val=i+1 if dfMap.loc[i+1].validSeat else '')
                ,"{val:^5}".format(val=i+2 if dfMap.loc[i+2].validSeat else '')
                ,"{val:^5}".format(val=i+3 if dfMap.loc[i+3].validSeat else '')
                ,colSep
                ,"{val:^5}".format(val=i+4 if dfMap.loc[i+4].validSeat else '')
                ,"{val:^5}".format(val=i+5 if dfMap.loc[i+5].validSeat else '')
                ,"{val:^5}".format(val=i+6 if dfMap.loc[i+6].validSeat else '')
                ,"{val:^5}".format(val=i+7 if dfMap.loc[i+7].validSeat else '')
            )

print('hoi')