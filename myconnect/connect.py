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


# return a chinese name 'description' of a english field name
def get_description(engName: str):
    # TODO: This list in not yet complete
    _DICT = {'none': u'無',
             'category': u'物品大項',
             'subcategory': u'物品細目',
             'name': u'物品名稱',
             'unit': u'單位',
             'brand': u'品牌',
             'spec': u'規格',
             'objectID': u'物品編號',
             'serial': u'流水號',
             'source': u'來源',
             'price': u'價格',
             'amount': u'數量',
             'place': u'存置地點',
             'keepYear': u'保管年限',
             'keepDepartment': u'保管單位',
             'useDepartment': u'使用單位',
             'keeper': u'保管人',
             'remark': u'備註事項'}
    return _DICT.get(engName, None)


def get_field_id(chName: str):
    con, cur = _get_connection()
    sqlstr = ('select ID from hvhnonc_fields where description=?')
    params = (chName, )
    row = cur.execute(sqlstr, params).fetchone()
    return row[0]
