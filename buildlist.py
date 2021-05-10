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
    print(fileList)
    for file in fileList:
        print(fileList[file] + " : ./Wordlists/" + file)
        try:
            os.symlink("." + fileList[file], "./Wordlists/" + file)
        except:
            os.mkdir("Wordlists")
            os.symlink("." + fileList[file], "./Wordlists/" + file)

def checkDir(path):
    returnList = {}
    print(path)
    for file in os.listdir(path):
        if file == ".git":
            continue
        elif os.path.isdir(path + "/" + file):
            print(path + " : " + file)
            tempReturn = checkDir(path + "/" + file)
            for item in tempReturn:
                try:
                    returnList[item] = tempReturn[item]
                except:
                    returnList[item + "1"] = tempReturn[item]
        else:
            if file == "CREDIT.txt":
                continue
            elif file == "README.md":
                continue
            else:
                print(file + " is a file")
                returnList[file] = path + "/" + file
    return returnList

main()