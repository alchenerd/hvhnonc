# -*- coding: utf-8 -*-
"""
Created on Tue Oct  2 11:08:53 2018

@author: 戴佳燊 (alchenerd@gmail.com)

@project name: Hualien Veterans Home NON-Consumables dbms (HVHNONC)
"""

import sys
from PyQt5 import QtWidgets, QtGui

# my modules
import init
from myqtpy.Index import Index
from myqtpy.Login import Login

# default font for the Qt
_myDefaultFont = QtGui.QFont("微軟正黑體", 16, QtGui.QFont.Bold)


def login():
    """Open a login dialog for the user."""
    dialog = QtWidgets.QDialog()
    Login(dialog)
    return dialog.exec_()


def main():
    # if the database file is not there, build a new one via .sql
    init.build_db()
    app = QtWidgets.QApplication(sys.argv)
    app.setFont(_myDefaultFont)
    # authenticate here
    if login():
        mainWindow = QtWidgets.QMainWindow()
        Index(mainWindow)
        mainWindow.show()
        sys.exit(app.exec_())


if __name__ == "__main__":
    main()
