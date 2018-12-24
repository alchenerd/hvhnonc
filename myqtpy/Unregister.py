# -*- coding: utf-8 -*-
import sqlite3
import sys

from PyQt5 import QtCore, QtWidgets

from _unregister_skeleton import Ui_Dialog as UnregisterDialog
from SearchBox import SearchBox
from Filter import Filter
from myconnect import connect

"""
@author: alchenerd (alchenerd@gmail.com)
"""
# These are mine
if __name__ == '__main__':
    sys.path.append('../')
else:
    sys.path.append('./myqtpy/')


class Unregister(QtWidgets.QDialog, UnregisterDialog):
    def __init__(self, dialog):
        super(self.__class__, self).__init__(dialog)
        self.setupUi(dialog)
        self.isEnabled = None
        self.iid = None # in_ID
        self.unregisterIdIndex = -1
        self.unregisgerIdDict = self.get_id_dict('unregister')
        self.getPreviousBtn.clicked.connect(self.onclick_prev)
        self.getNextBtn.clicked.connect(self.onclick_next)
        self.searchBtn.clicked.connect(self.on_searchBtn_clicked)
        self.formBtn.clicked.connect(self.on_formBtn_clicked)
        self.selectRecordBtn.clicked.connect(self.on_selectRecordBtn_clicked)
        self.saveBtn.clicked.connect(self.on_saveBtn_clicked)
        self.deleteBtn.clicked.connect(self.on_deleteBtn_clicked)
        self.unregister_amount.textEdited.connect(self.amount_edit)
        self.clear_all_fields()
        self.disable_all_fields()

    def on_saveBtn_clicked(self):
        """ Callback function when saveBtn is clicked. """
        print('on_saveBtn_clicked')
        # check if valid field
        if not self.check_user_input():
            return
        # check if valid unregisterIdIndex
        if self.unregisterIdIndex in range(len(self.unregisgerIdDict)):
            # valid id, ask user save as new or writeover
            choice = self.ask_new_or_writeover()
            if choice == 'new':
                self.save_as_new()
            elif choice == 'write_over':
                self.write_over()
            elif choice == 'cancel':
                return
        else:
            # invalid id, check if new record(editable):
            if self.isEnabled == True:
                if self.ask_confirm():
                    self.save_as_new()
        # update unregisgerIdDict
        self.unregisgerIdDict = self.get_id_dict('unregister')

    #TODO: finish the 4 saving methods below
    def ask_confirm(self) -> bool:
        """ Asks user 'Are you sure?'. """
        mb = QtWidgets.QMessageBox()
        mb.setIcon(QtWidgets.QMessageBox.Question)
        mb.setWindowTitle(u'確定?')
        mb.setText(u'確定要存入一筆新資料嗎?')
        mb.addButton(u'取消', QtWidgets.QMessageBox.RejectRole)
        mb.addButton(u'確定', QtWidgets.QMessageBox.AcceptRole)
        return mb.exec_()


    def ask_new_or_writeover(self) -> str:
        """ Asks user if save as new or writeover with a messagebox.

        Returns
        -------
        str
            'cancel', 'new' or 'writeover', which indicates the user's choice.
        """
        mb = QtWidgets.QMessageBox()
        mb.setWindowTitle('存入資料')
        mb.setText('請選擇存入本筆資料的方式：')
        mb.addButton('取消', QtWidgets.QMessageBox.RejectRole)
        mb.addButton('新增一筆', QtWidgets.QMessageBox.YesRole)
        mb.addButton('覆蓋本筆', QtWidgets.QMessageBox.NoRole)
        res = mb.exec_()
        if res == 0:
            return 'cancel'
        elif res == 1:
            return 'new'
        elif res == 2:
            return 'write_over'

    def check_user_input(self) -> bool:
        """ Checks if the user input of unregister form is valid.

        Returns
        -------
        bool
            The user input's validity.
            In case of returning False, a messagebox will popup and
            inform user where went wrong.
        """
        print('check_user_input')
        if not self.isEnabled:
            return False
        # We check amount > 0 only for now.
        if int(self.unregister_amount.text()) <= 0:
            QtWidgets.QMessageBox.warning(
                    self, u'錯誤', u'除帳數量不可小於等於0!')
            return False
        return True

    def update_cache(self):
        """ Update the user input into cache. """
        con, cur = connect._get_connection()
        sqlstr = ('insert or ignore into hvhnonc_cache ({columns}) '
                  'values ({questionmarks})')
        d = {}
        columns = ['this_ID', 'this_value', 'change_ID', 'change_value']
        d['columns'] = (', '.join(columns))
        d['questionmarks'] = ('?, ' * len(columns))[:-2]
        widgetsToUpdate = ['reason', 'unregister_place']
        for w in widgetsToUpdate:
            params = ['0', '', connect.get_field_id(w),
                      getattr(self, w).currentText()]
            cur.execute(sqlstr.format(**d), params)
        con.commit()
        con.close()

    def save_as_new(self):
        """ Save users input to database as a new row via sqlite."""
        print('save_as_new')
        con, cur = connect._get_connection()
        sqlstr = ('insert into hvhnonc_out({fields}) values({questionmarks})')
        d = {}
        d['fields'] = ('in_ID, unregister_date, amount, reason, '
                       'unregister_place, unregister_remark')
        params = [str(self.iid), self.unregister_date.date().toPyDate(),
                  self.unregister_amount.text(), self.reason.currentText(),
                  self.unregister_place.currentText(),
                  self.unregister_remark.text()]
        d['questionmarks'] = ('?, ' * len(params))[:-2]
        cur.execute(sqlstr.format(**d), params)
        con.commit()
        con.close()
        self.update_cache()
        QtWidgets.QMessageBox.information(self, '成功', '已存入一筆資料')

    def write_over(self):
        """ Write over old record with the user input via sqlite.

        The old record is located with
        self.unregisgerIdDict[self.unregisterIdIndex])."""
        print('write_over')
        con, cur = connect._get_connection()
        sqlstr = ('update hvhnonc_out set {settings} where ID=?')
        d = {}
        d['settings'] = ''
        fields = ['in_ID', 'unregister_date', 'amount', 'reason',
                  'unregister_place', 'unregister_remark']
        params = [str(self.iid), self.unregister_date.date().toPyDate(),
                  self.unregister_amount.text(), self.reason.currentText(),
                  self.unregister_place.currentText(),
                  self.unregister_remark.text()]
        for f in fields:
            d['settings'] += '{} = ?, '.format(f)
        d['settings'] = d['settings'][:-2]
        params += (str(self.unregisgerIdDict[self.unregisterIdIndex]),)
        cur.execute(sqlstr.format(**d), params)
        con.commit()
        con.close()
        self.update_cache()
        QtWidgets.QMessageBox.information(self, '成功', '已覆蓋一筆資料')

    def on_deleteBtn_clicked(self):
        print('on_deleteBtn_clicked')

    def on_selectRecordBtn_clicked(self):
        # open a search box
        self.sb = QtWidgets.QDialog()
        Filter(self.sb, mode='both')
        returnID = self.sb.exec_()
        if returnID == 0:
            return
        self.unregisterIdIndex = -1
        self.update_field_by_id(returnID)

    def on_formBtn_clicked(self):
        # open a search box
        self.sb = QtWidgets.QDialog()
        Filter(self.sb, mode='out')
        returnID = self.sb.exec_()
        if returnID == 0:
            return
        self.unregisterIdIndex = -1
        self.update_field_by_id(returnID)

    def on_searchBtn_clicked(self):
        # open a search box
        self.sb = QtWidgets.QDialog()
        SearchBox(self.sb, 'both')
        # self.sb.exec_() returns a hvhnonc_in ID or a negative hvhnonc_out ID
        returnID = self.sb.exec_()
        if returnID == 0:
            return
        self.unregisterIdIndex = -1
        self.update_field_by_id(returnID)

    def update_field_by_id(self, returnID: int):
        if returnID < 0:
            oid = -returnID
            for k, id in self.unregisgerIdDict.items():
                if id == oid:
                    self.unregisterIdIndex = k
            iid = self.get_inID(oid)
        else:
            # return id has no unregister record
            oid = -1
            iid = returnID
            self.unregisterIdIndex = -1
        self.iid = iid
        self.load_inRecord(iid)
        self.load_history_record(iid)
        self.load_outRecord(oid)
        self.enable_some_fields()
        self.amount_initialize()

    def amount_initialize(self):
        if self.unregister_amount.text() in (None, ''):
            return
        # get total amount
        totalAmount = int(self.amount.text())
        # get unregistered amount
        try:
            unregisteredAmount = int(self.unregistered_amount.text())
        except ValueError:
            unregisteredAmount = 0
        # calculate remain
        remain = totalAmount - unregisteredAmount
        self.remain_amount.setText(str(remain))

    def amount_edit(self):
        if self.unregister_amount.text() in (None, ''):
            return
        # get total amount
        totalAmount = int(self.amount.text())
        # get unregistered amount
        if self.unregisterIdIndex == -1:
            unregisteredAmount = 0
        else:
            unregisteredAmount = int(self.unregistered_amount.text())
        # get editingAmount
        try:
            editingAmount  = int(self.unregister_amount.text())
        except ValueError:
            QtWidgets.QMessageBox.warning(self, '錯誤', '數量需為正整數!')
            self.unregister_amount.setText(
                    str(totalAmount - unregisteredAmount))
            return
        # calculate remain
        remain = totalAmount - unregisteredAmount - editingAmount
        if remain < 0:
            QtWidgets.QMessageBox.warning(self, '錯誤', '剩餘數量不可小於0!')
            self.unregister_amount.setText(
                    str(totalAmount - unregisteredAmount))
        else:
            self.remain_amount.setText(str(remain))

    # enable some fields for user editing
    def enable_some_fields(self):
        self.isEnabled = True
        fieldsToEnable = ['unregister_date', 'unregister_amount', 'reason',
                          'unregister_place', 'unregister_remark']
        fieldsToEnable = [getattr(self, x) for x in fieldsToEnable]
        for field in fieldsToEnable:
            field.setEnabled(True)

    def get_id_dict(self, fromWhere: str):
        where = ''
        if fromWhere == 'register':
            where = 'hvhnonc_in'
            dateField = 'acquire_date'
        if fromWhere == 'unregister':
            where = 'hvhnonc_out'
            dateField = 'unregister_date'
        con, cursor = connect._get_connection()
        sqlstr = ('select ID from {0} order by {1};'.format(where, dateField))
        cursor.execute(sqlstr)
        rows = cursor.fetchall()
        con.close()
        return {i: row[0] for i, row in enumerate(rows)}

    def get_inID(self, oid: int) -> int:
        con, cursor = connect._get_connection()
        sqlstr = ('select in_ID from hvhnonc_out where ID = ?')
        params = (oid,)
        cursor.execute(sqlstr, params)
        row = cursor.fetchone()
        con.close()
        if row:
            return row[0]
        else:
            return -1

    def onclick_next(self):
        if self.unregisterIdIndex == -1:
            self.unregisterIdIndex = 0
        elif self.unregisterIdIndex == len(self.unregisgerIdDict) - 1:
            QtWidgets.QMessageBox.warning(self, u'到底了', u'已到達最末筆')
        else:
            self.unregisterIdIndex += 1
        oid = self.unregisgerIdDict[self.unregisterIdIndex] # outID
        self.update_field_by_id(-oid) # negative value for unregister record

    def onclick_prev(self):
        if self.unregisterIdIndex == -1:
            self.unregisterIdIndex = len(self.unregisgerIdDict) - 1
        elif self.unregisterIdIndex == 0:
            QtWidgets.QMessageBox.warning(self, u'到頂了', u'已到達第一筆')
        else:
            self.unregisterIdIndex -= 1
        oid = self.unregisgerIdDict[self.unregisterIdIndex] # outID
        self.update_field_by_id(-oid) # negative value for unregister record

    def clear_history_record(self):
        widgetsToClear = ('last_unregister_date', 'unregistered_amount',
                          'unregistered_count')
        widgetsToClear = [self.__dict__.get(x) for x in widgetsToClear]
        for widget in widgetsToClear:
            if isinstance(widget, QtWidgets.QLineEdit):
                widget.clear()
            elif isinstance(widget, QtWidgets.QComboBox):
                widget.clearEditText()
            elif isinstance(widget, QtWidgets.QDateEdit):
                (y, m, d) = (1800, 1, 1)
                date = QtCore.QDate(y, m, d)
                widget.setDate(date)

    def load_history_record(self, iid: int):
        con, cursor = connect._get_connection()
        con.row_factory = sqlite3.Row
        cursor = con.cursor()
        sqlstr = ('select '
                      'max(unregister_date) as last_unregister_date, '
                      'count(*) as unregistered_count, '
                      'sum(amount) as unregistered_amount '
                  'from hvhnonc_out '
                  'where in_ID=?'
                  'limit 1;')
        params = (iid,)
        cursor.execute(sqlstr, params)
        row = cursor.fetchone()
        if not row or None in row:
            self.clear_history_record()
            return
        con.close()
        for k in row.keys():
            try:
                w = getattr(self, k)
            except:
                continue
            if isinstance(w, QtWidgets.QLineEdit):
                w.setText(str(row[k]))
            elif isinstance(w, QtWidgets.QComboBox):
                w.setEditText(str(row[k]))
            elif isinstance(w, QtWidgets.QDateEdit):
                (y, m, d) = map(int, row[k].split('-'))
                date = QtCore.QDate(y, m, d)
                w.setDate(date)

    def load_inRecord(self, iid: int):
        con, cursor = connect._get_connection()
        con.row_factory = sqlite3.Row
        cursor = con.cursor()
        sqlstr = ('select * from hvhnonc_in where ID = ?')
        params = (iid,)
        cursor.execute(sqlstr, params)
        row = cursor.fetchone()
        con.close()
        for k in row.keys():
            try:
                w = getattr(self, k)
            except:
                continue
            if isinstance(w, QtWidgets.QLineEdit):
                w.setText(str(row[k]))
            elif isinstance(w, QtWidgets.QComboBox):
                w.setEditText(str(row[k]))
            elif isinstance(w, QtWidgets.QDateEdit):
                (y, m, d) = map(int, row[k].split('-'))
                date = QtCore.QDate(y, m, d)
                w.setDate(date)

    def clear_out_fields(self):
        widgetsToClear = ('unregister_date', 'unregister_amount', 'reason',
                          'unregister_place', 'unregister_remark')
        widgetsToClear = [self.__dict__.get(x) for x in widgetsToClear]
        for widget in widgetsToClear:
            if isinstance(widget, QtWidgets.QLineEdit):
                widget.clear()
            elif isinstance(widget, QtWidgets.QComboBox):
                widget.clearEditText()
            elif isinstance(widget, QtWidgets.QDateEdit):
                date = QtCore.QDate()
                date = QtCore.QDate.currentDate()
                widget.setDate(date)
        self.unregister_amount.setText('0')

    def load_outRecord(self, oid: int):
        if oid == -1:
            self.clear_out_fields()
            return
        con, cursor = connect._get_connection()
        con.row_factory = sqlite3.Row
        cursor = con.cursor()
        sqlstr = ('select * from hvhnonc_out where ID = ?')
        params = (oid,)
        cursor.execute(sqlstr, params)
        row = cursor.fetchone()
        con.close()
        for k in row.keys():
            if k == 'amount':
                w = getattr(self, 'unregister_amount')
            else:
                try:
                    w = getattr(self, k)
                except:
                    continue
            if isinstance(w, QtWidgets.QLineEdit):
                w.setText(str(row[k]))
            elif isinstance(w, QtWidgets.QComboBox):
                w.setEditText(str(row[k]))
            elif isinstance(w, QtWidgets.QDateEdit):
                (y, m, d) = map(int, row[k].split('-'))
                date = QtCore.QDate(y, m, d)
                w.setDate(date)

    def clear_all_fields(self):
        widgetsToClear = {k: i for k, i in self.__dict__.items() if (
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

    def disable_all_fields(self):
        self.isEnabled = False
        self.idIndex = -1
        widgetsToDisable = {k: i for k, i in self.__dict__.items() if (
            isinstance(i, QtWidgets.QComboBox) or
                isinstance(i, QtWidgets.QLineEdit) or
            isinstance(i, QtWidgets.QDateEdit))}
        for w in widgetsToDisable.values():
            w.setEnabled(False)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QDialog()
    ui = Unregister(dialog)
    dialog.show()
    sys.exit(app.exec_())
