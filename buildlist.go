package main
/** 
 * Builds a directory of wordlists from gathered wordlists.
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
	"bufio"
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"strings"
)

/**
 * Structure to hold basic file information
 * FName is the filename
 * FPath is the absolute path to the file
 * FCats is a slice containing the categories that the file belongs to
 */
type fileInfo struct {
	FName string
	FPath string
	FCats []string
}

// Main function
func main() {
	fmt.Println("It begins...")
	readDir("lib/")														//Sets the directory to start from
	var fileList []fileInfo												//Set up the slice to hold file Information
	var categoryList []string											//Set up the slice to hold categories
	fileList = readDir("lib/")											//Get all of the filenames
	categoryList = getCategories(fileList)								//Compile a list of unique category names from fileList
	createDirs(categoryList)											//Create directories for categories
	createSymlinks(fileList)											//Create symlinks of lists in directories just created
	fmt.Println("It is done!")
}

/**
 * Usage: readDir(path-to-start) 
 * returns []fileInfo
 * 
 * readDir function recursively scans the directories belowthe supplied 
 * starting directory (in this case, lib/)
 * 
 * basePath [string] - This is the starting directory for file searching
 * 
 * The objective is to find a ".categories" file for each directory that
 * has wordlists to be included.
 * 
 * The .categories files must be formatted in the following way, with one
 * line per text file to index:
 * [Filename]:[Comma,Separated,Categories,List]
 * 
 * Note that category entries do allow multiword categories to be used
 * 
 * The function will take care of saving the absolute path to the file, but
 * the directory provided must end with a trailing /
 */
func readDir(basePath string) []fileInfo {
	var returnList []fileInfo											//This is the slice holding file information
	var tempList []fileInfo												//This is the slice holding the returned lists from recursively-called functions
	files, err := ioutil.ReadDir(basePath)								//Read the directory, gather filenames
	if err != nil {
		log.Fatal(err)													//Error logging
	}
	for _, f := range files {											//Iterate throm directory contents to find .categories and sub-directories
		if f.IsDir() {													//Check to see if the item is a directory
			tempList = readDir(basePath + f.Name() + "/")				//Recursively call function to descend into sub-directories
			for _, line := range tempList {
				returnList = append(returnList,line)
			}
		} else {														//For those not-so-directory moments
			if f.Name() == ".categories" {								//Check to see if the item is the .categories file
				file, err := os.Open(basePath + ".categories")
				if err != nil {
					log.Fatal(err)										//Error logging
					return nil											//Return nothing on error
				}
				defer file.Close()										//Close the file after function exits
				scanner := bufio.NewScanner(file)						//Scanner object to scan .categories
				for scanner.Scan() {
					var returnFile fileInfo								//Set up an object to hold file information
					fileString := strings.Split(scanner.Text(), ":")	//Split the line to a filename and categories
					categories := strings.Split(fileString[1], ",")		//Split the categories into individual elements.
					returnFile.FName = fileString[0]					//Set file properties
					returnFile.FPath = basePath + fileString[0]			//Set file properties
					returnFile.FCats = categories						//Set file properties
					returnList = append(returnList, returnFile)			//Append file information to returnList
				}
				if err := scanner.Err(); err != nil {
					log.Fatal(err)										//Error logging
				}
			}
		}
	}
	return returnList													//Return returnList to calling function
}

/**
 * Usage: createSymlinks(fileList []fileInfo)
 * 
 * createSymlinks takes the information that was gathered with readDir
 * and creates the category directories and symbli9nks in the Wordlists
 * directory.
 * 
 * fileList is a slice of time fileInfo. It should contain all of the 
 * data garnered from the function readDir(). It is possible to use
 * this function manually, but it is designed for use in the way above.
 * 
 * This function should be called either to work in a directory with a 
 * static filestructure, or after createDirs() has been run
 */
func createSymlinks(fileList []fileInfo){
	basePath := "Wordlists/"										//Sets the base path for symlinking
//	fmt.Println(basePath)
	for _, file := range fileList{									//Iterate through each file in fileList
		cats := file.FCats											//Set the categories to symlink in
//		fmt.Println(cats)
		for _, cat := range cats{									//Iterate over categories to create symlinks
			tempPath := basePath + cat + "/" + file.FName			//Set up the path to symlink to
//			fmt.Println(cat)
//			fmt.Println(tempPath)
			os.Symlink(file.FPath, tempPath)						//Symlink the file
		}
	}
}

/**
 * Usage: createDirs(categoryList []string)
 * 
 * Creates the directories for the various categories
 */
func createDirs(categoryList []string){
	basePath := "Wordlists/"										//Sets the base path to create category directories in
	for _, category := range categoryList {							//Iterate through the category list
		fmt.Println(basePath + category)
		os.Mkdir((basePath + category), 0777)						//Make the directories
	}
}

/**
 * Usage: getCategories(fileList []fileInfo) 
 * returns []string
 * 
 * This function assembles all of the categories assigned in a fileList
 * and removes the duplicates, leaving a simple list to create of directories
 * instead of checking with each category to see if the directory yet exists
 */
func getCategories(fileList []fileInfo) []string {
	var categoryList []string										//List to hold categories to return
	for _, file := range fileList {
		var tempCatList []string									//Temporary list to iterate over and gather categories
		tempCatList = file.FCats									//Loads categories from the current file to tempCatList
		for cat := range tempCatList {								//Iterate over tempCatList to check categories
			_, found := Find(categoryList, tempCatList[cat])		//Check to see if the category has already been loaded
			if !found {												//If the category has not been loaded, add it
				categoryList = append(categoryList,tempCatList[cat])//Append to categoryList
			}
		}
	}
	return categoryList
}

/**
 * Usage: Find(list []string, val string)
 * Returns: int, bool
 * 
 * Finds the index of a value in a list, and returns the index value
 * If the item is found, it returns True
 * If the item is not found, it returns False
 */
func Find(list []string, val string) (int, bool) {
	for i, item := range list {										//Iterate through the passed list of strings to see if it exists in a larger group of strings
		if item == val {											//See if the item is in the list
			return i, true											//If so, return the index and that it was found
		}
	}
	return -1, false												//Otherwise, return an index of -1 and false
}

/**
 * Usage: checkDir(dirPath string)
 * Returns: bool
 * 
 * Checks to see if the .categories file exists in the directory
 * supplied (dirPath) and returns true/false
 */
func checkCats(dirPath string) (bool) {
	var catsExist bool													//Holds true/false value of if .categories exist
	if _, err := os.Stat(dirPath + ".categories"); os.IsNotExist(err) {	//Checks to see if .categories exist
		catsExist = false												//Returns false if not
	} else {
		catsExist = true												//Otherwise returns true
	}
	return catsExist
}

/**
 * Usage: checkDir(dirPath string)
 * Returns: []string
 * 
 * Checks for subdirectories and returns a list of subdirectories in the
 * directory supplied (dirPath)
 */
func checkDir(dirPath string) []string {
	var dirList []string
	files, err := ioutil.ReadDir(dirPath)								//Read the directory, gather filenames
	if err != nil {
		log.Fatal(err)													//Error logging
	}
	for _, f := range files {											//Iterate throm directory contents to find sub-directories
		if f.IsDir() {													//Check to see if the item is a directory
			dirList = append(dirList,dirPath + f.Name())				//If so, add it to the list
		}
	}
	return dirList
}

func configCheck(basePath string) {
}