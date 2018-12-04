# -*- coding: utf-8 -*-
"""
Created on Tue Dec  4 13:54:57 2018

@author: alchenerd (alchenerd@gmail.com)
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from myqtpy._login_skeleton import Ui_Form as Form

class Login(QtWidgets.QWidget, Form):
    def __init__(self, parent):
        super(self.__class__, self).__init__(parent)
        self.setupUi(parent)
        self.show()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    index = Login(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())
