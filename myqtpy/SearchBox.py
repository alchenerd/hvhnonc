# -*- coding: utf-8 -*-
"""
@author: alchenerd (alchenerd@gmail.com)
"""
from PyQt5 import QtWidgets

# These modules are mine
if __name__ == '__main__':
    from _search_box_skeleton import Ui_Dialog as SearchBoxDialog
    from SearchResult import SearchResult
    import sys
    sys.path.append('../')
else:
    from myqtpy._search_box_skeleton import Ui_Dialog as SearchBoxDialog
    from myqtpy.SearchResult import SearchResult
from myconnect import connect


class SearchBox(QtWidgets.QDialog, SearchBoxDialog):
    def __init__(self, dialog):
        super(self.__class__, self).__init__(dialog)
        self.setupUi(dialog)
        self.fetch_options(self.query)
        self.searchBtn.clicked.connect(
                lambda: self.on_searchBtn_clicked(dialog))

    def fetch_options(self, widget):
        widgets = {k: w for k, w in self.__dict__.items()
                if isinstance(w, QtWidgets.QComboBox)}
        con, cursor = connect._get_connection()
        for k, w in widgets.items():
            sqlstr = ('select change_value '
                      'from hvhnonc_cache '
                      'where this_ID=0 '
                      'and change_ID=? '
                      'order by rowid desc;')
            params = (connect.get_field_id(k),)
            cursor.execute(sqlstr, params)
            rows = cursor.fetchall()
            options = [row[0] for row in rows]
            w.clear()
            w.addItems(options)
            w.clearEditText()
        con.close()

    def on_searchBtn_clicked(self, dialog):
        #update search cache
        self.update_field_cache()
        # open a search result window
        self.resultWindow = QtWidgets.QDialog()
        sqlstr = ('select * '
                  'from hvhnonc_in '
                  'where name like :q '
                  'or category like :q '
                  'or subcategory like :q '
                  'or brand like :q '
                  'or spec like :q '
                  'or place like :q '
                  'or keep_department like :q '
                  'or use_department like :q '
                  'or keeper like :q '
                  'or remark like :q '
                  'order by rowid asc')
        params = ('%{}%'.format(self.query.currentText()),)
        SearchResult(self.resultWindow, sqlstr, params)
        dialog.done(self.resultWindow.exec_())

    def update_field_cache(self):
        con, cursor= connect._get_connection()
        comboboxes = {k:w for k, w in self.__dict__.items()
                if isinstance(w, QtWidgets.QComboBox)}
        sqlstr = ('insert or ignore into '
                  'hvhnonc_cache(this_ID, this_value, '
                  'change_ID, change_value) '
                  'values(?, ?, ?, ?);')
        for k, w in comboboxes.items():
            if k in ('query',):
                params = (0, '',
                          connect.get_field_id(k),
                          w.currentText())
                cursor.execute(sqlstr, params)
        con.commit()
        con.close()


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = SearchBox(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
