# -*- coding: utf-8 -*-
"""
@author: alchenerd (alchenerd@gmail.com)
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from myqtpy._index_skeleton import Ui_MainWindow as indexUi
from myqtpy.Login import Login


class Index(QtWidgets.QMainWindow, indexUi):
    def __init__(self, parent = None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(parent)
        # Call a login form
        self.loginForm = QtWidgets.QWidget()
        self.loginFormUi = Login(self)
        self.loginFormUi.setupUi(self.loginForm)
        self.loginForm.show()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    index = Index(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())