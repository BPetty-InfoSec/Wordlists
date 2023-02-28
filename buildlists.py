import bin.mainmenu as menu
from contextlib import closing
import sqlite3

# Create database tables
def CreateDBTables():
    with closing(sqlite3.connect("bin/wordlists.db")) as con:
        with closing(con.cursor()) as cur:
            listsTable = "CREATE TABLE lists (id, name, categories, filePath)"
            categoriesTable = "CREATE TABLE categories (id, name)"
            try:
                cur.execute(listsTable)
            except sqlite3.OperationalError:
                print("Main table already exists.")
            
            try:
                cur.execute(categoriesTable)
            except sqlite3.OperationalError:
                print("Categories table already exists.")

def main():
    CreateDBTables()
    menu.DisplayMenu()

main()