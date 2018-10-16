# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 16:44:09 2018

@author: alchenerd (alchenerd@gmail.com)

initialization of the dbms
"""

import sqlite3

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