# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 15:39:07 2018

@author: alchenerd (alchenerd@gmail.com)
"""

import tkinter as tk
from tkinter import ttk

import noncgui.utils as utils

class PrintNonc(tk.Toplevel):
    def __init__(self, parent, *args, **kwargs):
        s = ttk.Style()
        s.configure('printNonc.TButton', font=utils._default_button_font)
        tk.Toplevel.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.attributes("-topmost", "true")
        self.attributes("-topmost", "false")
        self.title("列印")
        self.geometry(utils._default_toplevel_size)
        self.resizable(False, False)
        # gui
        self.l = tk.Label(self, text="列印畫面", font=utils._default_font)
        self.l.pack()
        # buttons
        self.btn_quit = ttk.Button(self, text='返回',
                                   style="printNonc.TButton",
                                   command=self.quitMe)
        self.btn_quit.pack()
        # focus
        self.grab_set()

    def quitMe(self):
        self.destroy()