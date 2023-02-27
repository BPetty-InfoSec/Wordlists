import bin.mainmenu as menu
import sqlite3

con = sqlite3.connect("bin/wordlists.db")
cur = con.cursor()

def main():
    menu.DisplayMenu()

main()