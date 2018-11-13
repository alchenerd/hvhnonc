# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 16:44:09 2018

@author: alchenerd (alchenerd@gmail.com)

Builds a database for furthur use
"""

import sqlite3

def buildDatabase(sqlname: str = "HVHNONC.db.sql", dbname: str = "HVHNONC.db"):
    executeScriptsFromFile(sqlname, dbname)


def executeScriptsFromFile(filename, DBname):
    # Open and read the file as a single buffer
    connect = sqlite3.connect(DBname)
    cursor = connect.cursor()
    fd = open(filename, 'r', encoding="utf-8")
    sqlFile = fd.read()
    fd.close()
    sqlCommands = sqlFile.split(';')
    sqlCommands.pop(0)
    for command in sqlCommands:
        try:
            cursor.execute(command)
        except Exception as e:
            print("init.py: ", e)
    connect.close()