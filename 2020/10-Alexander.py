import pandas as pd
from io import StringIO

blTesting = True
day=10

if blTesting:
    with open(f'{day}-sample-input1.txt', 'r') as file: data = file.read().split('\n')
    # with open(f'{day}-sample-input2.txt', 'r') as file: data = file.read().split('\n')
else:
    with open(f'{day}-Alexander-input.txt', 'r') as file: data = file.read().split('\n')

def countAdjs(row):
    return((df[(df['item'] > row['item']) & (df['item'] <= (row['item'] +3))].item.count()))

def extraPath(row):
    if row['countAdjs'] == 3:
        # 3 adjs leads to 6 altPaths
        return(4)
    elif row['countAdjs'] == 2:
        # 2 adjs leads to 2 altPaths... only if it is not part of a 3 step
        if (df[df['item'] == row['prevItem']]['countAdjs'].max()) != 3:
            return(2)
    
    return (0)
    #return(max(0, row['countAdjs']-1))

def extraPaths(row):
    if row['extraPath'] > 0:
        pathsToThisPoint = 1 + df[df['item'] < row['item']]['extraPath'].sum()
        pathsFromThisPoint = df[df['item'] >= row['item']]['extraPath'].sum()
    else:
        return(0)



def possibleChildren(row):
    listOfChildren = list(df[(df['item'] > row['item']) & (df['item'] <= (row['item'] +3))]['item'])
    return(listOfChildren)
        

def possibleParents(row):
    # df of previousRecords
    prevRows = df[(df['item'] >= (row['item']-3)) & (df['item'] < row['item'])]
    listOfParents = []
    if prevRows.shape[0] > 0:
        for curRow in prevRows.itertuples():
            if row['item'] in getattr(curRow, 'possibleChildren'): listOfParents.append(getattr(curRow, 'item'))
    return(listOfParents)

def numPaths(row):
    numPaths = 1
    if len(row['possibleParents']) == 0:
        pass
    elif len(row['possibleParents']) == 1:
        parent = row['possibleParents'][0]
        numPaths = (df.loc['n'+str(parent)]['numPaths'])
    else:
        # for every parent that is not known before, multiply the paths by 2
        prevRows = df[df['item'] < row['item']]
        knownParents =[]
        for i in list(prevRows['possibleParents']):
            knownParents.extend(i)
        knownParents =set(knownParents)

        for parent in row['possibleParents']:
            if parent not in knownParents:
                numPaths = df.loc['n'+str(parent)]['numPaths'] * 2
    df.at['n'+str(row['item']), 'numPaths'] = numPaths
    return (numPaths)



def possiblePaths(row):
    # lists the possiblePaths to get here; it is a list of lists
    possiblePaths = []
    if len(row['possibleParents']) == 0:
        # we are at the start
        possiblePaths.append([row['item']])
    else:
        for parent in row['possibleParents']:
            for path in df.loc['n' + str(parent)]['possiblePaths']:
                possiblePaths.append(path + [(row['item'])])
    df.at['n'+str(row['item']), 'possiblePaths'] = possiblePaths
    return(possiblePaths)



#convert to ints
data.append('0')
data = sorted(list(map(int,data)))
data.append(max(data)+3)
df = pd.read_fwf(StringIO('\n'.join(map(str,data))),  names=["item"], infer_nrows=10000)
df['itemName'] = df.apply(lambda x: 'n' + str(x['item']), axis=1)
df = df.set_index("itemName", inplace = False) 
df['prevItem'] = df.shift(1).item
df['prevItem'] = df['prevItem'].fillna(0)
df['nextItem'] = df.shift(-1).item
df['nextItem'] = df['nextItem'].fillna(df['item'].max()+3)
df['deltaPrev'] = df.apply(lambda x: x['item'] - x['prevItem'], axis=1 )
df['deltaNext'] = df.apply(lambda x: x['nextItem'] - x['item'], axis=1 )

# print('Number of delta 1: ', df[df.deltaPrev == 1].deltaPrev.count())
# print('Number of delta 3: ', df[df.deltaPrev == 3].deltaPrev.count())

answer = df[df.deltaPrev == 1].deltaPrev.count() * df[df.deltaPrev == 3].deltaPrev.count()

print (f'The answer to part 1 is: {answer}')

# how many possible arrangements
# 
df['countAdjs'] = df.apply(countAdjs, axis=1)
df['extraPath'] = df.apply(extraPath, axis=1)
df['extraPaths'] = df.apply(extraPaths, axis=1)
df['possibleChildren'] = df.iloc[:,0].map(lambda _: [])
df['possibleChildren'] = df.apply(possibleChildren, axis=1)#, result_type='expand')
df['possibleParents'] = df.iloc[:,0].map(lambda _: [])
df['possibleParents'] = df.apply(possibleParents, axis=1)
df['possiblePaths'] = df.iloc[:,0].map(lambda _: [])
df['possiblePaths'] = df.apply(possiblePaths, axis=1)

df['numPathsSimple'] = df.apply(lambda x: len(x['possiblePaths']), axis=1)
df['numPaths'] = 1
df['numPaths'] =df.apply(numPaths, axis=1)

answer = len(df.iloc[-1]['possiblePaths'])
print(df)
print (f'The answer to part 2 is: {answer}')
