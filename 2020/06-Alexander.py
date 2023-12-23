# we are looking for the number of unique answers per group

# a group is split by two \n's
# each member of a group is split by a single \n

# count number of unique chars in string
# len(set("stackoverflow"))

# importing pandas module 
import pandas as pd 
# import regular expressions
import re
# Importing the StringIO module. 
from io import StringIO 
# Function to print common characters of two Strings  
# in alphabetical order  
from collections import Counter 

def findNumOfCommonChars(row):
    # not used anymore
    answerList = row.answerPerPerson
    if '' in answerList: answerList.remove('') 
    # convert each strings into counter dictionary  
    commonDict = Counter(answerList[0]) 
    for answer in answerList:
        dictNew = Counter(answer)
        # take intersection of these dictionaries  
        commonDict = commonDict & dictNew
    # get a list of common elements  
    commonChars = list(commonDict.elements())  

    # sort list in ascending order to print resultant  
    # string on alphabetical order  
    commonChars = sorted(commonChars)  

    # join characters without space to produce  
    # resultant string  
    return (''.join(commonChars))


# read text file
strFileName = '06-sample-input.txt'
strFileName = '06-Alexander-input.txt'
fileContent = open(strFileName).read()

# replace every newline that is not preceded by a newline and split it on the remaining new lines
fileContentClean = re.sub(r'(?<!\n)\n', "", fileContent) + '\n'
fileContentClean = fileContent.split('\n\n')
fileContentClean = [i.replace('\n', ',') for i in fileContentClean] 
fileContentClean = '\n'.join(fileContentClean)

df = pd.read_fwf(StringIO(fileContentClean),  names=["input"], infer_nrows=10000)
df['uniqueAnswers'] = df.apply(lambda x: len(set(x['input'].replace(',',''))), axis=1 )
#print(df)
print ('Total number of unique answers: ', int(df['uniqueAnswers'].sum()))

df['answerPerPerson'] = df.apply(lambda x: x['input'].split(','), axis=1 )
#df['commonAnswersPerGroupA'] = df.apply(findNumOfCommonChars, axis=1)
df['commonAnswersPerGroup'] = df.apply(lambda x: ''.join(sorted(set.intersection(*map(set,(x['answerPerPerson']))))) , axis=1)
df['numOfCommonAnswersPerGroup'] = df.apply(lambda x: len(set.intersection(*map(set,(x['answerPerPerson'])))) , axis=1)


#df['numOfCommonAnswersPerGroupB'] = df.apply(lambda x: len(x['commonAnswersPerGroupA']), axis=1)
print ('Total number of common answers: ', int(df['numOfCommonAnswersPerGroup'].sum()))
# print ('Total number of common answers: ', int(df['numOfCommonAnswersPerGroupB'].sum()))


# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)
# pd.set_option('display.width', None)
#pd.set_option('display.max_colwidth', -1)
print(df)

print('hoi')