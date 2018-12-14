# -*- coding: utf-8 -*-
"""
@author: alchenerd (alchenerd@gmail.com)
"""

from PyQt5 import QtWidgets
import sys
# These are mine
if __name__ == '__main__':
    sys.path.append('../')
else:
    sys.path.append('./myqtpy/')
from _unregister_skeleton import Ui_Dialog as UnregisterDialog

class Unregister(QtWidgets.QDialog, UnregisterDialog):
    def __init__(self, dialog):
        super(self.__class__, self).__init__(dialog)
        self.setupUi(dialog)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QDialog()
    ui = Unregister(dialog)
    dialog.show()
    sys.exit(app.exec_())
