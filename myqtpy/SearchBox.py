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
    def __init__(self, dialog, mode: str):
        # mode = ('in', 'both')
        self.mode = mode
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
        Q_IN = (
                'select '
                    'ID, '
                    '"入帳" as type, '
                    'name, '
                    'acquire_date as date, '
                    'keeper, '
                    'remark '
                'from '
                    'hvhnonc_in '
                'where '
                    'name like :q or category like :q '
                    'or subcategory like :q or brand like :q '
                    'or spec like :q or place like :q '
                    'or keep_department like :q or use_department like :q '
                    'or keeper like :q or remark like :q ')
        Q_OUT = (
                'select '
                    'hvhnonc_out.ID as ID, '
                    '"除帳" as type, '
                    'hvhnonc_in.name as name, '
                    'hvhnonc_out.unregister_date as date, '
                    'hvhnonc_in.keeper as keeper, '
                    'hvhnonc_out.unregister_remark as remark '
                'from '
                    'hvhnonc_out '
                'left join '
                    'hvhnonc_in '
                'on '
                    'hvhnonc_out.in_ID = hvhnonc_in.ID '
                    'and (hvhnonc_in.name like :q '
                    'or hvhnonc_in.category like :q '
                    'or hvhnonc_in.subcategory like :q '
                    'or hvhnonc_in.brand like :q '
                    'or hvhnonc_in.spec like :q '
                    'or hvhnonc_in.place like :q '
                    'or hvhnonc_in.keep_department like :q '
                    'or hvhnonc_in.use_department like :q '
                    'or hvhnonc_in.keeper like :q '
                    'or hvhnonc_in.remark like :q) ')
        Q_BOTH = (Q_IN + 'union all ' + Q_OUT + 'order by date')
        if self.mode == 'in':
            sqlstr = Q_IN
        if self.mode == 'out':
            sqlstr = Q_OUT
        if self.mode == 'both':
            sqlstr = Q_BOTH
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
