# some recursion...


# parse list
# each bag color has a fixed number of childs; in the end there are bags without children
# any bag color can have multiple parents; at the start of the chain there are bags without parents

# build a dict or df
# index key: color name
# parents: [parent: color name, parent: color name]
# children: [child: color name, qty: number, child: color name, qty: number]


# importing pandas module 
import pandas as pd 
# import regular expressions
import re
# Importing the StringIO module. 
from io import StringIO 

def assignBag(dictB, currentbag, childrenlist):
    # this function returns the adjusted dictionary
    if dictB.get(currentbag) is None: dictB[currentbag] = {}
    if dictB[currentbag].get('children') is None: dictB[currentbag]['children'] = {}
    for child in childrenlist:
        regex = re.match('(\d+)(.+$)', child.strip() )
        if regex is None:
            qty = 0
            childbag = 'no child'
        else:
            qty = regex.groups()[0]
            childbag = regex.groups()[1].strip()

        
        dictB[currentbag]['children'][childbag] = qty
        if dictB.get(childbag) is None: dictB[childbag] = {}
        if dictB[childbag].get('parents') is None: dictB[childbag]['parents'] = []
        dictB[childbag]['parents'].append(currentbag)
    return dictB

def listAncestors(dictB, start, curList):
    if dictB[start].get('parents') is not None:
        for p in (dictB[start]['parents']):
            if p not in curList: curList.append(p)
            listAncestors(dictB, p, curList)
    return curList

def countChildren(dictB, start, curCountList, level, parent, Sfactor):
    while len(curCountList) < level+1: curCountList.append(0)
    
    if dictB[start]['children'].get('no child') is None:
        for c in (dictB[start]['children']):
            if parent == '': 
                curCountList[level] += Sfactor * int(dictB[start]['children'][c])
                curCountList[level] += 0
                Cfactor = 1
            else:
                # travel upward to the parent until original basestart to determine the Sfactor
                Cfactor = Sfactor * int(dictB[parent]['children'][start])
                curCountList[level] += Cfactor * int(dictB[start]['children'][c])
            countChildren(dictB, c, curCountList, level + 1, start, Cfactor)
    else:
        #curCountList[level] += int(dictB[parent]['children'][start]) # * int(dictB[start]['children'])
        curCountList[level] += 0
        
    return curCountList



# read text file
strFileName = '07-sample-input.txt'
strFileName = '07-sample-input2.txt'
strFileName = '07-Alexander-input.txt'
fileContent = open(strFileName).read()

fileContentClean = re.sub(r' bags contain ', "|", fileContent) + '\n' # parent
bags = {}

df = pd.read_fwf(StringIO(fileContentClean),  names=["input"], infer_nrows=10000)
df['self'] = df.apply(lambda x: x['input'].split('|')[0], axis=1)
df['children'] = df.apply(lambda x: x['input'].split('|')[1].rstrip('.').split(','), axis=1)
df['children'] = df.apply(lambda x: [re.sub(r' bags*', '', y) for y in x['children']], axis=1)

for index, row in df.iterrows():
    bags = assignBag(bags, row['self'], row['children'])

# How many colors can, eventually, contain at least one shiny gold bag?
# After building the datastructure, open 'shiny gold', recurse through each parent until there are no parents and add the outcome to the list

resultList = listAncestors(bags, 'shiny gold', [])

numOfChild = countChildren(bags, 'shiny gold', [], 0, '', 1)

print('shiny gold has ', len(resultList), ' ancestors')
print('shiny gold has ', sum(numOfChild), ' children')

print ('hoi') 