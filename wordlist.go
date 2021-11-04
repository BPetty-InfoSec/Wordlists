package main

/**
 * Builds a directory of wordlists from gathered many wordlists.
 * Wordlists are organized by category once a .categories file
 * with the correct syntax is added to each directory containing
 * word lists. Works with git repositories, so it is entirely
 * possible (and fully intended) to allow the user to clone
 * wordlist git repositories into the repository directory
 * (lib/ by default)
 * Once the categories are assigned, directories for each
 * unique category are created in the designated (Wordlists/
 * by default) directory, and finally symlinks to the files
 * in the cloned repositories are created.
 *
 * Respects existing files/directories, so it is safe to run
 * more than once, allowing an easy workflow of cloning a repository,
 * creating the .categories file, and then running buildlist again
 * to update the master set of lists.
 *
 * In the end, the purpose of this application is to create an
 * easily-accessible master-listing of various lists from different
 * sources, categorized by use, for use with tools such as
 * DirBuster (or goBuster) and BurpSuite.
 */

import (
	"fmt"
	"os"
)

/**
 **	******************** STRUCTURES ********************
 */

/**
 **	Structure to hold file information
 */
type fileInfo struct {
	FName string   // Holds the name of the file. What will be symlinked
	FPath string   // Path to file
	FCats []string // Categories for the file
	FType string   // If the item is a File or Directory
}

/**
 **	******************** GLOBAL CONSTANTS ********************
 *
 *	Find list of files to ignore in checkIgnore()
 *
 */
const (
	libDir      = "./lib"
	wordlistDir = "./Wordlists"
)

/**
 **	******************** MAIN FUNCTION ********************
 */
func main() {

	// Get command line arguments and parse them into the "cliFlags" string.
	// Used for controlling program behavior.
	var cliFlag string
	if len(os.Args) == 1 {
		cliFlag = "all"
	} else {
		cliFlag = checkFlags()
	}

	// ***** DEBUG *****
	fmt.Println(os.Args)
	fmt.Println(cliFlag)

	readDirs(cliFlag)
}

/**
 **	Checks the command line arguments when app is run
 **	Returns a string containing either:
 *		1: "config"		This tells the app to only set up
 *						categories only, does not create
 *						symlinks
 *		2: "symlink"	This tells the app to create symlinks
 *						without going through and setting up
 *						categories
 *		3: "all"		This tells the app to do everything
 */
func checkFlags() string {
	var cliFlag string

	fmt.Println("******* DEBUG *******")
	fmt.Println("Passed length check")
	fmt.Println("***** END DEBUG *****")

	// Check what arguments were passed.
	// Return flag if valid, otherwise call showHelp()
	switch os.Args[1] {
	case "-i":
		cliFlag = "config"
	case "--index":
		cliFlag = "config"
	case "-b":
		cliFlag = "symlink"
	case "--build":
		cliFlag = "symlink"
	case "-h":
		showHelp()
	case "--help":
		showHelp()
	case "-a":
		cliFlag = "all"
	case "--all":
		cliFlag = "all"
	case "":
		cliFlag = "all"
	default:
		showHelp()
	}
	return cliFlag
}

/**
 **	Show the help for this application.
 */
func showHelp() {
	fmt.Println("Usage:  wordlist [Options]")
	fmt.Println()
	fmt.Println("This app builds a list of categorized wordlists from those contained in the /lib")
	fmt.Println("subdirectory, and symlinks them into the Wordlists directory. It is designed to")
	fmt.Println("function normally even when git repos are cloned into /lib.")
	fmt.Println()
	fmt.Println("Options:")
	fmt.Println("-h, --help\tShow this help information.")
	fmt.Println("-i, --index\tIndex all wordlists, allowing for categorization, but do not create symlinks.")
	fmt.Println("-b, --build\tBuild the list from current information, without re-indexing.")
	fmt.Println("-a, --all\tBuild and re-index the list [default behavior]")
	fmt.Println()
}

/**
 **	Contains the logic for reading directories and acting on them
 *	@param cliFlag: Checks to what the user wants to do
 */
