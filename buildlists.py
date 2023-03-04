import bin.mainmenu as menu
import bin.findfiles as findfiles
import bin.createDB as createDB

def main():
    createDB.CreateDBTables()
    menu.DisplayMenu()
    print(findfiles.GetFilenames("lib"))

main()