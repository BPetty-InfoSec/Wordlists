import sqlite3
import os
from contextlib import closing
import bin.findfiles as findfiles
import bin.menucommands as commands


def AddFilesToDB(filesList):
    with closing(sqlite3.connect("bin/wordlists.db")) as con:
        with closing(con.cursor()) as cur:
            listsQuery = "SELECT * FROM lists"
            contents = cur.execute(listsQuery)
            dbFiles = cur.fetchall()
            foundFile = False
            for line in filesList:
                for row in dbFiles:
                    if line in row:
                        foundFile = True
                        break
                    else:
                        foundFile = False
                if foundFile == False:
                    fileName = os.path.basename(line)
                    insertRow = "INSERT INTO lists (name,categories,filePath) VALUES (?,?,?)"
                    cur.execute(insertRow, (fileName, "", line))
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
    return categoriesList


def ModifyCategory(categoryName):
    with closing(sqlite3.connect("bin/wordlists.db")) as con:
        with closing(con.cursor()) as cur:
            categoriesQuery = "SELECT * FROM categories WHERE name=?"
            updateQuery = "UPDATE categories SET name = ? WHERE name = ?"
            cur.execute(categoriesQuery, (str(categoryName),))
            categoryRecord = cur.fetchall()
            newCategoryName = input(
                "Enter new name for the category \"" + str(categoryRecord[0][0]) + "\": ")
            cur.execute(updateQuery, (newCategoryName, str(categoryName)))
            con.commit()
    commands.ShowCategories()


def AddCategory(categoryName):
    with closing(sqlite3.connect("bin/wordlists.db")) as con:
        with closing(con.cursor()) as cur:
            insertQuery = "INSERT INTO categories (name) values (?)"
            cur.execute(insertQuery, (categoryName,))
            con.commit()
    commands.ShowCategories()


def DeleteCategory(categoryName):
    with closing(sqlite3.connect("bin/wordlists.db")) as con:
        with closing(con.cursor()) as cur:
            deleteQuery = "DELETE FROM categories WHERE name=?"
            cur.execute(deleteQuery, (categoryName,))
            con.commit()
    commands.ShowCategories()


def ReadWordLists():
    wordLists = []
    with closing(sqlite3.connect("bin/wordlists.db")) as con:
        with closing(con.cursor()) as cur:
            getListsQuery = "SELECT * FROM lists"
            cur.execute(getListsQuery)
            wordLists = cur.fetchall()
    return wordLists


def AddCategoriesToList(listItem, categoriesList):
    with closing(sqlite3.connect("bin/wordlists.db")) as con:
        with closing(con.cursor()) as cur:
            getListsQuery = "SELECT * FROM lists WHERE name = ?"
            cur.execute(getListsQuery, (str(listItem[0]),))
            updateListQuery = "UPDATE lists SET categories = ? where filePath = ?"
            filePath = listItem[2]
            cur.execute(updateListQuery, (categoriesList, filePath))
            con.commit()

def ReadDirOptions(dirPath):
    ignoreFiles = []
    with closing(sqlite3.connect("bin/wordlists.db")) as con:
        with closing(con.cursor()) as cur:
            getOptionsQuery = "SELECT * FROM dirOptions WHERE dirName = ?"
            cur.execute(getOptionsQuery,(dirPath,))
            ignoreFiles = cur.fetchall()
    return ignoreFiles

def AddDirOption(dirPath, ignoreFile):
    with closing(sqlite3.connect("bin/wordlists.db")) as con:
        with closing(con.cursor()) as cur:
            addDirOptionQuery = "INSERT INTO dirOptions (dirPath, ignoreFile) VALUES (?,?)"
            cur.execute(addDirOptionQuery, (dirPath, ignoreFile))
            con.commit()

def RemoveDirOption(dirPath, ignoreFile):
    with closing(sqlite3.connect("bin/wordlists.db")) as con:
        with closing(con.cursor()) as cur:
            removeDirOptionQuery = "DELETE FROM dirOptions WHERE dirPath = ? AND ignoreFile = ?"
            cur.execute(removeDirOptionQuery, (dirPath, ignoreFile))
            con.commit()