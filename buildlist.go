package main

/** 
 * Refactoring buildlist.py into Golang 
 * Objectives are improvements in behavior
 * with regards to similarly named files,
 * as well as adding a categorization system
 * to make finding right list easier.
*/

import (
	"bufio"
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"strings"
)

// Structure to hold necessary file information
type fileInfo struct {
	FName string
	FPath string
	FCats []string
}

// Main function
func main() {
	readDir("lib/")
	var fileList []fileInfo
	fileList = readDir("lib/")
	fmt.Print("fileList: ")
	fmt.Println(fileList)
}

/**
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
	var returnList []fileInfo					//This is the slice holding file information
	var tempList []fileInfo						//This is the slice holding the returned lists from recursively-called functions
	files, err := ioutil.ReadDir(basePath)		//Read the directory, gather filenames
	if err != nil {
		log.Fatal(err)							//Error logging
	}
	for _, f := range files {					//Iterate throm directory contents to find .categories and sub-directories
		if f.IsDir() {							//Check to see if the item is a directory
			fmt.Println("-- " + f.Name() + " is a directory! Descending into directory.")
			tempList = readDir(basePath + f.Name() + "/")	//Recursively call function to descend into sub-directories
			for _, line := range tempList {
				returnList = append(returnList,line)
			}
		} else {								//For those not-so-directory moments
			fmt.Println("-- " + f.Name() + " is not a directory")
			if f.Name() == ".categories" {		//Check to see if the item is the .categories file
				file, err := os.Open(basePath + ".categories")
				if err != nil {
					log.Fatal(err)				//Error logging
					return nil					//Return nothing on error
				}
				defer file.Close()				//Close the file after function exits
				scanner := bufio.NewScanner(file)	//Scanner object to scan .categories
				for scanner.Scan() {
					fmt.Println("Start for")
					var returnFile fileInfo		//Set up an object to hold file information
					fmt.Println(scanner.Text())
					fileString := strings.Split(scanner.Text(), ":")	//Split the line to a filename and categories
					categories := strings.Split(fileString[1], ",")		//Split the categories into individual elements.
					returnFile.FName = fileString[0]					//+--\
					returnFile.FPath = basePath + fileString[0]			//+---Set file properties
					returnFile.FCats = categories						//+--/
					fmt.Println(categories)
					fmt.Println(returnFile)
					fmt.Print("returnList: ")
					fmt.Println(returnList)
					returnList = append(returnList, returnFile)			//Append file information to returnList
				}
				if err := scanner.Err(); err != nil {
					log.Fatal(err)				//Error logging
				}
			}
		}
	}
	return returnList							//Return returnList to calling function
}
