import sqlite3
import json
from contextlib import closing

# Create database tables
def CreateDBTables():
    with closing(sqlite3.connect("bin/wordlists.db")) as con:
        with closing(con.cursor()) as cur:
            listsTable = "CREATE TABLE lists (name, categories, filePath)"
            categoriesTable = "CREATE TABLE categories (name)"
            menuOptionsTable = "CREATE TABLE menuOptions (option, name)"
            
            # Try to create the main lists table
            try:
                cur.execute(listsTable)
            except sqlite3.OperationalError:
                print("Main table already exists.")
            
            # Try to create the categories table
            try:
                cur.execute(categoriesTable)
            except sqlite3.OperationalError:
                print("Categories table already exists.")
            
            # Try to create the menu options table
            try:
                cur.execute(menuOptionsTable)
            except sqlite3.OperationalError:
                print("Menu Options table already exists.")
            
def LoadOptionsIntoMenu():
    menuOptionsQuery = "SELECT * FROM menuOptions"
    optsFile = open("bin/menuoptions.json")
    menuOptions = json.load(optsFile)
    insertMenuOptions = "INSERT INTO menuOptions (option, name) VALUES (?, ?)"

    with closing(sqlite3.connect("bin/wordlists.db")) as con:
        with closing(con.cursor()) as cur:

            # Try to load the menu options into the database
            cur.execute(menuOptionsQuery)
            currentOptions = cur.fetchall()
            foundOption = False
            for menuOption in menuOptions:
                print("Loading: " + str(menuOption))
                for currentOption in currentOptions:
                    if menuOption[0] in currentOption:
                        print("Matched for the selector, skipping")
                        foundOption = True
                        break
                    if menuOption[1] in currentOption:
                        print("Matched for the value, skipping")
                        foundOption = True
                        break
                if foundOption == False:
                    print("Didn't match anything. Update here.")
                    cur.execute(insertMenuOptions, (menuOption[0], menuOption[1]))
                    con.commit()
                else:
                    foundOption = False
