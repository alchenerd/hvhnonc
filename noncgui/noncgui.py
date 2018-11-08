# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 11:13:25 2018
@author: alchenerd (alchenerd@gmail.com)
The module where I put tkinter frames, toplevels, and their functions
"""

import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import hashlib
import datetime as dt

from __init__ import __version__

_welcome_image = "kaiba.gif"
_default_toplevel_size = "665x411"
_default_font = (None, 15)
_default_button_font = (None, 15)
_default_database = "HVHNONC.db"
if __name__ == "__main__":
    _default_database = "../HVHNONC.db"

# TODO: <alchenerd@gmail.com>
# Refactor the whole thing using the CompoundField class
# Someday it will be done...
# ...someday.

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

    def updateDate(self, event = None):
        d = (self.y.get(), self.m.get(), self.d.get())
        self.variable.set("-".join(d))


class CompoundField():
    def __init__(self, parent: tk.BaseWidget = None, widgetType: str = None,
                 description: str = "標籤", fieldName: str = None,
                 enabledState: str = None, **kwargs):
        self.parent = parent
        self.label = tk.Label(parent, text=description+"：",
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

class Index(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        parent.geometry("640x350")
        parent.title("非消耗品管理系統 (v"+__version__+")")
        parent.focus_force()
        parent.resizable(False, False)
        # listbox font style
        parent.option_add('*TCombobox*Listbox.font', _default_font)
        # an image
        photo = tk.PhotoImage(file=_welcome_image)
        self.label_welcome = tk.Label(image=photo)
        self.label_welcome.image = photo
        self.label_welcome.place(x=20, y=20)
        # buttons
        indexBtnStyle = ttk.Style()
        indexBtnStyle.configure('index.TButton', font=('Helvetica', 20))
        self.btn_register = ttk.Button(
                self, text="輸入", style="index.TButton",
                command=self.registerPressed)
        self.btn_register.place(x=444, y=30)
        self.btn_unregister = ttk.Button(
                self, text="除帳", style="index.TButton",
                command=self.unregisterPressed)
        self.btn_unregister.place(x=444, y=90)
        self.btn_print = ttk.Button(
                self, text="列印", style="index.TButton",
                command=self.printPressed)
        self.btn_print.place(x=444, y=150)
        self.btn_maintenance = ttk.Button(
                self, text="維護", style="index.TButton",
                command=self.maintenancePressed)
        self.btn_maintenance.place(x=444, y=210)
        self.btn_quit = ttk.Button(
                self, text="離開", style="index.TButton",
                command=self.quitHVHODBMS)
        self.btn_quit.place(x=444, y=270)
        self.pack(expand=True, fill="both")
        Login(self)

    def registerPressed(self):
        register(self)

    def unregisterPressed(self):
        unregister(self)

    def printPressed(self):
        printNonc(self)

    def maintenancePressed(self):
        maintenance(self)

    def quitHVHODBMS(self):
        self.parent.destroy()


class Login(tk.Toplevel):
    def __init__(self, parent, *args, **kwargs):
        tk.Toplevel.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.attributes("-topmost", "true")
        self.attributes("-topmost", "false")
        self.title("登入")
        self.geometry("250x115")
        self.resizable(False, False)
        # user info
        self.label_username = tk.Label(self, text="帳號:",
                                       font=_default_font)
        self.label_password = tk.Label(self, text="密碼:",
                                       font=_default_font)
        self.label_username.place(x=4,y=10)
        self.label_password.place(x=4,y=40)
        self.var_username = tk.StringVar()
        self.var_username.set("administrator")
        self.var_password = tk.StringVar()
        self.var_password.set("veteranshome")
        self.entry_username = tk.Entry(
                self, textvariable=self.var_username, font=_default_font)
        self.entry_password = tk.Entry(
                self, textvariable=self.var_password,
                font=_default_font, show="*")
        self.entry_username.place(x=58, y=13)
        self.entry_password.place(x=58, y=43)
        # buttons
        s = ttk.Style()
        s.configure('login.TButton', font=_default_button_font)
        self.btn_login = ttk.Button(
                self, text='登入', style="login.TButton",
                command=self.validate)
        self.btn_login.place(x=6, y=75)
        self.btn_quit = ttk.Button(
                self, text='離開', style="login.TButton",
                command=self.abortLogin)
        self.btn_quit.place(x=134, y=75)
        self.bind("<Return>", self.catchReturn)
        # focus and listen
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.abortLogin)

    def abortLogin(self):
        self.parent.parent.destroy()

    def catchReturn(self, event):
        self.validate()

    def validate(self):
        # check for valid username and password
        # restriction: printable ASCII char[20]
        username = self.var_username.get()
        password = self.var_password.get()
        if self.isValid(username, password):
            # database stuff
            connect, cursor = _getConnection(_default_database)
            sqlstr = ("select * from hvhnonc_users where username='"
                      + self.var_username.get() + "';")
            #print(sqlstr)
            cursor.execute(sqlstr)
            row = cursor.fetchone()
            connect.close()
            # row = [(ID, username, hash_SHA256, salt)]
            #print(row)
            if row == None:
                messagebox.showerror(
                        "錯誤", "不正確的帳號或密碼", parent=self)
                return;
            DB_hash = row[2]
            DB_salt = row[3]
            # SHA256 hash the DB_salt + password
            sha256 = hashlib.sha256()
            data = DB_salt + password
            sha256.update(data.encode("utf-8"))
            localHash = sha256.hexdigest()
            #print(sha256.hexdigest())
            if localHash == DB_hash:
                self.parent.parent.focus_force()
                self.destroy()
            else:
                messagebox.showerror(
                        "錯誤", "不正確的帳號或密碼", parent=self)
        else:
            # <meme> is this error handling? </meme>
            messagebox.showerror(
                    "錯誤", "帳號與密碼須為20字以內的英數字", parent=self)

    def isValid(self, username, password):
        if (username.isalnum() and len(username) <= 20
            and password.isalnum() and len(password) <= 20):
             return True
        else:
             return False


class register(tk.Toplevel):
    def __init__(self, parent, *args, **kwargs):
        self.state = "none"
        self.book = self.getAllRecords()
        self.index = 0
        # button style for register form
        s = ttk.Style()
        s.configure('register.TButton', font=_default_button_font)
        # initialization
        tk.Toplevel.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        # pop to topmost but don't get in the way
        self.attributes("-topmost", "true")
        self.attributes("-topmost", "false")
        self.title("輸入")
        self.geometry(_default_toplevel_size)
        self.resizable(False, False)
        # register form GUI
        # category
        self.lb_cat = tk.Label(self, text="物品大項: ",
                               font=_default_font)
        self.lb_cat.grid(row=0, column=0, padx=5, pady=5)
        self.category = tk.StringVar()
        self.cb_cat = ttk.Combobox(
                self, width=20, textvariable=self.category,
                font=_default_font, state="readonly")
        self.cb_cat.grid(row=0, column=1, padx=5, pady=5)
        # subcategory
        self.lb_subcat = tk.Label(self, text="物品細目: ",
                                  font=_default_font)
        self.lb_subcat.grid(row=0, column=2, padx=5, pady=5)
        self.subcategory = tk.StringVar()
        self.cb_subcat = ttk.Combobox(
                self, width=20, textvariable=self.subcategory,
                font=_default_font, state="readonly")
        self.cb_subcat.grid(row=0, column=3, padx=5, pady=5)
        # name
        self.lb_name = tk.Label(self, text="物品名稱: ",
                                font=_default_font)
        self.lb_name.grid(row=1, column=0, padx=5, pady=5)
        self.name = tk.StringVar()
        self.cb_name = ttk.Combobox(
                self, width=20, textvariable=self.name,
                font=_default_font)
        self.cb_name.grid(row=1, column=1, padx=5, pady=5)
        # unit
        self.lb_unit = tk.Label(
                self, text="單位: ", font=_default_font)
        self.lb_unit.grid(row=1, column=2, padx=5, pady=5)
        self.unit = tk.StringVar()
        self.cb_unit = ttk.Combobox(
                self, width=20, textvariable=self.unit,
                font=_default_font)
        self.cb_unit.grid(row=1, column=3, padx=5, pady=5)
        # brand
        self.lb_brand = tk.Label(self, text="品牌: ",
                                 font=_default_font)
        self.lb_brand.grid(row=2, column=0, padx=5, pady=5)
        self.brand = tk.StringVar()
        self.cb_brand = ttk.Combobox(self, width=20,
                                     textvariable=self.brand,
                                     font=_default_font)
        self.cb_brand.grid(row=2, column=1, padx=5, pady=5)
        # spec
        self.lb_spec = tk.Label(self, text="規格: ",
                                font=_default_font)
        self.lb_spec.grid(row=2, column=2, padx=5, pady=5)
        self.spec = tk.StringVar()
        self.cb_spec = ttk.Combobox(self, width=20,
                                    textvariable=self.spec,
                                    font=_default_font)
        self.cb_spec.grid(row=2, column=3, padx=5, pady=5)
        # serial
        self.f_serial = tk.Frame(self)
        self.lb_objID = tk.Label(
                self.f_serial, text="物品編號: ", font=_default_font)
        self.lb_objID.pack(side='left', padx=10)
        self.objID = tk.StringVar()
        self.ent_objID = tk.Entry(
                self.f_serial, width=18, textvariable=self.objID,
                font=_default_font, state="disabled")
        self.ent_objID.pack(side='left', padx=10)
        self.lb_serial = tk.Label(
                self.f_serial, text="流水號: ", font=_default_font)
        self.lb_serial.pack(side='left', padx=10)
        self.serial = tk.StringVar()
        self.ent_serial = tk.Entry(
                self.f_serial, width=5, textvariable=self.serial,
                font=_default_font, state="disabled")
        self.ent_serial.pack(side='left', padx=10)
        self.btn_lookupSerial = ttk.Button(
                self.f_serial, text="流水號總覽",
                style="register.TButton", command=self.lookupSerial)
        self.btn_lookupSerial.pack(side='left', padx=10)
        self.f_serial.grid(row=3, column=0, columnspan=4,
                           padx=5, pady=5)
        # in date
        self.lb_in_date = tk.Label(
                self, text="購置日期: ", font=_default_font)
        self.lb_in_date.grid(row=4, column=0, padx=5, pady=5)
        self.f_in_date = tk.Frame(self)
        self.in_date_yy = tk.StringVar()
        self.cb_in_date_yy = ttk.Combobox(
                self.f_in_date, width=3, textvariable=self.in_date_yy,
                font=_default_font)
        self.cb_in_date_yy.pack(side='left')
        self.lb_in_date_yy = tk.Label(self.f_in_date, text="年",
                                      font=_default_font)
        self.lb_in_date_yy.pack(side='left')
        self.in_date_mm = tk.StringVar()
        self.cb_in_date_mm = ttk.Combobox(
                self.f_in_date, width=2, textvariable=self.in_date_mm,
                font=_default_font)
        self.cb_in_date_mm.pack(side='left')
        self.lb_in_date_mm = tk.Label(self.f_in_date, text="月",
                                      font=_default_font)
        self.lb_in_date_mm.pack(side='left')
        self.in_date_dd = tk.StringVar()
        self.cb_in_date_dd = ttk.Combobox(
                self.f_in_date, width=2, textvariable=self.in_date_dd,
                font=_default_font)
        self.cb_in_date_dd.pack(side='left')
        self.lb_in_date_dd = tk.Label(self.f_in_date, text="日",
                                      font=_default_font)
        self.lb_in_date_dd.pack(side='left')
        self.f_in_date.grid(row=4, column=1, padx=5, pady=5)
        # key date
        self.lb_key_date = tk.Label(self, text="建帳日期: ",
                                    font=_default_font)
        self.lb_key_date.grid(row=4, column=2, padx=5, pady=5)
        self.f_key_date = tk.Frame(self)
        self.key_date_yy = tk.StringVar()
        self.cb_key_date_yy = ttk.Combobox(
                self.f_key_date, width=3,
                textvariable=self.key_date_yy, font=_default_font)
        self.cb_key_date_yy.pack(side='left')
        self.lb_key_date_yy = tk.Label(self.f_key_date, text="年",
                                       font=_default_font)
        self.lb_key_date_yy.pack(side='left')
        self.key_date_mm = tk.StringVar()
        self.cb_key_date_mm = ttk.Combobox(
                self.f_key_date, width=2,
                textvariable=self.key_date_mm, font=_default_font)
        self.cb_key_date_mm.pack(side='left')
        self.lb_key_date_mm = tk.Label(self.f_key_date, text="月",
                                       font=_default_font)
        self.lb_key_date_mm.pack(side='left')
        self.key_date_dd = tk.StringVar()
        self.cb_key_date_dd = ttk.Combobox(
                self.f_key_date, width=2,
                textvariable=self.key_date_dd, font=_default_font)
        self.cb_key_date_dd.pack(side='left')
        self.lb_key_date_dd = tk.Label(self.f_key_date, text="日",
                                       font=_default_font)
        self.lb_key_date_dd.pack(side='left')
        self.f_key_date.grid(row=4, column=3, padx=5, pady=5)
        # source, price, amount are in the same frame
        self.f_sourcePriceAmount = tk.Frame(self)
        self.lb_source = tk.Label(
                self.f_sourcePriceAmount, text="來源: ",
                font=_default_font)
        self.lb_source.pack(side='left', padx=10)
        self.source = tk.StringVar()
        self.cb_source = ttk.Combobox(
                self.f_sourcePriceAmount, width=8,
                textvariable=self.source, font=_default_font,
                state="readonly")
        self.cb_source.pack(side='left', padx=10)
        self.lb_price = tk.Label(self.f_sourcePriceAmount,
                                 text="價格: ", font=_default_font)
        self.lb_price.pack(side='left', padx=10)
        self.price = tk.StringVar()
        self.ent_price = tk.Entry(
                self.f_sourcePriceAmount, width=8,
                textvariable=self.price, font=_default_font)
        self.ent_price.pack(side='left', padx=10)
        self.lb_amount = tk.Label(self.f_sourcePriceAmount,
                                  text="數量: ", font=_default_font)
        self.lb_amount.pack(side='left', padx=10)
        self.amount = tk.StringVar()
        self.cb_amount = tk.Entry(
                self.f_sourcePriceAmount, width=8,
                textvariable=self.amount, font=_default_font)
        self.cb_amount.pack(side='left', padx=10)
        self.f_sourcePriceAmount.grid(row=5, column=0, columnspan=4,
                                      padx=5, pady=5)
        # place
        self.lb_place = tk.Label(self, text="存置地點: ",
                                 font=_default_font)
        self.lb_place.grid(row=6, column=0, padx=5, pady=5)
        self.place = tk.StringVar()
        self.cb_place = ttk.Combobox(
                self, width=20, textvariable=self.place,
                font=_default_font)
        self.cb_place.grid(row=6, column=1, padx=5, pady=5)
        # lifespan(in years)
        self.lb_keep_year = tk.Label(self, text="保管年限: ",
                                     font=_default_font)
        self.lb_keep_year.grid(row=6, column=2, padx=5, pady=5)
        self.keep_year = tk.StringVar()
        self.f_keep_year = tk.Frame(self)
        self.ent_keep_year = tk.Entry(
                self.f_keep_year, width=15,
                textvariable=self.keep_year, font=_default_font)
        self.ent_keep_year.pack(side="left")
        self.lb_keep_year_yy = tk.Label(self.f_keep_year, text="年",
                                        font=_default_font)
        self.lb_keep_year_yy.pack(side="left")
        self.f_keep_year.grid(row=6, column=3, padx=5, pady=5)
        # keeper department
        self.lb_keep_dept = tk.Label(self, text="保管單位: ",
                                     font=_default_font)
        self.lb_keep_dept.grid(row=7, column=0, padx=5, pady=5)
        self.keep_dept = tk.StringVar()
        self.cb_keep_dept = ttk.Combobox(
                self, width=20, textvariable=self.keep_dept,
                font=_default_font)
        self.cb_keep_dept.grid(row=7, column=1, padx=5, pady=5)
        # use department
        self.lb_use_dept = tk.Label(self, text="使用單位: ",
                                    font=_default_font)
        self.lb_use_dept.grid(row=7, column=2, padx=5, pady=5)
        self.use_dept = tk.StringVar()
        self.cb_use_dept = ttk.Combobox(
                self, width=20, textvariable=self.use_dept,
                font=_default_font)
        self.cb_use_dept.grid(row=7, column=3, padx=5, pady=5)
        # keeper(person)
        self.lb_keeper = tk.Label(self, text="保管人: ",
                                  font=_default_font)
        self.lb_keeper.grid(row=8, column=0, padx=5, pady=5)
        self.keeper = tk.StringVar()
        self.cb_keeper = ttk.Combobox(
                self, width=20, textvariable=self.keeper,
                font=_default_font)
        self.cb_keeper.grid(row=8, column=1, padx=5, pady=5)
        # remarks
        self.lb_remark = tk.Label(self, text="備註事項: ",
                                  font=_default_font)
        self.lb_remark.grid(row=9, column=0, padx=5, pady=5)
        self.remark = tk.StringVar()
        self.cb_remark = ttk.Combobox(
                self, width=32, textvariable=self.remark,
                font=_default_font)
        self.cb_remark.grid(row=9, column=1, columnspan=2,
                             padx=5, pady=5)
        # buttons for searching
        self.f_bottomright = tk.Frame(self)
        self.btn_search = ttk.Button(
                self.f_bottomright, text='檢索',
                style="register.TButton", command=self.search)
        self.btn_search.pack(side="left")
        self.btn_saveThis = ttk.Button(
                self.f_bottomright, text='本筆存入',
                style="register.TButton", command=self.saveThis)
        self.btn_saveThis.pack(side="left")
        self.f_bottomright.grid(row=9, column=3, padx=5, pady=5)
        # seperator
        self.seperator = ttk.Separator(self,orient="horizontal").grid(
                row=10, columnspan=4, sticky="ew")
        # bottom navigation bar
        self.f_bottomButtons = tk.Frame(self)
        self.btn_quit = ttk.Button(
                self.f_bottomButtons, text='返回',
                style="register.TButton", command=self.quitMe)
        self.btn_quit.pack(side="left")
        self.btn_next = ttk.Button(
                self.f_bottomButtons, text='下一筆',
                style="register.TButton", command=self.fetchNext)
        self.btn_next.pack(side="left")
        self.btn_last = ttk.Button(
                self.f_bottomButtons, text='上一筆',
                style="register.TButton", command=self.fetchLast)
        self.btn_last.pack(side="left")
        self.btn_del_this = ttk.Button(
                self.f_bottomButtons, text='刪除本筆',
                style="register.TButton", command=self.deleteThis)
        self.btn_del_this.pack(side="left")
        self.btn_lookup_form = ttk.Button(
                self.f_bottomButtons, text='表單',
                style="register.TButton", command=self.lookupForm)
        self.btn_lookup_form.pack(side="left")
        self.btn_new_form = ttk.Button(
                self.f_bottomButtons, text='新增一筆',
                style="register.TButton", command=self.newForm)
        self.btn_new_form.pack(side="left")
        self.f_bottomButtons.grid(row=11, column=0, columnspan=4,
                                  padx=5, pady=5)
        # for updating purposes
        self.widgetsToDisable = [self.cb_cat, self.cb_subcat,
                                self.cb_name, self.cb_unit,
                                self.cb_brand, self.cb_spec,
                                self.cb_in_date_yy,
                                self.cb_in_date_mm,
                                self.cb_in_date_dd,
                                self.cb_key_date_yy,
                                self.cb_key_date_mm,
                                self.cb_key_date_dd,
                                self.cb_source, self.ent_price,
                                self.cb_amount, self.cb_place,
                                self.ent_keep_year, self.cb_keep_dept,
                                self.cb_use_dept, self.cb_keeper,
                                self.cb_remark, ]
        self.readonlyWidgets = [self.cb_cat, self.cb_subcat,
                                self.cb_source, ]
        # NOTE: 'normal' here means status='normal'
        self.normalWidgets = [self.cb_name, self.cb_unit,
                              self.cb_brand, self.cb_spec,
                              self.cb_in_date_yy,
                              self.cb_in_date_mm,
                              self.cb_in_date_dd,
                              self.cb_key_date_yy,
                              self.cb_key_date_mm,
                              self.cb_key_date_dd,
                              self.ent_price, self.cb_amount,
                              self.cb_place, self.ent_keep_year,
                              self.cb_keep_dept, self.cb_use_dept,
                              self.cb_keeper, self.cb_remark, ]
        self.textVariables = [self.objID, self.serial, self.category,
                              self.subcategory, self.name, self.brand,
                              self.spec, self.unit,
                              self.in_date_yy,
                              self.in_date_mm,
                              self.in_date_dd,
                              self.key_date_yy,
                              self.key_date_mm,
                              self.key_date_dd,
                              self.price, self.amount, self.place,
                              self.keep_year, self.source,
                              self.keep_dept, self.use_dept,
                              self.keeper, self.remark, ]
        # dictionary for frequently used widgets
        self.widgetDict = {
                "物品大項": self.cb_cat,
                "物品細目": self.cb_subcat,
                "物品名稱": self.cb_name,
                "單位": self.cb_unit,
                "品牌": self.cb_brand,
                "規格": self.cb_spec,
                "物品編號": self.ent_objID,
                "流水號": self.ent_serial,
                "購置日期_年": self.cb_in_date_yy,
                "購置日期_月": self.cb_in_date_mm,
                "購置日期_日": self.cb_in_date_dd,
                "建帳日期_年": self.cb_key_date_yy,
                "建帳日期_月": self.cb_key_date_mm,
                "建帳日期_日": self.cb_key_date_dd,
                "來源": self.cb_source,
                "價格": self.ent_price,
                "數量": self.cb_amount,
                "存置地點": self.cb_place,
                "保管年限": self.ent_keep_year,
                "保管單位": self.cb_keep_dept,
                "使用單位": self.cb_use_dept,
                "保管人": self.cb_keeper,
                "備註事項": self.cb_remark,
        }
        self.strvarDict = {
                "物品大項": self.category,
                "物品細目": self.subcategory,
                "物品名稱": self.name,
                "單位": self.unit,
                "品牌": self.brand,
                "規格": self.spec,
                "物品編號": self.objID,
                "流水號": self.serial,
                "購置日期_年": self.in_date_yy,
                "購置日期_月": self.in_date_mm,
                "購置日期_日": self.in_date_dd,
                "建帳日期_年": self.key_date_yy,
                "建帳日期_月": self.key_date_mm,
                "建帳日期_日": self.key_date_dd,
                "來源": self.source,
                "價格": self.price,
                "數量": self.amount,
                "存置地點": self.place,
                "保管年限": self.keep_year,
                "保管單位": self.keep_dept,
                "使用單位": self.use_dept,
                "保管人": self.keeper,
                "備註事項": self.remark,
        }
        self.updateByState(self.state)
        # get the focus in the system
        self.grab_set()

    def getAllRecords(self):
        # connect to db
        connect, cursor = _getConnection(_default_database)
        sqlstr = "select * from hvhnonc_in;"
        cursor.execute(sqlstr)
        return cursor.fetchall()

    def updateByState(self, state):
        #print(state)
        #print(type(state))
        if state.isalpha():
            state = state.lower()
        if state == "none":
            for i in self.widgetsToDisable:
                i.config(state="disabled")
            self.clearAllFields()
            return
        elif state == "new":
            for i in self.readonlyWidgets:
                i.config(state="readonly")
            for i in self.normalWidgets:
                i.config(state="normal")
            self.initializeAllField()
            self.clearAllFields()
            self.setAsToday(self.cb_in_date_yy, self.cb_in_date_mm,
                            self.cb_in_date_dd)
            self.setAsToday(self.cb_key_date_yy, self.cb_key_date_mm,
                            self.cb_key_date_dd)
            return
        else:
            # lookup in book
            self.index = self.lookupIndexInBook(state)
            #print(index)
            if self.index in range(0, len(self.book)):
                for i in self.readonlyWidgets:
                    i.config(state="readonly")
                for i in self.normalWidgets:
                    i.config(state="normal")
                self.initializeAllField()
                record = self.book[self.index]
                self.objID.set(str(record[1]))
                self.serial.set(str(record[2]))
                self.category.set(str(record[3]))
                self.subcategory.set(str(record[4]))
                self.name.set(str(record[5]))
                self.brand.set(str(record[6]))
                self.spec.set(str(record[7]))
                self.unit.set(str(record[8]))
                # in_date: yyyy-mm-dd
                in_date = str(record[9]).split('-')
                self.in_date_yy.set(str(int(in_date[0])-1911))
                self.in_date_mm.set(in_date[1])
                self.in_date_dd.set(in_date[2])
                # key_date: yyyy-mm-dd
                key_date = str(record[10]).split('-')
                self.key_date_yy.set(str(int(key_date[0])-1911))
                self.key_date_mm.set(key_date[1])
                self.key_date_dd.set(key_date[2])
                # end of date setting
                self.price.set(str(record[11]))
                self.amount.set(str(record[12]))
                self.place.set(str(record[13]))
                self.keep_year.set(str(record[14]))
                self.source.set(str(record[15]))
                self.keep_dept.set(str(record[16]))
                self.use_dept.set(str(record[17]))
                self.keeper.set(str(record[18]))
                self.remark.set(str(record[19]))
                return
            # invalid state
            tk.messagebox.showerror("錯誤", "未知的狀態", parent=self)
            self.state = "none"
            self.updateByState(self.state);

    def setAsToday(self, yearbox, monthbox, daybox):
        yearbox.set(dt.datetime.now().year - 1911)
        monthbox.set(dt.datetime.now().month)
        daybox.set(dt.datetime.now().day)

    def lookupIndexInBook(self, state):
        try:
            int(state)
        except ValueError:
            return None
        for i, sublist in enumerate(self.book):
            if int(state) in (sublist[0],):
                return i
        return None

    def clearAllFields(self):
        for i in self.textVariables:
            i.set("")

    def initializeAllField(self):
        # 物品大項
        connect, cursor = _getConnection(_default_database)
        connect.row_factory = lambda cursor, row: row[0]
        sqlstr = "select description from hvhnonc_category;"
        cursor.execute(sqlstr)
        catagories = cursor.fetchall()
        self.cb_cat['values'] = catagories
        self.cb_cat.bind("<<ComboboxSelected>>",
                         self.onCategorySelected)
        # 物品細目
        self.cb_subcat.bind("<<ComboboxSelected>>",
                            self.onSubcategorySelected)
        # 物品名稱
        self.cb_name.bind("<<ComboboxSelected>>", self.onNameSelected)
        # 年
        thisYear = dt.datetime.now().year - 1911
        years = list(reversed(range(1, thisYear+1)))
        self.cb_in_date_yy.config(values=years)
        self.cb_key_date_yy.config(values=years)
        # 月
        months = list(range(1,13))
        self.cb_in_date_mm.config(values=months)
        self.cb_key_date_mm.config(values=months)
        # 日
        days = list(range(1,32))
        self.cb_in_date_dd.config(values=days)
        self.cb_key_date_dd.config(values=days)
        # 來源
        sources = ["購置","撥用","贈送"]
        self.cb_source.config(values=sources)
        sqlstr = (  """
                    select change_value
                    from hvhnonc_in_cache
                    where (
                        this_ID=0 and
                        change_ID=(
                            select ID
                            from hvhnonc_fields
                            where description=?))
                    order by rowid desc limit 30;
                    """)
        # 存置地點
        cursor.execute(sqlstr, ("存置地點", ))
        places = cursor.fetchall()
        self.cb_place['values'] = places
        # 保管單位
        cursor.execute(sqlstr, ("保管單位", ))
        keep_depts = cursor.fetchall()
        self.cb_keep_dept['values'] = keep_depts
        # 使用單位
        cursor.execute(sqlstr, ("使用單位", ))
        use_depts = cursor.fetchall()
        self.cb_use_dept['values'] = use_depts
        # 保管人
        cursor.execute(sqlstr, ("保管人", ))
        keepers = cursor.fetchall()
        self.cb_keeper['values'] = keepers
        # 備註事項
        cursor.execute(sqlstr, ("備註事項", ))
        remarks = cursor.fetchall()
        self.cb_remark['values'] = remarks
        connect.close()

    def onCategorySelected(self, event):
        connect, cursor = _getConnection(_default_database)
        connect.row_factory = lambda cursor, row: row[0]
        sqlstr = ("""
                  select description
                  from hvhnonc_subcategory
                  where parent_ID=(
                      select ID
                      from hvhnonc_category
                      where description=?);
                  """)
        cursor.execute(sqlstr, (self.category.get(),))
        subcatagories = cursor.fetchall()
        self.cb_subcat.config(values=subcatagories)

        if (len(self.cb_subcat['values']) > 0 and
            self.cb_subcat.get() != self.cb_subcat['values'][0]):
            self.cb_subcat.set(self.cb_subcat['values'][0])
            self.onSubcategorySelected(None)
        connect.close()

    def onSubcategorySelected(self, event):
        # update product name
        connect, cursor = _getConnection(_default_database)
        sqlstr = ("""select change_value
                  from hvhnonc_in_cache
                  where (
                      this_ID=(
                          select ID
                          from hvhnonc_fields
                          where description=?) and
                      this_value=? and
                      change_ID=(
                          select ID
                          from hvhnonc_fields
                          where description=?)
                  );""")
        params = ("物品細目", self.subcategory.get(), "物品名稱")
        cursor.execute(sqlstr, params)
        rows = cursor.fetchall()
        self.cb_name.config(values=rows)
        if (len(self.cb_name['values']) > 0 and
            self.cb_name.get() != self.cb_name['values'][0]):
            self.cb_name.set(self.cb_name['values'][0])
            self.onNameSelected(None)
        connect.close()

    def onNameSelected(self, event):
        # update product name
        connect,cursor = _getConnection(_default_database)
        sqlstr = ("""
                  select change_value
                  from hvhnonc_in_cache
                  where (
                      this_ID=(
                          select ID
                          from hvhnonc_fields
                          where description=?) and
                      this_value=? and
                      change_ID=(
                          select ID
                          from hvhnonc_fields
                          where description=?))
                  order by rowid desc limit 30;
                  """)
        params = ["物品名稱", self.name.get(), "",]
        # 單位
        params[2] = "單位"
        cursor.execute(sqlstr, params)
        units = cursor.fetchall()
        self.cb_unit.config(values=units)
        if (len(self.cb_unit['values']) > 0 and
            self.cb_unit.get() != self.cb_unit['values'][0]):
            self.cb_unit.set(self.cb_unit['values'][0])
        # 品牌
        params[2] = "品牌"
        cursor.execute(sqlstr, params)
        brands = cursor.fetchall()
        self.cb_brand.config(values=brands)
        if (len(self.cb_brand['values']) > 0 and
            self.cb_brand.get() != self.cb_brand['values'][0]):
            self.cb_brand.set(self.cb_brand['values'][0])
        # 規格
        params[2] = "規格"
        cursor.execute(sqlstr, params)
        specs = cursor.fetchall()
        self.cb_spec.config(values=specs)
        if (len(self.cb_spec['values']) > 0 and
            self.cb_spec.get() != self.cb_spec['values'][0]):
            self.cb_spec.set(self.cb_spec['values'][0])
        connect.close()

    def getFieldIDByName(self, name):
        # connect to db
        connect,cursor = _getConnection(_default_database)
        connect.row_factory = lambda cursor, row: row[0]
        sqlstr = (  """
                    select ID
                    from hvhnonc_fields
                    where description=?;
                    """)
        cursor.execute(sqlstr, name)
        hit = cursor.fetchone()
        if hit:
            return hit[0]
        return None

    def lookupSerial(self):
        # open a toplevel
        self.SerialWindow(self)

    class SerialWindow(tk.Toplevel):
        def __init__(self, parent, *args, **kwargs):
            # treeview styles
            style = ttk.Style()
            style.configure("Treeview", font=_default_font)
            style.configure("Treeview.Heading", font=_default_font)
            # init
            tk.Toplevel.__init__(self, parent, *args, **kwargs)
            self.parent = parent
            self.attributes("-topmost", "true")
            self.attributes("-topmost", "false")
            # get serials from db_in
            # connect to db
            connect,cursor = _getConnection(_default_database)
            sqlstr = "select count(distinct name) from hvhnonc_in;"
            cursor.execute(sqlstr)
            itemCount = cursor.fetchone()
            self.title("序號: 共{}筆".format(itemCount[0]))
            self.geometry("640x500")
            # get all objIDs and sqlIDs
            sqlstr = (  """
                        select object_ID, name, count(*)
                        from hvhnonc_in
                        group by object_ID, name
                        order by object_ID, serial_ID;
                        """)
            cursor.execute(sqlstr)
            data = cursor.fetchall()
            # make a tree view
            sb = tk.Scrollbar(self)
            tv = ttk.Treeview(self, yscrollcommand=sb.set,
                              columns=('1', '2', '3'),show="headings")
            tv.heading('1',text='編號')
            tv.heading('2',text='品名')
            tv.heading('3',text='數量')
            tv.column('3', anchor="e")
            sb.config(command=tv.yview)
            for d in data:
                tv.insert("", "end", values=d)
            sb.pack(side="right", fill="y")
            tv.pack(fill="both", expand=1)
            connect.close()
            self.grab_set()

    def search(self):
        # open a toplevel
        self.SearchWindow(self)

    class SearchWindow(tk.Toplevel):
        def __init__(self, parent, *args, **kwargs):
            s = ttk.Style()
            s.configure('search.TButton', font=_default_button_font)
            tk.Toplevel.__init__(self, parent, *args, **kwargs)
            self.parent = parent
            self.attributes("-topmost", "true")
            self.attributes("-topmost", "false")
            self.title("檢索")
            self.resizable(False, False)
            self.geometry("465x60")
            # searchbar
            self.l_search = tk.Label(self, text="請輸入想要檢索的關鍵字:",
                                     font=_default_font)
            self.l_search.grid(row=0, column=0)
            self.parent.query = tk.StringVar()
            self.cb_searchbar = ttk.Combobox(
                    self, width=20, textvariable=self.parent.query,
                    font=_default_font)
            # get search cache from db
            connect,cursor = _getConnection(_default_database)
            connect.row_factory = lambda cursor, row: row[0]
            sqlstr = ("select change_value "
                      "from hvhnonc_in_cache "
                      "where change_ID = ("
                      "select ID from hvhnonc_fields "
                      "where description = '檢索') "
                      "order by rowid desc limit 30;")
            cursor.execute(sqlstr)
            rows = cursor.fetchall()
            history = []
            for row in rows:
                history.append(row[0])
            print(history)
            self.cb_searchbar.config(values=history)
            self.cb_searchbar.grid(row=0, column=1)
            # buttons
            self.f_buttons = tk.Frame(self)
            self.btn_cancel = ttk.Button(
                    self.f_buttons, text="取消", style='search.TButton',
                    command=self.quitMe)
            self.btn_cancel.pack(side="left")
            self.btn_submit = ttk.Button(
                    self.f_buttons, text="檢索", style='search.TButton',
                    command=self.onSubmitClick)
            self.btn_submit.pack(side="left")
            self.f_buttons.grid(row=1, column=1, sticky="se")
            # listen to return
            self.bind("<Return>", self.catchReturn)
            self.grab_set()

        def catchReturn(self, event):
            self.onSubmitClick()

        def quitMe(self):
            self.destroy()

        def onSubmitClick(self):
            # update search cache
            connect,cursor = _getConnection(_default_database)
            sqlstr = (
                    "replace into hvhnonc_in_cache(this_ID, this_value, "
                    "change_ID, change_value) "
                    "values(0, 'none', ("
                        "select ID "
                        "from hvhnonc_fields "
                        "where description = '檢索'), "
                    "?);")
            cursor.execute(sqlstr, (self.parent.query.get(), ))
            connect.commit()
            # open a result toplevel
            self.SearchResultWindow(self.parent)
            self.destroy()

        class SearchResultWindow(tk.Toplevel):
            def __init__(self, parent, *args, **kwargs):
                # treeview styles
                style = ttk.Style()
                style.configure("Treeview", font=_default_font)
                style.configure("Treeview.Heading", font=_default_font)
                # init
                tk.Toplevel.__init__(self, parent, *args, **kwargs)
                self.parent = parent
                self.attributes("-topmost", "true")
                self.attributes("-topmost", "false")
                self.title("檢索結果")
                self.geometry("1200x600")
                # make a tree view
                sb = tk.Scrollbar(self)
                self.tv = ttk.Treeview(
                        self, yscrollcommand=sb.set,
                        columns=('1', '2', '3', '4', '5', '6'),
                        show="headings")
                self.tv['displaycolumns'] = ('2','3','4','5','6')
                self.tv.heading('1',text='ID')
                self.tv.heading('2',text='購置日期')
                self.tv.heading('3',text='品名')
                self.tv.heading('4',text='存置位置')
                self.tv.heading('5',text='保管人')
                self.tv.heading('6',text='備註')
                sb.config(command=self.tv.yview)
                # fetch the data
                # connect to db
                connect,cursor = _getConnection(_default_database)
                phrase = str(parent.query.get())
                sqlstr = (
                        "select ID, in_date, name, place, keeper, remark "
                        "from hvhnonc_in "
                        "where("
                            "category like :q or "
                            "subcategory like :q or "
                            "name like :q or "
                            "brand like :q or "
                            "spec like :q or "
                            "place like :q or "
                            "keep_department like :q or "
                            "use_department like :q or "
                            "keeper like :q or "
                            "remark like :q) "
                            "order by in_date desc;")
                cursor.execute(sqlstr, {'q': "%{}%".format(phrase)})
                data = cursor.fetchall()
                for d in data:
                    self.tv.insert("", "end", values=d)
                sb.pack(side="right", fill="y")
                self.tv.pack(fill="both", expand=1)
                # listen to double click
                self.tv.bind("<Double-1>", self.onDoubleClick)
                self.grab_set()

            def onDoubleClick(self, event):
                item = self.tv.identify('item',event.x,event.y)
                #print("you clicked on", self.tv.item(item,"values")[0])
                self.parent.state = str(self.tv.item(item,"values")[0])
                self.parent.updateByState(self.parent.state)
                self.destroy()

    def updateCache(self, sqlstr, thisName, thatName):
        connect,cursor = _getConnection(_default_database)
        # Update cache table
        # So next time when thisName is fed,
        # autocomplete thatName
        if self.strvarDict[thatName] is not "":
            params = [thisName, "none",
                      thatName, self.strvarDict[thatName].get(), ]
            if thisName not in ("無", ):
                params[1] = self.strvarDict[thisName].get()
            try:
                cursor.execute(sqlstr, params)
                connect.commit()
            except Exception as e:
                print("Exception in updateCache: %s" % e)
                tk.messagebox.showerror("錯誤 updateCache", str(e),
                                        parent=self)

    def updateAllCache(self, sqlstr):
        self.updateCache(sqlstr, "物品細目", "物品名稱")
        self.updateCache(sqlstr, "物品名稱", "單位")
        self.updateCache(sqlstr, "物品名稱", "品牌")
        self.updateCache(sqlstr, "物品名稱", "規格")
        self.updateCache(sqlstr, "無", "存置地點")
        self.updateCache(sqlstr, "無", "保管單位")
        self.updateCache(sqlstr, "無", "使用單位")
        self.updateCache(sqlstr, "無", "保管人")
        self.updateCache(sqlstr, "無", "備註事項")

    def saveThis(self):
        if (self.category.get() is "" or
            self.subcategory.get() is "" or
            self.name.get() is ""):
            tk.messagebox.showerror("錯誤","有欄位未填",parent=self)
            return
        connect, cursor = _getConnection(_default_database)
        #connect.set_trace_callback(print)
        # object_ID, serial_ID
        # objID is '6-(ID_cat)-(ID_subcat)'
        sqlstr = ("select parent_ID, ID "
                  "from hvhnonc_subcategory "
                  "where parent_ID=("
                  "select ID "
                  "from hvhnonc_category "
                  "where description=?) "
                  "and description=?;")
        params = (self.category.get(), self.subcategory.get(), )
        try:
            cursor.execute(sqlstr, params)
            row = cursor.fetchone()
            objID = ("6",
                     "{:02d}".format(int(row[0])),
                     "{:02d}".format(int(row[1])))
        except Exception as e:
            print("Exception in saveThis: %s" % e)
            tk.messagebox.showerror("錯誤1", str(e), parent=self)
        objID = " - ".join(objID)
        sqlstr = ("select serial_ID "
                  "from hvhnonc_in "
                  "where object_ID=? and name=?;")
        params = (objID, self.name.get(), )
        try:
            cursor.execute(sqlstr, params)
        except Exception as e:
            print("Exception in saveThis: %s" % e)
            tk.messagebox.showerror("錯誤2", str(e), parent=self)
        row = cursor.fetchone()
        if row is None:
            sqlstr = ("select count(distinct serial_ID) "
                      "from hvhnonc_in "
                      "where object_ID=?;")
            try:
                cursor.execute(sqlstr, (params[0], ))
                row = cursor.fetchone()
                serialID = "{:03}".format(int(row[0])+1)
            except Exception as e:
                print("Exception in saveThis: %s" % e)
                tk.messagebox.showerror("錯誤3", str(e), parent=self)
        else:
            serialID = str(row[0])
        # date string preparation
        tmp_in_date = "-".join(
                (str(int(self.in_date_yy.get()) + 1911),
                str("{:02}".format(int(self.in_date_mm.get()))),
                str("{:02}".format(int(self.in_date_dd.get()))), ))
        tmp_key_date = "-".join(
                (str(int(self.key_date_yy.get()) + 1911),
                str("{:02}".format(int(self.key_date_mm.get()))),
                str("{:02}".format(int(self.key_date_dd.get()))), ))
        # insert new row
        if self.state in ("new", ):
            # insertion statement
            sqlstr = ("insert into hvhnonc_in("
                      "object_ID, serial_ID, category, subcategory, "
                      "name, brand, spec, unit, in_date, key_date, "
                      "price, amount, place, keep_year, source, "
                      "keep_department, use_department, keeper, "
                      "remark) "
                      "values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, "
                      "?, ?, ?, ?, ?, ?);")
            params = (str(objID), str(serialID),
                    self.category.get(), self.subcategory.get(),
                    self.name.get(), self.brand.get(),
                    self.spec.get(), self.unit.get(),
                    str(tmp_in_date), str(tmp_key_date),
                    self.price.get(), self.amount.get(),
                    self.place.get(), self.keep_year.get(),
                    self.source.get(), self.keep_dept.get(),
                    self.use_dept.get(), self.keeper.get(),
                    self.remark.get(), )
            try:
                cursor.execute(sqlstr, params)
                connect.commit()
                tk.messagebox.showinfo("新增成功", "已新增一筆資料",
                                       parent=self)
            except Exception as e:
                print("Exception in saveThis: %s" % e)
                tk.messagebox.showerror("錯誤4", str(e), parent=self)
            # update cache table
            sqlstr = (  """
                        insert or ignore into
                         hvhnonc_in_cache(this_ID, this_value,
                                          change_ID, change_value)
                         values(
                            (select ID from hvhnonc_fields
                                 where description = ?),
                             ?,
                            (select ID from hvhnonc_fields
                                 where description = ?),
                             ?)
                        """)
            self.updateAllCache(sqlstr)
            # update book
            self.book = self.getAllRecords()
            connect.close()
            self.state = "none"
            self.updateByState(self.state)
        elif self.lookupIndexInBook(self.state) is not None:
            # if collide ask new or replace
            isWriteover = tk.messagebox.askyesnocancel(
                    "重複寫入",
                    "是否要複蓋掉這筆資料?(按否會新增一筆新資料)",
                    parent=self)
            if isWriteover is True:
                # replace
                sqlstr = ("replace into hvhnonc_in("
                          "ID, object_ID, serial_ID, "
                          "category, subcategory, "
                          "name, brand, spec, unit, "
                          "in_date, key_date, "
                          "price, amount, place, "
                          "keep_year, source, "
                          "keep_department, use_department, "
                          "keeper, remark) "
                          "values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, "
                          "?, ?, ?, ?, ?, ?, ?, ?);")
                params = (self.state, str(objID), str(serialID),
                        self.category.get(), self.subcategory.get(),
                        self.name.get(), self.brand.get(),
                        self.spec.get(), self.unit.get(),
                        str(tmp_in_date), str(tmp_key_date),
                        self.price.get(), self.amount.get(),
                        self.place.get(), self.keep_year.get(),
                        self.source.get(), self.keep_dept.get(),
                        self.use_dept.get(), self.keeper.get(),
                        self.remark.get(), )
                try:
                    cursor.execute(sqlstr, params)
                    connect.commit()
                    tk.messagebox.showinfo("覆寫成功", "已覆寫一筆資料",
                                           parent=self)
                except Exception as e:
                    print("Exception in saveThis: %s" % e)
                    tk.messagebox.showerror("錯誤5", str(e),
                                            parent=self)
                # update cache table
                sqlstr = ("insert or ignore into "
                          "hvhnonc_in_cache(this_ID, this_value, "
                          "change_ID, change_value) "
                          "values("
                          "(select ID from hvhnonc_fields "
                          "where description = ?), "
                          "?, "
                          "(select ID from hvhnonc_fields "
                          "where description = ?), "
                          "?)")
                self.updateAllCache(sqlstr)
                # update book
                self.book = self.getAllRecords()
                connect.close()
                self.state = "none"
                self.updateByState(self.state)
            elif isWriteover is False:
                # insert new row
                sqlstr = ("insert into hvhnonc_in("
                          "object_ID, serial_ID, "
                          "category, subcategory, "
                          "name, brand, spec, unit, "
                          "in_date, key_date, "
                          "price, amount, place, "
                          "keep_year, source, "
                          "keep_department, use_department, "
                          "keeper, remark) "
                          "values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, "
                          "?, ?, ?, ?, ?, ?, ?);")
                params = (str(objID), str(serialID),
                        self.category.get(), self.subcategory.get(),
                        self.name.get(), self.brand.get(),
                        self.spec.get(), self.unit.get(),
                        str(tmp_in_date), str(tmp_key_date),
                        self.price.get(), self.amount.get(),
                        self.place.get(), self.keep_year.get(),
                        self.source.get(), self.keep_dept.get(),
                        self.use_dept.get(), self.keeper.get(),
                        self.remark.get(),)
                try:
                    cursor.execute(sqlstr, params)
                    connect.commit()
                    tk.messagebox.showinfo("新增成功", "已新增一筆資料",
                                           parent=self)
                except Exception as e:
                    print("Exception in saveThis: %s" % e)
                    tk.messagebox.showerror("錯誤6", str(e),
                                            parent=self)
                # update cache table
                # sql insert template
                sqlstr = ("insert or ignore into "
                          "hvhnonc_in_cache(this_ID, this_value, "
                          "change_ID, change_value) "
                          "values("
                          "(select ID from hvhnonc_fields "
                          "where description = ?), "
                          "?, "
                          "(select ID from hvhnonc_fields "
                          "where description = ?), "
                          "?);")
                self.updateAllCache(sqlstr)
                # update book
                self.book = self.getAllRecords()
                connect.close()
                self.state = "none"
                self.updateByState(self.state)
            # do nothing if cancel is pressed

    def fetchNext(self):
        if self.state in ("none", "new"):
            self.index = 0
            self.state = str(self.book[self.index][0])
            self.updateByState(self.state)
        else:
            if self.index == len(self.book)-1:
                tk.messagebox.showinfo("到底了", "已到達最後一筆",
                                       parent=self)
            else:
                self.index = self.index+1
                self.state = str(self.book[self.index][0])
                self.updateByState(self.state)

    def fetchLast(self):
        if self.state in ("none", "new"):
            self.index = len(self.book)-1
            self.state = str(self.book[self.index][0])
            self.updateByState(self.state)
        else:
            if self.index == 0:
                tk.messagebox.showinfo("到頂了", "已到達第一筆",
                                       parent=self)
            else:
                self.index = self.index-1
                self.state = str(self.book[self.index][0])
                self.updateByState(self.state)

    def deleteThis(self):
        # deletes the row if it's in the book
        #print("deleteThis")
        if self.state in ("new", "none", ):
            tk.messagebox.showerror("錯誤", "不是資料庫內的資料",
                                    parent=self)
            self.state = "none"
            self.updateByState(self.state)
            return
        connect,cursor = _getConnection(_default_database)
        sqlstr = "delete from hvhnonc_in where ID=?;"
        param = (self.state, )
        try:
            cursor.execute(sqlstr, param)
            connect.commit()
            tk.messagebox.showinfo("刪除成功",
                                   "已刪除一筆ID為{}的資料".format(self.state),
                                   parent=self)
            # update the book
            self.book = self.getAllRecords()
        except sqlite3.Error as e:
            tk.messagebox.showerror("錯誤", "沒有這筆資料", parent=self)
            print(e.args[0])
        except Exception as e:
            tk.messagebox.showerror("錯誤", "未知的錯誤", parent=self)
            print(e)
        self.state = "none"
        self.updateByState(self.state)

    def lookupForm(self):
        #print("lookupForm")
        # opens a new toplevel for filtering
        self.FilterWindow(self)

    class FilterWindow(tk.Toplevel):
        def __init__(self, parent, *args, **kwargs):
            # init
            tk.Toplevel.__init__(self, parent, *args, **kwargs)
            self.parent = parent
            self.title("請輸入要篩選的範圍")
            self.geometry("665x290")
            # category
            self.lb_category = tk.Label(
                    self, text="物品大項: ", font=_default_font)
            self.lb_category.grid(row=0, column=0, padx=5, pady=5)
            self.category = tk.StringVar()
            self.cb_category = ttk.Combobox(
                    self, width=20, textvariable=self.category,
                    font=_default_font, state="readonly")
            self.cb_category.grid(row=0, column=1, padx=5, pady=5)
            # subcategory
            self.lb_subcategory = tk.Label(
                    self, text="物品細目: ", font=_default_font)
            self.lb_subcategory.grid(row=0, column=2, padx=5, pady=5)
            self.subcategory = tk.StringVar()
            self.cb_subcategory = ttk.Combobox(
                    self, width=20, textvariable=self.subcategory,
                    font=_default_font, state="readonly")
            self.cb_subcategory.grid(row=0, column=3, padx=5, pady=5)
            # name
            self.lb_name = tk.Label(
                    self, text="物品名稱: ", font=_default_font)
            self.lb_name.grid(row=1, column=0, padx=5, pady=5)
            self.name = tk.StringVar()
            self.cb_name = ttk.Combobox(
                    self, width=20, textvariable=self.name,
                    font=_default_font)
            self.cb_name.grid(row=1, column=1, padx=5, pady=5)
            # brand
            self.lb_brand = tk.Label(
                    self, text="品牌: ", font=_default_font)
            self.lb_brand.grid(row=1, column=2, padx=5, pady=5)
            self.brand = tk.StringVar()
            self.cb_brand = ttk.Combobox(
                    self, width=20, textvariable=self.brand,
                    font=_default_font)
            self.cb_brand.grid(row=1, column=3, padx=5, pady=5)
            # spec
            self.lb_spec = tk.Label(
                    self, text="規格: ", font=_default_font)
            self.lb_spec.grid(row=2, column=0, padx=5, pady=5)
            self.spec = tk.StringVar()
            self.cb_spec = ttk.Combobox(
                    self, width=20, textvariable=self.spec,
                    font=_default_font)
            self.cb_spec.grid(row=2, column=1, padx=5, pady=5)
            # price
            self.lb_price = tk.Label(
                    self, text="單價: ", font=_default_font)
            self.lb_price.grid(row=2, column=2, padx=5, pady=5)
            self.f_price = tk.Frame(self)
            self.price_min = tk.StringVar()
            self.ent_price_min = tk.Entry(
                    self.f_price, width=5, textvariable=self.price_min,
                    font=_default_font)
            self.ent_price_min.pack(side='left', padx=10)
            self.lb_sqig_price = tk.Label(
                    self.f_price, text=" ~ ", font=_default_font)
            self.lb_sqig_price.pack(side='left', padx=10)
            self.price_max = tk.StringVar()
            self.ent_price_max = tk.Entry(
                    self.f_price, width=5, textvariable=self.price_max,
                    font=_default_font)
            self.ent_price_max.pack(side='left', padx=10)
            self.f_price.grid(row=2, column=3, padx=5, pady=5)
            # in date (min~max)
            self.f_date = tk.Frame(self)
            self.lb_date = tk.Label(
                    self.f_date, text="購置日期: ", font=_default_font)
            self.lb_date.pack(side='left')
            self.date_yy_min = tk.StringVar()
            self.cb_date_yy_min = ttk.Combobox(
                    self.f_date, width=3, textvariable=self.date_yy_min,
                    font=_default_font)
            self.cb_date_yy_min.pack(side='left')
            self.lb_date_yy_min = tk.Label(
                    self.f_date, text="年", font=_default_font)
            self.lb_date_yy_min.pack(side='left')
            self.date_mm_min = tk.StringVar()
            self.cb_date_mm_min = ttk.Combobox(
                    self.f_date, width=2, textvariable=self.date_mm_min,
                    font=_default_font)
            self.cb_date_mm_min.pack(side='left')
            self.lb_date_mm_min = tk.Label(
                    self.f_date, text="月", font=_default_font)
            self.lb_date_mm_min.pack(side='left')
            self.date_dd_min = tk.StringVar()
            self.cb_date_dd_min = ttk.Combobox(
                    self.f_date, width=2, textvariable=self.date_dd_min,
                    font=_default_font)
            self.cb_date_dd_min.pack(side='left')
            self.lb_date_dd_min = tk.Label(
                    self.f_date, text="日", font=_default_font)
            self.lb_date_dd_min.pack(side='left')
            self.lb_sqig_date = tk.Label(
                    self.f_date, text="~", font=_default_font)
            self.lb_sqig_date.pack(side='left')
            self.date_yy_max = tk.StringVar()
            self.cb_date_yy_max = ttk.Combobox(
                    self.f_date, width=3, textvariable=self.date_yy_max,
                    font=_default_font)
            self.cb_date_yy_max.pack(side='left')
            self.lb_date_yy_max = tk.Label(
                    self.f_date, text="年", font=_default_font)
            self.lb_date_yy_max.pack(side='left')
            self.date_mm_max = tk.StringVar()
            self.cb_date_mm_max = ttk.Combobox(
                    self.f_date, width=2, textvariable=self.date_mm_max,
                    font=_default_font)
            self.cb_date_mm_max.pack(side='left')
            self.lb_date_mm_max = tk.Label(
                    self.f_date, text="月", font=_default_font)
            self.lb_date_mm_max.pack(side='left')
            self.date_dd_max = tk.StringVar()
            self.cb_date_dd_max = ttk.Combobox(
                    self.f_date, width=2, textvariable=self.date_dd_max,
                    font=_default_font)
            self.cb_date_dd_max.pack(side='left')
            self.lb_date_dd_max = tk.Label(
                    self.f_date, text="日", font=_default_font)
            self.lb_date_dd_max.pack(side='left')
            self.f_date.grid(row=3, column=0,
                             padx=5, pady=5, columnspan=4)
            # key date (min~max)
            self.f_key_date = tk.Frame(self)
            self.lb_key_date = tk.Label(
                    self.f_key_date, text="建帳日期: ",
                    font=_default_font)
            self.lb_key_date.pack(side='left')
            self.key_date_yy_min = tk.StringVar()
            self.cb_key_date_yy_min = ttk.Combobox(
                    self.f_key_date, width=3,
                    textvariable=self.key_date_yy_min,
                    font=_default_font)
            self.cb_key_date_yy_min.pack(side='left')
            self.lb_key_date_yy_min = tk.Label(
                    self.f_key_date, text="年", font=_default_font)
            self.lb_key_date_yy_min.pack(side='left')
            self.key_date_mm_min = tk.StringVar()
            self.cb_key_date_mm_min = ttk.Combobox(
                    self.f_key_date, width=2,
                    textvariable=self.key_date_mm_min,
                    font=_default_font)
            self.cb_key_date_mm_min.pack(side='left')
            self.lb_key_date_mm_min = tk.Label(
                    self.f_key_date, text="月", font=_default_font)
            self.lb_key_date_mm_min.pack(side='left')
            self.key_date_dd_min = tk.StringVar()
            self.cb_key_date_dd_min = ttk.Combobox(
                    self.f_key_date, width=2,
                    textvariable=self.key_date_dd_min,
                    font=_default_font)
            self.cb_key_date_dd_min.pack(side='left')
            self.lb_key_date_dd_min = tk.Label(
                    self.f_key_date, text="日", font=_default_font)
            self.lb_key_date_dd_min.pack(side='left')
            self.lb_sqig_key_date = tk.Label(
                    self.f_key_date, text="~", font=_default_font)
            self.lb_sqig_key_date.pack(side='left')
            self.key_date_yy_max = tk.StringVar()
            self.cb_key_date_yy_max = ttk.Combobox(
                    self.f_key_date, width=3,
                    textvariable=self.key_date_yy_max,
                    font=_default_font)
            self.cb_key_date_yy_max.pack(side='left')
            self.lb_key_date_yy_max = tk.Label(
                    self.f_key_date, text="年", font=_default_font)
            self.lb_key_date_yy_max.pack(side='left')
            self.key_date_mm_max = tk.StringVar()
            self.cb_key_date_mm_max = ttk.Combobox(
                    self.f_key_date, width=2,
                    textvariable=self.key_date_mm_max,
                    font=_default_font)
            self.cb_key_date_mm_max.pack(side='left')
            self.lb_key_date_mm_max = tk.Label(
                    self.f_key_date, text="月", font=_default_font)
            self.lb_key_date_mm_max.pack(side='left')
            self.key_date_dd_max = tk.StringVar()
            self.cb_key_date_dd_max = ttk.Combobox(
                    self.f_key_date, width=2,
                    textvariable=self.key_date_dd_max,
                    font=_default_font)
            self.cb_key_date_dd_max.pack(side='left')
            self.lb_key_date_dd_max = tk.Label(
                    self.f_key_date, text="日", font=_default_font)
            self.lb_key_date_dd_max.pack(side='left')
            self.f_key_date.grid(row=4, column=0,
                                 padx=5, pady=5, columnspan=4)
            # keeper department
            self.lb_keep_dept = tk.Label(
                    self, text="保管單位: ", font=_default_font)
            self.lb_keep_dept.grid(row=5, column=0, padx=5, pady=5)
            self.keep_dept = tk.StringVar()
            self.cb_keep_dept = ttk.Combobox(
                    self, width=20, textvariable=self.keep_dept,
                    font=_default_font)
            self.cb_keep_dept.grid(row=5, column=1, padx=5, pady=5)
            # place
            self.lb_place = tk.Label(
                    self, text="存置地點: ", font=_default_font)
            self.lb_place.grid(row=5, column=2, padx=5, pady=5)
            self.place = tk.StringVar()
            self.cb_place = ttk.Combobox(
                    self, width=20, textvariable=self.place,
                    font=_default_font)
            self.cb_place.grid(row=5, column=3, padx=5, pady=5)
            # use department
            self.lb_use_dept = tk.Label(
                    self, text="使用單位: ", font=_default_font)
            self.lb_use_dept.grid(row=6, column=0, padx=5, pady=5)
            self.use_dept = tk.StringVar()
            self.cb_use_dept = ttk.Combobox(
                    self, width=20, textvariable=self.use_dept,
                    font=_default_font)
            self.cb_use_dept.grid(row=6, column=1, padx=5, pady=5)
            # keeper
            self.lb_keeper = tk.Label(
                    self, text="保管人: ", font=_default_font)
            self.lb_keeper.grid(row=6, column=2, padx=5, pady=5)
            self.keeper = tk.StringVar()
            self.cb_keeper = ttk.Combobox(
                    self, width=20, textvariable=self.keeper,
                    font=_default_font)
            self.cb_keeper.grid(row=6, column=3, padx=5, pady=5)
            # bottom navigate bar
            self.f_bottomButtons = tk.Frame(self)
            self.btn_quit = ttk.Button(
                    self.f_bottomButtons, text='返回',
                    style="register.TButton", command=self.quitMe)
            self.btn_quit.pack(side="left")
            self.btn_next = ttk.Button(
                    self.f_bottomButtons, text='確定',
                    style="register.TButton", command=self.submit)
            self.btn_next.pack(side="left")
            self.f_bottomButtons.grid(row=7, column=3, padx=5, pady=5)
            self.initLookupForm()
            # liaten to enter key
            self.bind("<Return>", self.catchReturn)
            # get focus
            self.attributes("-topmost", "true")
            self.attributes("-topmost", "false")
            self.grab_set()

        def catchReturn(self, event):
            self.submit()

        def initLookupForm(self):
            connect,cursor = _getConnection(_default_database)
            # 物品大項
            sqlstr = "select description from hvhnonc_category;"
            cursor.execute(sqlstr)
            catagories = cursor.fetchall()
            self.cb_category.config(values=catagories)
            self.cb_category.bind(
                    "<<ComboboxSelected>>", self.onCategorySelected)
            # 物品細目 # 物品名稱 # 品牌 # 規格
            # initialized with onCategorySelected()
            # 購置日期(低)yyymmdd # 購置日期(高)yyymmdd
            # 建帳日期(低)yyymmdd # 建帳日期(高)yyymmdd
            self.initDateComboboxes(self.cb_date_yy_min,
                                    self.cb_date_mm_min,
                                    self.cb_date_dd_min)
            self.initDateComboboxes(self.cb_date_yy_max,
                                    self.cb_date_mm_max,
                                    self.cb_date_dd_max)
            self.initDateComboboxes(self.cb_key_date_yy_min,
                                    self.cb_key_date_mm_min,
                                    self.cb_key_date_dd_min)
            self.initDateComboboxes(self.cb_key_date_yy_max,
                                    self.cb_key_date_mm_max,
                                    self.cb_key_date_dd_max)
            # template
            sqlstr = ("select change_value from hvhnonc_in_cache "
                      "where this_ID = 0 and change_ID = ("
                      "select ID from hvhnonc_fields "
                      "where description=?)"
                      "order by rowid desc limit 30;")
            # 保管單位
            cursor.execute(sqlstr, ("保管單位", ))
            keep_dept = cursor.fetchall()
            self.cb_keep_dept['values'] = keep_dept
            # 存置地點
            cursor.execute(sqlstr, ("存置地點", ))
            places = cursor.fetchall()
            self.cb_place['values'] = places
            # 使用單位
            cursor.execute(sqlstr, ("使用單位", ))
            use_dept = cursor.fetchall()
            self.cb_use_dept['values'] = use_dept
            # 保管人
            cursor.execute(sqlstr, ("保管人", ))
            keepers = cursor.fetchall()
            self.cb_keeper['values'] = keepers
            connect.close()

        def initDateComboboxes(self, yearbox, monthbox, daybox):
            thisYear = dt.datetime.now().year - 1911
            years = list(reversed(range(1,thisYear+1)))
            yearbox.config(values=years)
            months = list(range(1,12+1))
            monthbox.config(values=months)
            days = list(range(1,31+1))
            daybox.config(values=days)

        def onCategorySelected(self, event):
            # update subcategory
            connect,cursor = _getConnection(_default_database)
            sqlstr = ("select description "
                      "from hvhnonc_subcategory "
                      "where parent_ID=("
                          "select ID "
                          "from hvhnonc_category "
                          "where description=?);")
            params = (self.cb_category.get(), )
            cursor.execute(sqlstr, params)
            subcatagories = cursor.fetchall()
            self.cb_subcategory.config(values=subcatagories)
            self.cb_subcategory.bind(
                    "<<ComboboxSelected>>", self.onSubcategorySelected)
            if (len(self.cb_subcategory['values']) > 0 and
                    self.cb_subcategory.get() !=
                    self.cb_subcategory['values'][0]):
                self.cb_subcategory.set(
                        self.cb_subcategory['values'][0])
            self.onSubcategorySelected(None)
            connect.close()

        def onSubcategorySelected(self, event):
            # update product name
            connect,cursor = _getConnection(_default_database)
            # get all item name in the same subcategory from cache
            sqlstr = ("select change_value "
                      "from hvhnonc_in_cache "
                      "where(this_ID=? "
                      "and this_value=? "
                      "and change_ID=?) "
                      "order by rowid desc limit 30;")
            params = (str(self.getFieldIDByName('物品細目')),
                      self.subcategory.get(),
                      str(self.getFieldIDByName('物品名稱')),)
            cursor.execute(sqlstr, params)
            cachehits = cursor.fetchall()
            connect.close()
            #print(cachehits)
            self.cb_name.config(values=cachehits)
            if (len(self.cb_name['values']) > 0 and
                    self.cb_name.get() != self.cb_name['values'][0]):
                self.cb_name.set(self.cb_name['values'][0])
            self.onNameSelected(None)

        def onNameSelected(self, event):
            # update spec and unit
            connect,cursor = _getConnection(_default_database)
            # get all item name in the same subcategory from cache
            sqlstr = ("select change_value "
                      "from hvhnonc_in_cache "
                      "where("
                          "this_ID=? "
                          "and this_value=? "
                          "and change_ID=?) "
                      "order by rowid desc limit 30;")
            # 品牌
            params = (str(self.getFieldIDByName('物品名稱')),
                      self.name.get(),
                      str(self.getFieldIDByName('品牌')), )
            cursor.execute(sqlstr, params)
            brands = cursor.fetchall()
            self.cb_brand.config(values=brands)
            if (len(self.cb_brand['values']) > 0 and
                    self.cb_brand.get() != self.cb_brand['values'][0]):
                    self.cb_brand.set(self.cb_brand['values'][0])
            # 規格
            params = (str(self.getFieldIDByName('物品名稱')),
                      self.name.get(),
                      str(self.getFieldIDByName('規格')), )
            cursor.execute(sqlstr, params)
            specs = cursor.fetchall()
            self.cb_spec.config(values=specs)
            if (len(self.cb_spec['values']) > 0 and
                    self.cb_spec.get() != self.cb_spec['values'][0]):
                    self.cb_spec.set(self.cb_spec['values'][0])
            connect.close()

        def getFieldIDByName(self, name):
            connect,cursor = _getConnection(_default_database)
            #connect.row_factory = lambda cursor, row: row[0]
            sqlstr = ("select ID "
                      "from hvhnonc_fields "
                      "where description=?;")
            cursor.execute(sqlstr, (name, ))
            hit = cursor.fetchone()
            if hit is not None:
                return hit[0]
            else:
                return None

        def quitMe(self):
            self.destroy()

        def submit(self):
            # open a result toplevel
            #print("lookupForm:submit")
            self.LookupResult(self)

        class LookupResult(tk.Toplevel):
            # basically it's a search result toplevel
            def __init__(self, parent, *args, **kwargs):
                # treeview styles
                style = ttk.Style()
                style.configure("Treeview", font=_default_font)
                style.configure("Treeview.Heading", font=_default_font)
                #init
                tk.Toplevel.__init__(self, parent, *args, **kwargs)
                self.parent = parent
                self.attributes("-topmost", "true")
                self.attributes("-topmost", "false")
                self.title("篩選結果")
                self.geometry("1200x600")
                self.resizable(False, False)
                # make a tree view
                sb = tk.Scrollbar(self)
                self.tv = ttk.Treeview(
                        self, yscrollcommand=sb.set,
                        columns=('1', '2', '3', '4', '5', '6'),
                        show="headings")
                self.tv['displaycolumns'] = ('2','3','4','5','6')
                self.tv.heading('1',text='ID')
                self.tv.heading('2',text='購置日期')
                self.tv.heading('3',text='品名')
                self.tv.heading('4',text='存置位置')
                self.tv.heading('5',text='保管人')
                self.tv.heading('6',text='備註')
                sb.config(command=self.tv.yview)
                # fetch the data
                connect,cursor = _getConnection(_default_database)
                #connect.set_trace_callback(print)
                params = []
                sqlstr = ("select ID, in_date, name, "
                          "place, keeper, remark "
                          "from hvhnonc_in "
                          "where (")
                if parent.category.get():
                    sqlstr += ("category like ? and ")
                    params.append("%{}%".format(parent.category.get()))
                if parent.subcategory.get():
                    sqlstr += ("subcategory like ? and ")
                    params.append("%{}%".format(
                            parent.subcategory.get()))
                if parent.name.get():
                    sqlstr += ("name like ? and ")
                    params.append("%{}%".format(parent.name.get()))
                if parent.brand.get():
                    sqlstr += ("brand like ? and ")
                    params.append("%{}%".format(parent.brand.get()))
                if parent.spec.get():
                    sqlstr += ("spec like ? and ")
                    params.append("%{}%".format(parent.spec.get()))
                if parent.place.get():
                    sqlstr += ("place like ? and ")
                    params.append("%{}%".format(parent.place.get()))
                if parent.keep_dept.get():
                    sqlstr += ("keep_department like ? and ")
                    params.append("%{}%".format(parent.keep_dept.get()))
                if parent.use_dept.get():
                    sqlstr += ("use_department like ? and ")
                    params.append("%{}%".format(parent.use_dept.get()))
                if parent.keeper.get():
                    sqlstr += ("keeper like ? and ")
                    params.append("%{}%".format(parent.keeper.get()))
                if (parent.price_min.get() or parent.price_max.get()):
                    if parent.price_min.get():
                        sqlstr += "(price >= ? and "
                        params.append(parent.price_min.get())
                    else:
                        sqlstr += "("
                    if parent.price_max.get():
                        sqlstr += "price <= ?) and "
                        params.append(parent.price_max.get())
                    else:
                        sqlstr += "1) and "
                # statement forging for between dates
                if (parent.date_yy_min.get() or
                    parent.date_yy_max.get()):
                    if parent.date_yy_min.get():
                        str_date_min = (
                                ""
                                + str(int(parent.date_yy_min.get())
                                +1911)
                                + "-"
                                + (parent.date_mm_min.get() \
                                if parent.date_mm_min.get() else "01")
                                + "-"
                                + (parent.date_dd_min.get() \
                                if parent.date_dd_min.get() else "01")
                                )
                    else:
                        str_date_min = "'1911-01-01'"
                    if parent.date_yy_max.get():
                        str_date_max = (
                                ""
                                + str(int(parent.date_yy_max.get())
                                +1911)
                                + "-"
                                + (parent.date_mm_max.get() \
                                if parent.date_mm_max.get() else "12")
                                + "-"
                                + (parent.date_dd_max.get() \
                                if parent.date_dd_max.get() else "31")
                                )
                    else:
                        str_date_max = "date('now')"
                    sqlstr += ("(strftime('%Y-%m-%d', in_date) "
                               "between ? and ?) and ")
                    params.append(str_date_min)
                    params.append(str_date_max)
                # do the same for key_date
                if (parent.key_date_yy_min.get() or
                    parent.key_date_yy_max.get()):
                    if parent.key_date_yy_min.get():
                        str_key_date_min = (
                                ""
                                + str(int(parent.key_date_yy_min.get())
                                + 1911)
                                + "-"
                                + (parent.key_date_mm_min.get() \
                                if parent.key_date_mm_min.get() \
                                else "01")
                                + "-"
                                + (parent.key_date_dd_min.get() \
                                if parent.key_date_dd_min.get() \
                                else "01")
                                )
                    else:
                        str_key_date_min = "'1911-01-01'"
                    if parent.key_date_yy_max.get():
                        str_key_date_max = (
                                ""
                                + str(int(parent.key_date_yy_max.get())
                                + 1911)
                                + "-"
                                + (parent.key_date_mm_max.get() \
                                if parent.key_date_mm_max.get() \
                                else "12")
                                + "-"
                                + (parent.key_date_dd_max.get() \
                                if parent.key_date_dd_max.get() \
                                else "31")
                                )
                    else:
                        str_key_date_max = "date('now')"
                    sqlstr += (
                            "(strftime('%Y-%m-%d', key_date) "
                            "between ? and ?) and ")
                    params.append(str_key_date_min)
                    params.append(str_key_date_max)
                # where(1) if no input
                sqlstr += "1) order by in_date desc;"
                cursor.execute(sqlstr, params)
                data = cursor.fetchall()
                self.title("篩選結果: 共{}筆".format(len(data)))
                for d in data:
                    self.tv.insert("", "end", values=d)
                sb.pack(side="right", fill="y")
                self.tv.pack(fill="both", expand=1)
                # listen to double click
                self.tv.bind("<Double-1>", self.onDoubleClick)
                # grab focus
                self.grab_set()
                # listen to self close event. if so, close parent
                self.protocol("WM_DELETE_WINDOW", self.abortLookup)

            def onDoubleClick(self, event):
                item = self.tv.identify('item',event.x,event.y)
                #print("you clicked on", self.tv.item(item, "values")[0])
                self.parent.parent.state = str(
                        self.tv.item(item, "values")[0])
                self.parent.parent.updateByState(
                        self.parent.parent.state)
                self.parent.destroy()

            def abortLookup(self):
                self.parent.destroy()

    def newForm(self):
        self.state = 'new'
        self.updateByState(self.state)

    def quitMe(self):
        self.destroy()


class unregister(tk.Toplevel):
    def __init__(self, parent, *args, **kwargs):
        # for update purposes
        self.state = "none"
        self.inBook = self.getAllRecords("hvhnonc_in")
        self.outBook = self.getAllRecords("hvhnonc_out")
        self.inIndex = 0
        self.outIndex = 0
        # styles
        s = ttk.Style()
        s.configure('unregister.TButton', font=_default_button_font)
        tk.Toplevel.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.title("除帳")
        self.geometry("665x509")
        self.resizable(False, False)
        # Four main frame in the GUI
        self.f_mainForm = tk.Frame(self)
        self.f_historyForm = tk.Frame(self)
        self.f_unregisterForm = tk.Frame(self)
        self.f_bottomNavigationBar = tk.Frame(self)
        # main form
        # category(combobox), subcategory(combobox)
        self.l_category = tk.Label(self.f_mainForm, text="物品大項：",
                                   font=_default_font)
        self.category = tk.StringVar()
        self.cb_category = ttk.Combobox(self.f_mainForm, width=20,
                                        textvariable=self.category,
                                        font=_default_font)
        self.l_category.grid(row=0, column=0, padx=5, pady=5)
        self.cb_category.grid(row=0, column=1, padx=5, pady=5)
        self.l_subcategory = tk.Label(self.f_mainForm, text="物品細目：",
                                   font=_default_font)
        self.subcategory = tk.StringVar()
        self.cb_subcategory = ttk.Combobox(self.f_mainForm, width=20,
                                           textvariable=self.subcategory,
                                           font=_default_font)
        self.l_subcategory.grid(row=0, column=2, padx=5, pady=5)
        self.cb_subcategory.grid(row=0, column=3, padx=5, pady=5)
        # name(combobox), unit(combobox)
        self.l_name = tk.Label(self.f_mainForm, text="物品名稱：",
                               font=_default_font)
        self.name = tk.StringVar()
        self.cb_name = ttk.Combobox(self.f_mainForm, width=20,
                                    textvariable=self.name,
                                    font=_default_font)
        self.l_name.grid(row=1, column=0, padx=5, pady=5)
        self.cb_name.grid(row=1, column=1, padx=5, pady=5)
        self.l_unit = tk.Label(self.f_mainForm, text="單位：",
                               font=_default_font)
        self.unit = tk.StringVar()
        self.cb_unit = ttk.Combobox(self.f_mainForm, width=20,
                                    textvariable=self.unit,
                                    font=_default_font)
        self.l_unit.grid(row=1, column=2, padx=5, pady=5)
        self.cb_unit.grid(row=1, column=3, padx=5, pady=5)
        # brand(combobox), spec(combobox)
        self.l_brand = tk.Label(self.f_mainForm, text="品牌：",
                                font=_default_font)
        self.brand = tk.StringVar()
        self.cb_brand = ttk.Combobox(self.f_mainForm, width=20,
                                     textvariable=self.brand,
                                     font=_default_font)
        self.l_brand.grid(row=2, column=0, padx=5, pady=5)
        self.cb_brand.grid(row=2, column=1, padx=5, pady=5)
        self.l_spec = tk.Label(self.f_mainForm, text="規格：",
                               font=_default_font)
        self.spec = tk.StringVar()
        self.cb_spec = ttk.Combobox(self.f_mainForm, width=20,
                                    textvariable=self.spec,
                                    font=_default_font)
        self.l_spec.grid(row=2, column=2, padx=5, pady=5)
        self.cb_spec.grid(row=2, column=3, padx=5, pady=5)
        # objID(entry), serial(entry)
        self.l_objID = tk.Label(self.f_mainForm, text="物品編號：",
                              font=_default_font)
        self.objID = tk.StringVar()
        self.ent_objID = tk.Entry(self.f_mainForm, width=20,
                                  textvariable=self.objID,
                                  font=_default_font)
        self.l_objID.grid(row=3, column=0, padx=5, pady=5)
        self.ent_objID.grid(row=3, column=1, padx=5, pady=5)
        self.l_serial = tk.Label(self.f_mainForm, text="流水號：",
                                 font=_default_font)
        self.serial = tk.StringVar()
        self.ent_serial = tk.Entry(self.f_mainForm, width=20,
                                   textvariable=self.serial,
                                   font=_default_font)
        self.l_serial.grid(row=3, column=2, padx=5, pady=5)
        self.ent_serial.grid(row=3, column=3, padx=5, pady=5)
        # inDate(cb*3), keepYear(entry)
        # a dedicated date frame
        self.f_inDate = tk.Frame(self.f_mainForm)
        self.l_inDate = tk.Label(self.f_inDate, text="取得日期：",
                                 font=_default_font)
        self.inDateY = tk.StringVar()
        self.inDateM = tk.StringVar()
        self.inDateD = tk.StringVar()
        self.cb_inDateY = ttk.Combobox(self.f_inDate, width=3,
                                       textvariable=self.inDateY,
                                       font=_default_font)
        self.l_inDateY = tk.Label(self.f_inDate, text="年",
                                  font=_default_font)
        self.cb_inDateM = ttk.Combobox(self.f_inDate, width=2,
                                       textvariable=self.inDateM,
                                       font=_default_font)
        self.l_inDateM = tk.Label(self.f_inDate, text="月",
                                  font=_default_font)
        self.cb_inDateD = ttk.Combobox(self.f_inDate, width=2,
                                       textvariable=self.inDateD,
                                       font=_default_font)
        self.l_inDateD = tk.Label(self.f_inDate, text="日",
                                  font=_default_font)
        # packing the date
        self.l_inDate.pack(side="left")
        self.cb_inDateY.pack(side="left")
        self.l_inDateY.pack(side="left")
        self.cb_inDateM.pack(side="left")
        self.l_inDateM.pack(side="left")
        self.cb_inDateD.pack(side="left")
        self.l_inDateD.pack(side="left")
        # pack date frame into main frame
        self.f_inDate.grid(row=4, column=0, padx=5, pady=5, columnspan=2)
        self.l_keepYear = tk.Label(self.f_mainForm, text="保存年限：",
                                   font=_default_font)
        self.keepYear = tk.StringVar()
        self.ent_keepYear = tk.Entry(self.f_mainForm, width=20,
                                     textvariable=self.keepYear,
                                     font=_default_font)
        self.l_keepYear.grid(row=4, column=2, padx=5, pady=5)
        # entry
        self.ent_keepYear.grid(row=4, column=3, padx=5, pady=5)
        # price(entry), amount(entry)
        self.l_price = tk.Label(self.f_mainForm, text="單價：",
                              font=_default_font)
        self.price = tk.StringVar()
        self.ent_price = tk.Entry(self.f_mainForm, width=20,
                                  textvariable=self.price,
                                  font=_default_font)
        self.l_price.grid(row=5, column=0, padx=5, pady=5)
        self.ent_price.grid(row=5, column=1, padx=5, pady=5)
        self.l_amount = tk.Label(self.f_mainForm, text="數量：",
                                 font=_default_font)
        self.amount = tk.StringVar()
        self.ent_amount = tk.Entry(self.f_mainForm, width=20,
                                   textvariable=self.amount,
                                   font=_default_font)
        self.l_amount.grid(row=5, column=2, padx=5, pady=5)
        self.ent_amount.grid(row=5, column=3, padx=5, pady=5)
        # keepDept(combobox), place(combobox)
        self.l_keepDept = tk.Label(self.f_mainForm, text="保管單位：",
                                   font=_default_font)
        self.keepDept = tk.StringVar()
        self.cb_keepDept = ttk.Combobox(self.f_mainForm, width=20,
                                        textvariable=self.keepDept,
                                        font=_default_font)
        self.l_keepDept.grid(row=6, column=0, padx=5, pady=5)
        self.cb_keepDept.grid(row=6, column=1, padx=5, pady=5)
        self.l_place = tk.Label(self.f_mainForm, text="存置地點：",
                                font=_default_font)
        self.place = tk.StringVar()
        self.cb_place = ttk.Combobox(self.f_mainForm, width=20,
                                     textvariable=self.place,
                                     font=_default_font)
        self.l_place.grid(row=6, column=2, padx=5, pady=5)
        self.cb_place.grid(row=6, column=3, padx=5, pady=5)
        # keeper(combobox), useDept(combobox)
        self.l_keeper = tk.Label(self.f_mainForm, text="保管人：",
                                 font=_default_font)
        self.keeper = tk.StringVar()
        self.cb_keeper = ttk.Combobox(self.f_mainForm, width=20,
                                      textvariable=self.keeper,
                                      font=_default_font)
        self.l_keeper.grid(row=7, column=0, padx=5, pady=5)
        self.cb_keeper.grid(row=7, column=1, padx=5, pady=5)
        self.l_useDept = tk.Label(self.f_mainForm, text="使用單位：",
                                  font=_default_font)
        self.useDept = tk.StringVar()
        self.cb_useDept = ttk.Combobox(self.f_mainForm, width=20,
                                       textvariable=self.useDept,
                                       font=_default_font)
        self.l_useDept.grid(row=7, column=2, padx=5, pady=5)
        self.cb_useDept.grid(row=7, column=3, padx=5, pady=5)
        # remark(entry)
        self.l_remark = tk.Label(self.f_mainForm, text="備註：",
                                 font=_default_font)
        self.remark = tk.StringVar()
        self.ent_remark = tk.Entry(self.f_mainForm, width=50,
                                  textvariable=self.remark,
                                  font=_default_font)
        self.l_remark.grid(row=8, column=0, padx=5, pady=5)
        self.ent_remark.grid(row=8, column=1, padx=5, pady=5,
                             columnspan=3, sticky="w")
        # history form
        # a frame for the date
        self.f_lastUnregisterDate = tk.Frame(self.f_historyForm)
        self.l_lastUnregisterDate = tk.Label(self.f_lastUnregisterDate,
                                             text="上次除帳：",
                                             font=_default_font)
        self.lastUnregisterDateY = tk.StringVar()
        self.lastUnregisterDateM = tk.StringVar()
        self.lastUnregisterDateD = tk.StringVar()
        self.cb_lastUnregisterDateY = ttk.Combobox(
                self.f_lastUnregisterDate, width=3,
                textvariable=self.lastUnregisterDateY, font=_default_font)
        self.l_lastUnregisterDateY = tk.Label(self.f_lastUnregisterDate,
                                              text="年", font=_default_font)
        self.cb_lastUnregisterDateM = ttk.Combobox(
                self.f_lastUnregisterDate, width=2,
                textvariable=self.lastUnregisterDateM, font=_default_font)
        self.l_lastUnregisterDateM = tk.Label(self.f_lastUnregisterDate,
                                              text="月", font=_default_font)
        self.cb_lastUnregisterDateD = ttk.Combobox(
                self.f_lastUnregisterDate, width=2,
                textvariable=self.lastUnregisterDateD, font=_default_font)
        self.l_lastUnregisterDateD = tk.Label(self.f_lastUnregisterDate,
                                              text="日", font=_default_font)
        # pack the date
        self.l_lastUnregisterDate.pack(side="left")
        self.cb_lastUnregisterDateY.pack(side="left")
        self.l_lastUnregisterDateY.pack(side="left")
        self.cb_lastUnregisterDateM.pack(side="left")
        self.l_lastUnregisterDateM.pack(side="left")
        self.cb_lastUnregisterDateD.pack(side="left")
        self.l_lastUnregisterDateD.pack(side="left")
        # pack the date frame
        self.f_lastUnregisterDate.pack(side="left", padx=5, pady=5)
        # count of the unregister times
        self.l_unregisterCount = tk.Label(self.f_historyForm, text="除帳次數",
                                          font=_default_font)
        self.unregisterCount = tk.StringVar()
        self.ent_unregisterCount = tk.Entry(self.f_historyForm, width=4,
                                            textvariable=self.unregisterCount,
                                            font=_default_font)
        self.l_unregisterCount.pack(side="left", padx=5, pady=5)
        self.ent_unregisterCount.pack(side="left", padx=5, pady=5)
        # amount of the unregistered
        self.l_amountUnregistered = tk.Label(self.f_historyForm,
                                             text="除帳數量：",
                                             font=_default_font)
        self.amountUnregistered = tk.StringVar()
        self.ent_amountUnregistered = tk.Entry(
                self.f_historyForm, width=4,
                textvariable=self.amountUnregistered, font=_default_font)
        self.l_amountUnregistered.pack(side="left", padx=5, pady=5)
        self.ent_amountUnregistered.pack(side="left", padx=5, pady=5)
        # unregister form self.f_unregisterForm
        # pack the first line into a frame
        self.f_firstLine = tk.Frame(self.f_unregisterForm)
        # a frame for the date
        self.f_unregisterDate = tk.Frame(self.f_firstLine)
        self.l_unregisterDate = tk.Label(self.f_unregisterDate,
                                         text="除帳日期：",
                                         font=_default_font)
        self.unregisterDateY = tk.StringVar()
        self.unregisterDateM = tk.StringVar()
        self.unregisterDateD = tk.StringVar()
        self.cb_unregisterDateY = ttk.Combobox(
                self.f_unregisterDate, width=3,
                textvariable=self.unregisterDateY, font=_default_font)
        self.l_unregisterDateY = tk.Label(self.f_unregisterDate,
                                              text="年", font=_default_font)
        self.cb_unregisterDateM = ttk.Combobox(
                self.f_unregisterDate, width=2,
                textvariable=self.unregisterDateM, font=_default_font)
        self.l_unregisterDateM = tk.Label(self.f_unregisterDate,
                                              text="月", font=_default_font)
        self.cb_unregisterDateD = ttk.Combobox(
                self.f_unregisterDate, width=2,
                textvariable=self.unregisterDateD, font=_default_font)
        self.l_unregisterDateD = tk.Label(self.f_unregisterDate,
                                              text="日", font=_default_font)
        # pack the date
        self.l_unregisterDate.pack(side="left")
        self.cb_unregisterDateY.pack(side="left")
        self.l_unregisterDateY.pack(side="left")
        self.cb_unregisterDateM.pack(side="left")
        self.l_unregisterDateM.pack(side="left")
        self.cb_unregisterDateD.pack(side="left")
        self.l_unregisterDateD.pack(side="left")
        # pack the date frame
        self.f_unregisterDate.pack(side="left", padx=5, pady=5)
        # count of the unregister
        self.l_unregisterAmount = tk.Label(self.f_firstLine,
                                           text="除帳數量", font=_default_font)
        self.unregisterAmount = tk.StringVar()
        self.ent_unregisterAmount = tk.Entry(
                self.f_firstLine, width=4, textvariable=self.unregisterAmount,
                font=_default_font)
        self.l_unregisterAmount.pack(side="left", padx=5, pady=5)
        self.ent_unregisterAmount.pack(side="left", padx=5, pady=5)
        # amount left
        self.l_unregisterRemain = tk.Label(
                self.f_firstLine, text="剩餘數量：", font=_default_font)
        self.unregisterRemain = tk.StringVar()
        self.ent_unregisterRemain = tk.Entry(
                self.f_firstLine, width=4, textvariable=self.unregisterRemain,
                font=_default_font)
        self.l_unregisterRemain.pack(side="left", padx=5, pady=5)
        self.ent_unregisterRemain.pack(side="left", padx=5, pady=5)
        # grid the f_firstLine
        self.f_firstLine.grid(row=0, column=0, columnspan=4)
        # reason(combobox), postTreatment(combobox)
        self.l_reason = tk.Label(self.f_unregisterForm,
                                           text="除帳原因：",
                                           font=_default_font)
        self.reason = tk.StringVar()
        self.cb_reason = ttk.Combobox(
                self.f_unregisterForm, width=20,
                textvariable=self.reason, font=_default_font)
        self.l_reason.grid(row=1, column=0, padx=5, pady=5)
        self.cb_reason.grid(row=1, column=1, padx=5, pady=5)
        self.l_postTreatment = tk.Label(self.f_unregisterForm,
                                          text="繳存地點：",
                                          font=_default_font)
        self.postTreatment = tk.StringVar()
        self.cb_postTreatment = ttk.Combobox(
                self.f_unregisterForm, width=20,
                textvariable=self.postTreatment, font=_default_font)
        self.l_postTreatment.grid(row=1, column=2, padx=5, pady=5)
        self.cb_postTreatment.grid(row=1, column=3, padx=5, pady=5)
        # frame for the last line
        self.f_lastLine = tk.Frame(self.f_unregisterForm)
        # unregisterRemark(combobox)
        self.l_unregisterRemark = tk.Label(self.f_lastLine, text="備註事項：",
                                           font=_default_font)
        self.unregisterRemark = tk.StringVar()
        self.cb_unregisterRemark = ttk.Combobox(
                self.f_lastLine, width=30, textvariable=self.unregisterRemark,
                font=_default_font)
        self.l_unregisterRemark.pack(side="left", padx=5)
        self.cb_unregisterRemark.pack(side="left", padx=5)
        # buttons
        self.btn_search = ttk.Button(
                self.f_lastLine, text='檢索', style="unregister.TButton",
                command=self.onButtonSearchClick)
        self.btn_save = ttk.Button(
                self.f_lastLine, text='本筆存入', style="unregister.TButton",
                command=self.onButtonSaveClick)
        self.btn_search.pack(side="left", padx=5)
        self.btn_save.pack(side="left", padx=5)
        self.f_lastLine.grid(row=2, column=0, padx=5, pady=5, columnspan=4,
                             sticky="w")
        # bottom navigation bar
        self.btn_quit = ttk.Button(
                self.f_bottomNavigationBar, text='返回',
                style="unregister.TButton", command=self.quitMe)
        self.btn_next = ttk.Button(
                self.f_bottomNavigationBar, text='下一筆',
                style="unregister.TButton", command=self.fetchNext)
        self.btn_last = ttk.Button(
                self.f_bottomNavigationBar, text='上一筆',
                style="unregister.TButton", command=self.fetchLast)
        self.btn_delete = ttk.Button(
                self.f_bottomNavigationBar, text='刪除本筆',
                style="unregister.TButton", command=self.onButtonDeleteClick)
        self.btn_form = ttk.Button(
                self.f_bottomNavigationBar, text='除帳表單',
                style="unregister.TButton", command=self.onButtonFormClick)
        self.btn_select = ttk.Button(
                self.f_bottomNavigationBar, text='選取資料',
                style="unregister.TButton", command=self.onButtonSelectClick)
        self.btn_quit.pack(side="left")
        self.btn_next.pack(side="left")
        self.btn_last.pack(side="left")
        self.btn_delete.pack(side="left")
        self.btn_form.pack(side="left")
        self.btn_select.pack(side="left")
        # seperators
        self.seperator1 = ttk.Separator(self, orient="horizontal")
        self.seperator2 = ttk.Separator(self, orient="horizontal")
        self.seperator3 = ttk.Separator(self, orient="horizontal")
        # the packing
        self.f_mainForm.pack()
        self.seperator1.pack(fill=tk.X)
        self.f_historyForm.pack()
        self.seperator2.pack(fill=tk.X)
        self.f_unregisterForm.pack()
        self.seperator3.pack(fill=tk.X)
        self.f_bottomNavigationBar.pack()
        # initialize the form
        self.updateByState("none")
        # focus
        self.grab_set()
        self.attributes("-topmost", "true")
        self.attributes("-topmost", "false")

    def updateByState(self, state):
        self.state = state
        if state == "none":
            # set all widgets as disabled
            widgets = (self.cb_category, self.cb_subcategory, self.cb_name,
                       self.cb_unit, self.cb_brand, self.cb_spec,
                       self.ent_objID, self.ent_serial,
                       self.cb_inDateY,
                       self.cb_inDateM,
                       self.cb_inDateD,
                       self.ent_keepYear, self.ent_price, self.ent_amount,
                       self.cb_keepDept, self.cb_place, self.cb_keeper,
                       self.cb_useDept, self.ent_remark,
                       self.cb_lastUnregisterDateY,
                       self.cb_lastUnregisterDateM,
                       self.cb_lastUnregisterDateD,
                       self.ent_unregisterCount, self.ent_amountUnregistered,
                       self.cb_unregisterDateY,
                       self.cb_unregisterDateM,
                       self.cb_unregisterDateD,
                       self.ent_unregisterAmount, self.ent_unregisterRemain,
                       self.cb_reason, self.cb_postTreatment,
                       self.cb_unregisterRemark, )
            for widget in widgets:
                widget.config(state="disabled")
            #clear them
            textVariables = (self.category, self.subcategory, self.name,
                             self.unit, self.brand, self.spec, self.objID,
                             self.serial,
                             self.inDateY, self.inDateM, self.inDateD,
                             self.keepYear, self.price, self.amount,
                             self.keepDept, self.place, self.keeper,
                             self.useDept, self.remark,
                             self.lastUnregisterDateY,
                             self.lastUnregisterDateM,
                             self.lastUnregisterDateD,
                             self.unregisterCount, self.amountUnregistered,
                             self.unregisterDateY,
                             self.unregisterDateM,
                             self.unregisterDateD,
                             self.unregisterAmount, self.unregisterRemain,
                             self.reason, self.postTreatment,
                             self.unregisterRemark, )
            for var in textVariables:
                var.set("")
        else:
            # expect an int ID
            try:
                int(state)
            except ValueError as ve:
                tk.messagebox.showerror("錯誤", ve, parent=self)
                self.updateByState("none")
                return
            # lookup the state(storing an ID) in the inBook
            inIndex = self.lookupIndexInBook(state, self.inBook)
            if inIndex == None:
                tk.messagebox.showerror("錯誤",
                                        "找不到索引值{}".format(state),
                                        parent=self)
                self.updateByState("none")
                return
            # print inBook values to the widgets
            row = self.inBook[inIndex]
            self.category.set(row[3])
            self.subcategory.set(row[4])
            self.name.set(row[5])
            self.unit.set(row[8])
            self.brand.set(row[6])
            self.spec.set(row[7])
            self.objID.set(row[1])
            self.serial.set(row[2])
            indate = row[9].split("-")
            self.inDateY.set(str(int(indate[0])-1911))
            self.inDateM.set(indate[1])
            self.inDateD.set(indate[2])
            self.keepYear.set(row[14])
            self.price.set(row[11])
            self.amount.set(row[12])
            self.keepDept.set(row[16])
            self.place.set(row[13])
            self.keeper.set(row[18])
            self.useDept.set(row[17])
            self.remark.set(row[19])
            # initialization
            self.initForm()
            outIndex = self.lookupIndexInBook(state, self.outBook)
            # if not in outbook print 0s
            if outIndex == None:
                self.unregisterCount.set("0")
                self.amountUnregistered.set("0")
            # if in outBook, fetch the latest row and count of that ID
            else:
                # upper section
                connect, cursor = _getConnection(_default_database)
                sqlstr = ("select count(*), out_date, sum(amount) "
                          "from hvhnonc_out where in_ID = ?"
                          "order by out_date desc limit 1;")
                cursor.execute(sqlstr, (self.state, ))
                data = cursor.fetchone()
                # get count
                self.unregisterCount.set(str(data[0]))
                # get date
                outDate = data[1].split("-")
                self.lastUnregisterDateY.set(str(int(outDate[0])-1911))
                self.lastUnregisterDateM.set(outDate[1])
                self.lastUnregisterDateD.set(outDate[2])
                # get sum
                self.amountUnregistered.set(str(data[2]))
                # these are the same as the lastest date
                self.unregisterDateY.set(self.lastUnregisterDateY.get())
                self.unregisterDateM.set(self.lastUnregisterDateM.get())
                self.unregisterDateD.set(self.lastUnregisterDateD.get())
                # get unregistered amount and its total
                sqlstr = ("select amount,  sum(amount) "
                          "from  hvhnonc_out "
                          "where in_ID = ?"
                          "order by out_date desc;")
                cursor.execute(sqlstr, (self.state, ))
                (lastAmount, TotalOutAmount) = cursor.fetchone()
                TotalOutAmount = int(TotalOutAmount)
                sqlstr = ("select amount "
                          "from  hvhnonc_in "
                          "where ID = ?;")
                cursor.execute(sqlstr, (self.state, ))
                TotalInAmount = int(cursor.fetchone()[0])
                # unregisterAmount is the last amount
                self.unregisterAmount.set(lastAmount)
                # remain is in.amount-sum(out.amount)
                self.unregisterRemain.set(str(TotalInAmount - TotalOutAmount))
                sqlstr = ("select reason,  post_treatment, remark "
                          "from  hvhnonc_out "
                          "where in_ID = ?"
                          "order by out_date desc limit 1;")
                cursor.execute(sqlstr, (self.state, ))
                data = cursor.fetchone()
                self.reason.set(data[0])
                self.postTreatment.set(data[1])
                self.unregisterRemark.set(data[2])
                connect.close()

    def initForm(self):
        # enable some widgets
        self.cb_unregisterDateY.config(state="normal")
        self.cb_unregisterDateM.config(state="normal")
        self.cb_unregisterDateD.config(state="normal")
        self.ent_unregisterAmount.config(state="normal")
        self.cb_reason.config(state="normal")
        self.cb_postTreatment.config(state="normal")
        self.cb_unregisterRemark.config(state="normal")
        # set lower part to ""
        self.unregisterCount.set("")
        self.amountUnregistered.set("")
        self.lastUnregisterDateY.set("")
        self.lastUnregisterDateM.set("")
        self.lastUnregisterDateD.set("")
        self.unregisterDateY.set("")
        self.unregisterDateM.set("")
        self.unregisterDateD.set("")
        self.unregisterAmount.set("")
        self.unregisterRemain.set("")
        self.reason.set("")
        self.postTreatment.set("")
        self.unregisterRemark.set("")
        # combobox values
        # unregisterDate: fill in the date choices
        thisYear = dt.datetime.now().year - 1911
        years = list(reversed(range(1, thisYear+1)))
        self.cb_unregisterDateY.config(values=years)
        self.cb_unregisterDateM.config(values=list(range(1,13)))
        self.cb_unregisterDateD.config(values=list(range(1,32)))
        # The others: read in cache and update
        connect, cursor = _getConnection(_default_database)
        sqlstr = ("select change_value "
                  "from hvhnonc_out_cache "
                  "where this_ID=("
                          "select ID from "
                          "hvhnonc_fields "
                          "where description=?) "
                  "and change_ID=("
                          "select ID from "
                          "hvhnonc_fields "
                          "where description=?)"
                  "order by rowid desc limit 30;")
        cursor.execute(sqlstr, ("無", "除帳原因"))
        rows = cursor.fetchall()
        self.cb_reason.config(values=rows)
        cursor.execute(sqlstr, ("無", "繳存地點"))
        rows = cursor.fetchall()
        self.cb_postTreatment.config(values=rows)
        cursor.execute(sqlstr, ("無", "除帳備註"))
        rows = cursor.fetchall()
        self.cb_unregisterRemark.config(values=rows)
        connect.close()

    def lookupIndexInBook(self, state, book):
        try:
            int(state)
        except ValueError:
            return None
        if book == self.outBook:
            i = 1
        else:
            i = 0
        for index, sublist in enumerate(book):
            if int(state) in (sublist[i],):
                return index
        return None

    def quitMe(self):
        self.destroy()

    def onButtonSearchClick(self):
        # open a toplevel for searching
        self.SearchWindow(self)

    class SearchWindow(tk.Toplevel):
        def __init__(self, parent, *args, **kwargs):
            s = ttk.Style()
            s.configure('search.TButton', font=_default_button_font)
            tk.Toplevel.__init__(self, parent, *args, **kwargs)
            self.parent = parent
            self.attributes("-topmost", "true")
            self.attributes("-topmost", "false")
            self.title("檢索")
            self.resizable(False, False)
            self.geometry("465x60")
            # searchbar
            self.l_search = tk.Label(self, text="請輸入想要檢索的關鍵字:",
                                     font=_default_font)
            self.l_search.grid(row=0, column=0)
            self.parent.query = tk.StringVar()
            self.cb_searchbar = ttk.Combobox(
                    self, width=20, textvariable=self.parent.query,
                    font=_default_font)
            # get search cache from db
            connect,cursor = _getConnection(_default_database)
            connect.row_factory = lambda cursor, row: row[0]
            sqlstr = ("select change_value "
                      "from hvhnonc_out_cache "
                      "where change_ID = ("
                      "select ID from hvhnonc_fields "
                      "where description = '檢索') "
                      "order by rowid desc limit 30;")
            cursor.execute(sqlstr)
            rows = cursor.fetchall()
            history = []
            for row in rows:
                history.append(row[0])
            self.cb_searchbar.config(values=history)
            self.cb_searchbar.grid(row=0, column=1)
            # buttons
            self.f_buttons = tk.Frame(self)
            self.btn_cancel = ttk.Button(
                    self.f_buttons, text="取消", style='search.TButton',
                    command=self.quitMe)
            self.btn_cancel.pack(side="left")
            self.btn_submit = ttk.Button(
                    self.f_buttons, text="檢索", style='search.TButton',
                    command=self.onSubmitClick)
            self.btn_submit.pack(side="left")
            self.f_buttons.grid(row=1, column=1, sticky="se")
            # listen to return
            self.bind("<Return>", self.catchReturn)
            self.grab_set()

        def catchReturn(self, event):
            self.onSubmitClick()

        def quitMe(self):
            self.destroy()

        def onSubmitClick(self):
            # update search cache
            connect,cursor = _getConnection(_default_database)
            sqlstr = (
                    "replace into hvhnonc_out_cache(this_ID, this_value, "
                    "change_ID, change_value) "
                    "values(0, 'none', ("
                        "select ID "
                        "from hvhnonc_fields "
                        "where description = '檢索'), "
                    "?);")
            cursor.execute(sqlstr, (self.parent.query.get(), ))
            connect.commit()
            # open a result toplevel
            self.SearchResultWindow(self.parent)
            self.destroy()

        class SearchResultWindow(tk.Toplevel):
            def __init__(self, parent, *args, **kwargs):
                # treeview styles
                style = ttk.Style()
                style.configure("Treeview", font=_default_font)
                style.configure("Treeview.Heading", font=_default_font)
                # init
                tk.Toplevel.__init__(self, parent, *args, **kwargs)
                self.parent = parent
                self.attributes("-topmost", "true")
                self.attributes("-topmost", "false")
                self.title("檢索結果")
                self.geometry("1200x600")
                # make a tree view
                sb = tk.Scrollbar(self)
                self.tv = ttk.Treeview(
                        self, yscrollcommand=sb.set,
                        columns=('1', '2', '3', '4', '5', '6'),
                        show="headings")
                self.tv['displaycolumns'] = ('2','3','4','5','6')
                self.tv.heading('1',text='ID')
                self.tv.heading('2',text='購置日期')
                self.tv.heading('3',text='品名')
                self.tv.heading('4',text='存置位置')
                self.tv.heading('5',text='保管人')
                self.tv.heading('6',text='備註')
                sb.config(command=self.tv.yview)
                # fetch the data
                # connect to db
                # still searching in hvhnonc_in
                connect,cursor = _getConnection(_default_database)
                phrase = str(parent.query.get())
                sqlstr = (
                        "select ID, in_date, name, place, keeper, remark "
                        "from hvhnonc_in "
                        "where("
                            "category like :q or "
                            "subcategory like :q or "
                            "name like :q or "
                            "brand like :q or "
                            "spec like :q or "
                            "place like :q or "
                            "keep_department like :q or "
                            "use_department like :q or "
                            "keeper like :q or "
                            "remark like :q) "
                            "order by in_date desc;")
                cursor.execute(sqlstr, {'q': "%{}%".format(phrase)})
                data = cursor.fetchall()
                for d in data:
                    self.tv.insert("", "end", values=d)
                sb.pack(side="right", fill="y")
                self.tv.pack(fill="both", expand=1)
                # listen to double click
                self.tv.bind("<Double-1>", self.onDoubleClick)
                self.grab_set()

            def onDoubleClick(self, event):
                item = self.tv.identify('item',event.x,event.y)
                #print("you clicked on", self.tv.item(item,"values")[0])
                self.parent.state = str(self.tv.item(item,"values")[0])
                self.parent.updateByState(self.parent.state)
                self.destroy()

    def onButtonSaveClick(self):
        tk.messagebox.showinfo("測試", "onButtonSaveClick", parent=self)

    def fetchNext(self):
        if self.state in ("none", ):
            self.outIndex = 0
            self.state = str(self.outBook[self.outIndex][1])
            self.updateByState(self.state)
        else:
            if self.outIndex == len(self.outBook) - 1:
                tk.messagebox.showinfo("到底了", "已到達最後一筆",
                                       parent=self)
            else:
                self.outIndex = self.outIndex + 1
                self.state = str(self.outBook[self.outIndex][1])
                self.updateByState(self.state)

    def fetchLast(self):
        if self.state in ("none", ):
            self.outIndex = len(self.outBook)-1
            self.state = str(self.outBook[self.outIndex][1])
            self.updateByState(self.state)
        else:
            if self.outIndex == 0:
                tk.messagebox.showinfo("到頂了", "已到達第一筆",
                                       parent=self)
            else:
                self.outIndex = self.outIndex - 1
                self.state = str(self.outBook[self.outIndex][1])
                self.updateByState(self.state)

    def onButtonDeleteClick(self):
        tk.messagebox.showinfo("測試", "onButtonDeleteClick", parent=self)

    def onButtonFormClick(self):
        # basically the onButtonSelectClick but only look for hchnonc_out
        self.selectFilter(self, source="out")

    def onButtonSelectClick(self):
        # open a select filter toplevel
        self.selectFilter(self, source="both")

    class selectFilter(tk.Toplevel):
        def __init__(self, parent, source: str = "both", *args, **kwargs):
            self.whereToLook = source
            s = ttk.Style()
            s.configure('selectFilter.TButton', font=_default_button_font)
            # init
            tk.Toplevel.__init__(self, parent, *args, **kwargs)
            self.parent = parent
            self.attributes("-topmost", "true")
            self.attributes("-topmost", "false")
            self.title("請選擇資料過濾條件")
            self.geometry("665x293")
            # GUI
            self.wdict = {}
            # category
            self.wdict["category"] = CompoundField(
                    self, "Combobox", "物品大類", "category", "readonly")
            self.wdict["category"].label.grid(row=0, column=0,
                                              padx=5, pady=5)
            self.wdict["category"].widget.grid(row=0, column=1,
                                               padx=5, pady=5)
            # subcategory
            self.wdict["subcategory"] = CompoundField(
                    self, "Combobox", "物品分類", "subcategory", "readonly")
            self.wdict["subcategory"].label.grid(row=0, column=2,
                                                 padx=5, pady=5)
            self.wdict["subcategory"].widget.grid(row=0, column=3,
                                                  padx=5, pady=5)
            # name
            self.wdict["name"] = CompoundField(
                    self, "Combobox", "物品名稱", "name", "normal")
            self.wdict["name"].label.grid(row=1, column=0, padx=5, pady=5)
            self.wdict["name"].widget.grid(row=1, column=1, padx=5, pady=5)
            # brand
            self.wdict["brand"] = CompoundField(
                    self, "Combobox", "品牌", "brand", "normal")
            self.wdict["brand"].label.grid(row=1, column=2, padx=5, pady=5)
            self.wdict["brand"].widget.grid(row=1, column=3, padx=5, pady=5)
            # spec
            self.wdict["spec"] = CompoundField(
                    self, "Combobox", "規格", "spec", "normal")
            self.wdict["spec"].label.grid(row=2, column=0, padx=5, pady=5)
            self.wdict["spec"].widget.grid(row=2, column=1, padx=5, pady=5)
            # price
            self.wdict["price"] = CompoundField(
                    self, "Entry", "單價", "price", "normal", opt="minmax")
            self.wdict["price"].widgetMin.config(width=10)
            self.wdict["price"].widgetMax.config(width=10)
            self.wdict["price"].label.grid(row=2, column=2, padx=5, pady=5)
            self.wdict["price"].widget.grid(row=2, column=3, padx=5, pady=5)
            # in_date
            self.wdict["in_date"] = CompoundField(
                    self, "DateFrame", "日期範圍", "in_date", "normal",
                    opt="minmax")
            self.wdict["in_date"].widgetMin.clear()
            self.wdict["in_date"].widgetMax.clear()
            self.wdict["in_date"].label.grid(row=3, column=0, padx=5, pady=5)
            self.wdict["in_date"].widget.grid(row=3, column=1, padx=5, pady=5,
                                              columnspan=3, sticky="w")
            # key_date
            self.wdict["key_date"] = CompoundField(
                    self, "DateFrame", "建帳日期", "key_date", "normal",
                    opt="minmax")
            self.wdict["key_date"].widgetMin.clear()
            self.wdict["key_date"].widgetMax.clear()
            self.wdict["key_date"].label.grid(row=4, column=0, padx=5, pady=5)
            self.wdict["key_date"].widget.grid(
                    row=4, column=1, padx=5, pady=5, columnspan=3, sticky="w")
            # keep_department
            self.wdict["keep_department"] = CompoundField(
                    self, "Combobox", "保管單位", "keep_department", "normal")
            self.wdict["keep_department"].label.grid(
                    row=5, column=0, padx=5, pady=5)
            self.wdict["keep_department"].widget.grid(
                    row=5, column=1, padx=5, pady=5)
            # place
            self.wdict["place"] = CompoundField(
                    self, "Combobox", "存置地點", "place", "normal")
            self.wdict["place"].label.grid(row=5, column=2, padx=5, pady=5)
            self.wdict["place"].widget.grid(row=5, column=3, padx=5, pady=5)
            # use_department
            self.wdict["use_department"] = CompoundField(
                    self, "Combobox", "使用單位", "use_department", "normal")
            self.wdict["use_department"].label.grid(
                    row=6, column=0, padx=5, pady=5)
            self.wdict["use_department"].widget.grid(
                    row=6, column=1, padx=5, pady=5)
            # keeper
            self.wdict["keeper"] = CompoundField(
                    self, "Combobox", "保管人", "keeper", "normal")
            self.wdict["keeper"].label.grid(row=6, column=2, padx=5, pady=5)
            self.wdict["keeper"].widget.grid(row=6, column=3, padx=5, pady=5)
            # cancel and submit buttons
            self.btn_cancel = ttk.Button(
                    self, text="取消", style="selectFilter.TButton",
                    command=self.quitMe)
            self.btn_cancel.grid(row=7, column=2, padx=5, pady=5)
            self.btn_submit = ttk.Button(
                    self, text="確定", style="selectFilter.TButton",
                    command=self.onSubmitClick)
            self.btn_submit.grid(row=7, column=3, padx=5, pady=5)
            # init form
            self.initForm()
            # focus
            self.grab_set()

        def initForm(self):
            # set all textVariables to ""
            for k, v in self.wdict.items():
                if v.widgetType == "Dateframe":
                    try:
                        if v.opt == "minmax":
                            v.widgetMin.clear()
                            v.widgetMax.clear()
                    except NameError:
                        v.widget.clear()
                else:
                    v.variable.set("")
            # fetch cache for view
            for k, v in self.wdict.items():
                self.fetchCache(v)
            # bind combobox select to update cache
            self.wdict["category"].widget.bind(
                    "<<ComboboxSelected>>", self.onCategorySelected)

        def onCategorySelected(self, state):
            self.fetchCache(self.wdict["subcategory"])

        def fetchCache(self, cf):
            # input: compoundfield
            connect,cursor = _getConnection(_default_database)
            sqlstr = ("")
            if cf.fieldName == "category":
                # update from hvhnonc_subcategory
                sqlstr = ("select description "
                          "from hvhnonc_category;")
                cursor.execute(sqlstr)
                rows = cursor.fetchall()
                catagories = []
                for row in rows:
                    catagories.append(row[0])
                cf.widget.config(values=catagories)
            elif cf.fieldName == "subcategory":
                # update from hvhnonc_subcategory
                sqlstr = ("select description "
                          "from hvhnonc_subcategory "
                          "where parent_ID=("
                          "select ID "
                          "from hvhnonc_category "
                          "where description=?);")
                param = (self.wdict["category"].variable.get(), )
                cursor.execute(sqlstr, param)
                rows = cursor.fetchall()
                subcatagories = []
                for row in rows:
                    subcatagories.append(row[0])
                cf.widget.config(values=subcatagories)
            elif cf.widgetType == "Combobox":
                # update from hvhnonc_out_cache
                sqlstr = ("select change_value "
                          "from hvhnonc_out_cache "
                          "where this_ID='0' and "
                          "this_value='none' and "
                          "change_ID=("
                              "select ID "
                              "from hvhnonc_fields "
                              "where description=?)")
                param = (cf.description, )
                cursor.execute(sqlstr, param)
                rows = cursor.fetchall()
                cf.widget.config(values=rows)
                pass

        def quitMe(self):
            self.destroy()

        def onSubmitClick(self):
            # select from hvhnonc_in and hvhnonc_out
            # open a tree toplevel showing the filtered results
            # copy paste from LookupResult
            self.LookupResult(self)

        class LookupResult(tk.Toplevel):
            # basically it's a search result toplevel
            def __init__(self, parent, *args, **kwargs):
                # treeview styles
                style = ttk.Style()
                style.configure("Treeview", font=_default_font)
                style.configure("Treeview.Heading", font=_default_font)
                #init
                tk.Toplevel.__init__(self, parent, *args, **kwargs)
                self.parent = parent
                self.attributes("-topmost", "true")
                self.attributes("-topmost", "false")
                self.title("篩選結果")
                self.geometry("1200x600")
                self.resizable(False, False)
                # make a tree view
                sb = tk.Scrollbar(self)
                self.tv = ttk.Treeview(
                        self, yscrollcommand=sb.set,
                        columns=('1', '2', '3', '4', '5', '6'),
                        show="headings")
                self.tv['displaycolumns'] = ('2','3','4','5','6')
                self.tv.heading('1',text='ID')
                self.tv.heading('2',text='日期')
                self.tv.heading('3',text='品名')
                self.tv.heading('4',text='存置位置')
                self.tv.heading('5',text='保管人')
                self.tv.heading('6',text='備註')
                sb.config(command=self.tv.yview)
                # fetch the data
                connect,cursor = _getConnection(_default_database)
                #connect.set_trace_callback(print)
                params = []
                q_in = ("select ID, in_date as date, name, "
                              "place as place, keeper, remark "
                              "from hvhnonc_in ")
                q_out = ("select in_ID as ID, out_date as date, name, "
                              "storage as place, '' as keeper, remark "
                              "from hvhnonc_out ")
                q_union = "union all "
                q_footer = "order by in_date desc;"
                q_where = "where ("
                for key, cf in parent.wdict.items():
                    # minmax
                    if hasattr(cf, "opt") and cf.opt == "minmax":
                        # in date range
                        if cf.widgetType == "Dateframe":
                            if (cf.widgetMin.variable.get() == "" and
                                cf.widgetMax.variable.get() == ""):
                                continue
                            tempMin = "1911-01-01"
                            tempMax = "date('now')"
                            if cf.widgetMin.variable.get() != "":
                                tempMin = cf.widgetMin.variable.get()
                            if cf.widgetMax.variable.get() != "":
                                tempMax = cf.widgetMax.variable.get()
                            q_where += ("(strftime('%Y-%m-%d', {}) "
                                       "between ? and ?) and ".format(key))
                            params.append(tempMin)
                            params.append(tempMax)
                        # in price range
                        elif cf.widgetType == "Entry":
                            tMin = cf.variableMin.get()
                            tMax = cf.variableMax.get()
                            if (tMin != "" and tMax != ""):
                                q_where += ("({0} >= ? and "
                                           "{0} <= ?) and ").format(key)
                                params.append(tMin)
                                params.append(tMax)
                            elif (tMin != "" and tMax == ""):
                                q_where += ("{0} >= ? and ".format(key))
                                params.append(tMin)
                            elif (tMin == "" and tMax != ""):
                                q_where += ("{0} <= ? and ".format(key))
                                params.append(tMax)
                            else:
                                pass
                    elif (cf.variable.get() != ""):
                        q_where += ("{} like ? and ".format(key))
                        params.append("%{}%".format(cf.variable.get()))
                    elif cf.widgetType in ("Combobox", "Entry"):
                        pass
                    else:
                        messagebox.showerror(
                                "err",
                                "unknown widget {0}:{1} in wdict".format(
                                        key, cf.widgetType),
                                parent=self)
                # where(1) if no input
                q_where += "1) "
                q_in_full = q_in + q_where
                q_where = q_where.replace("in_date", "out_date")
                q_where = q_where.replace("place", "storage")
                q_out_full = q_out + q_where
<<<<<<< HEAD
                if parent.whereToLook == "both":
                    params = params + params
                    cursor.execute(
                            q_in_full + q_union + q_out_full + q_footer,
                            params)
                elif parent.whereToLook == "in":
                    cursor.execute(
                            q_in_full + q_footer,
                            params)
                elif parent.whereToLook == "out":
                    cursor.execute(
                            q_out_full +
                            q_footer.replace("in_date", "out_date"),
                            params)
=======
                params = params + params
                cursor.execute(
                        q_in_full + q_union + q_out_full + q_footer,
                        params)
>>>>>>> 3cf0592fb508870a1777d60afd752a7497789bb3
                data = cursor.fetchall()
                self.title("篩選結果: 共{}筆".format(len(data)))
                for d in data:
                    self.tv.insert("", "end", values=d)
                sb.pack(side="right", fill="y")
                self.tv.pack(fill="both", expand=1)
                # listen to double click
                self.tv.bind("<Double-1>", self.onDoubleClick)
                # grab focus
                self.grab_set()
                # listen to self close event. if so, close parent
                self.protocol("WM_DELETE_WINDOW", self.abortLookup)

            def onDoubleClick(self, event):
                item = self.tv.identify('item',event.x,event.y)
                #print("you clicked on", self.tv.item(item, "values")[0])
                self.parent.parent.updateByState(
                        self.tv.item(item, "values")[0])
                self.parent.destroy()

            def abortLookup(self):
                self.parent.destroy()

    def getAllRecords(self, tablename):
        connect, cursor = _getConnection(_default_database)
        #connect.set_trace_callback(print)
        sqlstr = "select * from {};".format(tablename)
        cursor.execute(sqlstr)
        return cursor.fetchall()


class printNonc(tk.Toplevel):
    def __init__(self, parent, *args, **kwargs):
        s = ttk.Style()
        s.configure('printNonc.TButton', font=_default_button_font)
        tk.Toplevel.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.attributes("-topmost", "true")
        self.attributes("-topmost", "false")
        self.title("列印")
        self.geometry(_default_toplevel_size)
        self.resizable(False, False)
        #gui
        self.l = tk.Label(self, text="列印畫面", font=_default_font)
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


class maintenance(tk.Toplevel):
    def __init__(self, parent, *args, **kwargs):
        s = ttk.Style()
        s.configure('maintenance.TButton', font=_default_button_font)
        tk.Toplevel.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.attributes("-topmost", "true")
        self.attributes("-topmost", "false")
        self.title("維護")
        self.geometry(_default_toplevel_size)
        self.resizable(False, False)
        #gui
        self.l = tk.Label(self, text="維護畫面", font=_default_font)
        self.l.pack()
        # buttons
        self.btn_quit = ttk.Button(self, text='返回',
                                   style="maintenance.TButton",
                                   command=self.quitMe)
        self.btn_quit.pack()
        # focus
        self.grab_set()

    def quitMe(self):
        self.destroy()


def main():
    root = tk.Tk()
    # The combobox style for root, also seen in Index().__init__()
    root.option_add('*TCombobox*Listbox.font', _default_font)
    test = unregister.selectFilter(root, source="out")
    test.protocol("WM_DELETE_WINDOW", lambda: test.parent.destroy())
    root.mainloop()
    root.quit()


if __name__ == "__main__":
    main()
