# -*- coding: utf-8 -*-
"""
Created on Tue Oct  2 11:08:53 2018

@author: 戴佳燊 (alchenerd@gmail.com)

@project name: Hualien Veterans Home NON-Consumables dbms (HVHNONC)
"""

import tkinter as tk

import init
import gui


def main():
    init.buildDatabase()
    root = tk.Tk()
    gui.Index(root)
    root.mainloop()
    root.quit()


if __name__ == "__main__":
    main()