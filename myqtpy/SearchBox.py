# -*- coding: utf-8 -*-
"""
@author: alchenerd (alchenerd@gmail.com)
"""
from PyQt5 import QtWidgets

# These modules are mine
if __name__ == '__main__':
    from _search_box_skeleton import Ui_Dialog as SearchBoxDialog
    from SearchResult import SearchResult
else:
    from myqtpy._search_box_skeleton import Ui_Dialog as SearchBoxDialog
    from myqtpy.SearchResult import SearchResult


class SearchBox(QtWidgets.QDialog, SearchBoxDialog):
    def __init__(self, dialog):
        super(self.__class__, self).__init__(dialog)
        self.setupUi(dialog)
        self.searchBtn.clicked.connect(
                lambda: self.on_searchBtn_clicked(dialog))

    def on_searchBtn_clicked(self, dialog):
        print('::{}'.format(self.query.text()))
        dialog.accept()
        # open a search result window
        self.resultWindow = QtWidgets.QDialog()
        sqlstr = ('select * from hvhnonc_in where name like ?')
        params = ('%{}%'.format(self.query.text()),)
        SearchResult(self.resultWindow, sqlstr, params)
        self.resultWindow.exec_()


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = SearchBox(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
