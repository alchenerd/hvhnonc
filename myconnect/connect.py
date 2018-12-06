# -*- coding: utf-8 -*-
"""
@author: alchenerd (alchenerd@gmail.com)
"""
import sqlite3

_default_database = "HVHNONC.db"

def _get_connection(databaseName: str = _default_database):
    connect = sqlite3.connect(databaseName)
    return connect
