# -*- coding: utf-8 -*-
"""
@author: alchenerd (alchenerd@gmail.com)
"""

from PyQt5 import QtWidgets
from typing import Dict
import sys

# These are mine
if __name__ == '__main__':
    sys.path.append('../')
else:
    sys.path.append('./myqtpy/')

from _filter_skeleton import Ui_Dialog as FilterDialog
from myconnect import connect

class Filter(QtWidgets.QDialog, FilterDialog):
    def __init__(self, dialog):
        super(self.__class__, self).__init__(dialog)
        self.setupUi(dialog)
        self.init_all_fields()


    def init_all_fields(self):
        widgetsToInit = {k: i for k , i in self.__dict__.items()
                         if isinstance(i, QtWidgets.QComboBox)}
        # discard subcategory, name, unit, brand, spec
        blacklist = ('subcategory', 'name', 'brand', 'spec')
        for i in blacklist:
            widgetsToInit.pop(i)
        self.fetch_options(widgetsToInit)

    def fetch_options(self, widgets: Dict[str, QtWidgets.QComboBox]):
        print('\n'.join(widgets.keys()))
        # TODO: Initialize the Filter window
        con, cur = connect._get_connection()
        for key, widget in widgets.items():
            if key == 'category':
                sqlstr = ('select * from hvhnonc_category;')
        con.close()


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QDialog()
    ui = Filter(dialog)
    dialog.show()
    sys.exit(app.exec_())
