#!/usr/bin/python3

# Collect wordlists into a single directory
# Wordlists will be collected in the "lib" directory
# Each directory will contain a "CREDITS.txt" file that
# gives credit to the creator of the wordlists found in that
# directory and its subdirectories.
# Cloning git repos is supported, with README.md and
# similar files being automatically ignored.
# Wordlists will be symlinked into the "Wordlists" directory.

import os, json

class WordLists:
    pass

def main():
    fileList = checkDir()

def checkDir(path):
    workList = []

def iterName(iterName, curNum):             #Increase the number after a filename for duplicate files
    pass

def checkName(checkName, checkList):        # Check to see if a name is already in the list
    pass

main()