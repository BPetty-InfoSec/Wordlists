import sqlite3
import json
from contextlib import closing


def CreateDBTables():
    # Description: Create DB tables if they don't already exist
    # Try to create each table on startup. If the table already exists,
    # it will be skipped.
    # @params: None
    with closing(sqlite3.connect("bin/wordlists.db")) as con:
        with closing(con.cursor()) as cur:
            listsTable = "CREATE TABLE lists (name, categories, filePath)"
            categoriesTable = "CREATE TABLE categories (name)"
            menuOptionsTable = "CREATE TABLE menuOptions (option, name)"
            dirOptionsTable = "CREATE TABLE dirOptions (dirName, ignoreFiles)"

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

            # Try to create the directory options table
            try:
                cur.execute(dirOptionsTable)
            except sqlite3.OperationalError:
                print("Directory Options table already exists.")


def LoadOptionsIntoMenu():
    # Description: Load menu options from json file
    # The menuoptions.json file contains the selector
    # character as well as the name of the menu option
    # todo: Add support for extensibility through naming
    # todo: and placing extension .py files in a subirectory
    # todo: that will be imported as a whole.
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
                for currentOption in currentOptions:
                    if menuOption[0] in currentOption:
                        foundOption = True
                        break
                    if menuOption[1] in currentOption:
                        foundOption = True
                        break
                if foundOption == False:
                    cur.execute(insertMenuOptions,
                                (menuOption[0], menuOption[1]))
                    con.commit()
                else:
                    foundOption = False
