# importing pandas module 
import pandas as pd  
def countChar(row):
    LL, UL, char, pw = row.pwLowerLimit, row.pwUpperlimit, row.pwChar, row.pw
    return LL <= pw.count(char) <= UL

def validPw(row):
    LL, UL, char, pw = row.pwLowerLimit, row.pwUpperlimit, row.pwChar, row.pw
    return (pw[LL-1] == char) ^ (pw[UL-1] == char)

strFileName = '02-Alexander-input.txt'

# Convert the dictionary into DataFrame   
pwInput = pd.read_csv(strFileName,  names=["pwLowerLimit", "pwUpperlimit", "pwChar", "pw"], sep="-|\s+|: ")
pwInput['pwValid'] = pwInput.apply(countChar, axis=1) 
pwInput['pwValidM2'] = pwInput.apply(validPw, axis=1) 

pwInput.pwValid.value_counts()
pwInput.pwValidM2.value_counts()

#rslt_df = pwInput[pwInput.pwLowerLimit <= pwInput.pwCharOccur <= pwInput.pwUpperlimit]

pwInput



