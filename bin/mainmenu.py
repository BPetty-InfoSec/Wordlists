from os import system, name

def PrintHeader(title="Main Menu"):
    print("+" + "-=" * 38 + "-+")
    print("| " + title.center(75," ") + " |")
    print("+" + "-" * 77 + "+")

def PrintLine(optionL, optionR):
    leftOption = str(optionL[0]) + ".  " + optionL[1]
    if optionR:
        rightOption = str(optionR[0]) + "  " + optionR[1] 
    else:
        rightOption = ""
    print("|  " + leftOption.ljust(35, " ") + " | " + rightOption.ljust(35, " ") + "  |")
    
def PrintFooter():
    print("+" + "-" * 77 + "+")

def DisplayOptions(optionsL, optionsR):
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
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

def DisplayMenu():
    ClearScreen()
    PrintHeader()
    menuOptionsL = [[1,"Show Lists"], [2,"Build Lists"],[3,"Categories"]]
    menuOptionsR = [["X.", "Exit"],["W.","Wipe Database"]]
    DisplayOptions(menuOptionsL, menuOptionsR)
    PrintFooter()