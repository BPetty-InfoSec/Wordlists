from os import system, name
import sqlite3
from contextlib import closing
import bin.menucommands as commands

def DisplayMenu():
    """This is the function that will display the menu
    """
    menuOptionsL, menuOptionsR = LoadMenuOptions()  # Load menu options from menuoptions.json
    ClearScreen()                                   # Clear the screen
    PrintHeader()                                   # Prints the header (defaults to Main Menu)
    DisplayOptions(menuOptionsL, menuOptionsR)      # Displays the body of the menu
    PrintFooter()                                   # Prints the Footer
    GetInput()                                      # Gets user input

    
def PrintHeader(title="Main Menu"):
    """Prints the header for displaying the menu

    Args:
        title (str, optional): The title to be displayed in the header. Defaults to "Main Menu".
    """
    print("+" + "-=" * 38 + "-+")
    print("| " + title.center(75," ") + " |")
    print("+" + "-" * 77 + "+")

def PrintLine(optionL, optionR):
    """Prints a single line of the menu.
    This will show a 2-column menu-style list.
    The optionL and optionR Lists are composed of Lists themselves.
    Each item in the List will itself have 2 items: an identifier and a name.
    Example: 
        optionL = [[1, "Left Line 1"], [2, "Left Line 2"]]
        optionR = [["A", "Right Line 1"], ["B", "Right Line 2"]]
        Those options would display something like this (spacing not to scale):
        | 1. Left Line 1          | A. Right Line 1          |
        | 2. Left Line 2          | B. Right Line 2          |
    To show lists in 1, 2, or 3 columns of simple values, see the functions
    for ShowListSingleColumn, ShowListDoubleColumn, ShowListTripleColumn
    
    Args:
        optionL (list): List of options for the left side of the menu.
        optionR (list): List of options for the right side of the menu.
    """
    leftOption = str(optionL[0]) + ".  " + optionL[1]
    if optionR:
        rightOption = str(optionR[0]) + ".  " + optionR[1] 
    else:
        rightOption = ""
    print("|  " + leftOption.ljust(35, " ") + " | " + rightOption.ljust(35, " ") + "  |")
    
def PrintFooter():
    """Prints a simple footer line
    """
    print("+" + "-" * 77 + "+")

def DisplayOptions(optionsL, optionsR):
    """Handles the logic for printing menu lines.
    The actual printing of these lines is handled by the PrintLine function.

    Args:
        optionsL (list): A list of 2-value lists to comprise the left column of the menu
        optionsR (list): A list of 2-value lists to comprise the right column of the menu
    """
    lenL = len(optionsL)
    lenR = len(optionsR)
    if lenL > lenR:
        for index in range(len(optionsL)):
            if index < lenR:
                PrintLine(optionsL[index], optionsR[index])
            else:
                PrintLine(optionsL[index], "")
    else:
        for index in range(len(optionsR)):
            if index < lenL:
                PrintLine(optionsL[index], optionsR[index])
            else:
                PrintLine("", optionsR[index])
            
def ClearScreen():
    """Clears the screen based on what OS the app is running on
    """
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

def LoadMenuOptions():
    """This function returns a list of menu options from the database
    This will take menu options with an integer value for the identifier and place them on the left side.
    Options with a string value for the identifier will be placed on the right side

    Returns:
        list (x2): This will return the left and right options for use in menu display
    """
    leftOptions = []
    rightOptions = []
    with closing(sqlite3.connect("bin/wordlists.db")) as con:
        with closing(con.cursor()) as cur:
            cur.execute("SELECT * FROM menuOptions")
            menuOptions = cur.fetchall()
            for item in menuOptions:
                if str(type(item[0])) == "<class 'int'>":
                    leftOptions.append(item)
                else:
                    rightOptions.append(item)
    return leftOptions, rightOptions

def ShowListSingleColumn(listItems):
    """Shows items in a single-column list

    Args:
        listItems (list): A list of items to display
    """
    for item in listItems:
        print("| " + item.center(75, " ") + " |")

def ShowListDoubleColumn(listItems):
    """Shows items in a double-column list

    Args:
        listItems (list): A list of items to display
    """
    loopCount = 1
    lineItems = []
    for item in listItems:
        lineItems.append(item)
        if loopCount == 2:
            print(  "| " + lineItems[0].center(36, " ") + 
                    " | " + lineItems[1].center(36, " ") + 
                    " |")
        loopCount += 1
        if loopCount > 2:
            loopCount = 1
            lineItems = []
    if len(lineItems) < 2:
        print("| " + lineItems[0].center(36, " ") + " | " + "|".rjust(38," "))
        
def ShowListTripleColumn(listItems):
    # Shows items in a triple-column list
    #
    # Args:
    # param listItems (list): A list of items to display
    loopCount = 1
    lineItems = []
    for item in listItems:
        lineItems.append(item)
        if loopCount == 3:
            print(  "| " + lineItems[0].center(23, " ") +
                    " | " + lineItems[1].center(23, " ") + 
                    " | " + lineItems[2].center(23, " ") +
                    " |")
        loopCount += 1
        if loopCount > 3:
            loopCount = 1
            lineItems = []
    remainderItems = len(lineItems)
    if remainderItems == 1:
        print(  "| " + lineItems[0].center(23, " ") +
                " | " + " "*23 + " | " + 
                "|".rjust(25," "))
    if remainderItems == 2:
        print(  "| " + lineItems[0].center(23, " ") +
                " | " + lineItems[1].center(23, " ") +
                " | " + "|".rjust(25, " "))

def GetInput():
    # Gets input from the user
    # 
    # todo: change to use a single-keypress value
    # todo: validate input
    # todo: handle default (non-validated) choices
    optionChosen = input("\nChoose Option: ")
    if optionChosen == "3":
        commands.ShowCategories()
