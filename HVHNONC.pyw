# -*- coding: utf-8 -*-
"""
Created on Tue Oct  2 11:08:53 2018

@author: 戴佳燊 (alchenerd@gmail.com)

@project name: Hualien Veterans Home NON-Consumables dbms (HVHNONC)
"""

from PyQt5 import QtWidgets, QtGui

import init
from myqtpy.Index import Index
from myqtpy.Login import Login

_myDefaultFont = QtGui.QFont("微軟正黑體", 16, QtGui.QFont.Bold)


def login():
    dialog = QtWidgets.QDialog()
    Login(dialog)
    return dialog.exec_()


def main():
    init.build_db()
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setFont(_myDefaultFont)
    if login():
        mainWindow = QtWidgets.QMainWindow()
        Index(mainWindow)
        mainWindow.show()
        sys.exit(app.exec_())


if __name__ == "__main__":
    main()
