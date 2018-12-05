# -*- coding: utf-8 -*-
"""
@author: alchenerd (alchenerd@gmail.com)
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from myqtpy._index_skeleton import Ui_MainWindow as IndexUi
from myqtpy.Dummy import Dummy


class Index(QtWidgets.QMainWindow, IndexUi):
    def __init__(self, mainWindow):
        super(self.__class__, self).__init__(mainWindow)
        self.setupUi(mainWindow)

    def setupUi(self, mainWindow):
        super(self.__class__, self).setupUi(mainWindow)
        self.addBtn.clicked.connect(
                lambda: self.on_btn_clicked(type='add'))
        self.removeBtn.clicked.connect(
                lambda: self.on_btn_clicked(type='remove'))
        self.printBtn.clicked.connect(
                lambda: self.on_btn_clicked(type='print'))
        self.maintenanceBtn.clicked.connect(
                lambda: self.on_btn_clicked(type='maintenance'))
        self.quitBtn.clicked.connect(QtCore.QCoreApplication.instance().quit)

    def on_btn_clicked(self, type):
        self.childWindow = QtWidgets.QDialog()
        ui = Dummy(self.childWindow)
        self.childWindow.setWindowTitle(type)
        self.childWindow.show()
        self.childWindow.exec_()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    index = Index(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())
