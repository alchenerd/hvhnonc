# -*- coding: utf-8 -*-
"""
Created on Tue Oct  2 11:08:53 2018

@author: 戴佳燊 (alchenerd@gmail.com)

@project name: Hualien Veterans Home NON-Consumables dbms (HVHNONC)
"""

from PyQt5 import QtWidgets

import init
from myqtpy.Index import Index
from myqtpy.Login import Login

def login():
    dialog = QtWidgets.QDialog()
    Login(dialog)
    return dialog.exec_()


def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    if login():
        init.buildDatabase()
        mainWindow = QtWidgets.QMainWindow()
        Index(mainWindow)
        mainWindow.show()
        sys.exit(app.exec_())


if __name__ == "__main__":
    main()