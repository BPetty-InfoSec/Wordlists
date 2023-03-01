import os

def GetFilenames(pathVar):
    listing = os.listdir(pathVar)
    filesList = []
    dirsList = []
    for item in listing:
        if os.path.isfile(pathVar + "/" + item):
            filesList.append(pathVar + "/" + item)
        else:
            dirsList.append(pathVar + "/" + item)
    for dir in dirsList:
        addList = GetFilenames(dir)
        for item in addList:
            filesList.append(item)
    return filesList
