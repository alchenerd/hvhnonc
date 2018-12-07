# -*- coding: utf-8 -*-
"""
@author: alchenerd (alchenerd@gmail.com)
"""

from PyQt5 import QtWidgets, QtCore
from typing import Dict
import sqlite3
# These modules are mine
if __name__ == '__main__':
    from _register_skeleton import Ui_Dialog as RegisterDialog
    import sys
    sys.path.append('../')
    from myconnect import connect
else:
    from myqtpy._register_skeleton import Ui_Dialog as RegisterDialog
    from myconnect import connect

class Register(QtWidgets.QDialog, RegisterDialog):
    def __init__(self, dialog):
        super(self.__class__, self).__init__(dialog)
        self.setupUi(dialog)
        self.returnBtn.clicked.connect(dialog.reject)
        self.createBtn.clicked.connect(self.on_createBtn_clicked)
        self.category.currentTextChanged.connect(self.on_category_changed)
        self.name.currentTextChanged.connect(self.on_name_changed)
        self.subcategory.currentTextChanged.connect(
                self.on_subcategory_changed)
        self.idDict = self.get_id_dict()
        self.idIndex = -1
        self.getNextBtn.clicked.connect(self.onclick_next_record)
        self.getPreviousBtn.clicked.connect(self.onclick_previous_record)
        self.disable_all_fields()
        self.clear_all_fields()

    def onclick_previous_record(self):
        # modify idIndex
        if self.idIndex == -1:
            self.idIndex = len(self.idDict) - 1
        elif self.idIndex == 0:
            QtWidgets.QMessageBox.warning(self, u'到頂了', u'已到達第一筆')
        else:
            self.idIndex -= 1
        print('previous: {}'.format(self.idIndex))
        # update view using new idIndex
        record = self.get_record(self.idDict[self.idIndex])
        self.init_all_fields()
        self.update_by_record(record)

    def onclick_next_record(self):
        # modify idIndex
        if self.idIndex == -1:
            self.idIndex = 0
        elif self.idIndex == len(self.idDict) - 1:
            QtWidgets.QMessageBox.warning(self, u'到底了', u'已到達最末筆')
        else:
            self.idIndex += 1
        # update view using new idIndex
        record = self.get_record(self.idDict[self.idIndex])
        print('next: {}'.format(self.idIndex))
        self.init_all_fields()
        self.update_by_record(record)

    def update_by_record(self, rec: sqlite3.Row):
        for k in rec.keys():
            try:
                x = getattr(self, k)
                if isinstance(x, QtWidgets.QComboBox):
                    if x.isEditable():
                        x.setEditText(rec[k])
                    else:
                        x.setCurrentText(rec[k])
                elif isinstance(x, QtWidgets.QLineEdit):
                    x.setText(str(rec[k]))
                elif isinstance(x, QtWidgets.QDateEdit):
                    year, month, day = map(int, rec[k].split('-'))
                    date = QtCore.QDate(year, month, day)
                    x.setDate(date)
            except Exception as e:
                if k != 'ID':
                    print(e)

    def get_record(self, index: int):
        con, cursor= connect._get_connection()
        con.row_factory = sqlite3.Row
        cursor = con.cursor()
        sqlstr = ('select * from hvhnonc_in where ID=?')
        params = (str(index),)
        cursor.execute(sqlstr, params)
        return cursor.fetchone()

    def get_id_dict(self):
        con, cursor= connect._get_connection()
        sqlstr = ('select ID from hvhnonc_in order by acquire_date;')
        cursor.execute(sqlstr)
        rows = cursor.fetchall()
        return {i: row[0] for i, row in enumerate(rows)}

    def on_name_changed(self):
        # update unit, brand, spec from hvhnonc_in_cache
        con, cursor= connect._get_connection()
        sqlstr = ('select change_value '
                  'from hvhnonc_in_cache '
                  'where this_ID=? '
                  'and this_value=? '
                  'and change_ID=?')
        params = [connect.get_field_id(connect.get_description('name')),
                  self.name.currentText()]
        # unit
        p = params + [connect.get_field_id(connect.get_description('unit')),]
        cursor.execute(sqlstr, p)
        rows = cursor.fetchall()
        self.unit.clear()
        if rows:
            self.unit.addItems([row[0] for row in rows])
        # brand
        p = params + [connect.get_field_id(connect.get_description('brand')),]
        cursor.execute(sqlstr, p)
        rows = cursor.fetchall()
        self.brand.clear()
        if rows:
            self.brand.addItems([row[0] for row in rows])
        # spec
        p = params + [connect.get_field_id(connect.get_description('spec')),]
        cursor.execute(sqlstr, p)
        rows = cursor.fetchall()
        self.spec.clear()
        if rows:
            self.spec.addItems([row[0] for row in rows])

    def on_subcategory_changed(self):
        # update name from hvhnonc_in_cache
        con, cursor= connect._get_connection()
        sqlstr = ('select change_value '
                  'from hvhnonc_in_cache '
                  'where this_ID=? '
                  'and this_value=? '
                  'and change_ID=?')
        params = [
                connect.get_field_id(connect.get_description('subcategory')),
                self.subcategory.currentText(),
                connect.get_field_id(connect.get_description('name'))]
        cursor.execute(sqlstr, params)
        rows = cursor.fetchall()
        self.name.clear()
        if rows:
            self.name.addItems([row[0] for row in rows])
        self.name.clearEditText()

    def on_category_changed(self):
        # update subcategory
        con, cursor= connect._get_connection()
        sqlstr = ('select description '
                  'from hvhnonc_subcategory '
                  'where parent_ID=('
                  'select ID '
                  'from hvhnonc_category '
                  'where description=?);')
        params = (self.category.currentText(),)
        cursor.execute(sqlstr, params)
        rows = cursor.fetchall()
        options = [row[0] for row in rows]
        self.subcategory.clear()
        self.subcategory.addItems(options)

    def on_createBtn_clicked(self):
        self.idIndex = -1
        self.init_all_fields()

    def init_all_fields(self):
        self.enable_all_fields()
        self.clear_all_fields()
        widgetsToInit = {k: i for k , i in self.__dict__.items()
                         if isinstance(i, QtWidgets.QComboBox)}
        # discard subcategory, name, unit, brand, spec
        blacklist = ('subcategory', 'name', 'unit', 'brand', 'spec')
        for i in blacklist:
            widgetsToInit.pop(i)
        self.fetch_options(widgetsToInit)

    def fetch_options(self, d: Dict[str, QtWidgets.QComboBox]):
        con, cursor= connect._get_connection()
        for key, widget in d.items():
            # constant choices
            if key == 'source':
                options = ['購置', '撥用', '贈送']
                widget.addItems(options)
                continue
            # fetch options from hvhnonc_category
            elif key == 'category':
                sqlstr = ('select description '
                          'from hvhnonc_category '
                          'order by ID')
                cursor.execute(sqlstr)
                rows = cursor.fetchall()
                options = [row[0] for row in rows]
                widget.addItems(options)
                widget.clearEditText()
            # fetch options from hvhnonc_in_cache
            else:
                sqlstr = ('select change_value '
                          'from hvhnonc_in_cache '
                          'where this_ID=0 and '
                          'change_ID=?')
                params = (connect.get_field_id(connect.get_description(key)),)
                cursor.execute(sqlstr, params)
                rows = cursor.fetchall()
                options = [row[0] for row in rows]
                widget.addItems(options)
                widget.clearEditText()
        con.close()

    def enable_all_fields(self):
        widgetsToEnable = {k: i for k , i in self.__dict__.items() if (
                isinstance(i, QtWidgets.QComboBox) or
                isinstance(i, QtWidgets.QLineEdit) or
                isinstance(i, QtWidgets.QDateEdit))}
        for w in widgetsToEnable.values():
            w.setEnabled(True)

    def disable_all_fields(self):
        widgetsToDisable = {k: i for k , i in self.__dict__.items() if (
                isinstance(i, QtWidgets.QComboBox) or
                isinstance(i, QtWidgets.QLineEdit) or
                isinstance(i, QtWidgets.QDateEdit))}
        for w in widgetsToDisable.values():
            w.setEnabled(False)

    def clear_all_fields(self):
        widgetsToClear = {k: i for k , i in self.__dict__.items() if (
                isinstance(i, QtWidgets.QComboBox) or
                isinstance(i, QtWidgets.QLineEdit) or
                isinstance(i, QtWidgets.QDateEdit))}
        for i in widgetsToClear.values():
            if isinstance(i, QtWidgets.QComboBox):
                i.clearEditText()
                i.clear()
            elif isinstance(i, QtWidgets.QLineEdit):
                i.clear()
            elif isinstance(i, QtWidgets.QDateEdit):
                date = QtCore.QDate()
                date = QtCore.QDate.currentDate()
                i.setDate(date)

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Register(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
