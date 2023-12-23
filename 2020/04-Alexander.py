# importing pandas module 
import pandas as pd 
# import regular expressions
import re

# Importing the StringIO module. 
from io import StringIO 

def validatePP(row):
    byrR = 1920 <= row.byr <=2002 
    iyrR = 2010 <= row.iyr <=2020
    eyrR = 2020 <= row.eyr <= 2030
    
    hgtR = False
    if row.hgt[-2:] == 'cm': 
        hgtR = 150 <= int(row.hgt[:-2]) <= 193
    elif row.hgt[-2:] == 'in':
        hgtR = 59 <= int(row.hgt[:-2])  <=76
    else:
        False

    if re.match(r'#[a-f0-9]{6}', row.hcl):
        hclR = True
    else:
        hclR = False

    eclR = row.ecl in ["amb", "blu" ,"brn", "gry", "grn" ,"hzl", "oth"]

    if re.match(r'(?<!\d)\d{9}(?!\d)', row.pid):
        pidR = True
    else:
        pidR = False

    return byrR and iyrR and eyrR and hgtR and hclR and eclR and pidR


# read text file
strFileName = '04-Alexander-input.txt'
fileContent = open(strFileName).read()

# replace every newline that is not preceded by a newline and split it on the remaining new lines
fileContentClean = re.sub(r'(?<!\n)\n', " ", fileContent) + '\n'


# now rework it to be a JSON format with records
# '[{"c1":1,"c2":2},{"c1":3,"c2":4}]'
fileContentClean = re.sub(r'((\S*):)', r'"\2":', fileContentClean)
fileContentClean = re.sub(r'(:(\S*))', r':"\2",', fileContentClean)
fileContentClean = re.sub(r'(, *\n)', r'\n', fileContentClean)
fileContentClean = re.sub(r'(\n)', r'},\n{', fileContentClean)
fileContentClean = '[{' + fileContentClean.rstrip('{')

fileContentClean = fileContentClean.rstrip(',\n') + ']'

df = pd.read_json(StringIO(fileContentClean), orient="records")

# Count the number of valid passports - those that have all required fields. 
# Treat cid as optional. In your batch file, how many passports are valid

dfResult = df[df.ecl.isnull() | df.eyr.isnull() | df.hcl.isnull() | df.pid.isnull() | df.iyr.isnull() | df.byr.isnull() | df.hgt.isnull() == False]

dfResult['validPP'] = dfResult.apply(validatePP, axis=1)
#dfResult.validPP.value_counts()

print ('We found ', (dfResult[dfResult.validPP == True].shape[0]) , ' valid passports' )
# store the data into a pandas frame

