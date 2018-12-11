# -*- coding: utf-8 -*-
"""
@author: alchenerd (alchenerd@gmail.com)
"""
from PyQt5 import QtWidgets
from typing import Tuple
import sqlite3

# These modules are mine
if __name__ == '__main__':
    from _search_result_skeleton import Ui_Dialog as SearchResultDialog
    import sys
    sys.path.append('../')
else:
    from myqtpy._search_result_skeleton import Ui_Dialog as SearchResultDialog
from myconnect import connect

class SearchResult(QtWidgets.QDialog, SearchResultDialog):
    def __init__(self, dialog, sqlstr: str, params: Tuple[str, ...]):
        super(self.__class__, self).__init__(dialog)
        self.setupUi(dialog)
        con, cursor = connect._get_connection()
        con.row_factory = sqlite3.Row
        cursor = con.cursor()
        self.sqlstr = sqlstr
        self.params = params
        rows = None
        try:
            cursor.execute(sqlstr, params)
            rows = cursor.fetchall()
        except Exception as e:
            print("Error in SearchResult", e)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(0)
        if rows and len(rows):
            colLen = len(rows[0])
        else:
            colLen = 0
        self.tableWidget.setColumnCount(colLen)
        if rows and len(rows):
            print(rows[0].keys())
            headerLabels = [connect.get_description(i) for i in rows[0].keys()]
            self.tableWidget.setHorizontalHeaderLabels(headerLabels)
        for i, row in enumerate(rows):
            self.tableWidget.insertRow(i)
            for j, k in enumerate(row.keys()):
                self.tableWidget.setItem(
                        i, j, QtWidgets.QTableWidgetItem(str(row[k])))


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    sqlstr = ('select * from hvhnonc_fields')
    params = None
    ui = SearchResult(Dialog, sqlstr, params)
    Dialog.show()
    sys.exit(app.exec_())
