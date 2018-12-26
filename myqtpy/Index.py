# -*- coding: utf-8 -*-
"""
@author: alchenerd (alchenerd@gmail.com)
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from myqtpy._index_skeleton import Ui_MainWindow as IndexUi
from myqtpy.Dummy import Dummy
from myqtpy.Register import Register
from myqtpy.Unregister import Unregister
from myqtpy.PrintMenu import PrintMenu


class Index(QtWidgets.QMainWindow, IndexUi):
    def __init__(self, mainWindow):
        super(self.__class__, self).__init__(mainWindow)
        self.setupUi(mainWindow)

    def setupUi(self, mainWindow):
        super(self.__class__, self).setupUi(mainWindow)
        self.addBtn.clicked.connect(
                lambda: self.on_btn_clicked(type_='register'))
        self.removeBtn.clicked.connect(
                lambda: self.on_btn_clicked(type_='unregister'))
        self.printBtn.clicked.connect(
                lambda: self.on_btn_clicked(type_='print'))
        self.maintenanceBtn.clicked.connect(
                lambda: self.on_btn_clicked(type_='maintenance'))
        self.quitBtn.clicked.connect(QtCore.QCoreApplication.instance().quit)

    def on_btn_clicked(self, type_):
        self.childWindow = QtWidgets.QDialog()
        if type_ == 'register':
            ui = Register(self.childWindow)
        elif type_ == 'unregister':
            ui = Unregister(self.childWindow)
        elif type_ == 'print':
            ui = PrintMenu(self.childWindow)
        else:
            ui = Dummy(self.childWindow)
            self.childWindow.setWindowTitle(type_)
        self.childWindow.show()
        self.childWindow.exec_()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    index = Index(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())
