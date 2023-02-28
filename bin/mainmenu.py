def PrintHeader(title="Main Menu"):
    print("+-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- " + title.center(21, " ") + " -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-+")

def PrintLine(optionL, optionR):
    leftOption = str(optionL[0]) + ".  " + optionL[1]
    # rightOption = optionR[0] + "  " + optionR[1] 
    rightOption = ""
    print("|  " + leftOption.ljust(49, " ") + " | " + rightOption.ljust(49, " ") + "  |")

def DisplayOptions(optionsL, optionsR):
    if len(optionsL) > len(optionsR):
        for item in optionsL:
            PrintLine(item,"")

def DisplayMenu():
    PrintHeader()
    menuOptionsL = [[1,"Show Lists"], [2,"Build Lists"],[3,"Categories"]]
    menuOptionsR = [["X.", "Exit"],["W.","Wipe Database"]]
    DisplayOptions(menuOptionsL, menuOptionsR)