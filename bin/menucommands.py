import bin.dbaccess as dbaccess
import bin.menu as menu

def ShowCategories():
    print("Got here!")
    categoriesList = dbaccess.ReadCategories()
    menu.ClearScreen()
    menu.PrintHeader("Currently Available Categories")
    menu.ShowListTripleColumn(categoriesList)
    menu.PrintFooter()
    input("\n\nPress Enter to continue...")
    menu.DisplayMenu()