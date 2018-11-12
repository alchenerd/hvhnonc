# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 15:26:17 2018

@author: alchenerd (alchenerd@gmail.com)
"""

import sqlite3
import tkinter as tk
from tkinter import ttk
import datetime as dt

_welcome_image = "kaiba.gif"
_default_toplevel_size = "665x411"
_default_font = (None, 15)
_default_button_font = (None, 15)
_default_database = "HVHNONC.db"
if __name__ == "__main__":
    _default_database = "../HVHNONC.db"


def _getConnection(databaseName):
    connect = sqlite3.connect(_default_database)
    cursor = connect.cursor()
    return connect, cursor


class DateFrame(tk.Frame):
    def __init__(self, parent: tk.BaseWidget = None,
                 variable: tk.StringVar = None):
        tk.Frame.__init__(self, parent)
        self.variable = variable
        self.y = tk.StringVar()
        self.m = tk.StringVar()
        self.d = tk.StringVar()
        self.cb_y = ttk.Combobox(self, width=3, textvariable=self.y,
                                 font=_default_font)
        self.cb_m = ttk.Combobox(self, width=2, textvariable=self.m,
                                 font=_default_font)
        self.cb_d = ttk.Combobox(self, width=2, textvariable=self.d,
                                 font=_default_font)
        self.l_y = tk.Label(self, text="年", font=_default_font)
        self.l_m = tk.Label(self, text="月", font=_default_font)
        self.l_d = tk.Label(self, text="日", font=_default_font)
        self.cb_y.pack(side="left")
        self.l_y.pack(side="left")
        self.cb_m.pack(side="left")
        self.l_m.pack(side="left")
        self.cb_d.pack(side="left")
        self.l_d.pack(side="left")
        years = list(reversed(range(1, dt.datetime.now().year - 1911 + 1)))
        self.cb_y.config(values=years)
        months = list(range(1, 12 + 1))
        self.cb_m.config(values=months)
        days = list(range(1, 31 + 1))
        self.cb_d.config(values=days)
        self.setAsToday()
        self.updateDate()
        self.cb_y.bind("<<ComboboxSelected>>", self.updateDate)
        self.cb_m.bind("<<ComboboxSelected>>", self.updateDate)
        self.cb_d.bind("<<ComboboxSelected>>", self.updateDate)

    def setAsToday(self):
        y = dt.datetime.now().year - 1911
        m = dt.datetime.now().month
        d = dt.datetime.now().day
        self.y.set(str(y))
        self.m.set(str(m))
        self.d.set(str(d))
        self.updateDate()

    def clear(self):
        self.y.set("")
        self.m.set("")
        self.d.set("")
        self.variable.set("")

    def updateDate(self, event=None):
        d = (self.y.get(), self.m.get(), self.d.get())
        self.variable.set("-".join(d))


class CompoundField():
    def __init__(self, parent: tk.BaseWidget = None, widgetType: str = None,
                 description: str = "標籤", fieldName: str = None,
                 enabledState: str = None, **kwargs):
        self.parent = parent
        self.label = tk.Label(parent, text=description + "：",
                              font=_default_font)
        self.widgetType = widgetType.title()
        self.widget = None
        self.variable = tk.StringVar()
        self.enabledState = enabledState.lower()
        self.widget = self.getWidget(widgetType, parent, self.variable)
        if "opt" in kwargs and kwargs["opt"] == "minmax":
            self.opt = "minmax"
            self.widget = tk.Frame(parent)
            self.variableMin = tk.StringVar()
            self.variableMax = tk.StringVar()
            self.widgetMin = self.getWidget(widgetType, self.widget,
                                            self.variableMin)
            self.tilde = tk.Label(self.widget, text="~", font=_default_font)
            self.widgetMax = self.getWidget(widgetType, self.widget,
                                            self.variableMax)
            self.widgetMin.pack(side="left")
            self.tilde.pack(side="left")
            self.widgetMax.pack(side="left")
        self.fieldName = fieldName
        self.description = description

    def getWidget(self, widgetType, parent, variable):
        if widgetType == "Entry":
            return tk.Entry(parent, textvariable=variable,
                            font=_default_font, width=20)
        if widgetType == "Combobox":
            return ttk.Combobox(parent, textvariable=variable,
                                font=_default_font, width=20)
        if widgetType == "DateFrame":
            return DateFrame(parent, variable)