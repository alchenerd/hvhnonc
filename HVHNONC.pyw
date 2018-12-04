# -*- coding: utf-8 -*-
"""
Created on Tue Oct  2 11:08:53 2018

@author: 戴佳燊 (alchenerd@gmail.com)

@project name: Hualien Veterans Home NON-Consumables dbms (HVHNONC)
"""

#import tkinter as tk
from PyQt5 import QtWidgets

import init
#import gui
from myqtpy.Index import Index

def main():
    """
    init.buildDatabase()
    root = tk.Tk()
    gui.Index(root)
    root.mainloop()
    root.quit()
    """
    init.buildDatabase()
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    Index(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()