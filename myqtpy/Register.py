# -*- coding: utf-8 -*-
"""
@author: alchenerd (alchenerd@gmail.com)
"""

from PyQt5 import QtWidgets, QtCore
from typing import Dict
# These modules are mine
if __name__ == '__main__':
    from _register_skeleton import Ui_Dialog as RegisterDialog
    import sys
    sys.path.append('../')
    from myconnect.connect import _get_connection
else:
    from myqtpy._register_skeleton import Ui_Dialog as RegisterDialog
    from myconnect.connect import _get_connection

class Register(QtWidgets.QDialog, RegisterDialog):
    def __init__(self, dialog):
        super(self.__class__, self).__init__(dialog)
        self.setupUi(dialog)
        self.returnBtn.clicked.connect(dialog.reject)
        self.createBtn.clicked.connect(self.on_createBtn_clicked)
        self.disable_all_fields()
        self.clear_all_fields()

    def on_createBtn_clicked(self):
        self.init_all_fields()

    def init_all_fields(self):
        self.enable_all_fields()
        widgetsToInit = {k: i for k , i in self.__dict__.items()
                         if isinstance(i, QtWidgets.QComboBox)}
        # discard subcategory, name, unit, brand, spec
        blacklist = ('subcategory', 'name', 'unit', 'brand', 'spec')
        for i in blacklist:
            widgetsToInit.pop(i)
        self.fetch_options(widgetsToInit)

    def fetch_options(self, d: Dict[str, QtWidgets.QComboBox]):
        con = _get_connection()
        for key, widget in d.items():
            # fetch options from hvhnonc
            if key == 'category':
                pass
            else:
                pass
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