func readDirs(cliFlag string) { //[]fileInfo {
	// var fileList []string
	var allFiles []fileInfo

	// Open the /lib directory and read directories inside of it
	file, err := os.Open(libDir)
	if err != nil {
		fmt.Println("/lib directory not found: ", err)
		os.Exit(1)
	}
	defer file.Close()

	// Read the contents of /lib
	libList, _ := file.Readdir(0)

	// Extract the top-level directories for lists to read
	var topLevelDirs []string
	for _, dir := range libList {
		if dir.IsDir() == true {
			topLevelDirs = append(topLevelDirs, dir.Name())
		}
	}
	// ***** DEBUG *****
	fmt.Println("topLevelDirs: ", topLevelDirs)

	// Call dirList() on each top level directory.
	for _, dir := range topLevelDirs {
		var tempList []fileInfo
		tempList = dirList(dir, cliFlag)
		for _, item := range tempList {
			allFiles = append(allFiles, item)
		}
	}
}

/**
 **	Read a directory and return a list of files
 **	Recursive function. Calls itself to read further subdirectories
 *	@param dirToRead - The directory to be read
 *	@param cliFlag - Arguments from the CLI
 *
 **	Returns:
 **		[]fileList - List of files found
 **		[]configList - List of directories with .categories files
 *
 *	TODO: Add recursion
 *	TODO: Add Logic to handle cliArgs
 */
func dirList(directory string, cliFlag string) []fileInfo { //, []string
	// Slice to hold attributes of the contents of the directory
	var contentsList []fileInfo

	// Create file object to read directory contents
	file, err := os.Open("./lib/" + directory)
	if err != nil {
		fmt.Println("Err: " + err.Error())
	}
	defer file.Close()

	// Get the contents of the directory, and store them in contentsList.
	dirContents, _ := file.ReadDir(0)
	for _, item := range dirContents {
		var tempInfo fileInfo
		tempInfo.FName = item.Name()
		tempInfo.FPath = "./lib/" + directory
		if item.IsDir() == true {
			tempInfo.FType = "DIR"
		} else {
			tempInfo.FType = "FILE"
		}
		contentsList = append(contentsList, tempInfo)
	}

	// Create a list of directories from contentsList if required by CLI arguments
	var directoriesList []string
	for _, item := range contentsList {
		if item.FType == "DIR" {
			directoriesList = append(directoriesList, item.FPath+"/"+item.FName)
		}
	}

	// Create a list of directories from contentsList if required by CLI arguments.
	var filesList []string
	for _, item := range contentsList {
		if item.FType == "FILE" {
			filesList = append(filesList, item.FPath+"/"+item.FName)
		}
	}

	// Check for .categories file
	var catIndex int
	var catFound bool
	catIndex, catFound = findFile(filesList, ".categories")

	// ***** DEBUG *****
	fmt.Println()
	fmt.Print("Directories: ")
	fmt.Println(directoriesList)
	fmt.Println()
	fmt.Print("Files: ")
	fmt.Println(filesList)
	fmt.Println()
	fmt.Print("All Contents: ")
	fmt.Println(contentsList)
	fmt.Println()
	fmt.Print("Found .categories: ")
	fmt.Print(catIndex)
	fmt.Print(": ")
	fmt.Println(catFound)

	return contentsList
}

/**
 **	Function to find a string (file) in a slice of filenames.
 *	@param sliceToSearch []string: Slice to be searched
 *	@param findString string: Filename to search for
 **	Returns:
 **		1. int: Index number of found file. -1 if not found.
 **		2. bool: True if found, False if not found.
 */
func findFile(sliceToSearch []string, findString string) (int, bool) {
	for i, item := range sliceToSearch {
		if item == findString {
			return i, true
		}
	}
	return -1, false
}

/**
 **	Function to return a list (slice) if filenames to be ignored
 **	These are generally files put in place by GitHub for various
 **	purposes, and are irrelevant as wordlists.
 */
func checkIgnore() []string {
	ignoreItems := []string{
		"LICENSE",
		"README",
		"README.md",
		"CODE_OF_CONDUCT.md",
		".git",
		".gitignore",
		".github",
		".gitattributes",
	}
	return ignoreItems
}
