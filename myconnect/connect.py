# -*- coding: utf-8 -*-
"""
@author: alchenerd (alchenerd@gmail.com)
"""
import sqlite3

_default_database = "HVHNONC.db"


def _get_connection(databaseName: str = _default_database):
    connect = sqlite3.connect(databaseName)
    cursor = connect.cursor()
    return connect, cursor
    row = cur.execute(sqlstr, params).fetchone()
    try:
        return row[0]
    except Exception as e:
        print(e, name)
        return None

def get_ch_name(name: str):
    try:
        name.encode('ascii')
    except UnicodeEncodeError:
        return name
    con, cur = _get_connection()
    sqlstr = ('select ch_name from hvhnonc_fields where en_name=? limit 1;')
    params = (name,)
    row = cur.execute(sqlstr, params).fetchone()
    try:
        return row[0]
    except Exception as e:
        if name not in ('ID, old_ID'):
            print(e, name, 'get_ch_name')
        return name

def get_field_id(name: str) -> int:
    con, cur = _get_connection()
    sqlstr = ('select ID '
              'from hvhnonc_fields '
              'where ch_name=:name '
              'or en_name=:name')
    params = {'name': name}
    row = cur.execute(sqlstr, params).fetchone()
    try:
        return row[0]
    except Exception as e:
        print(e, name, 'get_field_id')
        return None
