from zipfile import ZipFile 
import os
import io
import re

for f in os.scandir(os.getcwd()):
    if f.is_file():
        fileName, fileExt = os.path.splitext(f.name)
        # print(f.name)
        match fileExt:
            case ".zip":
                zipFile = f.name
                pass
            case ".txt":
                txtFile = f.name
                pass
del f, fileName, fileExt

# try and open the zipfile using a password from the text-file

with open(txtFile, 'rb') as f: # open pw list as binary
    fContent = f.read().splitlines()

thisZip = ZipFile(zipFile, "r")

thisFlag = None
results = []
while thisFlag == None:
    for nextZip in thisZip.infolist():
        if nextZip.filename[-4:] in (".zip", ".txt"):
            # for i, pw in enumerate(fContent[4999:]): # is possible for the test input
            for i, pw in enumerate(fContent): # [4999:] is possible for the test input
                pass
                try:
                    zContent = thisZip.read(nextZip.filename, pwd=pw)
                except:
                    pass # try again with the next password
                else:
                    # print("found", nextZip.filename, i, pw)
                    if nextZip.filename == "flag.txt":
                        pass
                        thisFlag = zContent.decode()
                        thisFlag = re.match(pattern='FLAG\{(.+)\}', string=thisFlag).groups()[0]
                        break
                    thisZip = ZipFile(io.BytesIO(zContent), "r")
                    del nextZip, i, pw
                    break
    # thisFlag = zContent

assert thisFlag != None
pass

print(thisFlag)