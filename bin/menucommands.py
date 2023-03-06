import bin.dbaccess as dbaccess
import bin.display as display
import bin.findfiles as files

def ShowCategories():
    categoriesList = dbaccess.ReadCategories()
    display.ClearScreen()
    display.PrintHeader("Currently Available Categories", 3)
    display.ShowListTripleColumn(categoriesList, False)
    display.PrintFooter(3)
    input("\nPress Enter to continue...")
    display.DisplayMenu()

def EditCategories():
    editPrompt = "\nDo you want to:\n\t(A)dd\n\t(E)dit\n\t(D)elete\n\t(<ENTER> to return)\nChoice: "
    categoriesList = dbaccess.ReadCategories()
    display.ClearScreen()
    display.PrintHeader("Edit Categories", 3)
    display.ShowListTripleColumn(categoriesList, True)
    display.PrintFooter(3)
    userChoice = input(editPrompt)
    if userChoice.upper() == "E" :
        categoryChosen = int(input("\nEnter the number of the category you want to edit: "))
        dbaccess.ModifyCategory(categoriesList[categoryChosen - 1])
    elif userChoice.upper() == "A":
        newCategory = input("\nEnter the name of the new category: ")
        dbaccess.AddCategory(newCategory)
    elif userChoice.upper() == "D":
        deleteCategory = int(input("\nEnter the number of the category you want to delete: "))
        dbaccess.DeleteCategory(categoriesList[deleteCategory - 1])
    else:
        display.DisplayMenu()

def BuildLists():
    filesList = files.GetFilenames()
    dbaccess.AddFilesToDB(filesList)
    display.DisplayMenu()
    
def ShowLists():
    wordLists = dbaccess.ReadWordLists()
    display.ShowWordLists(wordLists)
    input("\nPress Enter to continue")
    display.DisplayMenu()

def AssignCategories():
    wordlists = dbaccess.ReadWordLists()
    lists = []
    for item in wordlists:
        lists.append(item[0])
    display.PrintHeader("Available Wordlists")
    display.ShowListTripleColumn(list, True)
    display.PrintFooter(3)
    listChoice = int(input("\nSelect a list: "))
    chosenList = wordlists[listChoice - 1]
    display.PrintHeader("Available Categories")
    categories = dbaccess.ReadCategories()
    display.ShowListTripleColumn(categories, True)
    display.PrintFooter(3)
    doneChoosing = False
    addCategories = []
    while doneChoosing == False:
        multiChoice = input("Choose a category. Enter X to stop: ")
        if multiChoice.upper() == "X":
            doneChoosing = True
        else:
            isNumber = multiChoice.isnumeric()
            if isNumber:
                addCategories.append(int(multiChoice)-1)
            else:
                doneChoosing = True
    if len(addCategories) > 0:
        dbaccess.AddCategoriesToList(chosenList,addCategories)