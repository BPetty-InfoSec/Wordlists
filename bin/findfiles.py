import os
import bin.dbaccess as dbaccess


def GetFilenames(pathVar="lib"):
    if os.name == 'nt':
        dirSep = "\\"
    else:
        dirSep = "/"
    ignoreFiles = dbaccess.ReadDirOptions(pathVar)
    listing = os.listdir(pathVar)
    filesList = []
    dirsList = []
    for item in listing:
        if os.path.isfile(pathVar + dirSep + item):
            if item not in ignoreFiles:
                filesList.append(pathVar + dirSep + item)
        else:
            dirsList.append(pathVar + dirSep + item)
    for dir in dirsList:
        addList = GetFilenames(dir)
        for item in addList:
            filesList.append(item)
    return filesList

def GetDirNames(pathVar="lib"):
    if os.name == 'nt':
        dirSep = "\\"
    else:
        dirSep = "/" 
    listing = os.listdir(pathVar)
    dirsList = []
    for item in listing:
        if not os.path.isfile(pathVar + dirSep + item):
            dirsList.append(pathVar + dirSep + item)
    for dir in dirsList:
        addList = GetDirNames(dir)
        for item in addList:
            dirsList.append(item)
    return dirsList