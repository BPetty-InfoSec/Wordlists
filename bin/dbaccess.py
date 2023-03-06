import sqlite3, os
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
                    cur.execute(insertRow,(fileName,"[]",line))
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
            newCategoryName = input("Enter new name for the category \"" + str(categoryRecord[0][0]) + "\": ")
            cur.execute(updateQuery, (newCategoryName,str(categoryName)))
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
            updateListQuery = "UPDATE lists SET categories = ? where name = ?"
            selectedList = cur.fetchall()
            categories = []
            getCategoryQuery = "SELECT * FROM categories WHERE name = ?"
            for item in categoriesList:
                cur.execute(getCategoryQuery, (item,))
                categories.append(cur.fetchall())
            cur.execute(updateListQuery, (listItem, categories))
            con.commit()