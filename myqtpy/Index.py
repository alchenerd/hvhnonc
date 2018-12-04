# -*- coding: utf-8 -*-
"""
@author: alchenerd (alchenerd@gmail.com)
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from myqtpy._index_skeleton import Ui_MainWindow as indexUi


class Index(QtWidgets.QMainWindow, indexUi):
    def __init__(self, parent = None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(parent)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    index = Index(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())
