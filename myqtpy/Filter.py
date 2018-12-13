# -*- coding: utf-8 -*-
"""
@author: alchenerd (alchenerd@gmail.com)
"""

from PyQt5 import QtWidgets, QtCore
from typing import Dict, Tuple, List
import sys

# These are mine
if __name__ == '__main__':
    sys.path.append('../')
else:
    sys.path.append('./myqtpy/')

from _filter_skeleton import Ui_Dialog as FilterDialog
from myconnect import connect
from SearchResult import SearchResult

class Filter(QtWidgets.QDialog, FilterDialog):
    def __init__(self, dialog):
        super(self.__class__, self).__init__(dialog)
        self.setupUi(dialog)
        self.category.currentTextChanged.connect(self.on_category_changed)
        self.subcategory.currentTextChanged.connect(
                self.on_subcategory_changed)
        self.name.currentTextChanged.connect(self.on_name_changed)
        self.purchase_date_chk.stateChanged.connect(self.on_pdatehk_changed)
        self.acquire_date_chk.stateChanged.connect(self.on_adatechk_changed)
        self.submitBtn.clicked.connect(
                lambda: self.on_submitBtn_clicked(dialog))
        self.init_all_fields()

    def on_submitBtn_clicked(self, dialog):
        print('on_submitBtn_clicked')
        # open a search result window
        self.resultWindow = QtWidgets.QDialog()
        sqlstr, params = self.load_form_query()
        SearchResult(self.resultWindow, sqlstr, params)
        dialog.done(self.resultWindow.exec_())

    def load_form_query(self) -> Tuple[str, List[str]]:
        sqlstr = 'select * from hvhnonc_in where ('
        params = []
        comboboxes = {key: value for key, value in self.__dict__.items()
                      if isinstance(value, QtWidgets.QComboBox)}
        for key, widget in comboboxes.items():
            if widget.currentText() not in (None, ''):
                print(widget.currentText())
                sqlstr += ('{} like ? and '.format(key))
                params.append('%{}%'.format(widget.currentText()))
        # price range
        price = {}
        if (self.price_min.text() not in (None, '')
            or self.price_max.text() not in (None, '')):
            try:
                price['min'] = int(self.price_min.text())
            except ValueError as ve:
                if self.price_min.text() == '':
                    price['min'] = 0
                else:
                    QtWidgets.QMessageBox.critical(self, '錯誤', str(ve))
            try:
                price['max'] = int(self.price_max.text())
            except ValueError as ve:
                if self.price_max.text() == '':
                    # maximum int of sqlite3
                    price['max'] = 2 ** 63 - 1
                else:
                    QtWidgets.QMessageBox.critical(self, '錯誤', str(ve))
            print('price: ', price)
            sqlstr += '(price >= ? and price <= ?) and '
            params += [str(price['min']), str(price['max'])]
        # purchase_date: QDateEdit
        if self.purchase_date_chk.checkState():
            minDate = self.purchase_date_min.date().toPyDate()
            maxDate = self.purchase_date_max.date().toPyDate()
            sqlstr += ("(strftime('%Y-%m-%d', {}) "
                      "between ? and ?) and ".format('purchase_date'))
            params.append(str(minDate))
            params.append(str(maxDate))
        # acquire_date: QDateEdit
        if self.acquire_date_chk.checkState():
            minDate = self.acquire_date_min.date().toPyDate()
            maxDate = self.acquire_date_max.date().toPyDate()
            sqlstr += ("(strftime('%Y-%m-%d', {}) "
                      "between ? and ?) and ".format('acquire_date'))
            params.append(str(minDate))
            params.append(str(maxDate))
        sqlstr += '1) order by acquire_date desc;'
        print(sqlstr)
        print('::'.join(params))
        return sqlstr, params


    def on_pdatehk_changed(self, state: int):
        self.purchase_date_min.setEnabled(bool(state))
        self.purchase_date_max.setEnabled(bool(state))
        print(self.purchase_date_chk.checkState())

    def on_adatechk_changed(self, state: int):
        self.acquire_date_min.setEnabled(bool(state))
        self.acquire_date_max.setEnabled(bool(state))
        print(self.acquire_date_chk.checkState())

    def on_name_changed(self):
        # update brand, spec from hvhnonc_cache
        con, cursor= connect._get_connection()
        sqlstr = ('select change_value '
                  'from hvhnonc_cache '
                  'where this_ID=? '
                  'and this_value=? '
                  'and change_ID=?')
        params = [connect.get_field_id('name'),
                  self.name.currentText()]
        # brand
        p = params + [connect.get_field_id('brand'),]
        cursor.execute(sqlstr, p)
        rows = cursor.fetchall()
        self.brand.clear()
        if rows:
            self.brand.addItems([row[0] for row in rows])
        self.brand.clearEditText()
        # spec
        p = params + [connect.get_field_id('spec'),]
        cursor.execute(sqlstr, p)
        rows = cursor.fetchall()
        self.spec.clear()
        if rows:
            self.spec.addItems([row[0] for row in rows])
        con.close()
        self.spec.clearEditText()

    def on_subcategory_changed(self):
        # update name from hvhnonc_cache
        con, cursor= connect._get_connection()
        sqlstr = ('select change_value '
                  'from hvhnonc_cache '
                  'where this_ID=? '
                  'and this_value=? '
                  'and change_ID=?')
        params = [connect.get_field_id('subcategory'),
                  self.subcategory.currentText(),
                  connect.get_field_id('name')]
        cursor.execute(sqlstr, params)
        rows = cursor.fetchall()
        con.close()
        names = [row[0] for row in rows]
        self.name.clear()
        self.name.addItems(names)
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

    def init_all_fields(self):
        widgetsToInit = {k: i for k , i in self.__dict__.items()
                         if isinstance(i, QtWidgets.QComboBox)}
        # discard subcategory, name, unit, brand, spec
        blacklist = ('subcategory', 'name', 'brand', 'spec')
        for i in blacklist:
            widgetsToInit.pop(i)
        self.fetch_options(widgetsToInit)
        # disable all QDateEdit
        widgetsToDisable = {k: i for k , i in self.__dict__.items()
                         if isinstance(i, QtWidgets.QDateEdit)}
        for w in widgetsToDisable.values():
            w.setEnabled(False)

    def fetch_options(self, widgets: Dict[str, QtWidgets.QComboBox]):
        print('\n'.join(widgets.keys()))
        con, cur = connect._get_connection()
        for key, widget in widgets.items():
            if key == 'category':
                sqlstr = ('select description from hvhnonc_category;')
                cur.execute(sqlstr)
                rows = cur.fetchall()
                categories = [row[0] for row in rows]
                widget.clear()
                widget.addItems(categories)
                widget.clearEditText()
            # fetch options from hvhnonc_cache
            else:
                sqlstr = ('select change_value '
                          'from hvhnonc_cache '
                          'where this_ID=0 and '
                          'change_ID=?')
                params = (connect.get_field_id(key),)
                cur.execute(sqlstr, params)
                rows = cur.fetchall()
                options = [row[0] for row in rows]
                widget.addItems(options)
                widget.clearEditText()
        con.close()


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QDialog()
    ui = Filter(dialog)
    dialog.show()
    sys.exit(app.exec_())
