#!/usr/bin/python3

# Collect wordlists into a single directory
# Wordlists will be collected in the "lib" directory
# Each directory will contain a "CREDITS.txt" file that
# gives credit to the creator of the wordlists found in that
# directory and its subdirectories.
# Cloning git repos is supported, with README.md and
# similar files being automatically ignored.
# Wordlists will be symlinked into the "Wordlists" directory.

import os

def main():
    fileList = checkDir("./lib")
    #print(fileList)
    for file in fileList:
        #print(fileList[file] + " : ./Wordlists/" + file)
        try:                                #Create symlinks in ./Wordlists
            os.symlink("." + fileList[file], "./Wordlists/" + file)
        except:                             #Create ./Wordlists if it doesn't exist
            os.mkdir("Wordlists")
            os.symlink("." + fileList[file], "./Wordlists/" + file)

def checkDir(path):
    returnList = {}
    #print(path)
    for file in os.listdir(path):
        if file == ".git":                  #Skip the .git directory in repos
            continue
        elif os.path.isdir(path + "/" + file):  #If this is a directory recursively call function
            #print(path + " : " + file)
            tempReturn = checkDir(path + "/" + file)
            for item in tempReturn:         #Process recursively processed files into returnList
                try:
                    if checkName(item,returnList):  #Check if name exists
                        i = 0               #Loop iteration counter
                        while not checkName(item,returnList):
                            item = iterName(item)   #Find a name that will work
                            i += 1
                        else:
                            returnList[item] = tempReturn[item]
                    else:
                        returnList[item] = tempReturn[item] #Add file and path to returnList
                except:
                    returnList["2" + item] = tempReturn[item]   #Avoid edge case with identical filenames
        else:                               #If this is a file, process the file
            if file == "CREDIT.txt":        #Skip CREDIT.txt files
                continue
            elif file == "README.md":       #Skip README files
                continue
            elif file == "LICENSE":         #Skip LICENSE files
                continue
            elif file == "CODE_OF_CONDUCT.md":   #Skip CODE_OF_CONDUCT files
                continue
            elif file == "CONTRIBUTING.md": #Skip CONTRIBUTING
                continue
            elif file == "CONTRIBUTORS.md": #Skip CONTRIBUTORS
                continue
            elif file == ".buildignore":    #Skip directories with this file
                return []
            else:
                #print(file + " is a file")
                returnList[file] = path + "/" + file    #Add the filename and path to the returnList dictionary
    return returnList

def iterName(iterName, curNum):             #Increase the number after a filename for duplicate files
    nameString = iterName.split('.')        #Split the string at "."
    nameString[0] = nameString[0] + str(int(curNum) + 1)
    for part in nameString:                 #Reconstruct string, even if multiple "."
        returnName = nameString[part]
    return returnName

def checkName(checkName, checkList):        # Check to see if a name is already in the list
    if checkName in checkList:
        return False
    else:
        return True

main()