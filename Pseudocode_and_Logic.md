# **Logic and Pseudocode for BuildList**

*This document is to reflect the logic and some basic pseudocode for the ./buildlist.go application.*

## **Concept**
BuildList will do three things:
1. Check all subdirectories under /lib for wordlists, recursively
2. Check to see if any of those directories contain the .categories file. There will be 4 options:
    - No: To create a .categories file for the directory
    - No: Not to create a .categories file for that directory, and leave it unindexed
    - Yes: To modify the .categories file
    - Yes: To leave the .categories file the way that it is.
3. If a .categories file exists, take each wordlist file in the file, and symlink it to the Wordlists directory, under the subdirectory matching each of the category names for it.

This sounds somewhat simple. Experience has proven that it is not.

### **Additional Functionality**
- Add flags functionality to only check for .categories files, or to skip categorization and simply build the Wordlists directory
- Show a preview (5 lines, perhaps) of each file when asking to create a .categories file for the directory, to give some insight with unfamiliar lists and directories

Main function:
- Check for flags
- If flags are present, proceed based on the flags present
    - If the flag is for checking for .categories only (-i, or --index):
        - Run through the subdirectories to check for .categories files.
        - If the subdirectory does not have a .categories file, ask if it should be created
            - If yes: start a .categories file
                - Display 5 lines of each file in the directory in turn, and allow input of categories as desired
                - Enter an "X" if the file is not to be categorized, and so left out of the Wordlists directory entirely
            - If no:
                - Skip this directory and move to the next directory in line, be it subdirectory or main directory
        - If the directory does have a categories file:
            - Ask if the file should be modified
            - Show the categories file to the user, with line numbers.
            - Allow the user to choose line numbers to modify.
    - If the flag is for just creating the Wordlist directory (-b or --build):
        - Run through the directories in /lib, and symlink all of the files appropriately
- If flags are not present, use both functions: checking for .categories, allowing modification, as well as symlinking files after categorization is complete.

---
## **_Template_**
**_PARAMETERS:_** <parameters>

**_RETURNS:_** <returns>

**_DESCRIPTION:_** <description>

**_LOGIC:_**
1. <Logic>
2. <Logic>

---
## **_Type: fileInfo_**

**_DESCRIPTION:_** This is a type to hold file information

**_Setup_**
1. FName
    - File Name
2. FPath
    - File Path
3. FCats
    - Categories for the file to be symlinked to
4. FType
    - Whether the item is a directory or a file

---
## **_Main_**
**_PARAMETERS:_** None

**_RETURNS:_** None

**_DESCRIPTION:_** This function is the main processing body. It's job is basically to call functions in a logical order to get the job done.

**_LOGIC:_**
1. Check for flags
    - Call checkFlags()
    - If flags are present:
        - Yes:
            - Read returned flags
            - If --index:
                - Call readDirs() with "config" parameter
            - ElseIf --symlink:
                - Call readDirs() with "symlink" parameter
            - Else:
                - Call readDirs() with "all" parameter
        - Else:
            - Call readDirs() with "all" parameter

---
## **_checkFlags()_**
**_PARAMETERS:_** None

**_RETURNS:_** cmdFlag (string)

**_DESCRIPTION:_** This function returns the flags listed on the command line when runing ./buildlist.go

**_LOGIC:_**
1. Check to see what flags were specified on the command line
    - --index:
        - Return "config"
    - --build:
        - Return "symlink"
    - Else:
        - Return "all"

---
## **_readDirs(cmdFlag) fileList_**
**_PARAMETERS:_** cmdFlag (string): Either "all", "symlink", or "config"

**_RETURNS:_** mainConfig (type configList)

**_DESCRIPTION:_** This function contains the logic for reading everything under the /lib directory

**_LOGIC:_**
1. Declare:
    - filesList (fileList)
    - configStatus (configList)
