# -*- coding: utf-8 -*-
"""
@author: alchenerd (alchenerd@gmail.com)
"""

from PyQt5 import QtWidgets, QtCore
from typing import Dict
import sqlite3
import sys

# These modules are mine
if __name__ == '__main__':
    sys.path.append('../')
else:
    sys.path.append('./myqtpy/')
from _register_skeleton import Ui_Dialog as RegisterDialog
from SearchBox import SearchBox
from SearchResult import SearchResult
from Filter import Filter
from myconnect import connect

class Register(QtWidgets.QDialog, RegisterDialog):
    def __init__(self, dialog):
        super(self.__class__, self).__init__(dialog)
        self.setupUi(dialog)
        self.returnBtn.clicked.connect(dialog.reject)
        self.createBtn.clicked.connect(self.on_createBtn_clicked)
        self.saveBtn.clicked.connect(self.on_saveBtn_clicked)
        self.deleteBtn.clicked.connect(self.on_deleteBtn_clicked)
        self.searchBtn.clicked.connect(self.on_searchBtn_clicked)
        self.formBtn.clicked.connect(self.on_formBtn_clicked)
        self.category.currentTextChanged.connect(self.on_category_changed)
        self.subcategory.currentTextChanged.connect(
                self.on_subcategory_changed)
        self.name.currentTextChanged.connect(self.on_name_changed)
        self.idDict = self.get_id_dict()
        self.idIndex = -1
        self.getNextBtn.clicked.connect(self.onclick_next_record)
        self.getPreviousBtn.clicked.connect(self.onclick_previous_record)
        self.lookupSerialBtn.clicked.connect(self.on_serial_lookup_clicked)
        self.isEnabled = None
        self.clear_all_fields()
        self.disable_all_fields()

    def on_serial_lookup_clicked(self):
        # open a result window
        sqlstr = ("select object_ID, name, count(*) as '數量' "
                  "from hvhnonc_in group by name")
        self.resultWindow = QtWidgets.QDialog()
        params = []
        self.sr = SearchResult(self.resultWindow, sqlstr, params)
        self.resultWindow.resize(320,600)
        self.sr.tableWidget.doubleClicked.disconnect()
        self.resultWindow.exec_()

    def on_formBtn_clicked(self):
        # open a filter window
        self.filterWindow = QtWidgets.QDialog()
        Filter(self.filterWindow)
        returnID = self.filterWindow.exec()
        if not returnID:
            return
        # update the self.idIndex
        self.idIndex = self.getIdIndex(returnID)
        # fetch a record from the db
        con, cursor= connect._get_connection()
        con.row_factory = sqlite3.Row
        cursor = con.cursor()
        sqlstr = ('select * from hvhnonc_in where ID=?')
        params = (returnID,)
        cursor.execute(sqlstr, params)
        record = cursor.fetchone()
        con.close()
        self.init_all_fields()
        self.update_by_record(record)

    def on_searchBtn_clicked(self):
        # open a search box
        self.sb = QtWidgets.QDialog()
        SearchBox(self.sb, 'in')
        # self.sb.exec_() returns a hvhnonc_in ID
        returnID = self.sb.exec_()
        if returnID == 0:
            return
        self.idIndex = self.getIdIndex(returnID)
        # set self id index
        for k, i in self.idDict.items():
            if i == returnID:
                self.idIndex = k
        # fetch a record from the db
        con, cursor= connect._get_connection()
        con.row_factory = sqlite3.Row
        cursor = con.cursor()
        sqlstr = ('select * from hvhnonc_in where ID=?')
        params = (returnID,)
        cursor.execute(sqlstr, params)
        record = cursor.fetchone()
        con.close()
        self.init_all_fields()
        self.update_by_record(record)

    def on_saveBtn_clicked(self):
        if not self.isEnabled:
            return
        if not self.form_is_valid():
            return
        if self.idIndex == -1:
            # a new record
            self.save_as_new()
        elif self.idIndex in range(len(self.idDict.keys())):
            # index in history, ask for write over or save as new
            qmb = QtWidgets.QMessageBox(self)
            qmb.setIcon(QtWidgets.QMessageBox.Question)
            qmb.setWindowTitle(u'要覆蓋嗎?')
            qmb.setText(u'請選擇本筆儲存方式')
            qmb.addButton('覆蓋本筆', QtWidgets.QMessageBox.YesRole)
            qmb.addButton('新增一筆', QtWidgets.QMessageBox.NoRole)
            qmb.addButton('取消', QtWidgets.QMessageBox.RejectRole)
            reply = qmb.exec_()
            # hacky since the reply is questionably coded
            dActions = {
                    0: lambda: self.write_over(
                            str(self.idDict[self.idIndex])),
                    1: self.save_as_new,
                    2: lambda: None}
            dActions[reply]()

    # validate the form, and pop messagebox if invalid
    def form_is_valid(self) -> bool:
        messagebox = QtWidgets.QMessageBox(self)
        messagebox.addButton('確認', QtWidgets.QMessageBox.YesRole)
        messagebox.setWindowTitle('錯誤')
        messagebox.setIcon(QtWidgets.QMessageBox.Critical)
        msg = '在以下欄位發現有問題：\n'
        isValid = True
        # category: not null
        if not self.category.currentText():
            isValid = False
            msg += '-物品大項未填\n'
        # subcategory: not null
        if not self.subcategory.currentText():
            isValid = False
            msg += '-物品細目未填\n'
        # name: not null
        if not self.name.currentText():
            isValid = False
            msg += '-物品名稱未填\n'
        # price: int not null > 0
        price = self.price.text()
        if not price:
            isValid = False
            msg += '-單價未填\n'
        elif (not price.isnumeric() or int(price) < 0):
            isValid = False
            msg += '-單價須為正數\n'
        # amount: int not null >0
        amount = self.amount.text()
        if not amount:
            isValid = False
            msg += '-數量未填\n'
        elif (not amount.isnumeric() or int(amount) < 0):
            isValid = False
            msg += '-數量須為正數\n'
        # keep_year: int not null >0
        keep_year = self.keep_year.text()
        if not keep_year:
            isValid = False
            msg += '-保管年限未填\n'
        elif (not keep_year.isnumeric() or int(keep_year) < 0):
            isValid = False
            msg += '-保管年限須為正數\n'
        # keep_department: not null
        if not self.keep_department.currentText():
            isValid = False
            msg += '-保管單位未填\n'
        if not isValid:
            messagebox.setText(msg[:-1])
            messagebox.exec_()
        return isValid

    def save_as_new(self):
        con, cursor= connect._get_connection()
        # detemine the object_ID and serial_ID
        sqlstr = ('select parent_ID, ID '
                  'from hvhnonc_subcategory '
                  'where parent_ID=('
                  'select ID '
                  'from hvhnonc_category '
                  'where description=?) '
                  'and description=?;')
        params = (self.category.currentText(), self.subcategory.currentText())
        cursor.execute(sqlstr, params)
        row = cursor.fetchone()
        row = ('6', '{:02d}'.format(row[0]), '{:02d}'.format(row[1]))
        object_ID = ' - '.join(row)
        sqlstr = ('select max(serial_ID) '
                  'from hvhnonc_in '
                  'where object_ID=? and name=?')
        name = self.name.currentText()
        params = (object_ID, name)
        cursor.execute(sqlstr, params)
        row = cursor.fetchone()
        if row and row[0]:
            serial_ID = '{:03}'.format(int(row[0]) + 1)
        else:
            serial_ID = '001'
        # save as new using sqlite
        sqlstr = ('insert into hvhnonc_in('
                  'object_ID, serial_ID, category, subcategory, '
                  'name, brand, spec, unit, purchase_date, acquire_date, '
                  'price, amount, place, keep_year, source, '
                  'keep_department, use_department, keeper, '
                  'remark) '
                  'values({});')
        params = (object_ID, serial_ID,
                  self.category.currentText(),
                  self.subcategory.currentText(),
                  self.name.currentText(),
                  self.brand.currentText(),
                  self.spec.currentText(),
                  self.unit.currentText(),
                  self.purchase_date.date().toPyDate(),
                  self.acquire_date.date().toPyDate(),
                  self.price.text(),
                  self.amount.text(),
                  self.place.currentText(),
                  self.keep_year.text(),
                  self.source.currentText(),
                  self.keep_department.currentText(),
                  self.use_department.currentText(),
                  self.keeper.currentText(),
                  self.remark.currentText())
        questionmarks = ('?, ' * len(params))[:-2]
        cursor.execute(sqlstr.format(questionmarks), params)
        con.commit()
        con.close()
        # update field cache
        self.update_field_cache()
        # show success messagebox
        QtWidgets.QMessageBox.information(
                self, u'成功',
                u'已新增一筆資料: {}'.format(self.name.currentText()))
        # reset form
        self.clear_all_fields()
        self.disable_all_fields()

    def write_over(self, id: str):
        con, cursor= connect._get_connection()
        sqlstr = ('replace into hvhnonc_in('
                  'ID, object_ID, serial_ID, '
                  'category, subcategory, '
                  'name, brand, spec, unit, '
                  'purchase_date, acquire_date, '
                  'price, amount, place, '
                  'keep_year, source, '
                  'keep_department, use_department, '
                  'keeper, remark) '
                  'values({});')
        params = (self.idDict[self.idIndex],
                  self.object_ID.text(),
                  self.serial_ID.text(),
                  self.category.currentText(),
                  self.subcategory.currentText(),
                  self.name.currentText(),
                  self.brand.currentText(),
                  self.spec.currentText(),
                  self.unit.currentText(),
                  self.purchase_date.date().toPyDate(),
                  self.acquire_date.date().toPyDate(),
                  self.price.text(),
                  self.amount.text(),
                  self.place.currentText(),
                  self.keep_year.text(),
                  self.source.currentText(),
                  self.keep_department.currentText(),
                  self.use_department.currentText(),
                  self.keeper.currentText(),
                  self.remark.currentText())
        questionmarks = ('?, ' * len(params))[:-2]
        cursor.execute(sqlstr.format(questionmarks), params)
        con.commit()
        con.close()
        self.update_field_cache()
        # show success messagebox
        msg = u'已複寫一筆資料: {}({})'.format(
                self.name.currentText(), self.idDict[self.idIndex])
        QtWidgets.QMessageBox.information(self, u'成功', msg)
        # reset form
        self.clear_all_fields()
        self.disable_all_fields()

    def update_field_cache(self):
        con, cursor= connect._get_connection()
        comboboxes = {k:w for k, w in self.__dict__.items()
                if isinstance(w, QtWidgets.QComboBox)}
        for k, w in comboboxes.items():
            sqlstr = ('insert or ignore into '
                      'hvhnonc_cache(this_ID, this_value, '
                      'change_ID, change_value) '
                      'values(?, ?, ?, ?);')
            if k in ('category', 'subcategory', 'source'):
                continue
            if k in ('name'):
                params = (connect.get_field_id('subcategory'),
                          self.subcategory.currentText(),
                          connect.get_field_id(k),
                          w.currentText())
            elif k in ('unit', 'brand', 'spec'):
                params = (connect.get_field_id('name'),
                          self.name.currentText(),
                          connect.get_field_id(k),
                          w.currentText())
            else:
                params = (0, '',
                          connect.get_field_id(k),
                          w.currentText())
            cursor.execute(sqlstr, params)
        con.commit()
        con.close()

    def on_deleteBtn_clicked(self):
        if not self.isEnabled:
            return
        if self.idIndex == -1:
            QtWidgets.QMessageBox.critical(self, '錯誤', '不能刪除未存入的資料')
            return
        mb = QtWidgets.QMessageBox(self)
        mb.setWindowTitle('確認刪除')
        mb.setText('確定要刪除本筆: {} 嗎?'.format(self.name.currentText()))
        mb.addButton('取消', QtWidgets.QMessageBox.NoRole)
        mb.addButton('確定', QtWidgets.QMessageBox.YesRole)
        toDelete = mb.exec_()
        if toDelete:
            con, cursor= connect._get_connection()
            sqlstr = ('delete from hvhnonc_in where ID=?;')
            params = (self.idDict[self.idIndex],)
            cursor.execute(sqlstr, params)
            con.commit()
            con.close()
            msg = u'已刪除一筆資料: {}({})'.format(
                    self.name.currentText(), self.idDict[self.idIndex])
            QtWidgets.QMessageBox.information(self, u'成功', msg)
        else:
            return
        # reset form
        self.clear_all_fields()
        self.disable_all_fields()

    def onclick_previous_record(self):
        self.idDict = self.get_id_dict()
        # modify idIndex
        if self.idIndex == -1:
            self.idIndex = len(self.idDict) - 1
        elif self.idIndex == 0:
            QtWidgets.QMessageBox.warning(self, u'到頂了', u'已到達第一筆')
        else:
            self.idIndex -= 1
        # update view using new idIndex
        record = self.get_record(self.idDict[self.idIndex])
        self.init_all_fields()
        self.update_by_record(record)

    def onclick_next_record(self):
        self.idDict = self.get_id_dict()
        # modify idIndex
        if self.idIndex == -1:
            self.idIndex = 0
        elif self.idIndex == len(self.idDict) - 1:
            QtWidgets.QMessageBox.warning(self, u'到底了', u'已到達最末筆')
        else:
            self.idIndex += 1
        # update view using new idIndex
        record = self.get_record(self.idDict[self.idIndex])
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
                if k not in ('ID', 'old_ID'):
                    print(e)

    def get_record(self, index: int):
        con, cursor= connect._get_connection()
        con.row_factory = sqlite3.Row
        cursor = con.cursor()
        sqlstr = ('select * from hvhnonc_in where ID=?')
        params = (str(index),)
        cursor.execute(sqlstr, params)
        res = cursor.fetchone()
        con.close()
        return res

    def getIdIndex(self, id: int):
        for k, v in self.idDict.items():
            if v == id:
                return k

    def get_id_dict(self):
        con, cursor= connect._get_connection()
        sqlstr = ('select ID from hvhnonc_in order by acquire_date;')
        cursor.execute(sqlstr)
        rows = cursor.fetchall()
        con.close()
        return {i: row[0] for i, row in enumerate(rows)}

    def on_name_changed(self):
        # update unit, brand, spec from hvhnonc_cache
        con, cursor= connect._get_connection()
        sqlstr = ('select change_value '
                  'from hvhnonc_cache '
                  'where this_ID=? '
                  'and this_value=? '
                  'and change_ID=?')
        params = [connect.get_field_id('name'),
                  self.name.currentText()]
        # unit
        p = params + [connect.get_field_id('unit'),]
        cursor.execute(sqlstr, p)
        rows = cursor.fetchall()
        self.unit.clear()
        if rows:
            self.unit.addItems([row[0] for row in rows])
        # brand
        p = params + [connect.get_field_id('brand'),]
        cursor.execute(sqlstr, p)
        rows = cursor.fetchall()
        self.brand.clear()
        if rows:
            self.brand.addItems([row[0] for row in rows])
        # spec
        p = params + [connect.get_field_id('spec'),]
        cursor.execute(sqlstr, p)
        rows = cursor.fetchall()
        self.spec.clear()
        if rows:
            self.spec.addItems([row[0] for row in rows])
        con.close()

    def on_subcategory_changed(self):
        # update name from hvhnonc_cache
        con, cursor= connect._get_connection()
        sqlstr = ('select change_value '
                  'from hvhnonc_cache '
                  'where this_ID=? '
                  'and this_value=? '
                  'and change_ID=?')
        params = [
                connect.get_field_id('subcategory'),
                self.subcategory.currentText(),
                connect.get_field_id('name')]
        cursor.execute(sqlstr, params)
        rows = cursor.fetchall()
        con.close()
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
        con.close()
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
            # fetch options from hvhnonc_cache
            else:
                sqlstr = ('select change_value '
                          'from hvhnonc_cache '
                          'where this_ID=0 and '
                          'change_ID=?')
                params = (connect.get_field_id(key),)
                cursor.execute(sqlstr, params)
                rows = cursor.fetchall()
                options = [row[0] for row in rows]
                widget.addItems(options)
                widget.clearEditText()
        con.close()

    def enable_all_fields(self):
        self.isEnabled = True
        self.idDict = self.get_id_dict()
        widgetsToEnable = {k: i for k , i in self.__dict__.items() if (
                isinstance(i, QtWidgets.QComboBox) or
                isinstance(i, QtWidgets.QLineEdit) or
                isinstance(i, QtWidgets.QDateEdit))}
        for w in widgetsToEnable.values():
            w.setEnabled(True)

    def disable_all_fields(self):
        self.isEnabled = False
        self.idIndex = -1
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
                date = QtCore.QDate.currentDate()
                i.setDate(date)

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Register(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
