# -*- coding: utf-8 -*-
"""
Created on Tue Oct  2 11:08:53 2018

@author: 戴佳燊 (alchenerd@gmail.com)

@project name: HVHNONC
               (Hualien Veterans Home NON-Consumables dbms)
"""
import tkinter as tk
import sqlite3

import noncgui as gui


def tableInit():
    executeScriptsFromFile("HVHNONC.db.sql", "HVHNONC.db")


def executeScriptsFromFile(filename, DBname):
    # Open and read the file as a single buffer
    connect = sqlite3.connect(DBname)
    cursor = connect.cursor()
    fd = open(filename, 'r', encoding="utf-8")
    sqlFile = fd.read()
    fd.close()

    # all SQL commands (split on ';')
    sqlCommands = sqlFile.split(';')

    # discard 'BEGIN TRANSACTION...'
    sqlCommands.pop(0)

    # Execute every command from the input file
    for command in sqlCommands:
        # This will skip and report errors
        # For example, if the tables do not yet exist, this will skip over
        # the DROP TABLE commands
        try:
            cursor.execute(command)
        except Exception as inst:
            print("Command skipped: ", inst)
    connect.close()


def main():
    tableInit()
    root = tk.Tk()
    root.option_add('*TCombobox*Listbox.font', (None, 15))
    gui.Index(root)
    root.mainloop()
    root.quit()


if __name__ == "__main__":
    main()