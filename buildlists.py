import bin.menu as menu
import bin.findfiles as findfiles
import bin.createDB as createDB
import bin.dbaccess as dbaccess
import bin.menucommands as commands

def main():
    createDB.CreateDBTables()       # Creates DB tables if they don't already exist
    createDB.LoadOptionsIntoMenu()  # Updates the menu options from menuoptions.json
    menu.DisplayMenu()              # Displays the main menu

main()