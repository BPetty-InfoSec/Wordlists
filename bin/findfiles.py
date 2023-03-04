import os

def GetFilenames(pathVar):
    if os.name == 'nt':
        dirSep = "\\"
    else:
        dirSep = "/"
    listing = os.listdir(pathVar)
    filesList = []
    dirsList = []
    for item in listing:
        if os.path.isfile(pathVar + dirSep + item):
            filesList.append(pathVar + dirSep + item)
        else:
            dirsList.append(pathVar + dirSep + item)
    for dir in dirsList:
        addList = GetFilenames(dir)
        for item in addList:
            filesList.append(item)
    return filesList
