# -*- coding: utf-8 -*-
"""
@author: alchenerd (alchenerd@gmail.com)
"""
import sqlite3

_default_database = "HVHNONC.db"

def _get_connection(databaseName: str = _default_database,
                    useSQL3Row: bool = False):
    """Return a sqlite3 connection and it's cursor.

    User can set useSQL3Row to true, making cursor return sqilte3.Row"""
    connect = sqlite3.connect(databaseName)
    if useSQL3Row:
        connect.row_factory = sqlite3.Row
    cursor = connect.cursor()
    return connect, cursor

def get_ch_name(name: str):
    """Return a chinese name according to the database."""
    try:
        name.encode('ascii')
    # Not returning None beacause we need a usable name
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
    """Return a column's ID(which is a field in the GUI form)."""
    con, cur = _get_connection()
    sqlstr = (
            'select '
                'ID '
            'from '
                'hvhnonc_fields '
            'where '
                'ch_name=:name '
            'or '
                'en_name=:name')
    params = {'name': name}
    row = cur.execute(sqlstr, params).fetchone()
    try:
        return row[0]
    except Exception as e:
        print(e, name, 'get_field_id')
        return None
