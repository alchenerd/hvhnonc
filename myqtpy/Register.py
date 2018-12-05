# -*- coding: utf-8 -*-
"""
@author: alchenerd (alchenerd@gmail.com)
"""

from PyQt5 import QtWidgets
# These are mine
if __name__ == '__main__':
    from _register_skeleton import Ui_Dialog as RegisterDialog
else:
    from myqtpy._register_skeleton import Ui_Dialog as RegisterDialog

class Register(QtWidgets.QDialog, RegisterDialog):
    def __init__(self, dialog):
        super(self.__class__, self).__init__(dialog)
        self.setupUi(dialog)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Register(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