2. Read the /lib directory: call dirList("/lib", cmdFlag) and populate variables filesList (fileList) and configStatus ([]string)
3. Check cmdFlag:
    - If cmdFlag == "--symlink":
        - Iterate through filesList and create symlinks and directories in /Wordlists directory
    - ElseIf cmdFlag == "--config"
        - Iterate through configStatus
            - For each populated entry:
                - Show .categories file
                - Ask if user wishes to modify file
                - If YES:
                    - Allow user to modify by calling modifyCats(\<path>)
                - Else:
                    - Skip modifying, move to next item
            - For each UNpopulated entry:
                - Show files in current path
                - Ask user if wishes to create .categories file for this directory
                - If YES:
                    - Allow user to modify by calling modifyCats(\<path>)
                    - update configStatus to reflect changes
                - Else:
                    - Skip modifying, move to next item
        - Exit cleanly
    - Else:
        - Iterate through configStatus
            - For each populated entry:
                - Show .categories file
                - Ask if user wishes to modify file
                - If YES:
                    - Allow user to modify by calling modifyCats(\<path>)
                - Else:
                    - Skip modifying, move to next item
            - For each UNpopulated entry:
                - Show files in current path
                - Ask user if wishes to create .categories file for this directory
                - If YES:
                    - Allow user to modify by calling modifyCats(\<path>)
                    - update configStatus to reflect changes
                - Else:
                    - Skip modifying, move to next item
        - Modify filesList to match .categories file in configStatus
        - Iterate through filesList and create symlinks and directories in /Wordlists directory

---
## **_dirList(directory, cmdFlag) dirList configList_**
**_PARAMETERS:_** 
1. directory (string)
2. cmdFlag (string)

**_RETURNS:_** 
1. dirList (fileList)
2. configList ([]string)

**_DESCRIPTION:_** This function reads the contents of a specific directory and returns the list of contents, along with whether the item is a file or directory. This function is recursive, and does all of the heavy lifting for reading the directories. If the cmdFlag variable is not "symlink" then configList slice will be populated with the paths of directories that need to have .categories files set. Essentially what happens, is that each time this function is called, it will call itself again for each directory that it finds. Basically, it will descend to the bottom of each directory structure in turn, working its way back up to the /lib folder before going to the next directory, returning and appending the files as necessary.

**_LOGIC:_**
1. Read the entire contents of the directory, as passed by the directory parameter
2. Check if cmdFlag is "config"
    - If YES: 
        - skip all files, except for .categories, add all directories to dirList
        - If the .categories file DOES NOT exist:
            - Add current path to configList
    - ELSE:
        - Add all files and directories to dirList
        - Check if cmdFlag is "symlink"
        - if YES:
            - Add contents of .categories file to dirList via populateFromCategories("\<Current Path>")
        - ELSE:
            - Add all files and directories to dirList
            - Add current path to configList
3. Start a for loop and iterate over dirList
    - If the item is a file, skip it
    - If the item is a directory, call dirList() with the directory's FPath value, save to _tempList and _tempPath
4. Append _tempList to dirList
5. Append _tempPath to configList
    - if there is a .categories file, add NULL to _tempList
5. Return dirList and configList

---
## **_populateFromCategories(workPath) fileList_**
**_PARAMETERS:_** workPath (string)

**_RETURNS:_** filesList (fileList)

**_DESCRIPTION:_** This function reads the .categories file in a directory and returns the values of the non-null entries for symlinking

**_LOGIC:_**
1. Read .categories file in workPath
2. Iterate through each line in file
3. Check categories on line:
    - If NULL:
        - Skip entry
    - Else:
        - Add file, path, and categories to filesList, set FType to file
4. Return filesList

---
## **_modifyCats(path) []string_**
**_PARAMETERS:_** <parameters>

**_RETURNS:_** <returns>

**_DESCRIPTION:_** <description>

**_LOGIC:_**
1. <Logic>
2. <Logic>