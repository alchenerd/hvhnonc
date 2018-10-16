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
import datetime

from __init__ import __version__

WELCOME_IMAGE = "kaiba.gif"
DEFAULT_TOPLEVEL_SIZE = "665x410"
DEFAULT_FONT = (None, 15)
DATABASE_NAME = "HVHNONC.db"

class Index(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        parent.geometry("640x350")
        parent.title("非消耗品管理系統 (v"+__version__+")")
        parent.focus_force()
        parent.resizable(False, False)
        # listbox font style
        parent.option_add('*TCombobox*Listbox.font', DEFAULT_FONT)
        # an image
        photo = tk.PhotoImage(file=WELCOME_IMAGE)
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
        self.title("登入")
        self.geometry("250x115")
        self.resizable(False, False)
        # user info
        self.label_username = tk.Label(self, text="帳號:",
                                       font=DEFAULT_FONT)
        self.label_password = tk.Label(self, text="密碼:",
                                       font=DEFAULT_FONT)
        self.label_username.place(x=4,y=10)
        self.label_password.place(x=4,y=40)
        self.var_username = tk.StringVar()
        self.var_username.set("administrator")
        self.var_password = tk.StringVar()
        self.var_password.set("veteranshome")
        self.entry_username = tk.Entry(
                self, textvariable=self.var_username, font=DEFAULT_FONT)
        self.entry_password = tk.Entry(
                self, textvariable=self.var_password,
                font=DEFAULT_FONT, show="*")
        self.entry_username.place(x=58, y=13)
        self.entry_password.place(x=58, y=43)
        # buttons
        s = ttk.Style()
        s.configure('login.TButton', font=('Helvetica', 13))
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
        self.attributes("-topmost", "false")

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
            connect = sqlite3.connect(DATABASE_NAME)
            cursor = connect.cursor()
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
        # for update purposes
        self.state = "none"
        # for fetch next/fetch last purposes,
        # needs update after every insert
        self.book = self.getAllRecords()
        self.index = 0
        # button style for register form
        s = ttk.Style()
        s.configure('register.TButton', font=('Helvetica', 13))
        # initialization
        tk.Toplevel.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        # pop to topmost but don't get in the way
        self.attributes("-topmost", "true")
        self.attributes("-topmost", "false")
        self.title("輸入")
        self.geometry(DEFAULT_TOPLEVEL_SIZE)
        self.resizable(False, False)
        # register form GUI
        # category
        self.lb_cat = tk.Label(self, text="物品大項: ",
                               font=DEFAULT_FONT)
        self.lb_cat.grid(row=0, column=0, padx=5, pady=5)
        self.category = tk.StringVar()
        self.cb_cat = ttk.Combobox(
                self, width=20, textvariable=self.category,
                font=DEFAULT_FONT, state="readonly")
        self.cb_cat.grid(row=0, column=1, padx=5, pady=5)
        # subcategory
        self.lb_subcat = tk.Label(self, text="物品細目: ",
                                  font=DEFAULT_FONT)
        self.lb_subcat.grid(row=0, column=2, padx=5, pady=5)
        self.subcategory = tk.StringVar()
        self.cb_subcat = ttk.Combobox(
                self, width=20, textvariable=self.subcategory,
                font=DEFAULT_FONT, state="readonly")
        self.cb_subcat.grid(row=0, column=3, padx=5, pady=5)
        # name
        self.lb_name = tk.Label(self, text="物品名稱: ",
                                font=DEFAULT_FONT)
        self.lb_name.grid(row=1, column=0, padx=5, pady=5)
        self.name = tk.StringVar()
        self.cb_name = ttk.Combobox(
                self, width=20, textvariable=self.name,
                font=DEFAULT_FONT)
        self.cb_name.grid(row=1, column=1, padx=5, pady=5)
        # unit
        self.lb_unit = tk.Label(
                self, text="單位: ", font=DEFAULT_FONT)
        self.lb_unit.grid(row=1, column=2, padx=5, pady=5)
        self.unit = tk.StringVar()
        self.cb_unit = ttk.Combobox(
                self, width=20, textvariable=self.unit,
                font=DEFAULT_FONT)
        self.cb_unit.grid(row=1, column=3, padx=5, pady=5)
        # brand
        self.lb_brand = tk.Label(self, text="品牌: ",
                                 font=DEFAULT_FONT)
        self.lb_brand.grid(row=2, column=0, padx=5, pady=5)
        self.brand = tk.StringVar()
        self.cb_brand = ttk.Combobox(self, width=20,
                                     textvariable=self.brand,
                                     font=DEFAULT_FONT)
        self.cb_brand.grid(row=2, column=1, padx=5, pady=5)
        # spec
        self.lb_spec = tk.Label(self, text="規格: ", font=DEFAULT_FONT)
        self.lb_spec.grid(row=2, column=2, padx=5, pady=5)
        self.spec = tk.StringVar()
        self.cb_spec = ttk.Combobox(self, width=20,
                                    textvariable=self.spec,
                                    font=DEFAULT_FONT)
        self.cb_spec.grid(row=2, column=3, padx=5, pady=5)
        # serial
        self.f_serial = tk.Frame(self)
        self.lb_objID = tk.Label(
                self.f_serial, text="物品編號: ", font=DEFAULT_FONT)
        self.lb_objID.pack(side='left', padx=10)
        self.objID = tk.StringVar()
        self.ent_objID = tk.Entry(
                self.f_serial, width=18, textvariable=self.objID,
                font=DEFAULT_FONT)
        self.ent_objID.pack(side='left', padx=10)
        self.lb_serial = tk.Label(
                self.f_serial, text="流水號: ", font=DEFAULT_FONT)
        self.lb_serial.pack(side='left', padx=10)
        self.serial = tk.StringVar()
        self.ent_serial = tk.Entry(
                self.f_serial, width=5, textvariable=self.serial,
                font=DEFAULT_FONT)
        self.ent_serial.pack(side='left', padx=10)
        self.btn_lookupSerial = ttk.Button(
                self.f_serial, text="流水號總覽", style="register.TButton",
                command=self.lookupSerial)
        self.btn_lookupSerial.pack(side='left', padx=10)
        self.f_serial.grid(row=3, column=0, columnspan=4,
                           padx=5, pady=5)
        # in date
        self.lb_in_date = tk.Label(
                self, text="購置日期: ", font=DEFAULT_FONT)
        self.lb_in_date.grid(row=4, column=0, padx=5, pady=5)
        self.f_in_date = tk.Frame(self)
        self.in_date_yy = tk.StringVar()
        self.cb_in_date_yy = ttk.Combobox(
                self.f_in_date, width=3, textvariable=self.in_date_yy,
                font=DEFAULT_FONT)
        self.cb_in_date_yy.pack(side='left')
        self.lb_in_date_yy = tk.Label(self.f_in_date, text="年",
                                      font=DEFAULT_FONT)
        self.lb_in_date_yy.pack(side='left')
        self.in_date_mm = tk.StringVar()
        self.cb_in_date_mm = ttk.Combobox(
                self.f_in_date, width=2, textvariable=self.in_date_mm,
                font=DEFAULT_FONT)
        self.cb_in_date_mm.pack(side='left')
        self.lb_in_date_mm = tk.Label(self.f_in_date, text="月",
                                      font=DEFAULT_FONT)
        self.lb_in_date_mm.pack(side='left')
        self.in_date_dd = tk.StringVar()
        self.cb_in_date_dd = ttk.Combobox(
                self.f_in_date, width=2, textvariable=self.in_date_dd,
                font=DEFAULT_FONT)
        self.cb_in_date_dd.pack(side='left')
        self.lb_in_date_dd = tk.Label(self.f_in_date, text="日",
                                      font=DEFAULT_FONT)
        self.lb_in_date_dd.pack(side='left')
        self.f_in_date.grid(row=4, column=1, padx=5, pady=5)
        # key date
        self.lb_key_date = tk.Label(self, text="建帳日期: ",
                                    font=DEFAULT_FONT)
        self.lb_key_date.grid(row=4, column=2, padx=5, pady=5)
        self.f_key_date = tk.Frame(self)
        self.key_date_yy = tk.StringVar()
        self.cb_key_date_yy = ttk.Combobox(
                self.f_key_date, width=3, textvariable=self.key_date_yy,
                font=DEFAULT_FONT)
        self.cb_key_date_yy.pack(side='left')
        self.lb_key_date_yy = tk.Label(self.f_key_date, text="年",
                                       font=DEFAULT_FONT)
        self.lb_key_date_yy.pack(side='left')
        self.key_date_mm = tk.StringVar()
        self.cb_key_date_mm = ttk.Combobox(
                self.f_key_date, width=2, textvariable=self.key_date_mm,
                font=DEFAULT_FONT)
        self.cb_key_date_mm.pack(side='left')
        self.lb_key_date_mm = tk.Label(self.f_key_date, text="月",
                                       font=DEFAULT_FONT)
        self.lb_key_date_mm.pack(side='left')
        self.key_date_dd = tk.StringVar()
        self.cb_key_date_dd = ttk.Combobox(
                self.f_key_date, width=2, textvariable=self.key_date_dd,
                font=DEFAULT_FONT)
        self.cb_key_date_dd.pack(side='left')
        self.lb_key_date_dd = tk.Label(self.f_key_date, text="日",
                                       font=DEFAULT_FONT)
        self.lb_key_date_dd.pack(side='left')
        self.f_key_date.grid(row=4, column=3, padx=5, pady=5)
        # source, price, amount in the same line(thus in the same frame)
        self.f_sourcePriceAmount = tk.Frame(self)
        self.lb_source = tk.Label(
                self.f_sourcePriceAmount, text="來源: ",
                font=DEFAULT_FONT)
        self.lb_source.pack(side='left', padx=10)
        self.source = tk.StringVar()
        self.cb_source = ttk.Combobox(
                self.f_sourcePriceAmount, width=8,
                textvariable=self.source, font=DEFAULT_FONT,
                state="readonly")
        self.cb_source.pack(side='left', padx=10)
        self.lb_price = tk.Label(self.f_sourcePriceAmount,
                                 text="價格: ", font=DEFAULT_FONT)
        self.lb_price.pack(side='left', padx=10)
        self.price = tk.StringVar()
        self.ent_price = tk.Entry(
                self.f_sourcePriceAmount, width=8,
                textvariable=self.price, font=DEFAULT_FONT)
        self.ent_price.pack(side='left', padx=10)
        self.lb_amount = tk.Label(self.f_sourcePriceAmount,
                                  text="數量: ", font=DEFAULT_FONT)
        self.lb_amount.pack(side='left', padx=10)
        self.amount = tk.StringVar()
        self.cb_amount = tk.Entry(
                self.f_sourcePriceAmount, width=8,
                textvariable=self.amount, font=DEFAULT_FONT)
        self.cb_amount.pack(side='left', padx=10)
        self.f_sourcePriceAmount.grid(row=5, column=0, columnspan=4,
                                      padx=5, pady=5)
        # place
        self.lb_place = tk.Label(self, text="存置地點: ",
                                 font=DEFAULT_FONT)
        self.lb_place.grid(row=6, column=0, padx=5, pady=5)
        self.place = tk.StringVar()
        self.cb_place = ttk.Combobox(
                self, width=20, textvariable=self.place,
                font=DEFAULT_FONT)
        self.cb_place.grid(row=6, column=1, padx=5, pady=5)
        # lifespan(in years)
        self.lb_keep_year = tk.Label(self, text="保管年限: ",
                                     font=DEFAULT_FONT)
        self.lb_keep_year.grid(row=6, column=2, padx=5, pady=5)
        self.keep_year = tk.StringVar()
        self.f_keep_year = tk.Frame(self)
        self.ent_keep_year = tk.Entry(
                self.f_keep_year, width=15, textvariable=self.keep_year,
                font=DEFAULT_FONT)
        self.ent_keep_year.pack(side="left")
        self.lb_keep_year_yy = tk.Label(self.f_keep_year, text="年",
                                        font=DEFAULT_FONT)
        self.lb_keep_year_yy.pack(side="left")
        self.f_keep_year.grid(row=6, column=3, padx=5, pady=5)
        # keeper department
        self.lb_keep_dept = tk.Label(self, text="保管單位: ",
                                     font=DEFAULT_FONT)
        self.lb_keep_dept.grid(row=7, column=0, padx=5, pady=5)
        self.keep_dept = tk.StringVar()
        self.cb_keep_dept = ttk.Combobox(
                self, width=20, textvariable=self.keep_dept,
                font=DEFAULT_FONT)
        self.cb_keep_dept.grid(row=7, column=1, padx=5, pady=5)
        # use department
        self.lb_use_dept = tk.Label(self, text="使用單位: ",
                                    font=DEFAULT_FONT)
        self.lb_use_dept.grid(row=7, column=2, padx=5, pady=5)
        self.use_dept = tk.StringVar()
        self.cb_use_dept = ttk.Combobox(
                self, width=20, textvariable=self.use_dept,
                font=DEFAULT_FONT)
        self.cb_use_dept.grid(row=7, column=3, padx=5, pady=5)
        # keeper(person)
        self.lb_keeper = tk.Label(self, text="保管人: ",
                                  font=DEFAULT_FONT)
        self.lb_keeper.grid(row=8, column=0, padx=5, pady=5)
        self.keeper = tk.StringVar()
        self.cb_keeper = ttk.Combobox(
                self, width=20, textvariable=self.keeper,
                font=DEFAULT_FONT)
        self.cb_keeper.grid(row=8, column=1, padx=5, pady=5)
        # remarks
        self.lb_remark = tk.Label(self, text="備註事項: ",
                                  font=DEFAULT_FONT)
        self.lb_remark.grid(row=9, column=0, padx=5, pady=5)
        self.remark = tk.StringVar()
        self.ent_remark = tk.Entry(
                self, width=32, textvariable=self.remark,
                font=DEFAULT_FONT)
        self.ent_remark.grid(row=9, column=1, columnspan=2,
                             padx=5, pady=5)
        # buttons for searching
        self.f_bottomright = tk.Frame(self)
        self.btn_search = ttk.Button(
                self.f_bottomright, text='檢索', style="register.TButton",
                command=self.search)
        self.btn_search.pack(side="left")
        self.btn_saveThis = ttk.Button(
                self.f_bottomright, text='本筆存入', style="register.TButton",
                command=self.saveThis)
        self.btn_saveThis.pack(side="left")
        self.f_bottomright.grid(row=9, column=3, padx=5, pady=5)
        # seperator
        self.seperator = ttk.Separator(self,orient="horizontal").grid(
                row=10, columnspan=4, sticky="ew")
        # bottom navigation bar
        self.f_bottomButtons = tk.Frame(self)
        self.btn_quit = ttk.Button(
                self.f_bottomButtons, text='返回', style="register.TButton",
                command=self.quitMe)
        self.btn_quit.pack(side="left")
        self.btn_next = ttk.Button(
                self.f_bottomButtons, text='下一筆', style="register.TButton",
                command=self.fetchNext)
        self.btn_next.pack(side="left")
        self.btn_last = ttk.Button(
                self.f_bottomButtons, text='上一筆', style="register.TButton",
                command=self.fetchLast)
        self.btn_last.pack(side="left")
        self.btn_del_this = ttk.Button(
                self.f_bottomButtons, text='刪除本筆',
                style="register.TButton", command=self.deleteThis)
        self.btn_del_this.pack(side="left")
        self.btn_lookup_form = ttk.Button(
                self.f_bottomButtons, text='表單', style="register.TButton",
                command=self.lookupForm)
        self.btn_lookup_form.pack(side="left")
        self.btn_new_form = ttk.Button(
                self.f_bottomButtons, text='新增一筆',
                style="register.TButton", command=self.newForm)
        self.btn_new_form.pack(side="left")
        self.f_bottomButtons.grid(row=11, column=0, columnspan=4,
                                  padx=5, pady=5)
        self.updateByState(self.state)
        # get the focus in the system
        self.grab_set()

    def getAllRecords(self):
        # connect to db
        connect = sqlite3.connect(DATABASE_NAME)
        cursor = connect.cursor()
        sqlstr = "select * from hvhnonc_in;"
        cursor.execute(sqlstr)
        return cursor.fetchall()

    def updateByState(self, state):
        #print(state)
        state = state.lower()
        if state in ("none",):
            self.cb_cat.config(state="disabled")
            self.cb_subcat.config(state="disabled")
            self.cb_name.config(state="disabled")
            self.cb_unit.config(state="disabled")
            self.cb_brand.config(state="disabled")
            self.cb_spec.config(state="disabled")
            self.cb_in_date_yy.config(state="disabled")
            self.cb_in_date_mm.config(state="disabled")
            self.cb_in_date_dd.config(state="disabled")
            self.cb_key_date_yy.config(state="disabled")
            self.cb_key_date_mm.config(state="disabled")
            self.cb_key_date_dd.config(state="disabled")
            self.cb_source.config(state="disabled")
            self.ent_price.config(state="disabled")
            self.cb_amount.config(state="disabled")
            self.cb_place.config(state="disabled")
            self.ent_keep_year.config(state="disabled")
            self.cb_keep_dept.config(state="disabled")
            self.cb_use_dept.config(state="disabled")
            self.cb_keeper.config(state="disabled")
            self.ent_remark.config(state="disabled")
            self.clearAllField()
            return
        elif state in ("new",):
            self.cb_cat.config(state="readonly")
            self.cb_subcat.config(state="readonly")
            self.cb_name.config(state="normal")
            self.cb_unit.config(state="normal")
            self.cb_brand.config(state="normal")
            self.cb_spec.config(state="normal")
            self.cb_in_date_yy.config(state="normal")
            self.cb_in_date_mm.config(state="normal")
            self.cb_in_date_dd.config(state="normal")
            self.cb_key_date_yy.config(state="normal")
            self.cb_key_date_mm.config(state="normal")
            self.cb_key_date_dd.config(state="normal")
            self.cb_source.config(state="readonly")
            self.ent_price.config(state="normal")
            self.cb_amount.config(state="normal")
            self.cb_place.config(state="normal")
            self.ent_keep_year.config(state="normal")
            self.cb_keep_dept.config(state="normal")
            self.cb_use_dept.config(state="normal")
            self.cb_keeper.config(state="normal")
            self.ent_remark.config(state="normal")
            self.initializeAllField()
            self.clearAllField()
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
                self.cb_cat.config(state="readonly")
                self.cb_subcat.config(state="readonly")
                self.cb_name.config(state="normal")
                self.cb_unit.config(state="normal")
                self.cb_brand.config(state="normal")
                self.cb_spec.config(state="normal")
                self.cb_in_date_yy.config(state="normal")
                self.cb_in_date_mm.config(state="normal")
                self.cb_in_date_dd.config(state="normal")
                self.cb_key_date_yy.config(state="normal")
                self.cb_key_date_mm.config(state="normal")
                self.cb_key_date_dd.config(state="normal")
                self.cb_source.config(state="readonly")
                self.ent_price.config(state="normal")
                self.cb_amount.config(state="normal")
                self.cb_place.config(state="normal")
                self.ent_keep_year.config(state="normal")
                self.cb_keep_dept.config(state="normal")
                self.cb_use_dept.config(state="normal")
                self.cb_keeper.config(state="normal")
                self.ent_remark.config(state="normal")
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
                # in_date: mm/dd/yyyy
                in_date = str(record[9]).split('/')
                self.in_date_yy.set(in_date[2])
                self.in_date_mm.set(in_date[0])
                self.in_date_dd.set(in_date[1])
                # key_date: mm/dd/yyyy
                key_date = str(record[10]).split('/')
                self.key_date_yy.set(key_date[2])
                self.key_date_mm.set(key_date[0])
                self.key_date_dd.set(key_date[1])
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
        yearbox.set(datetime.datetime.now().year - 1911)
        monthbox.set(datetime.datetime.now().month)
        daybox.set(datetime.datetime.now().day)

    def lookupIndexInBook(self, state):
        #print("state == ", state)
        for i, sublist in enumerate(self.book):
            #print("sublist == {}, {}".format(i, sublist))
            if int(state) in sublist:
                #print("sublist found! {}, {}".format(i, sublist))
                return i

    def clearAllField(self):
        self.objID.set("")
        self.serial.set("")
        self.category.set("")
        self.subcategory.set("")
        self.name.set("")
        self.brand.set("")
        self.spec.set("")
        self.unit.set("")
        self.in_date_yy.set("")
        self.in_date_mm.set("")
        self.in_date_dd.set("")
        self.key_date_yy.set("")
        self.key_date_mm.set("")
        self.key_date_dd.set("")
        self.price.set("")
        self.amount.set("")
        self.place.set("")
        self.keep_year.set("")
        self.source.set("")
        self.keep_dept.set("")
        self.use_dept.set("")
        self.keeper.set("")
        self.remark.set("")

    def initializeAllField(self):
        for c in range(23):
            if c in (1,):
                # 物品大項
                # get categories from db
                connect = sqlite3.connect(DATABASE_NAME)
                connect.row_factory = lambda cursor, row: row[0]
                cursor = connect.cursor()
                sqlstr = "select description from hvhnonc_category;"
                cursor.execute(sqlstr)
                catagories = cursor.fetchall()
                self.cb_cat['values'] = catagories
                self.cb_cat.bind("<<ComboboxSelected>>",
                                 self.onCategorySelected)
                connect.close()
            elif c in (2,):
                # 物品細目
                self.cb_subcat.bind("<<ComboboxSelected>>",
                                    self.onSubcategorySelected)
            elif c in (3,):
                # 物品名稱
                self.cb_name.bind("<<ComboboxSelected>>",
                                  self.onNameSelected)
            elif c in (4,5,6,):
                # 單位 品牌 規格
                pass
            elif c in (7,8,):
                #物品編號 流水號
                pass
            elif c in (9,12):
                # 購置日期_年
                thisYear = datetime.datetime.now().year - 1911
                years = list(reversed(range(1, thisYear+1)))
                self.cb_in_date_yy.config(values=years)
                self.cb_key_date_yy.config(values=years)
            elif c in (10,13):
                # 購置日期_月
                months = list(range(1,13))
                self.cb_in_date_mm.config(values=months)
                self.cb_key_date_mm.config(values=months)
            elif c in (11,14):
                # 購置日期_日
                days = list(range(1,32))
                self.cb_in_date_dd.config(values=days)
                self.cb_key_date_dd.config(values=days)
            elif c in (15,):
                # 來源
                sources = ["購置","撥用","贈送"]
                self.cb_source.config(values=sources)
            elif c in (16,17):
                #價格 數量
                pass
            elif c in (18,):
                # 存置地點
                # grab department from db in cache
                connect = sqlite3.connect(DATABASE_NAME)
                connect.row_factory = lambda cursor, row: row[0]
                cursor = connect.cursor()
                sqlstr = ("select change_value from hvhnonc_in_cache "
                          "where this_ID = 0 and change_ID = ("
                          "select ID from hvhnonc_fields "
                          "where description = '存置地點') "
                          "order by rowid desc limit 30;")
                cursor.execute(sqlstr)
                places = cursor.fetchall()
                self.cb_place['values'] = places
                connect.close()
            elif c in (19,):
                # 保管年限
                pass
            elif c in (20,):
                # 保管單位
                # grab department from db in cache
                connect = sqlite3.connect(DATABASE_NAME)
                connect.row_factory = lambda cursor, row: row[0]
                cursor = connect.cursor()
                sqlstr = ("select change_value from hvhnonc_in_cache "
                          "where this_ID = 0 and change_ID = ("
                          "select ID from hvhnonc_fields "
                          "where description = '保管單位') "
                          "order by rowid desc limit 30;")
                cursor.execute(sqlstr)
                keep_depts = cursor.fetchall()
                self.cb_keep_dept['values'] = keep_depts
                connect.close()
            elif c in (21,):
                # 使用單位
                # grab department from db in cache
                connect = sqlite3.connect(DATABASE_NAME)
                connect.row_factory = lambda cursor, row: row[0]
                cursor = connect.cursor()
                sqlstr = ("select change_value from hvhnonc_in_cache "
                          "where this_ID = 0 and change_ID = ("
                          "select ID from hvhnonc_fields "
                          "where description = '使用單位')"
                          "order by rowid desc limit 30;")
                cursor.execute(sqlstr)
                use_depts = cursor.fetchall()
                self.cb_use_dept['values'] = use_depts
                connect.close()
            elif c in (22,):
                # 保管人
                # grab department from db in cache
                connect = sqlite3.connect(DATABASE_NAME)
                connect.row_factory = lambda cursor, row: row[0]
                cursor = connect.cursor()
                sqlstr = ("select change_value from hvhnonc_in_cache "
                          "where this_ID = 0 and change_ID = ("
                          "select ID from hvhnonc_fields "
                          "where description = '保管人') "
                          "order by rowid desc limit 30;")
                cursor.execute(sqlstr)
                keepers = cursor.fetchall()
                self.cb_keeper['values'] = keepers
                connect.close()
            elif c in (22,):
                # 備註事項
                pass
            else:
                pass

    def onCategorySelected(self, event):
        connect = sqlite3.connect(DATABASE_NAME)
        connect.row_factory = lambda cursor, row: row[0]
        cursor = connect.cursor()
        sqlstr = ("select description from hvhnonc_subcategory "
                  "where parent_ID = ("
                  "select ID from hvhnonc_category "
                  "where description = '"
                  + self.category.get() + "');")
        cursor.execute(sqlstr)
        subcatagories = cursor.fetchall()
        self.cb_subcat['values'] = subcatagories
        if (len(self.cb_subcat['values']) > 0 and
            self.cb_subcat.get() != self.cb_subcat['values'][0]):
            self.cb_subcat.set(self.cb_subcat['values'][0])
            self.onSubcategorySelected(None)
        connect.close()

    def onSubcategorySelected(self, event):
        # update product name
        # connect to db
        connect = sqlite3.connect(DATABASE_NAME)
        cursor = connect.cursor()
        # get all item name in the same subcategory from cache
        sqlstr = ("select change_ID, change_value "
                  "from hvhnonc_in_cache "
                  "where (this_ID = '"
                  + str(self.getFieldIDByName('物品細目')) +
                  "' and this_value = '"
                  + self.subcategory.get() +
                  "') order by rowid desc limit 30;")
        #print(sqlstr)
        cursor.execute(sqlstr)
        cachehit = cursor.fetchall()
        connect.close()
        #print(cachehit)
        # update item name only
        tempvals=[]
        nameFieldID = self.getFieldIDByName('物品名稱')
        #print(nameFieldID)
        for c in cachehit:
            #print(c[1])
            if c[0] == nameFieldID:
                tempvals.append(c[1])
        #print(tempvals)
        self.cb_name.config(values=tempvals)
        if (len(self.cb_name['values']) > 0 and
            self.cb_name.get() != self.cb_name['values'][0]):
            self.cb_name.set(self.cb_name['values'][0])
            self.onNameSelected(None)

    def onNameSelected(self, event):
        # update product name
        # connect to db
        connect = sqlite3.connect(DATABASE_NAME)
        cursor = connect.cursor()
        # get all item name in the same subcategory from cache
        sqlstr = ("select change_ID, change_value "
                  "from hvhnonc_in_cache "
                  "where (this_ID = '"
                  + str(self.getFieldIDByName('物品名稱')) +
                  "' and this_value = '"
                  + self.name.get() +
                  "') order by rowid desc limit 30;")
        #print(sqlstr)
        cursor.execute(sqlstr)
        cachehit = cursor.fetchall()
        connect.close()
        #print(cachehit)
        # update things with a switch
        isCacheHit = [False]*7
        tempUnit = []
        tempBrand = []
        tempSpec = []
        for c in cachehit:
            if c[0] in (4,):
                # 單位
                tempUnit.append(c[1])
                isCacheHit[4] = True
            elif c[0] in (5,):
                # 品牌
                tempBrand.append(c[1])
                isCacheHit[5] = True
            elif c[0] in (6,):
                # 規格
                tempSpec.append(c[1])
                isCacheHit[6] = True
            else:
                tk.messagebox.showerror("錯誤", "未知的快取值",
                                        parent=self)
        if isCacheHit[4]:
            self.cb_unit.config(values=tempUnit)
            if (len(self.cb_unit['values']) > 0 and
                self.cb_unit.get() != self.cb_unit['values'][0]):
                self.cb_unit.set(self.cb_unit['values'][0])
        if isCacheHit[5]:
            self.cb_brand.config(values=tempBrand)
            if (len(self.cb_brand['values']) > 0 and
                self.cb_brand.get() != self.cb_brand['values'][0]):
                self.cb_brand.set(self.cb_brand['values'][0])
        if isCacheHit[6]:
            self.cb_spec.config(values=tempSpec)
            if (len(self.cb_spec['values']) > 0 and
                self.cb_spec.get() != self.cb_spec['values'][0]):
                self.cb_spec.set(self.cb_spec['values'][0])

    def getFieldIDByName(self, name):
        # connect to db
        connect = sqlite3.connect(DATABASE_NAME)
        connect.row_factory = lambda cursor, row: row[0]
        cursor = connect.cursor()
        sqlstr = ("select ID from hvhnonc_fields "
                  "where description = '" + name + "';")
        cursor.execute(sqlstr)
        hit = cursor.fetchone()
        if hit:
            return hit
        return None

    def lookupSerial(self):
        # open a toplevel
        self.SerialWindow(self)

    class SerialWindow(tk.Toplevel):
        def __init__(self, parent, *args, **kwargs):
            # treeview styles
            style = ttk.Style()
            style.configure("Treeview", font=DEFAULT_FONT)
            style.configure("Treeview.Heading", font=DEFAULT_FONT)
            # init
            tk.Toplevel.__init__(self, parent, *args, **kwargs)
            self.parent = parent
            self.attributes("-topmost", "true")
            self.attributes("-topmost", "false")
            # get serials from db_in
            # connect to db
            connect = sqlite3.connect(DATABASE_NAME)
            cursor = connect.cursor()
            sqlstr = "select count(distinct name) from hvhnonc_in;"
            cursor.execute(sqlstr)
            itemCount = cursor.fetchone()
            self.title("序號: 共{}筆".format(itemCount[0]))
            self.geometry("640x500")
            # get all objIDs and sqlIDs
            sqlstr = ("select object_ID, name, count(*) "
                      "from hvhnonc_in "
                      "group by object_ID, name "
                      "order by object_ID, serial_ID;")
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
            s.configure('search.TButton', font=('Helvetica', 13))
            tk.Toplevel.__init__(self, parent, *args, **kwargs)
            self.parent = parent
            self.attributes("-topmost", "true")
            self.attributes("-topmost", "false")
            self.title("檢索")
            self.resizable(False, False)
            self.geometry("465x60")
            # searchbar
            self.l_search = tk.Label(self, text="請輸入想要檢索的關鍵字:",
                                     font=DEFAULT_FONT)
            self.l_search.grid(row=0, column=0)
            self.parent.query = tk.StringVar()
            self.cb_searchbar = ttk.Combobox(
                    self, width=20, textvariable=self.parent.query,
                    font=DEFAULT_FONT)
            # get search cache from db
            connect = sqlite3.connect(DATABASE_NAME)
            cursor = connect.cursor()
            sqlstr = ("select change_value "
                      "from hvhnonc_in_cache "
                      "where change_ID = ("
                      "select ID from hvhnonc_fields "
                      "where description = '檢索') "
                      "order by rowid limit 30;")
            cursor.execute(sqlstr)
            history = cursor.fetchall()
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
            connect = sqlite3.connect(DATABASE_NAME)
            cursor = connect.cursor()
            sqlstr = ("replace into hvhnonc_in_cache"
                      "(this_ID, this_value, change_ID, change_value) "
                      "values (0, 'none', ("
                      "select ID from hvhnonc_fields "
                      "where description = '檢索'), '"
                      + self.parent.query.get() +
                      "');")
            #print(sqlstr)
            cursor.execute(sqlstr)
            connect.commit()
            # open a result toplevel
            self.SearchResultWindow(self.parent)
            self.destroy()

        class SearchResultWindow(tk.Toplevel):
            def __init__(self, parent, *args, **kwargs):
                # treeview styles
                style = ttk.Style()
                style.configure("Treeview", font=DEFAULT_FONT)
                style.configure("Treeview.Heading", font=DEFAULT_FONT)
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
                connect = sqlite3.connect(DATABASE_NAME)
                cursor = connect.cursor()
                phrase = parent.query.get()
                sqlstr = (
                        "select ID, in_date, name, "
                        "place, keeper, remark "
                        "from hvhnonc_in "
                        "where ("
                        "object_ID like '%" + phrase + "%' or "
                        "serial_ID like '%" + phrase+ "%' or "
                        "category like '%" + phrase+ "%' or "
                        "subcategory like '%" + phrase+ "%' or "
                        "name like '%" + phrase+ "%' or "
                        "brand like '%" + phrase+ "%' or "
                        "spec like '%" + phrase+ "%' or "
                        "in_date like '%" + phrase+ "%' or "
                        "key_date like '%" + phrase+ "%' or "
                        "place like '%" + phrase+ "%' or "
                        "source like '%" + phrase+ "%' or "
                        "keep_department like '%" + phrase+ "%' or "
                        "use_department like '%" + phrase+ "%' or "
                        "keeper like '%" + phrase+ "%' or "
                        "remark like '%" + phrase+ "%')"
                        " order by in_date;")
                #print(sqlstr)
                cursor.execute(sqlstr)
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
                self.parent.state = self.tv.item(item,"values")[0]
                self.parent.updateByState(self.parent.state)
                self.destroy()

    def saveThis(self):
        print("saveThis")

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
        print("deleteThis")

    def lookupForm(self):
        #print("lookupForm")
        # opens a new toplevel for filtering
        self.FilterWindow(self)

    class FilterWindow(tk.Toplevel):
        def __init__(self, parent, *args, **kwargs):
            # init
            tk.Toplevel.__init__(self, parent, *args, **kwargs)
            self.parent = parent
            self.attributes("-topmost", "true")
            self.title("請輸入要篩選的範圍")
            self.geometry("665x290")
            # category
            self.lb_category = tk.Label(
                    self, text="物品大項: ", font=DEFAULT_FONT)
            self.lb_category.grid(row=0, column=0, padx=5, pady=5)
            self.category = tk.StringVar()
            self.cb_category = ttk.Combobox(
                    self, width=20, textvariable=self.category,
                    font=DEFAULT_FONT, state="readonly")
            self.cb_category.grid(row=0, column=1, padx=5, pady=5)
            # subcategory
            self.lb_subcategory = tk.Label(
                    self, text="物品細目: ", font=DEFAULT_FONT)
            self.lb_subcategory.grid(row=0, column=2, padx=5, pady=5)
            self.subcategory = tk.StringVar()
            self.cb_subcategory = ttk.Combobox(
                    self, width=20, textvariable=self.subcategory,
                    font=DEFAULT_FONT, state="readonly")
            self.cb_subcategory.grid(row=0, column=3, padx=5, pady=5)
            # name
            self.lb_name = tk.Label(
                    self, text="物品名稱: ", font=DEFAULT_FONT)
            self.lb_name.grid(row=1, column=0, padx=5, pady=5)
            self.name = tk.StringVar()
            self.cb_name = ttk.Combobox(
                    self, width=20, textvariable=self.name,
                    font=DEFAULT_FONT)
            self.cb_name.grid(row=1, column=1, padx=5, pady=5)
            # brand
            self.lb_brand = tk.Label(
                    self, text="品牌: ", font=DEFAULT_FONT)
            self.lb_brand.grid(row=1, column=2, padx=5, pady=5)
            self.brand = tk.StringVar()
            self.cb_brand = ttk.Combobox(
                    self, width=20, textvariable=self.brand,
                    font=DEFAULT_FONT)
            self.cb_brand.grid(row=1, column=3, padx=5, pady=5)
            # spec
            self.lb_spec = tk.Label(
                    self, text="規格: ", font=DEFAULT_FONT)
            self.lb_spec.grid(row=2, column=0, padx=5, pady=5)
            self.spec = tk.StringVar()
            self.cb_spec = ttk.Combobox(
                    self, width=20, textvariable=self.spec,
                    font=DEFAULT_FONT)
            self.cb_spec.grid(row=2, column=1, padx=5, pady=5)
            # price
            self.lb_price = tk.Label(
                    self, text="單價: ", font=DEFAULT_FONT)
            self.lb_price.grid(row=2, column=2, padx=5, pady=5)
            self.f_price = tk.Frame(self)
            self.price_min = tk.StringVar()
            self.ent_price_min = tk.Entry(
                    self.f_price, width=5, textvariable=self.price_min,
                    font=DEFAULT_FONT)
            self.ent_price_min.pack(side='left', padx=10)
            self.lb_sqig_price = tk.Label(
                    self.f_price, text=" ~ ", font=DEFAULT_FONT)
            self.lb_sqig_price.pack(side='left', padx=10)
            self.price_max = tk.StringVar()
            self.ent_price_max = tk.Entry(
                    self.f_price, width=5, textvariable=self.price_max,
                    font=DEFAULT_FONT)
            self.ent_price_max.pack(side='left', padx=10)
            self.f_price.grid(row=2, column=3, padx=5, pady=5)
            # in date (min~max)
            self.f_date = tk.Frame(self)
            self.lb_date = tk.Label(
                    self.f_date, text="購置日期: ", font=DEFAULT_FONT)
            self.lb_date.pack(side='left')
            self.date_yy_min = tk.StringVar()
            self.cb_date_yy_min = ttk.Combobox(
                    self.f_date, width=3, textvariable=self.date_yy_min,
                    font=DEFAULT_FONT)
            self.cb_date_yy_min.pack(side='left')
            self.lb_date_yy_min = tk.Label(
                    self.f_date, text="年", font=DEFAULT_FONT)
            self.lb_date_yy_min.pack(side='left')
            self.date_mm_min = tk.StringVar()
            self.cb_date_mm_min = ttk.Combobox(
                    self.f_date, width=2, textvariable=self.date_mm_min,
                    font=DEFAULT_FONT)
            self.cb_date_mm_min.pack(side='left')
            self.lb_date_mm_min = tk.Label(
                    self.f_date, text="月", font=DEFAULT_FONT)
            self.lb_date_mm_min.pack(side='left')
            self.date_dd_min = tk.StringVar()
            self.cb_date_dd_min = ttk.Combobox(
                    self.f_date, width=2, textvariable=self.date_dd_min,
                    font=DEFAULT_FONT)
            self.cb_date_dd_min.pack(side='left')
            self.lb_date_dd_min = tk.Label(
                    self.f_date, text="日", font=DEFAULT_FONT)
            self.lb_date_dd_min.pack(side='left')
            self.lb_sqig_date = tk.Label(
                    self.f_date, text="~", font=DEFAULT_FONT)
            self.lb_sqig_date.pack(side='left')
            self.date_yy_max = tk.StringVar()
            self.cb_date_yy_max = ttk.Combobox(
                    self.f_date, width=3, textvariable=self.date_yy_max,
                    font=DEFAULT_FONT)
            self.cb_date_yy_max.pack(side='left')
            self.lb_date_yy_max = tk.Label(
                    self.f_date, text="年", font=DEFAULT_FONT)
            self.lb_date_yy_max.pack(side='left')
            self.date_mm_max = tk.StringVar()
            self.cb_date_mm_max = ttk.Combobox(
                    self.f_date, width=2, textvariable=self.date_mm_max,
                    font=DEFAULT_FONT)
            self.cb_date_mm_max.pack(side='left')
            self.lb_date_mm_max = tk.Label(
                    self.f_date, text="月", font=DEFAULT_FONT)
            self.lb_date_mm_max.pack(side='left')
            self.date_dd_max = tk.StringVar()
            self.cb_date_dd_max = ttk.Combobox(
                    self.f_date, width=2, textvariable=self.date_dd_max,
                    font=DEFAULT_FONT)
            self.cb_date_dd_max.pack(side='left')
            self.lb_date_dd_max = tk.Label(
                    self.f_date, text="日", font=DEFAULT_FONT)
            self.lb_date_dd_max.pack(side='left')
            self.f_date.grid(row=3, column=0,
                             padx=5, pady=5, columnspan=4)
            # key date (min~max)
            self.f_key_date = tk.Frame(self)
            self.lb_key_date = tk.Label(
                    self.f_key_date, text="建帳日期: ",
                    font=DEFAULT_FONT)
            self.lb_key_date.pack(side='left')
            self.date_yy_min = tk.StringVar()
            self.cb_key_date_yy_min = ttk.Combobox(
                    self.f_key_date, width=3,
                    textvariable=self.date_yy_min, font=DEFAULT_FONT)
            self.cb_key_date_yy_min.pack(side='left')
            self.lb_key_date_yy_min = tk.Label(
                    self.f_key_date, text="年", font=DEFAULT_FONT)
            self.lb_key_date_yy_min.pack(side='left')
            self.date_mm_min = tk.StringVar()
            self.cb_key_date_mm_min = ttk.Combobox(
                    self.f_key_date, width=2,
                    textvariable=self.date_mm_min, font=DEFAULT_FONT)
            self.cb_key_date_mm_min.pack(side='left')
            self.lb_key_date_mm_min = tk.Label(
                    self.f_key_date, text="月", font=DEFAULT_FONT)
            self.lb_key_date_mm_min.pack(side='left')
            self.date_dd_min = tk.StringVar()
            self.cb_key_date_dd_min = ttk.Combobox(
                    self.f_key_date, width=2,
                    textvariable=self.date_dd_min, font=DEFAULT_FONT)
            self.cb_key_date_dd_min.pack(side='left')
            self.lb_key_date_dd_min = tk.Label(
                    self.f_key_date, text="日", font=DEFAULT_FONT)
            self.lb_key_date_dd_min.pack(side='left')
            self.lb_sqig_key_date = tk.Label(
                    self.f_key_date, text="~", font=DEFAULT_FONT)
            self.lb_sqig_key_date.pack(side='left')
            self.date_yy_max = tk.StringVar()
            self.cb_key_date_yy_max = ttk.Combobox(
                    self.f_key_date, width=3,
                    textvariable=self.date_yy_max, font=DEFAULT_FONT)
            self.cb_key_date_yy_max.pack(side='left')
            self.lb_key_date_yy_max = tk.Label(
                    self.f_key_date, text="年", font=DEFAULT_FONT)
            self.lb_key_date_yy_max.pack(side='left')
            self.date_mm_max = tk.StringVar()
            self.cb_key_date_mm_max = ttk.Combobox(
                    self.f_key_date, width=2,
                    textvariable=self.date_mm_max, font=DEFAULT_FONT)
            self.cb_key_date_mm_max.pack(side='left')
            self.lb_key_date_mm_max = tk.Label(
                    self.f_key_date, text="月", font=DEFAULT_FONT)
            self.lb_key_date_mm_max.pack(side='left')
            self.date_dd_max = tk.StringVar()
            self.cb_key_date_dd_max = ttk.Combobox(
                    self.f_key_date, width=2,
                    textvariable=self.date_dd_max, font=DEFAULT_FONT)
            self.cb_key_date_dd_max.pack(side='left')
            self.lb_key_date_dd_max = tk.Label(
                    self.f_key_date, text="日", font=DEFAULT_FONT)
            self.lb_key_date_dd_max.pack(side='left')
            self.f_key_date.grid(row=4, column=0,
                                 padx=5, pady=5, columnspan=4)
            # keeper department
            self.lb_keep_dept = tk.Label(
                    self, text="保管單位: ", font=DEFAULT_FONT)
            self.lb_keep_dept.grid(row=5, column=0, padx=5, pady=5)
            self.keep_dept = tk.StringVar()
            self.cb_keep_dept = ttk.Combobox(
                    self, width=20, textvariable=self.keep_dept,
                    font=DEFAULT_FONT)
            self.cb_keep_dept.grid(row=5, column=1, padx=5, pady=5)
            # place
            self.lb_place = tk.Label(
                    self, text="存置地點: ", font=DEFAULT_FONT)
            self.lb_place.grid(row=5, column=2, padx=5, pady=5)
            self.place = tk.StringVar()
            self.cb_place = ttk.Combobox(
                    self, width=20, textvariable=self.place,
                    font=DEFAULT_FONT)
            self.cb_place.grid(row=5, column=3, padx=5, pady=5)
            # use department
            self.lb_use_dept = tk.Label(
                    self, text="使用單位: ", font=DEFAULT_FONT)
            self.lb_use_dept.grid(row=6, column=0, padx=5, pady=5)
            self.use_dept = tk.StringVar()
            self.cb_use_dept = ttk.Combobox(
                    self, width=20, textvariable=self.use_dept,
                    font=DEFAULT_FONT)
            self.cb_use_dept.grid(row=6, column=1, padx=5, pady=5)
            # keeper
            self.lb_keeper = tk.Label(
                    self, text="保管人: ", font=DEFAULT_FONT)
            self.lb_keeper.grid(row=6, column=2, padx=5, pady=5)
            self.keeper = tk.StringVar()
            self.cb_keeper = ttk.Combobox(
                    self, width=20, textvariable=self.keeper,
                    font=DEFAULT_FONT)
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
            self.grab_set()
            self.attributes("-topmost", "false")

        def catchReturn(self, event):
            self.submit()

        def initLookupForm(self):
            # connect to db
            connect = sqlite3.connect(DATABASE_NAME)
            cursor = connect.cursor()

            # 物品大項
            sqlstr = "select description from hvhnonc_category;"
            # print(sqlstr)
            cursor.execute(sqlstr)
            connect.commit()
            catagories = cursor.fetchall()
            self.cb_category.config(values=catagories)
            self.cb_category.bind(
                    "<<ComboboxSelected>>", self.onCategorySelected)

            # 物品細目
            # 物品名稱
            # 品牌
            # 規格
            # initialized with onCategorySelected()

            # 單價(低)
            # 單價(高)
            # no need for init

            # 購置日期(低)yyymmdd
            # 購置日期(高)yyymmdd
            # 建帳日期(低)yyymmdd
            # 建帳日期(高)yyymmdd
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

            connect = sqlite3.connect(DATABASE_NAME)
            connect.row_factory = lambda cursor, row: row[0]
            cursor = connect.cursor()
            # 保管單位
            sqlstr = ("select change_value from hvhnonc_in_cache "
                      "where this_ID = 0 and change_ID = ("
                      "select ID from hvhnonc_fields "
                      "where description = '保管單位')"
                      "order by rowid desc limit 30;")
            cursor.execute(sqlstr)
            keep_dept = cursor.fetchall()
            self.cb_keep_dept['values'] = keep_dept
            # 存置地點
            sqlstr = ("select change_value from hvhnonc_in_cache "
                      "where this_ID = 0 and change_ID = ("
                      "select ID from hvhnonc_fields "
                      "where description = '存置地點')"
                      "order by rowid desc limit 30;")
            cursor.execute(sqlstr)
            places = cursor.fetchall()
            self.cb_place['values'] = places
            # 使用單位
            sqlstr = ("select change_value from hvhnonc_in_cache "
                      "where this_ID = 0 and change_ID = ("
                      "select ID from hvhnonc_fields "
                      "where description = '使用單位')"
                      "order by rowid desc limit 30;")
            cursor.execute(sqlstr)
            use_dept = cursor.fetchall()
            self.cb_use_dept['values'] = use_dept
            # 保管人
            sqlstr = ("select change_value from hvhnonc_in_cache "
                      "where this_ID = 0 and change_ID = ("
                      "select ID from hvhnonc_fields "
                      "where description = '保管人')"
                      "order by rowid desc limit 30;")
            cursor.execute(sqlstr)
            keepers = cursor.fetchall()
            self.cb_keeper['values'] = keepers
            connect.close()

        def initDateComboboxes(self, yearbox, monthbox, daybox):
            thisYear = datetime.datetime.now().year - 1911
            yearbox.config(values=list(reversed(range(1,thisYear+1))))
            monthbox.config(values=list(range(1,12+1)))
            daybox.config(values=list(range(1,31+1)))

        def onCategorySelected(self, event):
            # update subcategory
            connect = sqlite3.connect(DATABASE_NAME)
            cursor = connect.cursor()
            sqlstr = ("select description from hvhnonc_subcategory "
                      "where parent_ID = "
                      "(select ID from hvhnonc_category "
                      "where description = '"
                      + self.cb_category.get() +
                      "' );")
            #print(sqlstr)
            cursor.execute(sqlstr)
            connect.commit()
            subcatagories = cursor.fetchall()
            self.cb_subcategory.config(values=subcatagories)
            self.cb_subcategory.bind(
                    "<<ComboboxSelected>>", self.onSubcategorySelected)
            self.onSubcategorySelected(None)
            if (len(self.cb_subcategory['values']) > 0 and
                self.cb_subcategory.get() !=
                self.cb_subcategory['values'][0]):
                self.cb_subcategory.set(
                        self.cb_subcategory['values'][0])
                self.onSubcategorySelected(None)
            connect.close()

        def onSubcategorySelected(self, event):
            # update other fields in the lookup form
            # namely 名稱, 品牌, 規格
                   # update product name
            # connect to db
            connect = sqlite3.connect(DATABASE_NAME)
            cursor = connect.cursor()
            # get all item name in the same subcategory from cache
            sqlstr = ("select change_ID, change_value "
                      "from hvhnonc_in_cache "
                      "where(this_ID = "
                      + str(self.getFieldIDByName('物品細目')) +
                      " and this_value = '"
                      + self.subcategory.get() +
                      "') order by rowid desc limit 30;")
            #print(sqlstr)
            cursor.execute(sqlstr)
            cachehits = cursor.fetchall()
            connect.close()
            #print(cachehits)
            # update item name only
            tempvals = []
            nameFieldID = self.getFieldIDByName('物品名稱')
            #print(nameFieldID)
            for c in cachehits:
                #print(c[1])
                if c[0] == nameFieldID:
                    tempvals.append(c[1])
            #print(tempvals)
            self.cb_name.config(values=tempvals)
            if (len(self.cb_name['values']) > 0 and
            self.cb_name.get() != self.cb_name['values'][0]):
                self.cb_name.set(self.cb_name['values'][0])
                self.onNameSelected(None)

        def onNameSelected(self, event):
            # update product name
            # connect to db
            connect = sqlite3.connect(DATABASE_NAME)
            cursor = connect.cursor()
            # get all item name in the same subcategory from cache
            sqlstr = ("select change_ID, change_value "
                      "from hvhnonc_in_cache "
                      "where(this_ID = "
                      + str(self.getFieldIDByName('物品名稱')) +
                      " and this_value = '"
                      + self.name.get() +
                      "') order by rowid desc limit 30;")
            #print(sqlstr)
            cursor.execute(sqlstr)
            cachehit = cursor.fetchall()
            connect.close()
            #print(cachehit)
            # update things with a switch
            isCacheHit = [False]*7
            tempBrand = []
            tempSpec = []
            for c in cachehit:
                if c[0] in (5,):
                    # 品牌
                    tempBrand.append(c[1])
                    isCacheHit[5] = True
                elif c[0] in (6,):
                    # 規格
                    tempSpec.append(c[1])
                    isCacheHit[6] = True
            if isCacheHit[5]:
                self.cb_brand.config(values=tempBrand)
                if (len(self.cb_brand['values']) > 0 and
                    self.cb_brand.get() != self.cb_brand['values'][0]):
                    self.cb_brand.set(self.cb_brand['values'][0])
            if isCacheHit[6]:
                self.cb_spec.config(values=tempSpec)
                if (len(self.cb_spec['values']) > 0 and
                    self.cb_spec.get() != self.cb_spec['values'][0]):
                    self.cb_spec.set(self.cb_spec['values'][0])

        def getFieldIDByName(self, name):
            # connect to db
            connect = sqlite3.connect(DATABASE_NAME)
            connect.row_factory = lambda cursor, row: row[0]
            cursor = connect.cursor()
            sqlstr = ("select ID from hvhnonc_fields "
                      "where description = '" + name + "';")
            cursor.execute(sqlstr)
            hit = cursor.fetchone()
            return hit

        def quitMe(self):
            self.destroy()

        def submit(self):
            print("lookupForm:submit")


    def newForm(self):
        self.state = 'new'
        self.updateByState(self.state)

    def quitMe(self):
        self.destroy()


class unregister(tk.Toplevel):
    def __init__(self, parent, *args, **kwargs):
        s = ttk.Style()
        s.configure('unregister.TButton', font=('Helvetica', 13))
        tk.Toplevel.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.attributes("-topmost", "true")
        self.attributes("-topmost", "false")
        self.title("除帳")
        self.geometry(DEFAULT_TOPLEVEL_SIZE)
        self.resizable(False, False)
        # gui
        self.l = tk.Label(self, text="除帳畫面", font=DEFAULT_FONT)
        self.l.pack()
        # buttons
        self.btn_quit = ttk.Button(self, text='返回',
                                   style="unregister.TButton",
                                   command=self.quitMe)
        self.btn_quit.pack()
        # focus
        self.grab_set()

    def quitMe(self):
        self.destroy()


class printNonc(tk.Toplevel):
    def __init__(self, parent, *args, **kwargs):
        s = ttk.Style()
        s.configure('printNonc.TButton', font=('Helvetica', 13))
        tk.Toplevel.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.attributes("-topmost", "true")
        self.attributes("-topmost", "false")
        self.title("列印")
        self.geometry(DEFAULT_TOPLEVEL_SIZE)
        self.resizable(False, False)
        #gui
        self.l = tk.Label(self, text="列印畫面", font=DEFAULT_FONT)
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
        s.configure('maintenance.TButton', font=('Helvetica', 13))
        tk.Toplevel.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.attributes("-topmost", "true")
        self.attributes("-topmost", "false")
        self.title("維護")
        self.geometry(DEFAULT_TOPLEVEL_SIZE)
        self.resizable(False, False)
        #gui
        self.l = tk.Label(self, text="維護畫面", font=DEFAULT_FONT)
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