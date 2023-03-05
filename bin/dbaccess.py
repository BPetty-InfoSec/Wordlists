import sqlite3
from contextlib import closing
import os

def AddFilesToDB(filesList):
    with closing(sqlite3.connect("bin/wordlists.db")) as con:
        with closing(con.cursor()) as cur:
            listsQuery = "SELECT * FROM lists"
            contents = cur.execute(listsQuery)
            dbFiles = cur.fetchall()
            print(dbFiles)
            print("Files List: " + str(filesList))
            foundFile = False
            for line in filesList:
                print("Line: " + line)
                for row in dbFiles:
                    print("Row: " + str(row))
                    if line in row:
                        foundFile = True
                        print("Found it!")
                        break
                    else:
                        print("Not on this line...")
                        foundFile = False
                if foundFile == False:
                    fileName = os.path.basename(line)
                    insertRow = "INSERT INTO lists (name,categories,filePath) VALUES (?,?,?)"
                    cur.execute(insertRow,(fileName,1,line))
                    con.commit()

def ReadCategories():
    categoriesList = []
    with closing(sqlite3.connect("bin/wordlists.db")) as con:
        with closing(con.cursor()) as cur:
            categoriesQuery = "SELECT * FROM categories"
            cur.execute(categoriesQuery)
            rawCategoriesList = cur.fetchall()
            for item in rawCategoriesList:
                categoriesList.append(item[0])
            print(categoriesList)
            input()
    return categoriesList