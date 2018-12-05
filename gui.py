# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 09:08:05 2018

@author: alchenerd (alchenerd@gmail.com)
"""

import datetime as dt
import hashlib
import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
from typing import Dict

from __init__ import __version__

_welcome_image = "kaiba.gif"
_default_toplevel_size = "681x421"
_default_font = (None, 15)
_default_button_font = (None, 15)
_default_database = "HVHNONC.db"


def _getConnection(databaseName: str = _default_database):
    connect = sqlite3.connect(databaseName)
    cursor = connect.cursor()
    return connect, cursor


# A frame that consists of 3 comboboxes: Year of Republic era, month, day
class DateFrame(tk.Frame):
    def __init__(
            self,
            parent: tk.BaseWidget = None,
            variable: tk.StringVar = None
    ):
        tk.Frame.__init__(self, parent)
        self.variable = variable
        self.y = tk.StringVar()
        self.m = tk.StringVar()
        self.d = tk.StringVar()
        self.cb_y = ttk.Combobox(
            self, width=3, textvariable=self.y, font=_default_font)
        self.cb_m = ttk.Combobox(
            self, width=2, textvariable=self.m, font=_default_font)
        self.cb_d = ttk.Combobox(
            self, width=2, textvariable=self.d, font=_default_font)
        self.l_y = tk.Label(self, text="年", font=_default_font)
        self.l_m = tk.Label(self, text="月", font=_default_font)
        self.l_d = tk.Label(self, text="日", font=_default_font)
        # form: "{}年{}月{}日"
        self.cb_y.pack(side="left")
        self.l_y.pack(side="left")
        self.cb_m.pack(side="left")
        self.l_m.pack(side="left")
        self.cb_d.pack(side="left")
        self.l_d.pack(side="left")
        # Conversion to the Year of Republic era, ascended
        years = list(reversed(range(1, dt.datetime.now().year - 1911 + 1)))
        self.cb_y.config(values=years)
        months = list(range(1, 12 + 1))
        self.cb_m.config(values=months)
        days = list(range(1, 31 + 1))
        self.cb_d.config(values=days)
        self.setAsToday()
        # updateVar(): modify the inner string variable
        self.updateVar()
        self.cb_y.bind("<<ComboboxSelected>>", self.updateVar)
        self.cb_m.bind("<<ComboboxSelected>>", self.updateVar)
        self.cb_d.bind("<<ComboboxSelected>>", self.updateVar)

    def setAsToday(self):
        y = dt.datetime.now().year - 1911
        m = dt.datetime.now().month
        d = dt.datetime.now().day
        self.y.set(str(y))
        self.m.set(str(m))
        self.d.set(str(d))
        self.updateVar()

    def clear(self):
        self.y.set("")
        self.m.set("")
        self.d.set("")
        self.variable.set("")

    def updateVar(self, event=None):
        d = (self.y.get(), self.m.get(), self.d.get())
        self.variable.set("-".join(d))


# The smallest unit in a form, consists a label and a tkinter widget
class CompoundField():
    # optional: span=True lets CompoundField contains two widgets:
    #           widgetMin and widgetMax
    def __init__(
            self,
            parent: tk.BaseWidget,
            widgetType: str,
            fieldName: str,
            enabledState: str = None,
            description: str = "標籤",
            **kwargs
    ):
        self.parent = parent
        self.label = tk.Label(parent, text=description + "：",
                              font=_default_font)
        if widgetType is not None:
            self.widgetType = widgetType.lower()
        if enabledState is not None:
            self.enabledState = enabledState.lower()
        self.fieldName = fieldName
        self.description = description
        # if kwargs["range"] is true
        if kwargs.get("span"):
            self.widget = tk.Frame(parent)
            self.variable = {}
            self.variable["min"] = tk.StringVar()
            self.variable["max"] = tk.StringVar()
            self.widget.min = self.createWidget(
                widgetType, self.widget, self.variable["min"])
            self.widget.tilde = tk.Label(
                self.widget, text="~", font=_default_font)
            self.widget.max = self.createWidget(
                widgetType, self.widget, self.variable["max"])
            self.widget.min.pack(side="left")
            self.widget.tilde.pack(side="left")
            self.widget.max.pack(side="left")
        else:
            self.variable = tk.StringVar()
            self.widget = self.createWidget(widgetType, parent, self.variable)

    def createWidget(
            self,
            widgetType: str = None,
            parent: tk.BaseWidget = None,
            variable: tk.StringVar = None):
        if widgetType is None:
            return
        if widgetType == "entry":
            return tk.Entry(parent, textvariable=variable,
                            font=_default_font, width=20)
        if widgetType == "combobox":
            return ttk.Combobox(parent, textvariable=variable,
                                font=_default_font, width=20)
        if widgetType == "dateframe":
            return DateFrame(parent, variable)
        if widgetType == "spinbox":
            return tk.Spinbox(parent, from_=1, to=100, textvariable=variable,
                              font=_default_font, width=20)


# returns the field ID from hvhnonc_fields
def getFieldIDByName(name: str):
    try:
        if name in (None, ""):
            return
        connect, cursor = _getConnection(_default_database)
        connect.row_factory = lambda cursor, row: row[0]
        sqlstr = ("select ID "
                  "from hvhnonc_fields "
                  "where description=?;")
        cursor.execute(sqlstr, (name,))
        hit = cursor.fetchone()
        if hit:
            return hit[0]
    except Exception as e:
        print("getFieldIDByName: {}".format(e))
        messagebox.showerror("錯誤", "執行查詢時出了問題: {}".format(e))
        return None


# The entry point of the whole gui module when imported
class Index(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        parent.geometry("640x350")
        parent.title("非消耗品管理系統 (v" + __version__ + ")")
        parent.focus_force()
        parent.resizable(False, False)
        parent.option_add("*Font", _default_font)
        parent.option_add("*Label.Font", _default_font)
        parent.option_add('*TCombobox*Listbox.font', _default_font)
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
        Register(self)

    def unregisterPressed(self):
        Unregister(self)

    def printPressed(self):
        PrintNonc(self)

    def maintenancePressed(self):
        Maintenance(self)

    def quitHVHODBMS(self):
        self.parent.destroy()


# The login form using sha256 as hash
class Login(tk.Toplevel):
    def __init__(self, parent, *args, **kwargs):
        tk.Toplevel.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.attributes("-topmost", "true")
        self.attributes("-topmost", "false")
        self.title("登入")
        self.geometry("250x115")
        self.resizable(False, False)
        # User info
        self.compFields = {}
        self.compFields["username"] = CompoundField(
            parent=self,
            widgetType="entry",
            description="帳號",
            fieldName="username")
        self.compFields["password"] = CompoundField(
            parent=self,
            widgetType="entry",
            description="密碼",
            fieldName="password")
        self.compFields["password"].widget.config(show='*')
        # Temporary username and password
        self.compFields["username"].variable.set("administrator")
        self.compFields["password"].variable.set("veteranshome")
        self.compFields["username"].label.place(x=0, y=11)
        self.compFields["password"].label.place(x=0, y=41)
        self.compFields["username"].widget.place(x=63, y=13)
        self.compFields["password"].widget.place(x=63, y=43)
        # buttons
        s = ttk.Style()
        s.configure('login.TButton', font=_default_button_font)
        self.btn_login = ttk.Button(
            self,
            text='登入',
            style="login.TButton",
            command=self.validate
        )
        self.btn_login.place(x=6, y=75)
        self.btn_quit = ttk.Button(
            self,
            text='離開',
            style="login.TButton",
            command=self.abortLogin
        )
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
        username = self.compFields["username"].variable.get()
        password = self.compFields["password"].variable.get()
        if self.isValid(username, password):
            connect, cursor = _getConnection(_default_database)
            sqlstr = ("select * "
                      "from hvhnonc_users "
                      "where username=? "
                      "limit 1;")
            cursor.execute(sqlstr, (username,))
            row = cursor.fetchone()
            connect.close()
            # row = [(ID, username, hash_SHA256, salt)]
            if row is None:
                messagebox.showerror(
                    "錯誤", "不正確的帳號或密碼", parent=self)
                return
            DB_hash = row[2]
            DB_salt = row[3]
            # SHA256 hash the DB_salt + password
            sha256 = hashlib.sha256()
            data = DB_salt + password
            sha256.update(data.encode("utf-8"))
            localHash = sha256.hexdigest()
            # print(sha256.hexdigest())
            if localHash == DB_hash:
                self.parent.parent.focus_force()
                self.destroy()
            else:
                messagebox.showerror(
                    "錯誤", "不正確的帳號或密碼", parent=self)
        else:
            # <meme> is this exception handling? </meme>
            messagebox.showerror(
                "錯誤", "帳號與密碼須為20字以內的英數字", parent=self)

    def isValid(self, username, password):
        if (username.isalnum() and len(username) <= 20 and
                password.isalnum() and len(password) <= 20):
            return True
        else:
            return False


# The toplevel which contains the register form to fill
class Register(tk.Toplevel):
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
        self.geometry("681x411")
        self.resizable(False, False)
        self.createWidgets()
        self.createView()
        self.updateByState("none")
        # get focus
        self.grab_set()

    def createWidgets(self) -> Dict[str, CompoundField]:
        # compound fields
        self.compFields = {}
        self.compFields["category"] = CompoundField(
            parent=self, widgetType="combobox", description="物品大項",
            fieldName="category", enabledState="readonly")
        self.compFields["subcategory"] = CompoundField(
            parent=self, widgetType="combobox", description="物品細目",
            fieldName="subcategory", enabledState="readonly")
        self.compFields["name"] = CompoundField(
            parent=self, widgetType="combobox", description="物品名稱",
            fieldName="name", enabledState="normal")
        self.compFields["unit"] = CompoundField(
            parent=self, widgetType="combobox", description="單位",
            fieldName="unit", enabledState="normal")
        self.compFields["brand"] = CompoundField(
            parent=self, widgetType="combobox", description="品牌",
            fieldName="brand", enabledState="normal")
        self.compFields["spec"] = CompoundField(
            parent=self, widgetType="combobox", description="規格",
            fieldName="spec", enabledState="normal")
        self.compFields["object_ID"] = CompoundField(
            parent=self, widgetType="entry",
            description="物品編號", fieldName="object_ID",
            enabledState="disabled")
        self.compFields["object_ID"].widget.config(state="disabled")
        # serial_ID frame
        self.f_serial = tk.Frame(self)
        self.compFields["serial_ID"] = CompoundField(
            parent=self.f_serial, widgetType="entry", description="流水號",
            fieldName="serial_ID", enabledState="disabled")
        self.compFields["serial_ID"].widget.config(width=5)
        self.compFields["serial_ID"].widget.config(state="disabled")
        self.btn_lookupSerial = ttk.Button(
            self.f_serial, text="流水號總覽", style="register.TButton",
            command=self.lookupSerial)
        # compound fields
        self.compFields["purchase_date"] = CompoundField(
            parent=self, widgetType="dateframe", description="購置日期",
            fieldName="purchase_date", enabledState="readonly")
        self.compFields["acquire_date"] = CompoundField(
            parent=self, widgetType="dateframe", description="取得日期",
            fieldName="acquire_date", enabledState="readonly")
        # source, price, amount are in the same frame
        self.f_SPA = tk.Frame(self)
        self.compFields["source"] = CompoundField(
            parent=self.f_SPA, widgetType="combobox", description="來源",
            fieldName="source", enabledState="normal")
        self.compFields["source"].widget.config(width=8)
        self.compFields["price"] = CompoundField(
            parent=self.f_SPA, widgetType="entry", description="單價",
            fieldName="price", enabledState="normal")
        self.compFields["price"].widget.config(width=8)
        self.compFields["amount"] = CompoundField(
            parent=self.f_SPA, widgetType="entry", description="數量",
            fieldName="amount", enabledState="normal")
        self.compFields["amount"].widget.config(width=8)
        self.compFields["place"] = CompoundField(
            parent=self, widgetType="combobox", description="存置地點",
            fieldName="place", enabledState="normal")
        self.compFields["keep_year"] = CompoundField(
            parent=self,
            widgetType=None,  # set as none to prevent widget creation
            description="保管年限", fieldName="keep_year",
            enabledState="normal")
        # keep_year widget is a special case(entry with a label)
        # therefore it is defined here
        self.compFields["keep_year"].widgetType = "entry"
        # using an additional base frame,
        # we can still point .widget to tk.Entry
        # (remember to pack/grid/place the frame, not the entry though)
        self.compFields["keep_year"].baseFrame = tk.Frame(self)
        self.compFields["keep_year"].widget = tk.Entry(
            self.compFields["keep_year"].baseFrame,
            textvariable=self.compFields["keep_year"].variable,
            font=_default_font)
        # additional label
        self.compFields["keep_year"].l_y = tk.Label(
            self.compFields["keep_year"].baseFrame, text="年",
            font=_default_font)
        # compound field
        self.compFields["keep_department"] = CompoundField(
            parent=self, widgetType="combobox", description="保管單位",
            fieldName="keep_department", enabledState="normal")
        self.compFields["use_department"] = CompoundField(
            parent=self, widgetType="combobox", description="使用單位",
            fieldName="use_department", enabledState="normal")
        self.compFields["keeper"] = CompoundField(
            parent=self, widgetType="combobox", description="保管人",
            fieldName="keeper", enabledState="normal")
        self.compFields["remark"] = CompoundField(
            parent=self, widgetType="combobox", description="備註事項",
            fieldName="remark", enabledState="normal")
        self.compFields["remark"].widget.config(width=33)
        # bottom right corner
        self.f_bottomright = tk.Frame(self)
        self.btn_search = ttk.Button(
            self.f_bottomright, text='檢索',
            style="register.TButton", command=self.search)
        self.btn_saveThis = ttk.Button(
            self.f_bottomright, text='本筆存入',
            style="register.TButton", command=self.saveThis)
        # seperator
        self.seperator = ttk.Separator(self, orient="horizontal")
        # bottom navigation bar
        self.f_bottomButtons = tk.Frame(self)
        self.btn_quit = ttk.Button(
            self.f_bottomButtons, text='返回',
            style="register.TButton", command=self.quitMe)
        self.btn_next = ttk.Button(
            self.f_bottomButtons, text='下一筆',
            style="register.TButton", command=self.fetchNext)
        self.btn_last = ttk.Button(
            self.f_bottomButtons, text='上一筆',
            style="register.TButton", command=self.fetchLast)
        self.btn_del_this = ttk.Button(
            self.f_bottomButtons, text='刪除本筆',
            style="register.TButton", command=self.deleteThis)
        self.btn_lookup_form = ttk.Button(
            self.f_bottomButtons, text='表單',
            style="register.TButton", command=self.lookupForm)
        self.btn_new_form = ttk.Button(
            self.f_bottomButtons, text='新增一筆',
            style="register.TButton", command=self.newForm)
        return self.compFields

    def createView(self):
        # not shrinking the code for readability
        # gridding
        self.compFields["category"].label.grid(
            row=0, column=0, padx=5, pady=5)
        self.compFields["category"].widget.grid(
            row=0, column=1, padx=5, pady=5)
        self.compFields["subcategory"].label.grid(
            row=0, column=2, padx=5, pady=5)
        self.compFields["subcategory"].widget.grid(
            row=0, column=3, padx=5, pady=5)
        self.compFields["name"].label.grid(row=1, column=0, padx=5, pady=5)
        self.compFields["name"].widget.grid(row=1, column=1, padx=5, pady=5)
        self.compFields["unit"].label.grid(row=1, column=2, padx=5, pady=5)
        self.compFields["unit"].widget.grid(row=1, column=3, padx=5, pady=5)
        self.compFields["brand"].label.grid(row=2, column=0, padx=5, pady=5)
        self.compFields["brand"].widget.grid(row=2, column=1, padx=5, pady=5)
        self.compFields["spec"].label.grid(row=2, column=2, padx=5, pady=5)
        self.compFields["spec"].widget.grid(row=2, column=3, padx=5, pady=5)
        self.compFields["object_ID"].label.grid(
            row=3, column=0, padx=5, pady=5)
        self.compFields["object_ID"].widget.grid(
            row=3, column=1, padx=5, pady=5)
        # serial_ID frame
        self.compFields["serial_ID"].label.pack(side='left', padx=15)
        self.compFields["serial_ID"].widget.pack(side='left', padx=15)
        self.btn_lookupSerial.pack(side='left', padx=15)
        self.f_serial.grid(row=3, column=2, columnspan=2, padx=5, pady=5)
        # continue gridding
        self.compFields["purchase_date"].label.grid(
            row=4, column=0, padx=5, pady=5)
        self.compFields["purchase_date"].widget.grid(
            row=4, column=1, padx=5, pady=5)
        self.compFields["acquire_date"].label.grid(
            row=4, column=2, padx=5, pady=5)
        self.compFields["acquire_date"].widget.grid(
            row=4, column=3, padx=5, pady=5)
        # source price amount(SPA) frame
        self.compFields["source"].label.pack(side='left', padx=10)
        self.compFields["source"].widget.pack(side='left', padx=10)
        self.compFields["price"].label.pack(side='left', padx=10)
        self.compFields["price"].widget.pack(side='left', padx=10)
        self.compFields["amount"].label.pack(side='left', padx=10)
        self.compFields["amount"].widget.pack(side='left', padx=10)
        self.f_SPA.grid(row=5, column=0, columnspan=4, padx=5, pady=5)
        # continue gridding
        self.compFields["place"].label.grid(row=6, column=0, padx=5, pady=5)
        self.compFields["place"].widget.grid(row=6, column=1, padx=5, pady=5)
        # keep_year (grid the base frame)
        self.compFields["keep_year"].widget.pack(side="left")
        self.compFields["keep_year"].l_y.pack(side="left")
        self.compFields["keep_year"].label.grid(
            row=6, column=2, padx=5, pady=5)
        self.compFields["keep_year"].baseFrame.grid(
            row=6, column=3, padx=5, pady=5)
        # continue gridding
        self.compFields["keep_department"].label.grid(
            row=7, column=0, padx=5, pady=5)
        self.compFields["keep_department"].widget.grid(
            row=7, column=1, padx=5, pady=5)
        self.compFields["use_department"].label.grid(
            row=7, column=2, padx=5, pady=5)
        self.compFields["use_department"].widget.grid(
            row=7, column=3, padx=5, pady=5)
        self.compFields["keeper"].label.grid(row=8, column=0, padx=5, pady=5)
        self.compFields["keeper"].widget.grid(row=8, column=1, padx=5, pady=5)
        self.compFields["remark"].label.grid(row=9, column=0, padx=5, pady=5)
        self.compFields["remark"].widget.grid(
            row=9, column=1, padx=5, pady=5, columnspan=2)
        # bottom right corner
        self.btn_search.pack(side="left")
        self.btn_saveThis.pack(side="left")
        self.f_bottomright.grid(row=9, column=3, padx=5, pady=5)
        self.seperator.grid(row=10, columnspan=4, sticky="ew")
        # bottom button frame
        self.btn_quit.pack(side="left")
        self.btn_next.pack(side="left")
        self.btn_last.pack(side="left")
        self.btn_del_this.pack(side="left")
        self.btn_lookup_form.pack(side="left")
        self.btn_new_form.pack(side="left")
        self.f_bottomButtons.grid(
            row=11, column=0, columnspan=4, padx=5, pady=5)

    def getAllRecords(self):
        connect, cursor = _getConnection(_default_database)
        sqlstr = "select * from hvhnonc_in;"
        cursor.execute(sqlstr)
        return cursor.fetchall()

    # Update the whole form and self.state
    def updateByState(self, state: str):
        # Legal states: 'none', 'new', '{}'.format(hvhnonc_in.ID)
        state = state.lower()
        self.state = state
        if state == "none":
            self.title("輸入")
            for i, v in self.compFields.items():
                if (isinstance(v.widget, tk.Entry)
                        or isinstance(v.widget, ttk.Combobox)):
                    v.widget.config(state="disabled")
                if isinstance(v.widget, DateFrame):
                    v.widget.cb_y.config(state="disabled")
                    v.widget.cb_m.config(state="disabled")
                    v.widget.cb_d.config(state="disabled")
            self.clearAllFields()
            return
        elif state == "new":
            self.title("輸入")
            self.initializeAllField()
            self.clearAllFields()
            for i, v in self.compFields.items():
                if (isinstance(v.widget, tk.Entry)
                        or isinstance(v.widget, ttk.Combobox)):
                    v.widget.config(state=v.enabledState)
                if isinstance(v.widget, DateFrame):
                    v.widget.cb_y.config(state=v.enabledState)
                    v.widget.cb_m.config(state=v.enabledState)
                    v.widget.cb_d.config(state=v.enabledState)
                    v.widget.setAsToday()
            return
        # the index mode
        else:
            try:
                self.index = self.lookupIndexInBook(int(state))
                self.title("輸入 ID={}".format(self.index))
            except:
                tk.messagebox.showerror("錯誤", "未知的狀態", parent=self)
                self.updateByState("none")
            if self.index in range(0, len(self.book)):
                for i, v in self.compFields.items():
                    if (isinstance(v.widget, tk.Entry)
                            or isinstance(v.widget, ttk.Combobox)):
                        v.widget.config(state=v.enabledState)
                    if isinstance(v.widget, DateFrame):
                        v.widget.cb_y.config(state=v.enabledState)
                        v.widget.cb_m.config(state=v.enabledState)
                        v.widget.cb_d.config(state=v.enabledState)
                        v.widget.setAsToday()
                self.initializeAllField()
                record = self.book[self.index]
                # set values
                things = ["object_ID", "serial_ID", "category", "subcategory",
                          "name", "brand", "spec", "unit"]
                for i, v in enumerate(things):
                    # skip record[0], it's unique ID
                    self.compFields[v].variable.set(str(record[i + 1]))
                # purchase_date: yyyy-mm-dd
                purchase_date = str(record[9]).split('-')
                purchase_date[0] = str(int(purchase_date[0]) - 1911)
                w = self.compFields["purchase_date"].widget
                w.y.set(purchase_date[0])
                w.m.set(purchase_date[1])
                w.d.set(purchase_date[2])
                w.updateVar()
                # acquire_date: yyyy-mm-dd
                acquire_date = str(record[10]).split('-')
                acquire_date[0] = str(int(acquire_date[0]) - 1911)
                w = self.compFields["acquire_date"].widget
                w.y.set(acquire_date[0])
                w.m.set(acquire_date[1])
                w.d.set(acquire_date[2])
                w.updateVar()
                # set more values
                things = ["price", "amount", "place", "keep_year", "source",
                          "keep_department", "use_department", "keeper", "remark"]
                for i, v in enumerate(things):
                    ii = i + 11
                    self.compFields[v].variable.set(str(record[ii]))

    # returns the index of state in self.book
    def lookupIndexInBook(self, state: int) -> int:
        for i, sublist in enumerate(self.book):
            if int(state) in (sublist[0],):
                return i
        return None

    def clearAllFields(self):
        for i, v in self.compFields.items():
            if (isinstance(v.widget, tk.Entry)
                    or isinstance(v.widget, ttk.Combobox)):
                v.variable.set("")
            if isinstance(v.widget, DateFrame):
                v.widget.y.set("")
                v.widget.m.set("")
                v.widget.d.set("")
                v.widget.updateVar()

    # init all field from the database data
    def initializeAllField(self):
        connect, cursor = _getConnection(_default_database)
        connect.row_factory = lambda cursor, row: row[0]
        sqlstr = "select description from hvhnonc_category;"
        cursor.execute(sqlstr)
        catagories = cursor.fetchall()
        self.compFields["category"].widget.config(values=catagories)
        self.compFields["category"].widget.bind(
            "<<ComboboxSelected>>", self.onCategorySelected)
        self.compFields["subcategory"].widget.bind(
            "<<ComboboxSelected>>", self.onSubcategorySelected)
        self.compFields["name"].widget.bind(
            "<<ComboboxSelected>>", self.onNameSelected)
        sources = ["購置", "撥用", "贈送"]
        self.compFields["source"].widget.config(values=sources)
        sqlstr = ("select change_value "
                  "from hvhnonc_in_cache "
                  "where("
                  "this_ID=0 and "
                  "change_ID=?)"
                  "order by rowid desc limit 30;")
        cursor.execute(sqlstr, (getFieldIDByName("存置地點"), ))
        places = cursor.fetchall()
        self.compFields["place"].widget.config(values=places)
        cursor.execute(sqlstr, (getFieldIDByName("保管單位"), ))
        keep_depts = cursor.fetchall()
        self.compFields["keep_department"].widget.config(values=keep_depts)
        cursor.execute(sqlstr, (getFieldIDByName("使用單位"), ))
        use_depts = cursor.fetchall()
        self.compFields["use_department"].widget.config(values=use_depts)
        cursor.execute(sqlstr, (getFieldIDByName("保管人"), ))
        keepers = cursor.fetchall()
        self.compFields["keeper"].widget.config(values=keepers)
        cursor.execute(sqlstr, (getFieldIDByName("備註事項"), ))
        remarks = cursor.fetchall()
        self.compFields["remark"].widget.config(values=remarks)
        connect.close()

    # callback functions for when the comboboxes are selected
    def onCategorySelected(self, event):
        connect, cursor = _getConnection(_default_database)
        connect.row_factory = lambda cursor, row: row[0]
        sqlstr = ("select description "
                  "from hvhnonc_subcategory "
                  "where parent_ID=("
                  "select ID "
                  "from hvhnonc_category "
                  "where description=?);")
        param = (self.compFields["category"].variable.get(),)
        cursor.execute(sqlstr, param)
        subcatagories = cursor.fetchall()
        connect.close()
        self.compFields["subcategory"].widget.config(values=subcatagories)
        if (len(subcatagories) > 0
                and self.compFields["subcategory"].variable.get()
                != subcatagories[0][0]):
            self.compFields["subcategory"].widget.set(subcatagories[0][0])
            self.onSubcategorySelected(None)

    def onSubcategorySelected(self, event):
        # update product name
        connect, cursor = _getConnection(_default_database)
        connect.row_factory = lambda cursor, row: row[0]
        sqlstr = ("select change_value "
                  "from hvhnonc_in_cache "
                  "where("
                  "this_ID=? and "
                  "this_value=? and "
                  "change_ID=?);")
        params = (getFieldIDByName("物品細目"),
                  self.compFields["subcategory"].variable.get(),
                  getFieldIDByName("物品名稱"))
        cursor.execute(sqlstr, params)
        rows = cursor.fetchall()
        connect.close()
        self.compFields["name"].widget.config(values=rows)
        if (len(rows) > 0
                and self.compFields["name"].variable.get() != rows[0][0]):
            self.compFields["name"].variable.set(rows[0][0])
        self.onNameSelected(None)

    def onNameSelected(self, event):
        # update product name
        connect, cursor = _getConnection(_default_database)
        connect.row_factory = lambda cursor, row: row[0]
        sqlstr = ("select change_value "
                  "from hvhnonc_in_cache "
                  "where ("
                  "this_ID=? and "
                  "this_value=? and "
                  "change_ID=?)"
                  "order by rowid desc limit 30;")
        params = [getFieldIDByName("物品名稱"),
                  self.compFields["name"].variable.get(), ""]
        params[2] = getFieldIDByName("單位")
        cursor.execute(sqlstr, params)
        units = cursor.fetchall()
        self.compFields["unit"].widget.config(values=units)
        if (len(units) > 0
                and self.compFields["unit"].variable.get() != units[0][0]):
            self.compFields["unit"].variable.set(units[0][0])
        params[2] = getFieldIDByName("品牌")
        cursor.execute(sqlstr, params)
        brands = cursor.fetchall()
        self.compFields["brand"].widget.config(values=brands)
        if (len(brands) > 0
                and self.compFields["brand"].variable.get() != brands[0][0]):
            self.compFields["brand"].widget.set(brands[0][0])
        params[2] = getFieldIDByName("規格")
        cursor.execute(sqlstr, params)
        specs = cursor.fetchall()
        self.compFields["spec"].widget.config(values=specs)
        if (len(specs) > 0
                and self.compFields["spec"].variable.get() != specs[0][0]):
            self.compFields["spec"].variable.set(specs[0][0])
        connect.close()

    # Callback of button('流水號總覽')
    def lookupSerial(self):
        # open a toplevel
        self.SerialWindow(self)

    class SerialWindow(tk.Toplevel):
        def __init__(self, parent, *args, **kwargs):
            # treeview styles
            style = ttk.Style()
            style.configure("Treeview", font=_default_font)
            style.configure("Treeview.Heading", font=_default_font)
            # initialization
            tk.Toplevel.__init__(self, parent, *args, **kwargs)
            self.parent = parent
            self.attributes("-topmost", "true")
            self.attributes("-topmost", "false")
            # get serials from db_in
            connect, cursor = _getConnection(_default_database)
            sqlstr = "select count(distinct name) from hvhnonc_in;"
            cursor.execute(sqlstr)
            itemCount = cursor.fetchone()
            self.title("序號: 共{}筆".format(itemCount[0]))
            self.geometry("640x500")
            # get all object_IDs and sqlIDs
            sqlstr = ("select object_ID, name, count(*) "
                      "from hvhnonc_in "
                      "group by object_ID, name "
                      "order by object_ID, serial_ID;")
            cursor.execute(sqlstr)
            data = cursor.fetchall()
            connect.close()
            # make a tree view
            sb = tk.Scrollbar(self)
            tv = ttk.Treeview(self, yscrollcommand=sb.set,
                              columns=('1', '2', '3'), show="headings")
            tv.heading('1', text='編號')
            tv.heading('2', text='品名')
            tv.heading('3', text='數量')
            tv.column('3', anchor="e")
            sb.config(command=tv.yview)
            for d in data:
                tv.insert("", "end", values=d)
            sb.pack(side="right", fill="y")
            tv.pack(fill="both", expand=1)
            # get focus
            self.grab_set()

    # Callback of button('檢索')
    def search(self):
        # open a toplevel
        self.SearchWindow(self)

    class SearchWindow(tk.Toplevel):
        def __init__(self, parent, *args, **kwargs):
            s = ttk.Style()
            s.configure('search.TButton', font=_default_button_font)
            tk.Toplevel.__init__(self, parent, *args, **kwargs)
            self.parent = parent
            # pop to topmost but don't get in the way
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
            connect, cursor = _getConnection(_default_database)
            connect.row_factory = lambda cursor, row: row[0]
            sqlstr = ("select change_value "
                      "from hvhnonc_in_cache "
                      "where change_ID=? "
                      "order by rowid desc limit 30;")
            cursor.execute(sqlstr, (getFieldIDByName("檢索"),))
            rows = cursor.fetchall()
            history = []
            for row in rows:
                history.append(row[0])
            # print(history)
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
            # listen to return key press
            self.bind("<Return>", self.catchReturn)
            # get focus
            self.grab_set()

        # When <Return> key is pressed, treat it like submit
        def catchReturn(self, event):
            self.onSubmitClick()

        def quitMe(self):
            self.destroy()

        # Callback of button('確定')
        def onSubmitClick(self):
            # update search cache
            connect, cursor = _getConnection(_default_database)
            sqlstr = ("replace into hvhnonc_in_cache("
                      "this_ID, this_value, change_ID, change_value) "
                      "values(0, 'none', ?, ?);")
            params = (getFieldIDByName("檢索"), self.parent.query.get())
            cursor.execute(sqlstr, params)
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
                    columns=('1', '2', '3', '4', '5', '6', '7'),
                    show="headings")
                self.tv['displaycolumns'] = ('2', '3', '4', '5', '6', '7')
                self.tv.heading('1', text='ID')
                self.tv.heading('2', text='購置日期')
                self.tv.heading('3', text='取得日期')
                self.tv.heading('4', text='品名')
                self.tv.heading('5', text='存置位置')
                self.tv.heading('6', text='保管人')
                self.tv.heading('7', text='備註')
                sb.config(command=self.tv.yview)
                # Get data
                connect, cursor = _getConnection(_default_database)
                phrase = str(parent.query.get())
                sqlstr = (
                    "select ID, purchase_date, acquire_date, name, place, "
                    "keeper, remark "
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
                    "order by acquire_date desc;")
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
                item = self.tv.identify('item', event.x, event.y)
                # print("you clicked on", self.tv.item(item,"values")[0])
                self.parent.state = str(self.tv.item(item, "values")[0])
                self.parent.updateByState(self.parent.state)
                self.destroy()

    def updateCache(self, sqlstr, thisName, thatName):
        connect, cursor = _getConnection(_default_database)
        # connect.set_trace_callback(print)
        # Update cache table
        # So next time when thisName is fed,
        # autocomplete thatName

        # get the value from thisName
        if thisName not in ('無',):
            thisCF = None
            for k, cf in self.compFields.items():
                if cf.description == thisName:
                    thisCF = cf
                    break
            thisVal = thisCF.variable.get()
        else:
            thisVal = "none"
        # get the value from thatName
        thatCF = None
        for k, cf in self.compFields.items():
            if cf.description == thatName:
                thatCF = cf
                break
        thatVal = thatCF.variable.get()
        if thatVal.strip() in (None, ""):
            return
        # construct parameters
        params = [getFieldIDByName(thisName), thisVal,
                  getFieldIDByName(thatName), thatVal]
        try:
            cursor.execute(sqlstr, params)
            connect.commit()
        except Exception as e:
            print("Exception in updateCache: %s" % e)
            tk.messagebox.showerror("錯誤 updateCache", str(e),
                                    parent=self)

    def updateAllCache(self, sqlstr):
        # the getFieldIDByName is called inside updateCache
        self.updateCache(sqlstr, "物品細目", "物品名稱")
        self.updateCache(sqlstr, "物品名稱", "單位")
        self.updateCache(sqlstr, "物品名稱", "品牌")
        self.updateCache(sqlstr, "物品名稱", "規格")
        self.updateCache(sqlstr, "無", "存置地點")
        self.updateCache(sqlstr, "無", "保管單位")
        self.updateCache(sqlstr, "無", "使用單位")
        self.updateCache(sqlstr, "無", "保管人")
        self.updateCache(sqlstr, "無", "備註事項")

    # Callback of button('本筆存入')
    def saveThis(self):
        connect, cursor = _getConnection(_default_database)
        connect.set_trace_callback(print)
        # check for valid values:
        # category: not null
        if not self.compFields["category"].variable.get():
            messagebox.showerror("錯誤", "物品大項未填", parent=self)
            return
        # subcategory: not null
        if not self.compFields["subcategory"].variable.get():
            messagebox.showerror("錯誤", "物品細目未填", parent=self)
            return
        # name: not null
        if not self.compFields["name"].variable.get():
            messagebox.showerror("錯誤", "物品名稱未填", parent=self)
            return
        # purchase_date: not null
        if not self.compFields["purchase_date"].variable.get():
            messagebox.showerror("錯誤", "購置日期未填或未填滿", parent=self)
            return
        # acquire_date: not null
        if not self.compFields["acquire_date"].variable.get():
            messagebox.showerror("錯誤", "取得日期未填或未填滿", parent=self)
            return
        # price: int not null
        if not self.compFields["price"].variable.get():
            messagebox.showerror("錯誤", "單價未填", parent=self)
            return
        try:
            int(self.compFields["price"].variable.get())
        except ValueError:
            messagebox.showerror("錯誤", "單價只能為數字", parent=self)
            return
        # amount: int not null >0
        if not self.compFields["amount"].variable.get():
            messagebox.showerror("錯誤", "數量未填", parent=self)
            return
        try:
            if int(self.compFields["amount"].variable.get()) <= 0:
                messagebox.showerror("錯誤", "數量僅能為正數", parent=self)
                return
        except ValueError:
            messagebox.showerror("錯誤", "數量只能為數字", parent=self)
            return
        # place: not null
        if not self.compFields["place"].variable.get():
            messagebox.showerror("錯誤", "存置地點未填", parent=self)
            return
        # keep_year: int not null >0
        if not self.compFields["keep_year"].variable.get():
            messagebox.showerror("錯誤", "保管年限未填", parent=self)
            return
        try:
            if int(self.compFields["keep_year"].variable.get()) <= 0:
                messagebox.showerror("錯誤", "保管年限僅能為正數",
                                     parent=self)
                return
        except ValueError:
            messagebox.showerror("錯誤", "保管年限只能為數字", parent=self)
            return
        # source: in ("購置", "贈送", "撥用")
        if self.compFields["source"].variable.get() not in (
                "購置", "贈送", "撥用"):
            messagebox.showerror("錯誤", "來源只能為'購置', '贈送', '撥用'",
                                 parent=self)
            return
        # keep_department: not null
        if not self.compFields["keep_department"].variable.get():
            messagebox.showerror("錯誤", "保管單位未填", parent=self)
            return
        # object_ID, serial_ID
        # object_ID is '6-(ID_cat)-(ID_subcat)'
        sqlstr = ("select parent_ID, ID "
                  "from hvhnonc_subcategory "
                  "where parent_ID=("
                  "select ID "
                  "from hvhnonc_category "
                  "where description=?) "
                  "and description=?;")
        category = self.compFields["category"].variable.get()
        subcategory = self.compFields["subcategory"].variable.get()
        params = (category, subcategory)
        try:
            cursor.execute(sqlstr, params)
            row = cursor.fetchone()
            object_ID = ("6",
                         "{:02d}".format(int(row[0])),
                         "{:02d}".format(int(row[1])))
        except Exception as e:
            print("Exception in saveThis: %s" % e)
            tk.messagebox.showerror("錯誤1", str(e), parent=self)
        object_ID = " - ".join(object_ID)
        sqlstr = ("select serial_ID "
                  "from hvhnonc_in "
                  "where object_ID=? and name=?;")
        name = self.compFields["name"].variable.get()
        params = (object_ID, name)
        try:
            cursor.execute(sqlstr, params)
        except Exception as e:
            print("Exception in saveThis: %s" % e)
            tk.messagebox.showerror("錯誤2", str(e), parent=self)
        row = cursor.fetchone()
        if row in (None,):
            sqlstr = ("select count(distinct serial_ID) "
                      "from hvhnonc_in "
                      "where object_ID=?;")
            try:
                cursor.execute(sqlstr, (params[0],))
                row = cursor.fetchone()
                serialID = "{:03}".format(int(row[0]) + 1)
            except Exception as e:
                print("Exception in saveThis: %s" % e)
                tk.messagebox.showerror("錯誤3", str(e), parent=self)
        else:
            serialID = str(row[0])
        # date string preparation
        purchase_date = self.compFields["purchase_date"].variable.get()
        year = int(purchase_date.split("-")[0])
        if year < 1911:
            purchase_date = purchase_date.replace(str(year), str(year + 1911))
        acquire_date = self.compFields["acquire_date"].variable.get()
        year = int(acquire_date.split("-")[0])
        if year < 1911:
            acquire_date = acquire_date.replace(str(year), str(year + 1911))
        # insert new row
        if self.state in ("new",):
            # insertion statement
            sqlstr = ("insert into hvhnonc_in("
                      "object_ID, serial_ID, category, subcategory, "
                      "name, brand, spec, unit, purchase_date, acquire_date, "
                      "price, amount, place, keep_year, source, "
                      "keep_department, use_department, keeper, "
                      "remark) "
                      "values({});")
            params = (str(object_ID), str(serialID),
                      category, subcategory, name,
                      self.compFields["brand"].variable.get(),
                      self.compFields["spec"].variable.get(),
                      self.compFields["unit"].variable.get(),
                      purchase_date, acquire_date,
                      self.compFields["price"].variable.get(),
                      self.compFields["amount"].variable.get(),
                      self.compFields["place"].variable.get(),
                      self.compFields["keep_year"].variable.get(),
                      self.compFields["source"].variable.get(),
                      self.compFields["keep_department"].variable.get(),
                      self.compFields["use_department"].variable.get(),
                      self.compFields["keeper"].variable.get(),
                      self.compFields["remark"].variable.get())
            sqlstr = sqlstr.format("?, " * (len(params) - 1) + "?")
            try:
                cursor.execute(sqlstr, params)
                connect.commit()
                tk.messagebox.showinfo("新增成功", "已新增一筆資料",
                                       parent=self)
            except Exception as e:
                print("Exception in saveThis: %s" % e)
                tk.messagebox.showerror("錯誤4", str(e), parent=self)
            # update cache table
            sqlstr = ("insert or ignore into "
                      "hvhnonc_in_cache("
                      "this_ID, this_value, change_ID, change_value) "
                      "values(?, ?, ?, ?);")
            self.updateAllCache(sqlstr)
            # update book
            self.book = self.getAllRecords()
            self.updateByState("none")
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
                          "purchase_date, acquire_date, "
                          "price, amount, place, "
                          "keep_year, source, "
                          "keep_department, use_department, "
                          "keeper, remark) "
                          "values({});")
                params = (self.state, str(object_ID), str(serialID),
                          category, subcategory, name,
                          self.compFields["brand"].variable.get(),
                          self.compFields["spec"].variable.get(),
                          self.compFields["unit"].variable.get(),
                          purchase_date, acquire_date,
                          self.compFields["price"].variable.get(),
                          self.compFields["amount"].variable.get(),
                          self.compFields["place"].variable.get(),
                          self.compFields["keep_year"].variable.get(),
                          self.compFields["source"].variable.get(),
                          self.compFields["keep_department"].variable.get(),
                          self.compFields["use_department"].variable.get(),
                          self.compFields["keeper"].variable.get(),
                          self.compFields["remark"].variable.get())
                sqlstr = sqlstr.format("?, " * (len(params) - 1) + "?")
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
                          "values(?, ?, ?, ?);")
                self.updateAllCache(sqlstr)
                # update book
                self.book = self.getAllRecords()
                self.updateByState("none")
            elif isWriteover is False:
                # insert new row
                sqlstr = ("insert into hvhnonc_in("
                          "object_ID, serial_ID, "
                          "category, subcategory, "
                          "name, brand, spec, unit, "
                          "purchase_date, acquire_date, "
                          "price, amount, place, "
                          "keep_year, source, "
                          "keep_department, use_department, "
                          "keeper, remark) "
                          "values({});")
                params = (str(object_ID), str(serialID),
                          category, subcategory, name,
                          self.compFields["brand"].variable.get(),
                          self.compFields["spec"].variable.get(),
                          self.compFields["unit"].variable.get(),
                          purchase_date, acquire_date,
                          self.compFields["price"].variable.get(),
                          self.compFields["amount"].variable.get(),
                          self.compFields["place"].variable.get(),
                          self.compFields["keep_year"].variable.get(),
                          self.compFields["source"].variable.get(),
                          self.compFields["keep_department"].variable.get(),
                          self.compFields["use_department"].variable.get(),
                          self.compFields["keeper"].variable.get(),
                          self.compFields["remark"].variable.get())
                sqlstr = sqlstr.format("?, " * (len(params) - 1) + "?")
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
                          "values(?, ?, ?, ?);")
                self.updateAllCache(sqlstr)
                self.book = self.getAllRecords()
                self.state = "none"
                self.updateByState(self.state)
            # do nothing if cancel is pressed
        connect.close()

    # Callback of button('下一筆')
    def fetchNext(self):
        if self.state in ("none", "new"):
            self.index = 0
            self.state = str(self.book[self.index][0])
            self.updateByState(self.state)
        else:
            if self.index == len(self.book) - 1:
                tk.messagebox.showinfo("到底了", "已到達最後一筆",
                                       parent=self)
            else:
                self.index = self.index + 1
                self.state = str(self.book[self.index][0])
                self.updateByState(self.state)

    # Callback of button('上一筆')
    def fetchLast(self):
        if self.state in ("none", "new"):
            self.index = len(self.book) - 1
            self.state = str(self.book[self.index][0])
            self.updateByState(self.state)
        else:
            if self.index == 0:
                tk.messagebox.showinfo("到頂了", "已到達第一筆",
                                       parent=self)
            else:
                self.index = self.index - 1
                self.updateByState(str(self.book[self.index][0]))

    # Callback of button('刪除本筆')
    def deleteThis(self):
        name = self.compFields.get("name").variable.get()
        confirmDelete = messagebox.askokcancel(
            "確定刪除?", "你確定要刪除這筆資料嗎?\n名稱:{}".format(name))
        if not confirmDelete:
            return
        # deletes the row if it's in the book
        # print("deleteThis")
        if self.state in ("new", "none", ):
            tk.messagebox.showerror("錯誤", "不是資料庫內的資料", parent=self)
            self.updateByState("none")
            return
        connect, cursor = _getConnection(_default_database)
        sqlstr = "delete from hvhnonc_in where ID=?;"
        param = (self.state, )
        try:
            cursor.execute(sqlstr, param)
            connect.commit()
            tk.messagebox.showinfo("刪除成功",
                                   "已刪除一筆ID:{}, 名稱:{}的資料".format(
                                       self.state, name),
                                   parent=self)
            # update the book
            self.book = self.getAllRecords()
        except sqlite3.Error as e:
            tk.messagebox.showerror("錯誤", "沒有這筆資料", parent=self)
            print(e.args[0])
        self.updateByState("none")

    # Callback of button('表單')
    def lookupForm(self):
        # print("lookupForm")
        # opens a new toplevel for filtering
        self.FilterWindow(self)

    class FilterWindow(tk.Toplevel):
        def __init__(self, parent, *args, **kwargs):
            tk.Toplevel.__init__(self, parent, *args, **kwargs)
            self.parent = parent
            self.title("請輸入要篩選的範圍")
            self.geometry("665x290")
            self.create_widgets()
            self.create_view()
            self.resizable(False, False)
            self.init_form()
            # listen to enter key
            self.bind("<Return>", self.catchReturn)
            # get focus
            self.attributes("-topmost", "true")
            self.attributes("-topmost", "false")
            self.grab_set()

        def create_widgets(self) -> Dict[str, CompoundField]:
            self.compFields = {}
            self.compFields["category"] = CompoundField(
                parent=self, widgetType="combobox",
                description="物品大項", fieldName="category",
                enabledState="readonly")
            self.compFields["subcategory"] = CompoundField(
                parent=self, widgetType="combobox",
                description="物品細目", fieldName="subcategory",
                enabledState="readonly")
            self.compFields["name"] = CompoundField(
                parent=self, widgetType="combobox",
                description="物品名稱", fieldName="name",
                enabledState="normal")
            self.compFields["brand"] = CompoundField(
                parent=self, widgetType="combobox",
                description="品牌", fieldName="brand",
                enabledState="normal")
            self.compFields["spec"] = CompoundField(
                parent=self, widgetType="combobox",
                description="規格", fieldName="spec",
                enabledState="normal")
            self.compFields["price"] = CompoundField(
                parent=self, widgetType="entry",
                description="單價", fieldName="price",
                enabledState="normal", span=True)
            self.compFields["price"].widget.min.config(width=5)
            self.compFields["price"].widget.max.config(width=5)
            self.compFields["purchase_date"] = CompoundField(
                parent=self, widgetType="dateframe",
                description="購置日期", fieldName="purchase_date",
                enabledState="readonly", span=True)
            self.compFields["acquire_date"] = CompoundField(
                parent=self, widgetType="dateframe",
                description="取得日期", fieldName="acquire_date",
                enabledState="readonly", span=True)
            self.compFields["keep_department"] = CompoundField(
                parent=self, widgetType="combobox",
                description="保管單位", fieldName="keep_department",
                enabledState="normal")
            self.compFields["place"] = CompoundField(
                parent=self, widgetType="combobox",
                description="存置地點", fieldName="place",
                enabledState="normal")
            self.compFields["use_department"] = CompoundField(
                parent=self, widgetType="combobox",
                description="使用單位", fieldName="use_department",
                enabledState="normal")
            self.compFields["keeper"] = CompoundField(
                parent=self, widgetType="combobox",
                description="保管人", fieldName="keeper",
                enabledState="normal")
            # bottom navigate bar
            self.f_bottomButtons = tk.Frame(self)
            self.btn_quit = ttk.Button(
                self.f_bottomButtons, text='返回',
                style="register.TButton", command=self.quitMe)
            self.btn_next = ttk.Button(
                self.f_bottomButtons, text='確定',
                style="register.TButton", command=self.submit)
            return self.compFields

        def create_view(self):
            self.compFields["category"].label.grid(
                row=0, column=0, padx=5, pady=5)
            self.compFields["category"].widget.grid(
                row=0, column=1, padx=5, pady=5)
            self.compFields["subcategory"].label.grid(
                row=0, column=2, padx=5, pady=5)
            self.compFields["subcategory"].widget.grid(
                row=0, column=3, padx=5, pady=5)
            self.compFields["name"].label.grid(
                row=1, column=0, padx=5, pady=5)
            self.compFields["name"].widget.grid(
                row=1, column=1, padx=5, pady=5)
            self.compFields["brand"].label.grid(
                row=1, column=2, padx=5, pady=5)
            self.compFields["brand"].widget.grid(
                row=1, column=3, padx=5, pady=5)
            self.compFields["spec"].label.grid(
                row=2, column=0, padx=5, pady=5)
            self.compFields["spec"].widget.grid(
                row=2, column=1, padx=5, pady=5)
            self.compFields["price"].label.grid(
                row=2, column=2, padx=5, pady=5)
            self.compFields["price"].widget.grid(
                row=2, column=3, padx=5, pady=5, sticky=tk.W)
            self.compFields["purchase_date"].label.grid(
                row=3, column=0, padx=5, pady=5)
            self.compFields["purchase_date"].widget.grid(
                row=3, column=1, padx=5, pady=5,
                columnspan=3, sticky=tk.W)
            self.compFields["acquire_date"].label.grid(
                row=4, column=0, padx=5, pady=5)
            self.compFields["acquire_date"].widget.grid(
                row=4, column=1, padx=5, pady=5,
                columnspan=3, sticky=tk.W)
            self.compFields["keep_department"].label.grid(
                row=5, column=0, padx=5, pady=5)
            self.compFields["keep_department"].widget.grid(
                row=5, column=1, padx=5, pady=5)
            self.compFields["place"].label.grid(
                row=5, column=2, padx=5, pady=5)
            self.compFields["place"].widget.grid(
                row=5, column=3, padx=5, pady=5)
            self.compFields["use_department"].label.grid(
                row=6, column=0, padx=5, pady=5)
            self.compFields["use_department"].widget.grid(
                row=6, column=1, padx=5, pady=5)
            self.compFields["keeper"].label.grid(
                row=6, column=2, padx=5, pady=5)
            self.compFields["keeper"].widget.grid(
                row=6, column=3, padx=5, pady=5)
            # Packing bottom row buttons
            self.btn_quit.pack(side="left")
            self.btn_next.pack(side="left")
            self.f_bottomButtons.grid(
                row=7, column=2, padx=5, pady=5,
                columnspan=2, sticky=tk.E)

        # Treat return key as submission
        def catchReturn(self, event):
            self.submit()

        # Initialize the lookup form with data from hvhnonc database
        def init_form(self):
            connect, cursor = _getConnection(_default_database)
            # 物品大項
            sqlstr = "select description from hvhnonc_category;"
            cursor.execute(sqlstr)
            row = cursor.fetchall()
            categories = []
            for item in row:
                categories.append(item[0])
            self.compFields["category"].widget.config(values=categories)
            # subcategory, name, brand, and spec
            # are initialized with onCategorySelected()
            self.compFields["category"].widget.bind(
                "<<ComboboxSelected>>", self.onCategorySelected)
            # clear dates
            self.compFields["purchase_date"].widget.min.clear()
            self.compFields["purchase_date"].widget.max.clear()
            self.compFields["acquire_date"].widget.min.clear()
            self.compFields["acquire_date"].widget.max.clear()
            # template
            sqlstr = ("select change_value from hvhnonc_in_cache "
                      "where this_ID=0 and change_ID=?"
                      "order by rowid desc limit 30;")
            # 保管單位
            cursor.execute(sqlstr, (getFieldIDByName("保管單位"),))
            row = cursor.fetchall()
            depts = []
            for item in row:
                depts.append(item[0])
            self.compFields["keep_department"].widget.config(values=depts)
            # 存置地點
            cursor.execute(sqlstr, (getFieldIDByName("存置地點"),))
            row = cursor.fetchall()
            places = []
            for item in row:
                places.append(item[0])
            self.compFields["place"].widget.config(values=places)
            # 使用單位
            cursor.execute(sqlstr, (getFieldIDByName("使用單位"),))
            row = cursor.fetchall()
            depts = []
            for item in row:
                depts.append(item[0])
            self.compFields["use_department"].widget.config(values=depts)
            # 保管人
            cursor.execute(sqlstr, (getFieldIDByName("保管人"),))
            row = cursor.fetchall()
            keepers = []
            for item in row:
                keepers.append(item[0])
            self.compFields["keeper"].widget.config(values=keepers)

        def onCategorySelected(self, event):
            # update subcategory
            connect, cursor = _getConnection(_default_database)
            sqlstr = ("select description "
                      "from hvhnonc_subcategory "
                      "where parent_ID=("
                      "select ID "
                      "from hvhnonc_category "
                      "where description=?);")
            param = (self.compFields["category"].variable.get(),)
            cursor.execute(sqlstr, param)
            rows = cursor.fetchall()
            subcats = []
            for row in rows:
                subcats.append(row[0])
            self.compFields["subcategory"].widget.config(values=subcats)
            self.compFields["subcategory"].widget.bind(
                "<<ComboboxSelected>>", self.onSubcategorySelected)
            if (len(subcats) > 0
                    and self.compFields["subcategory"].variable.get()
                    != subcats[0]):
                self.compFields["subcategory"].widget.set(subcats[0])
            self.onSubcategorySelected(None)
            connect.close()

        def onSubcategorySelected(self, event):
            # update product name
            connect, cursor = _getConnection(_default_database)
            # get all item name in the same subcategory from cache
            sqlstr = ("select change_value "
                      "from hvhnonc_in_cache "
                      "where(this_ID=? "
                      "and this_value=? "
                      "and change_ID=?) "
                      "order by rowid desc limit 30;")
            params = (str(getFieldIDByName('物品細目')),
                      self.compFields["subcategory"].variable.get(),
                      str(getFieldIDByName('物品名稱')),)
            cursor.execute(sqlstr, params)
            names = cursor.fetchall()
            connect.close()
            self.compFields["name"].widget.config(values=names)
            if (len(names) > 0
                    and self.compFields["name"].variable.get()
                    != names[0]):
                self.compFields["name"].widget.set(names[0])
            self.onNameSelected(None)

        def onNameSelected(self, event):
            # update spec and unit
            connect, cursor = _getConnection(_default_database)
            # get all item name in the same subcategory from cache
            sqlstr = ("select change_value "
                      "from hvhnonc_in_cache "
                      "where("
                      "this_ID=? "
                      "and this_value=? "
                      "and change_ID=?) "
                      "order by rowid desc limit 30;")
            # 品牌
            params = (str(getFieldIDByName('物品名稱')),
                      self.compFields["name"].variable.get(),
                      str(getFieldIDByName('品牌')),)
            cursor.execute(sqlstr, params)
            brands = []
            rows = cursor.fetchall()
            for row in rows:
                brands.append(row[0])
            self.compFields["brand"].widget.config(values=brands)
            if (len(brands) > 0 and
                    self.compFields["brand"].variable.get() != brands[0]):
                self.compFields["brand"].variable.set(brands[0])
            # 規格
            params = (str(getFieldIDByName('物品名稱')),
                      self.compFields["name"].variable.get(),
                      str(getFieldIDByName('規格')),)
            cursor.execute(sqlstr, params)
            rows = cursor.fetchall()
            specs = []
            for row in rows:
                specs.append(row[0])
            self.compFields["spec"].widget.config(values=specs)
            if (len(specs) > 0 and
                    self.compFields["spec"].variable.get() != specs[0]):
                self.compFields["spec"].variable.set(specs[0])
            connect.close()

        def quitMe(self):
            self.destroy()

        def submit(self):
            # open a result toplevel
            sqlstr = ("insert or ignore into "
                      "hvhnonc_in_cache("
                      "this_ID, this_value, change_ID, change_value) "
                      "values(?, ?, ?, ?);")
            self.updateAllCache(sqlstr)
            self.LookupResult(self)

        def updateAllCache(self, sqlstr=None):
            if not sqlstr:
                sqlstr = ("insert or ignore into "
                          "hvhnonc_in_cache("
                          "this_ID, this_value, change_ID, change_value) "
                          "values(?, ?, ?, ?);")
            # the getFieldIDByName is called inside updateCache
            self.updateCache(sqlstr, "物品細目", "物品名稱")
            self.updateCache(sqlstr, "物品名稱", "品牌")
            self.updateCache(sqlstr, "物品名稱", "規格")
            self.updateCache(sqlstr, "無", "保管單位")
            self.updateCache(sqlstr, "無", "使用單位")
            self.updateCache(sqlstr, "無", "存置地點")
            self.updateCache(sqlstr, "無", "保管人")

            # Update cache table
            # So next time when thisName is fed,
            # autocomplete thatName
        def updateCache(self, sqlstr, thisName, thatName):
            if not sqlstr:
                sqlstr = ("insert or ignore into "
                          "hvhnonc_in_cache("
                          "this_ID, this_value, change_ID, change_value) "
                          "values(?, ?, ?, ?);")
            connect, cursor = _getConnection(_default_database)
            # connect.set_trace_callback(print)
            # get the value from thisName
            if thisName not in ('無',):
                thisCF = None
                for k, cf in self.compFields.items():
                    if cf.description == thisName:
                        thisCF = cf
                        break
                thisVal = thisCF.variable.get()
            else:
                thisVal = "none"
            # get the value from thatName
            thatCF = None
            for k, cf in self.compFields.items():
                if cf.description == thatName:
                    thatCF = cf
                    break
            thatVal = thatCF.variable.get()
            if thatVal.strip() in (None, ""):
                return
            # construct parameters
            params = [getFieldIDByName(thisName), thisVal,
                      getFieldIDByName(thatName), thatVal]
            try:
                cursor.execute(sqlstr, params)
                connect.commit()
            except Exception as e:
                print("Exception in updateCache: %s" % e)
                tk.messagebox.showerror("錯誤 updateCache", str(e),
                                        parent=self)

        class LookupResult(tk.Toplevel):
            # basically it's a search result toplevel
            def __init__(self, parent, *args, **kwargs):
                # treeview styles
                style = ttk.Style()
                style.configure("Treeview", font=_default_font)
                style.configure("Treeview.Heading", font=_default_font)
                # initialization
                tk.Toplevel.__init__(self, parent, *args, **kwargs)
                self.parent = parent
                self.attributes("-topmost", "true")
                self.attributes("-topmost", "false")
                self.title("篩選結果")
                self.geometry("1200x600")
                self.resizable(True, True)
                # retrieve the dictionary
                compFields = parent.compFields
                # make a tree view
                sb = tk.Scrollbar(self)
                self.tv = ttk.Treeview(
                    self, yscrollcommand=sb.set,
                    columns=('1', '2', '3', '4', '5', '6', '7'),
                    show="headings")
                self.tv['displaycolumns'] = ('2', '3', '4', '5', '6', '7')
                self.tv.heading('1', text='ID')
                self.tv.heading('2', text='購置日期')
                self.tv.heading('3', text='取得日期')
                self.tv.heading('4', text='品名')
                self.tv.heading('5', text='存置位置')
                self.tv.heading('6', text='保管人')
                self.tv.heading('7', text='備註')
                sb.config(command=self.tv.yview)
                # fetch the data
                connect, cursor = _getConnection(_default_database)
                # connect.set_trace_callback(print)
                params = []
                sqlstr = ("select ID, purchase_date, acquire_date, name, "
                          "place, keeper, remark "
                          "from hvhnonc_in "
                          "where (")
                for key, cf in compFields.items():
                    try:  # Special cases: ranged data
                        values = {
                            "min": cf.variable["min"].get(),
                            "max": cf.variable["max"].get()}
                        if not (values["min"] or values["max"]):
                            continue
                        if "date" in cf.fieldName:
                            # handle empty date
                            if values["min"] in ("--", ""):
                                values["min"] = "1911-01-01"
                            if values["max"] in ("--", ""):
                                values["max"] = str(dt.datetime.now().date())
                            # handle empty month and day
                            values["min"] = values["min"].replace("--", "-01-")
                            if values["min"][-1] == "-":
                                values["min"] += "01"
                            values["max"] = values["max"].replace("--", "-12-")
                            if values["max"][-1] == "-":
                                values["max"] += "31"
                            # convert republic year to western year
                            year = int(values["min"].split('-')[0])
                            if year < 1911:
                                values["min"] = values["min"].replace(
                                    str(year), str(year + 1911))
                            year = int(values["max"].split('-')[0])
                            if year < 1911:
                                values["max"] = values["max"].replace(
                                    str(year), str(year + 1911))
                            # sql
                            sqlstr += ("(strftime('%Y-%m-%d', {}) "
                                       "between ? and ?) and ".format(
                                           cf.fieldName))
                            params.append(values["min"])
                            params.append(values["max"])
                        if "price" in cf.fieldName:
                            if (values["min"] and values["max"]):
                                sqlstr += ("({0} >= ? and "
                                           "{0} <= ?) and ".format(
                                               cf.fieldName))
                                params.append(values["min"], values["max"])
                            elif values["min"]:
                                sqlstr += "({} >= ?) and ".format(cf.fieldName)
                                params.append(values["min"])
                            elif values["max"]:
                                sqlstr += "({} <= ?) and ".format(cf.fieldName)
                                params.append(values["max"])
                            pass
                    except TypeError:
                        value = cf.variable.get()
                        if not value:
                            continue
                        sqlstr += "{} like ? and ".format(cf.fieldName)
                        params.append("%{}%".format(value))
                # where(1) if no input
                sqlstr += "1) order by acquire_date desc;"
                # print(sqlstr)
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
                item = self.tv.identify('item', event.x, event.y)
                # print("you clicked on", self.tv.item(item, "values")[0])
                self.parent.parent.state = str(
                    self.tv.item(item, "values")[0])
                self.parent.parent.updateByState(
                    self.parent.parent.state)
                self.parent.destroy()

            def abortLookup(self):
                self.parent.destroy()

    def newForm(self):
        self.updateByState('new')

    def quitMe(self):
        self.destroy()


class Unregister(tk.Toplevel):
    def __init__(self, parent, *args, **kwargs):
        # for update purposes
        self.state = "sleep"
        self.book = self.getAllIDs("hvhnonc_out")
        self.index = 0
        self.inID = 0
        # styles
        s = ttk.Style()
        s.configure('unregister.TButton', font=_default_button_font)
        tk.Toplevel.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.title("除帳")
        self.geometry("665x515")
        self.resizable(False, False)
        # Four main frames in the GUI
        self.f_mainForm = tk.Frame(self)
        self.f_historyForm = tk.Frame(self)
        self.f_unregisterForm = tk.Frame(self)
        self.f_bottomNavigationBar = tk.Frame(self)
        # A dictionary that records all the comp fields in Register
        self.compFields = {}
        # main form
        # category(combobox), subcategory(combobox)
        self.compFields["category"] = CompoundField(
            parent=self.f_mainForm,
            widgetType="combobox",
            fieldName="category",
            enabledState="readonly",
            description="物品大項")
        self.compFields["subcategory"] = CompoundField(
            parent=self.f_mainForm,
            widgetType="combobox",
            fieldName="subcategory",
            enabledState="readonly",
            description="物品細目")
        self.compFields["category"].label.grid(row=0, column=0,
                                               padx=5, pady=5)
        self.compFields["category"].widget.grid(row=0, column=1,
                                                padx=5, pady=5)
        self.compFields["subcategory"].label.grid(row=0, column=2,
                                                  padx=5, pady=5)
        self.compFields["subcategory"].widget.grid(row=0, column=3,
                                                   padx=5, pady=5)
        # name(combobox), unit(combobox)
        self.compFields["name"] = CompoundField(
            parent=self.f_mainForm,
            widgetType="combobox",
            fieldName="name",
            enabledState="normal",
            description="物品名稱")
        self.compFields["unit"] = CompoundField(
            parent=self.f_mainForm,
            widgetType="combobox",
            fieldName="unit",
            enabledState="normal",
            description="單位")
        self.compFields["name"].label.grid(row=1, column=0, padx=5, pady=5)
        self.compFields["name"].widget.grid(row=1, column=1, padx=5, pady=5)
        self.compFields["unit"].label.grid(row=1, column=2, padx=5, pady=5)
        self.compFields["unit"].widget.grid(row=1, column=3, padx=5, pady=5)
        # brand(combobox), spec(combobox)
        self.compFields["brand"] = CompoundField(
            parent=self.f_mainForm,
            widgetType="combobox",
            fieldName="brand",
            enabledState="normal",
            description="品牌")
        self.compFields["spec"] = CompoundField(
            parent=self.f_mainForm,
            widgetType="combobox",
            fieldName="spec",
            enabledState="normal",
            description="規格")
        self.compFields["brand"].label.grid(row=2, column=0, padx=5, pady=5)
        self.compFields["brand"].widget.grid(row=2, column=1, padx=5, pady=5)
        self.compFields["spec"].label.grid(row=2, column=2, padx=5, pady=5)
        self.compFields["spec"].widget.grid(row=2, column=3, padx=5, pady=5)
        # object_ID(entry), serial_ID(entry)
        self.compFields["object_ID"] = CompoundField(
            parent=self.f_mainForm,
            widgetType="entry",
            fieldName="object_ID",
            enabledState="disabled",
            description="物品編號")
        self.compFields["serial_ID"] = CompoundField(
            parent=self.f_mainForm,
            widgetType="entry",
            fieldName="serial_ID",
            enabledState="disabled",
            description="流水號")
        self.compFields["object_ID"].label.grid(
            row=3, column=0, padx=5, pady=5)
        self.compFields["object_ID"].widget.grid(
            row=3, column=1, padx=5, pady=5)
        self.compFields["serial_ID"].label.grid(
            row=3, column=2, padx=5, pady=5)
        self.compFields["serial_ID"].widget.grid(
            row=3, column=3, padx=5, pady=5)
        # acquire_date(dateframe), keepYear(entry)
        self.compFields["purchase_date"] = CompoundField(
            parent=self.f_mainForm,
            widgetType="dateframe",
            fieldName="purchase_date",
            enabledState="readonly",
            description="取得日期")
        self.compFields["keep_year"] = CompoundField(
            parent=self.f_mainForm,
            widgetType="entry",
            fieldName="keep_year",
            enabledState="normal",
            description="保存年限")
        self.compFields["purchase_date"].label.grid(row=4, column=0,
                                                    padx=5, pady=5)
        self.compFields["purchase_date"].widget.grid(row=4, column=1,
                                                     padx=5, pady=5)
        self.compFields["keep_year"].label.grid(row=4, column=2,
                                                padx=5, pady=5)
        self.compFields["keep_year"].widget.grid(row=4, column=3,
                                                 padx=5, pady=5)
        # price(entry), amount(entry)
        self.compFields["price"] = CompoundField(
            parent=self.f_mainForm,
            widgetType="entry",
            fieldName="price",
            enabledState="normal",
            description="單價")
        self.compFields["amount"] = CompoundField(
            parent=self.f_mainForm,
            widgetType="entry",
            fieldName="amount",
            enabledState="normal",
            description="數量")
        self.compFields["price"].label.grid(row=5, column=0, padx=5, pady=5)
        self.compFields["price"].widget.grid(row=5, column=1, padx=5, pady=5)
        self.compFields["amount"].label.grid(row=5, column=2, padx=5, pady=5)
        self.compFields["amount"].widget.grid(row=5, column=3, padx=5, pady=5)
        # keepDept(combobox), place(combobox)
        self.compFields["keep_department"] = CompoundField(
            parent=self.f_mainForm,
            widgetType="combobox",
            fieldName="keep_department",
            enabledState="normal",
            description="保管單位")
        self.compFields["place"] = CompoundField(
            parent=self.f_mainForm,
            widgetType="combobox",
            fieldName="place",
            enabledState="normal",
            description="存置地點")
        self.compFields["keep_department"].label.grid(row=6, column=0,
                                                      padx=5, pady=5)
        self.compFields["keep_department"].widget.grid(row=6, column=1,
                                                       padx=5, pady=5)
        self.compFields["place"].label.grid(row=6, column=2, padx=5, pady=5)
        self.compFields["place"].widget.grid(row=6, column=3, padx=5, pady=5)
        # keeper(combobox), useDept(combobox)
        self.compFields["keeper"] = CompoundField(
            parent=self.f_mainForm,
            widgetType="combobox",
            fieldName="keeper",
            enabledState="normal",
            description="保管人")
        self.compFields["use_department"] = CompoundField(
            parent=self.f_mainForm,
            widgetType="combobox",
            fieldName="use_department",
            enabledState="normal",
            description="使用單位")
        self.compFields["keeper"].label.grid(row=7, column=0, padx=5, pady=5)
        self.compFields["keeper"].widget.grid(row=7, column=1, padx=5, pady=5)
        self.compFields["use_department"].label.grid(row=7, column=2,
                                                     padx=5, pady=5)
        self.compFields["use_department"].widget.grid(row=7, column=3,
                                                      padx=5, pady=5)
        # remark(entry)
        self.compFields["remark"] = CompoundField(
            parent=self.f_mainForm,
            widgetType="entry",
            fieldName="remark",
            enabledState="normal",
            description="備註")
        self.compFields["remark"].widget.config(width=59)
        self.compFields["remark"].label.grid(row=8, column=0, padx=5, pady=5)
        self.compFields["remark"].widget.grid(row=8, column=1, padx=5, pady=5,
                                              columnspan=3, sticky="w")
        # history form
        # a frame for the date
        self.compFields["lastUnregisterDate"] = CompoundField(
            parent=self.f_historyForm,
            widgetType="dateframe",
            fieldName="out_date",
            enabledState="normal",
            description="上次除帳")
        self.compFields["lastUnregisterDate"].label.pack(
            side="left", padx=5, pady=5)
        self.compFields["lastUnregisterDate"].widget.pack(
            side="left", padx=5, pady=5)
        # count of the unregister times
        self.compFields["unregisterCount"] = CompoundField(
            parent=self.f_historyForm,
            widgetType="entry",
            fieldName="",
            enabledState="disabled",
            description="除帳次數")
        self.compFields["unregisterCount"].widget.config(width=3)
        self.compFields["unregisterCount"].label.pack(side="left",
                                                      padx=5, pady=5)
        self.compFields["unregisterCount"].widget.pack(side="left",
                                                       padx=5, pady=5)
        # amount of the unregistered
        self.compFields["amountUnregistered"] = CompoundField(
            parent=self.f_historyForm,
            widgetType="entry",
            fieldName="",
            enabledState="disabled",
            description="除帳數量")
        self.compFields["amountUnregistered"].widget.config(width=3)
        self.compFields["amountUnregistered"].label.pack(
            side="left", padx=5, pady=5)
        self.compFields["amountUnregistered"].widget.pack(
            side="left", padx=5, pady=5)
        # unregister form self.f_unregisterForm
        # pack the first line into a frame
        self.f_firstLine = tk.Frame(self.f_unregisterForm)
        self.compFields["unregisterDate"] = CompoundField(
            parent=self.f_firstLine,
            widgetType="dateframe",
            fieldName="out_date",
            enabledState="normal",
            description="除帳日期")
        self.compFields["unregisterDate"].label.pack(side="left",
                                                     padx=5, pady=5)
        self.compFields["unregisterDate"].widget.pack(side="left",
                                                      padx=5, pady=5)
        # count of the unregister
        self.compFields["unregisterAmount"] = CompoundField(
            parent=self.f_firstLine,
            widgetType="entry",
            fieldName="",
            enabledState="normal",
            description="除帳數量")
        self.compFields["unregisterAmount"].widget.config(width=3)
        self.compFields["unregisterAmount"].label.pack(side="left",
                                                       padx=5, pady=5)
        self.compFields["unregisterAmount"].widget.pack(side="left",
                                                        padx=5, pady=5)
        # amount left
        self.compFields["unregisterRemain"] = CompoundField(
            parent=self.f_firstLine,
            widgetType="entry",
            fieldName="",
            enabledState="disabled",
            description="剩餘數量")
        # Save the disabled background color
        self._DEFAULT_DBG = self.compFields["unregisterRemain"].widget.cget(
            "disabledbackground")
        # Auto update the unregisterRemain
        # by tracing write on unregisterAmount
        self.compFields["unregisterAmount"].variable.trace(
            "w", self.updateRemain)
        self.compFields["unregisterRemain"].widget.config(width=3)
        self.compFields["unregisterRemain"].label.pack(side="left",
                                                       padx=5, pady=5)
        self.compFields["unregisterRemain"].widget.pack(side="left",
                                                        padx=5, pady=5)
        # grid the f_firstLine
        self.f_firstLine.grid(row=0, column=0, columnspan=4)
        # the unregister form frame
        # reason(combobox), postTreatment(combobox)
        self.compFields["reason"] = CompoundField(
            parent=self.f_unregisterForm,
            widgetType="combobox",
            fieldName="reason",
            enabledState="normal",
            description="除帳原因")
        self.compFields["postTreatment"] = CompoundField(
            parent=self.f_unregisterForm,
            widgetType="combobox",
            fieldName="post_treatment",
            enabledState="normal",
            description="繳存地點")
        self.compFields["reason"].label.grid(row=1, column=0, padx=5, pady=5)
        self.compFields["reason"].widget.grid(row=1, column=1, padx=5, pady=5)
        self.compFields["postTreatment"].label.grid(row=1, column=2,
                                                    padx=5, pady=5)
        self.compFields["postTreatment"].widget.grid(row=1, column=3,
                                                     padx=5, pady=5)
        # frame for the last line
        self.f_lastLine = tk.Frame(self.f_unregisterForm)
        # unregisterRemark(combobox)
        self.compFields["unregisterRemark"] = CompoundField(
            parent=self.f_lastLine,
            widgetType="combobox",
            fieldName="remark",
            enabledState="normal",
            description="除帳備註")
        self.compFields["unregisterRemark"].widget.config(width=30)
        self.compFields["unregisterRemark"].label.pack(side="left", padx=5)
        self.compFields["unregisterRemark"].widget.pack(side="left", padx=5)
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
        self.updateUnregister(state="sleep")
        # focus
        self.grab_set()
        # get to the topmost but don't get in the way
        self.attributes("-topmost", "true")
        self.attributes("-topmost", "false")

    def updateUnregister(self, state: str = "awake", **kwargs):
        self.state = state
        if state == "sleep":
            # Disable and clear all widgets
            for key, cf in self.compFields.items():
                if "date" in key.lower():
                    cf.widget.cb_y.config(state="disabled")
                    cf.widget.cb_m.config(state="disabled")
                    cf.widget.cb_d.config(state="disabled")
                else:
                    cf.widget.config(state="disabled")
            for key, cf in self.compFields.items():
                if "date" in key.lower():
                    cf.widget.clear()
                else:
                    cf.variable.set("")
        elif state == "awake":
            # Fetch an outID from **kwargs
            outID = kwargs.get("outID", None)
            # print(outID)
            if outID is not None:
                # Fetch in_ID using out_ID
                connect, cursor = _getConnection(_default_database)
                sqlstr = ("select in_ID from hvhnonc_out where ID=?;")
                params = (outID,)
                row = cursor.execute(sqlstr, params).fetchone()
                inID = row[0]
                connect.close()
            else:
                inID = kwargs.get("inID", None)
            if inID is None:
                messagebox.showerror("錯誤", "找不到ID")
                self.updateUnregister(state="sleep")
                return
            # Try to get latest out_ID using in_ID again
            if outID is not None:
                connect, cursor = _getConnection(_default_database)
                sqlstr = ("select ID "
                          "from hvhnonc_out "
                          "where in_ID=? "
                          "order by ID desc;")
                params = (inID,)
                row = cursor.execute(sqlstr, params).fetchone()
                if row:
                    outID = row[0]
                connect.close()
            self.index = self.findIndex(inID=inID, outID=outID)
            self.title("除帳: {}[{},{}]".format(self.index, outID, inID))
            # show inData
            connect, cursor = _getConnection(_default_database)
            # connect.set_trace_callback(print)
            fields = ("category", "subcategory", "name", "unit", "brand",
                      "spec", "object_ID", "serial_ID", "purchase_date",
                      "keep_year", "price", "amount", "keep_department",
                      "place", "keeper", "use_department", "remark")
            sqlstr = ("select {} from hvhnonc_in where ID=?;")
            sqlstr = sqlstr.format(", ".join(fields))
            cursor.execute(sqlstr, (inID,))
            row = cursor.fetchone()
            for i, data in enumerate(row):
                if isinstance(self.compFields[fields[i]].widget, DateFrame):
                    date = "".join(data).split("-")
                    date[0] = str(int(date[0]) - 1911)
                    self.compFields[fields[i]].widget.y.set(date[0])
                    self.compFields[fields[i]].widget.m.set(date[1])
                    self.compFields[fields[i]].widget.d.set(date[2])
                    self.compFields[fields[i]].widget.updateVar()
                self.compFields[fields[i]].variable.set(data)
            # Initialize writable fields
            self.initForm()
            # show outData
            if not outID:
                self.compFields["unregisterCount"].variable.set("0")
                self.compFields["unregisterAmount"].variable.set("0")
                self.compFields["amountUnregistered"].variable.set("0")
            else:
                sqlstr = ("select count(*), out_date, amount, reason, "
                          "post_treatment, remark "
                          "from hvhnonc_out "
                          "where ID=?")
                params = (outID,)
                cursor.execute(sqlstr, params)
                row = cursor.fetchone()
                self.compFields["unregisterCount"].variable.set(row[0])
                date = "".join(row[1]).split("-")
                date[0] = str(int(date[0]) - 1911)
                self.compFields["lastUnregisterDate"].widget.y.set(date[0])
                self.compFields["lastUnregisterDate"].widget.m.set(date[1])
                self.compFields["lastUnregisterDate"].widget.d.set(date[2])
                self.compFields["lastUnregisterDate"].widget.updateVar()
                self.compFields["unregisterAmount"].variable.set(row[2])
                self.compFields["unregisterDate"].widget.y.set(date[0])
                self.compFields["unregisterDate"].widget.m.set(date[1])
                self.compFields["unregisterDate"].widget.d.set(date[2])
                self.compFields["unregisterDate"].widget.updateVar()
                self.compFields["reason"].variable.set(row[3])
                self.compFields["postTreatment"].variable.set(row[4])
                self.compFields["unregisterRemark"].variable.set(row[5])
                # get amount unregistered in the past
                sqlstr = ("select sum(amount) "
                          "from hvhnonc_out "
                          "where in_ID=?")
                cursor.execute(sqlstr, (inID,))
                (totalOutAmount,) = cursor.fetchone()
                self.compFields["amountUnregistered"].variable.set(
                    totalOutAmount)
            pass
        else:  # Invalid state
            print("Invalid state {}".format(state))

    # The callback to auto update unregisterRemain
    def updateRemain(self, n, m, x):
        if self.state in ("sleep",):
            return
        if x is not 'w':
            return
        try:
            # Get value from database
            connect, cursor = _getConnection(_default_database)
            # Get inAmount
            sqlstr = ("select amount from hvhnonc_in where ID=?")
            if self.index:
                params = (self.book[self.index][1],)
            else:
                params = (self.inID,)
            cursor.execute(sqlstr, params)
            inAmount = cursor.fetchone()[0]
            inAmount = int(inAmount)
        except (TypeError, ValueError):
            inAmount = 0
        try:
            # Get outAmount
            sqlstr = ("select sum(amount) from hvhnonc_out where in_ID=?")
            params = (self.book[self.index][1],)
            cursor.execute(sqlstr, params)
            outAmount = cursor.fetchone()[0]
            connect.close()
        except (TypeError, ValueError):
            outAmount = 0
        try:
            typedAmount = self.compFields["unregisterAmount"].variable.get()
            typedAmount = int(typedAmount)
        except (TypeError, ValueError):
            typedAmount = 0
        newAmount = inAmount - outAmount - typedAmount
        if newAmount < 0:
            self.compFields["unregisterRemain"].widget.config(
                disabledbackground="Misty Rose")
            self.compFields["unregisterRemain"].variable.set("0")
        else:
            self.compFields["unregisterRemain"].widget.config(
                disabledbackground=self._DEFAULT_DBG)
            self.compFields["unregisterRemain"].variable.set(str(newAmount))

    def initForm(self):
        # enable some widgets
        tempFields = (
            self.compFields["unregisterDate"],
            self.compFields["unregisterAmount"],
            self.compFields["reason"],
            self.compFields["postTreatment"],
            self.compFields["unregisterRemark"])
        for field in tempFields:
            if field.widgetType == "dateframe":
                field.widget.cb_y.config(state=field.enabledState)
                field.widget.cb_m.config(state=field.enabledState)
                field.widget.cb_d.config(state=field.enabledState)
            else:
                field.widget.config(state=field.enabledState)
        # set lower part to ""
        # date fields
        self.compFields["lastUnregisterDate"].widget.clear()
        self.compFields["unregisterDate"].widget.setAsToday()
        tempFields = (
            self.compFields["unregisterCount"],
            self.compFields["amountUnregistered"],
            self.compFields["unregisterAmount"],
            self.compFields["unregisterRemain"],
            self.compFields["reason"],
            self.compFields["postTreatment"],
            self.compFields["unregisterRemark"])
        for field in tempFields:
            field.variable.set("")
        # Read in cache and update
        connect, cursor = _getConnection(_default_database)
        sqlstr = ("select change_value "
                  "from hvhnonc_out_cache "
                  "where this_ID=? "
                  "and change_ID=?"
                  "order by rowid desc limit 30;")
        tempFields = (
            self.compFields["reason"],
            self.compFields["postTreatment"],
            self.compFields["unregisterRemark"])
        feildIDs = (
            getFieldIDByName("除帳原因"),
            getFieldIDByName("繳存地點"),
            getFieldIDByName("除帳備註"),)
        rows = []
        for ID in feildIDs:
            cursor.execute(sqlstr, (getFieldIDByName("無"), str(ID)))
            rows.append(cursor.fetchall())
        for i, field in enumerate(tempFields):
            field.widget.config(values=rows[i])
        connect.close()

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
            connect, cursor = _getConnection(_default_database)
            connect.row_factory = lambda cursor, row: row[0]
            sqlstr = ("select change_value "
                      "from hvhnonc_out_cache "
                      "where change_ID=? "
                      "order by rowid desc limit 30;")
            cursor.execute(sqlstr, (getFieldIDByName("檢索"),))
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
            connect, cursor = _getConnection(_default_database)
            sqlstr = (
                "replace into hvhnonc_out_cache(this_ID, this_value, "
                "change_ID, change_value) "
                "values(0, 'none', ?, ?);")
            params = (getFieldIDByName("檢索"), self.parent.query.get())
            cursor.execute(sqlstr, params)
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
                    columns=('0', '1', '2', '3', '4', '5', '6', '7'),
                    show="headings")
                self.tv['displaycolumns'] = ('0', '2', '3', '4', '5', '6')
                self.tv.heading('0', text='入/除帳')
                self.tv.heading('1', text='ID')
                self.tv.heading('2', text='購置日期')
                self.tv.heading('3', text='品名')
                self.tv.heading('4', text='存置位置')
                self.tv.heading('5', text='保管人')
                self.tv.heading('6', text='備註')
                self.tv.heading('7', text='outID')
                sb.config(command=self.tv.yview)
                # fetch the data
                # searching in hvhnonc_in
                connect, cursor = _getConnection(_default_database)
                # connect.set_trace_callback(print)
                phrase = str(parent.query.get())
                sqlin = ("select '入帳' as whichBook, ID as inID, "
                         "purchase_date as date, name, place, keeper, "
                         "remark, '' as outID "
                         "from hvhnonc_in ")
                sqlout = ("select '除帳' as whichBook, in_ID as inID, "
                          "out_date as date, name, storage as place, "
                          "'' as keeper, remark, ID as outID "
                          "from hvhnonc_out ")
                sqlwherein = ("where("
                              "category like :q or "
                              "subcategory like :q or "
                              "name like :q or "
                              "brand like :q or "
                              "spec like :q or "
                              "place like :q or "
                              "keep_department like :q or "
                              "use_department like :q or "
                              "keeper like :q or "
                              "remark like :q) ")
                sqlwhereout = ("where("
                               "category like :q or "
                               "subcategory like :q or "
                               "name like :q or "
                               "brand like :q or "
                               "spec like :q or "
                               "storage like :q or "
                               "remark like :q) ")
                sqlunion = ("union all ")
                sqlfooter = ("order by date desc, name desc;")
                sqlstr = (sqlin + sqlwherein + sqlunion +
                          sqlout + sqlwhereout + sqlfooter)
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
                item = self.tv.identify('item', event.x, event.y)
                # print("you clicked on", self.tv.item(item, "values")[0])
                self.inID = str(self.tv.item(item, "values")[1])
                out_ID = str(self.tv.item(item, "values")[7])
                if out_ID in (None, ""):
                    self.parent.updateUnregister(inID=self.inID)
                else:
                    self.parent.updateUnregister(inID=self.inID, outID=out_ID)
                self.destroy()

    def onButtonSaveClick(self):
        if self.state in ("sleep"):
            messagebox.showerror("錯誤", "無效的狀態: {}".format(self.state),
                                 parent=self)
            return
        # if self.index collide ask for update
        if self.index:
            isWriteover = tk.messagebox.askyesnocancel(
                "重複寫入",
                "是否要複蓋掉最近資料?(按否會新增一筆新資料)",
                parent=self)
            # if yes, update
            if isWriteover == True:
                self.writeOver()
            # if no, insert
            elif isWriteover == False:
                self.insertAsNew()
            # else pass
            else:
                pass
        # else(no collision), insert
        else:
            self.insertAsNew()

    def writeOver(self):
        # insert SQL
        connect, cursor = _getConnection(_default_database)
        sqlstr = ("update hvhnonc_out "
                  "set object_ID=?, "
                  "serial_ID=?, "
                  "category=?, "
                  "subcategory=?, "
                  "name=?, "
                  "brand=?, "
                  "spec=?, "
                  "unit=?, "
                  "out_date=?, "
                  "price=?, "
                  "amount=?, "
                  "storage=?, "
                  "reason=?, "
                  "post_treatment=?, "
                  "remark=? "
                  "where in_ID=? and rowid=("
                  "select max(rowid) "
                  "from hvhnonc_out "
                  "where in_ID=?)")
        # prepare unregisterDate in ROC years
        unregisterDate = self.compFields["unregisterDate"].variable.get()
        year = int(unregisterDate.split("-")[0])
        if year < 1911:
            unregisterDate = unregisterDate.replace(
                str(year), str(year + 1911))
        params = (self.compFields["object_ID"].variable.get(),
                  self.compFields["serial_ID"].variable.get(),
                  self.compFields["category"].variable.get(),
                  self.compFields["subcategory"].variable.get(),
                  self.compFields["name"].variable.get(),
                  self.compFields["brand"].variable.get(),
                  self.compFields["spec"].variable.get(),
                  self.compFields["unit"].variable.get(),
                  unregisterDate,
                  self.compFields["price"].variable.get(),
                  self.compFields["unregisterAmount"].variable.get(),
                  self.compFields["place"].variable.get(),
                  self.compFields["reason"].variable.get(),
                  self.compFields["postTreatment"].variable.get(),
                  self.compFields["unregisterRemark"].variable.get(),
                  int(self.inID), int(self.inID))
        try:
            cursor.execute(sqlstr, params)
            connect.commit()
            messagebox.showinfo(
                "覆寫", "已蓋過最新一筆資料:{}".format(
                    self.compFields["name"].variable.get()))
            # update book
            self.book = self.getAllIDs("hvhnonc_out")
            # update cache using default sqlstr
            self.updateAllCache()
            self.updateUnregister(state="sleep")
        except sqlite3.Error as e:
            messagebox.showerror("錯誤", "{}".format(e))
        pass

    def insertAsNew(self):
        # insert SQL
        connect, cursor = _getConnection(_default_database)
        sqlstr = (
            "insert into hvhnonc_out(in_ID, object_ID, serial_ID, "
            "category, subcategory, name, brand, spec, unit, out_date, "
            "price, amount, storage, reason, post_treatment, remark) "
            "values ({});")
        # prepare unregisterDate in ROC years
        unregisterDate = self.compFields["unregisterDate"].variable.get()
        year = int(unregisterDate.split("-")[0])
        if year < 1911:
            unregisterDate = unregisterDate.replace(
                str(year), str(year + 1911))

        params = (int(self.inID),
                  self.compFields["object_ID"].variable.get(),
                  self.compFields["serial_ID"].variable.get(),
                  self.compFields["category"].variable.get(),
                  self.compFields["subcategory"].variable.get(),
                  self.compFields["name"].variable.get(),
                  self.compFields["brand"].variable.get(),
                  self.compFields["spec"].variable.get(),
                  self.compFields["unit"].variable.get(),
                  unregisterDate,
                  self.compFields["price"].variable.get(),
                  self.compFields["unregisterAmount"].variable.get(),
                  self.compFields["place"].variable.get(),
                  self.compFields["reason"].variable.get(),
                  self.compFields["postTreatment"].variable.get(),
                  self.compFields["unregisterRemark"].variable.get())
        questionmarks = ", ".join(["?" for i in range(0, len(params))])
        try:
            cursor.execute(sqlstr.format(questionmarks,), params)
            connect.commit()
            messagebox.showinfo(
                "存入一筆", "已存入一筆新資料:{}".format(
                    self.compFields["name"].variable.get()))
            # update book
            self.book = self.getAllIDs("hvhnonc_out")
            # update cache using default sqlstr
            self.updateAllCache()
            self.updateUnregister(state="sleep")
        except sqlite3.IntegrityError:
            messagebox.showerror("錯誤", "有欄位不正確!")
            return
        except sqlite3.Error as e:
            messagebox.showerror("錯誤", "{}".format(e))
            self.updateUnregister(state="sleep")
            return
        self.updateUnregister(inID=self.inID)

    def fetchNext(self):
        try:
            if self.state in ("sleep",):
                self.index = 0
                self.outID = self.book[self.index][0]
                self.inID = self.book[self.index][1]
                self.updateUnregister(outID=self.outID)
            else:
                if self.index == len(self.book) - 1:
                    tk.messagebox.showinfo("到底了", "已到達最後一筆",
                                           parent=self)
                else:
                    self.index += 1
                    self.outID = self.book[self.index][0]
                    self.inID = self.book[self.index][1]
                    self.updateUnregister(outID=self.outID)
        except TypeError:
            tk.messagebox.showinfo("無效", "沒有下一筆", parent=self)

    def fetchLast(self):
        try:
            if self.state in ("sleep", ):
                self.index = len(self.book) - 1
                self.outID = self.book[self.index][0]
                self.inID = self.book[self.index][1]
                self.updateUnregister(outID=self.outID)
            else:
                if self.index == 0:
                    tk.messagebox.showinfo("到頂了", "已到達第一筆",
                                           parent=self)
                else:
                    self.index = self.index - 1
                    self.outID = self.book[self.index][0]
                    self.inID = self.book[self.index][1]
                    self.updateUnregister(outID=self.outID)
        except TypeError:
            tk.messagebox.showinfo("無效", "沒有上一筆", parent=self)

    def onButtonDeleteClick(self):
        connect, cursor = _getConnection(_default_database)
        if self.state in ("sleep", ):
            messagebox.showerror("錯誤", "非法的狀態{}".format(self.state))
        sqlstr = ("delete from hvhnonc_out "
                  "where in_ID=? and out_date=("
                  "select max(out_date) "
                  "from hvhnonc_out "
                  "where in_ID=?);")
        params = (self.inID, self.inID)
        try:
            cursor.execute(sqlstr, params)
            connect.commit()
            messagebox.showinfo(
                "刪除", "已刪除一筆資料:{}".format(
                    self.compFields["name"].variable.get()))
            # update book
            self.book = self.getAllIDs("hvhnonc_out")
            self.updateUnregister(state="sleep")
        except sqlite3.Error as e:
            messagebox.showerror("錯誤", "{}".format(e))

    def onButtonFormClick(self):
        # basically the onButtonSelectClick but only look for hchnonc_out
        self.SelectFilter(self, source="out")

    def onButtonSelectClick(self):
        # open a select filter toplevel
        self.SelectFilter(self, source="both")

    class SelectFilter(tk.Toplevel):
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
                parent=self, widgetType="combobox", description="物品大類",
                fieldName="category", enabledState="readonly")
            self.wdict["category"].label.grid(row=0, column=0,
                                              padx=5, pady=5)
            self.wdict["category"].widget.grid(row=0, column=1,
                                               padx=5, pady=5)
            # subcategory
            self.wdict["subcategory"] = CompoundField(
                parent=self, widgetType="combobox", description="物品分類",
                fieldName="subcategory", enabledState="readonly")
            self.wdict["subcategory"].label.grid(row=0, column=2,
                                                 padx=5, pady=5)
            self.wdict["subcategory"].widget.grid(row=0, column=3,
                                                  padx=5, pady=5)
            # name
            self.wdict["name"] = CompoundField(
                parent=self, widgetType="combobox", description="物品名稱",
                fieldName="name", enabledState="normal")
            self.wdict["name"].label.grid(row=1, column=0, padx=5, pady=5)
            self.wdict["name"].widget.grid(row=1, column=1, padx=5, pady=5)
            # brand
            self.wdict["brand"] = CompoundField(
                parent=self, widgetType="combobox", description="品牌",
                fieldName="brand", enabledState="normal")
            self.wdict["brand"].label.grid(row=1, column=2, padx=5, pady=5)
            self.wdict["brand"].widget.grid(row=1, column=3, padx=5, pady=5)
            # spec
            self.wdict["spec"] = CompoundField(
                parent=self, widgetType="combobox", description="規格",
                fieldName="spec", enabledState="normal")
            self.wdict["spec"].label.grid(row=2, column=0, padx=5, pady=5)
            self.wdict["spec"].widget.grid(row=2, column=1, padx=5, pady=5)
            # price
            self.wdict["price"] = CompoundField(
                parent=self, widgetType="entry", description="單價",
                fieldName="price", enabledState="normal", span=True)
            self.wdict["price"].widget.min.config(width=10)
            self.wdict["price"].widget.max.config(width=10)
            self.wdict["price"].label.grid(row=2, column=2, padx=5, pady=5)
            self.wdict["price"].widget.grid(row=2, column=3, padx=5, pady=5)
            # purchase_date
            self.wdict["purchase_date"] = CompoundField(
                parent=self, widgetType="dateframe", description="日期範圍",
                fieldName="purchase_date", enabledState="normal", span=True)
            self.wdict["purchase_date"].widget.min.clear()
            self.wdict["purchase_date"].widget.max.clear()
            self.wdict["purchase_date"].label.grid(
                row=3, column=0, padx=5, pady=5)
            self.wdict["purchase_date"].widget.grid(
                    row=3, column=1, padx=5, pady=5, columnspan=3, sticky="w")
            # acquire_date
            self.wdict["acquire_date"] = CompoundField(
                parent=self, widgetType="dateframe", description="建帳日期",
                fieldName="acquire_date", enabledState="normal", span=True)
            self.wdict["acquire_date"].widget.min.clear()
            self.wdict["acquire_date"].widget.max.clear()
            self.wdict["acquire_date"].label.grid(
                row=4, column=0, padx=5, pady=5)
            self.wdict["acquire_date"].widget.grid(
                row=4, column=1, padx=5, pady=5, columnspan=3, sticky="w")
            # keep_department
            self.wdict["keep_department"] = CompoundField(
                parent=self, widgetType="combobox", description="保管單位",
                fieldName="keep_department", enabledState="normal")
            self.wdict["keep_department"].label.grid(
                row=5, column=0, padx=5, pady=5)
            self.wdict["keep_department"].widget.grid(
                row=5, column=1, padx=5, pady=5)
            # place
            self.wdict["place"] = CompoundField(
                parent=self, widgetType="combobox", description="存置地點",
                fieldName="place", enabledState="normal")
            self.wdict["place"].label.grid(row=5, column=2, padx=5, pady=5)
            self.wdict["place"].widget.grid(row=5, column=3, padx=5, pady=5)
            # use_department
            self.wdict["use_department"] = CompoundField(
                parent=self, widgetType="combobox", description="使用單位",
                fieldName="use_department", enabledState="normal")
            self.wdict["use_department"].label.grid(
                row=6, column=0, padx=5, pady=5)
            self.wdict["use_department"].widget.grid(
                row=6, column=1, padx=5, pady=5)
            # keeper
            self.wdict["keeper"] = CompoundField(
                parent=self, widgetType="combobox", description="保管人",
                fieldName="keeper", enabledState="normal")
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
                if v.widgetType == "dateframe":
                    try:
                        v.widget.min.clear()
                        v.widget.max.clear()
                    except NameError:
                        v.widget.clear()
                try:
                    v.variable["min"].set("")
                    v.variable["max"].set("")
                except (KeyError, TypeError):
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
            connect, cursor = _getConnection(_default_database)
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
                param = (self.wdict["category"].variable.get(),)
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
                          "change_ID=?;")
                param = (getFieldIDByName(cf.description),)
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
                # init
                tk.Toplevel.__init__(self, parent, *args, **kwargs)
                self.parent = parent
                self.attributes("-topmost", "true")
                self.attributes("-topmost", "false")
                self.title("篩選結果")
                self.geometry("1200x600")
                # make a tree view
                sb = tk.Scrollbar(self)
                self.tv = ttk.Treeview(
                    self, yscrollcommand=sb.set,
                    columns=('1', '2', '3', '4', '5', '6', '7'),
                    show="headings")
                self.tv['displaycolumns'] = ('2', '3', '4', '5', '6')
                self.tv.heading('1', text='ID')
                self.tv.heading('2', text='日期')
                self.tv.heading('3', text='品名')
                self.tv.heading('4', text='存置位置')
                self.tv.heading('5', text='保管人')
                self.tv.heading('6', text='備註')
                self.tv.heading('7', text='outID')
                sb.config(command=self.tv.yview)
                # fetch the data
                connect, cursor = _getConnection(_default_database)
                # connect.set_trace_callback(print)
                params = []
                q_in = ("select ID, purchase_date as date, name, "
                        "place as place, keeper, remark , '' as out_ID "
                        "from hvhnonc_in ")
                q_out = ("select in_ID as ID, out_date as date, name, "
                         "storage as place, '' as keeper, remark, "
                         "ID as out_ID "
                         "from hvhnonc_out ")
                q_union = "union all "
                q_footer = "order by purchase_date desc;"
                q_where = "where ("
                for key, cf in parent.wdict.items():
                    # span == True
                    try:
                        cf.widget.tilde
                        if cf.widgetType == "dateframe":
                            # continue if there is nothing
                            if not (cf.widget.min.variable.get()
                                    or cf.widget.max.variable.get()):
                                continue
                            tempMin = "1911-01-01"
                            tempMax = "date('now')"
                            if cf.widget.min.variable.get():
                                tempMin = cf.widget.min.variable.get()
                                # convert to ROC years
                                year = int(tempMin.split('-')[0])
                                tempMin = tempMin.replace(
                                    str(year), str(year + 1911))
                            if cf.widget.max.variable.get():
                                tempMax = cf.widget.max.variable.get()
                                # convert to ROC years
                                year = int(tempMin.split('-')[0])
                                tempMin = tempMin.replace(
                                    str(year), str(year + 1911))
                            q_where += (
                                "(strftime('%Y-%m-%d', {}) "
                                "between ? and ?) and ".format(key))
                            params.append(tempMin)
                            params.append(tempMax)
                        # entry and span == True
                        elif cf.widgetType == "entry":
                            tMin = cf.variable["min"].get()
                            tMax = cf.variable["max"].get()
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
                    except AttributeError:
                        # no span
                        if cf.variable.get():
                            q_where += ("{} like ? and ".format(key))
                            params.append("%{}%".format(cf.variable.get()))
                # where(1) if no input
                q_where += "1) "
                q_in_full = q_in + q_where
                q_where = q_where.replace("purchase_date", "out_date")
                q_where = q_where.replace("place", "storage")
                q_out_full = q_out + q_where
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
                        q_out_full
                        + q_footer.replace("purchase_date", "out_date"),
                        params)
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
                item = self.tv.identify('item', event.x, event.y)
                # print("you clicked on", self.tv.item(item, "values")[0])
                self.parent.parent.inID = self.tv.item(item, "values")[0]
                in_ID = self.parent.parent.inID
                out_ID = self.tv.item(item, "values")[6]
                self.parent.parent.index = \
                    self.parent.parent.findIndex(in_ID, out_ID)
                if out_ID:
                    self.parent.parent.updateUnregister(
                        inID=in_ID, outID=out_ID)
                else:
                    self.parent.parent.updateUnregister(inID=in_ID)
                self.parent.destroy()

            def abortLookup(self):
                self.parent.destroy()

    def findIndex(self, inID: str, outID: str) -> int:
        if inID is None or outID is None:
            return None
        for i, row in enumerate(self.book):
            if (str(inID) == str(row[1])
                    and str(outID) == str(row[0])):
                return i
        return None

    def getAllIDs(self, tablename):
        connect, cursor = _getConnection(_default_database)
        # connect.set_trace_callback(print)
        sqlstr = "select ID, in_ID from {};".format(tablename)
        cursor.execute(sqlstr)
        return cursor.fetchall()

    def updateAllCache(self, sqlstr: str = None):
        if not sqlstr:
            sqlstr = ("insert or ignore into "
                      "hvhnonc_out_cache("
                      "this_ID, this_value, change_ID, change_value) "
                      "values(?, ?, ?, ?);")
        self.updateCache(sqlstr, "無", "除帳原因")
        self.updateCache(sqlstr, "無", "繳存地點")
        self.updateCache(sqlstr, "無", "除帳備註")

    def updateCache(self, sqlstr, thisName, thatName):
        connect, cursor = _getConnection(_default_database)
        # connect.set_trace_callback(print)
        # Update cache table
        # So next time when thisName is fed,
        # autocomplete thatName

        # get the value from thisName
        if thisName not in ('無',):
            thisCF = None
            for k, cf in self.compFields.items():
                if cf.description == thisName:
                    thisCF = cf
                    break
            thisVal = thisCF.variable.get()
        else:
            thisVal = "none"
        # get the value from thatName
        thatCF = None
        for k, cf in self.compFields.items():
            if cf.description == thatName:
                thatCF = cf
                break
        thatVal = thatCF.variable.get()
        if thatVal.strip() in (None, ""):
            return
        # construct parameters
        params = [getFieldIDByName(thisName), thisVal,
                  getFieldIDByName(thatName), thatVal]
        try:
            cursor.execute(sqlstr, params)
            connect.commit()
        except Exception as e:
            print("Exception in updateCache: %s" % e)
            tk.messagebox.showerror("錯誤 updateCache", str(e),
                                    parent=self)


class PrintNonc(tk.Toplevel):
    def __init__(self, parent, *args, **kwargs):
        s = ttk.Style()
        s.configure('printNonc.TButton', font=_default_button_font)
        tk.Toplevel.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.title("列印")
        self.geometry("657x421")
        self.resizable(False, False)
        # gui
        self.dateRangeFrame = self.DateRangeFrame(self)
        self.radioButtonFrame = self.RadioButtonFrame(self)
        self.otherFieldsFrame = self.OtherFieldsFrame(self)
        self.BottomButtonsFrame = self.BottomButtonsFrame(self)
        self.separator = ttk.Separator(self, orient="horizontal")
        self.radioButtonFrame.grid(row=0, pady=5)
        self.dateRangeFrame.grid(row=1, pady=5)
        self.separator.grid(row=2, sticky="ew")
        self.otherFieldsFrame.grid(row=3)
        self.BottomButtonsFrame.grid(row=4)
        # init
        self.initialize_field()
        # focus
        self.attributes("-topmost", "true")
        self.attributes("-topmost", "false")
        self.grab_set()

    def initialize_field(self):
        # last day of month, copied from stackoverflow
        # stackoverflow  "get-last-day-of-the-month-in-python"
        def last_day_of_month(any_day):
            next_month = (any_day.replace(day=28) + dt.timedelta(days=4))
            return next_month - dt.timedelta(days=next_month.day)

        # set date span to this month
        today = dt.datetime.today()
        monthStart = dt.datetime(today.year, today.month, 1)
        monthEnd = last_day_of_month(today)
        self.dateRangeFrame.cf["購置或取得日期"].widget.min.y.set(
                str(monthStart.year - 1911))
        self.dateRangeFrame.cf["購置或取得日期"].widget.min.m.set(
                str(monthStart.month))
        self.dateRangeFrame.cf["購置或取得日期"].widget.min.d.set(
                str(monthStart.day))
        self.dateRangeFrame.cf["購置或取得日期"].widget.min.updateVar()
        self.dateRangeFrame.cf["購置或取得日期"].widget.max.y.set(
                str(monthEnd.year - 1911))
        self.dateRangeFrame.cf["購置或取得日期"].widget.max.m.set(
                str(monthEnd.month))
        self.dateRangeFrame.cf["購置或取得日期"].widget.max.d.set(
                str(monthEnd.day))
        self.dateRangeFrame.cf["購置或取得日期"].widget.max.updateVar()


    def quitMe(self):
        self.destroy()

    class RadioButtonFrame(tk.Frame):
        def __init__(self, parent, *args, **kwargs):
            tk.Frame.__init__(self, parent, *args, **kwargs)
            self.parent = parent
            choices = {0: "[建帳]清單",
                       1: "統計月報表",
                       2: "非消耗品清冊",
                       3: "[除帳]減損單",
                       4: "動產財產卡",
                       5: "增加單",
                       6: "增減表",
                       7: "財產標籤",
                       8: "盤點紀錄",
                       9: "盤存表",
                       10: "財產保管卡"}
            self.radioVar = tk.IntVar()
            self.radioButtons = {}
            for i, description in choices.items():
                self.radioButtons[i] = tk.Radiobutton(
                    self, text=description, variable=self.radioVar,
                    value=i, font=_default_font)
                self.radioButtons[i].grid(row=i // 4, column=i % 4,
                                          sticky=tk.W)

    class DateRangeFrame(tk.Frame):
        def __init__(self, parent, *args, **kwargs):
            tk.Frame.__init__(self, parent, *args, **kwargs)
            self.parent = parent
            dateFields = ["購置或取得日期", "建帳日期"]
            self.cf = {}
            for i, field in enumerate(dateFields):
                self.cf[field] = CompoundField(self, "dateframe", "",
                                               "normal", field, span=True)
                self.cf[field].widget.min.clear()
                self.cf[field].widget.max.clear()
                self.cf[field].label.grid(row=i, column=0, sticky=tk.E)
                self.cf[field].widget.grid(row=i, column=1, sticky=tk.W)

    class OtherFieldsFrame(tk.Frame):
        def __init__(self, parent, *args, **kwargs):
            tk.Frame.__init__(self, parent, *args, **kwargs)
            self.parent = parent
            fields = {"category": "物品大項",
                      "subcategory": "物品細目",
                      "name": "物品名稱",
                      "place": "存置地點",
                      "keep_department": "保管單位",
                      "use_department": "使用單位",
                      "keeper": "保管人", }
            self.cf = {}
            i = 0
            for field, description in fields.items():
                self.cf[field] = CompoundField(
                    self, "combobox", field, "normal", description)
                if description in ("物品大項", "保管單位"):
                    self.cf[field].label.grid(
                            row=i, column=0, padx=5, pady=5)
                    self.cf[field].widget.grid(
                            row=i, column=1, padx=5, pady=5)
                elif description in ("物品細目", "使用單位"):
                    self.cf[field].label.grid(
                            row=i, column=2, padx=5, pady=5)
                    self.cf[field].widget.grid(
                            row=i, column=3, padx=5, pady=5)
                    i += 1  # new row
                else:
                    self.cf[field].label.grid(
                            row=i, column=0, padx=5, pady=5)
                    self.cf[field].widget.grid(
                            row=i, column=1, padx=5, pady=5)
                    i += 1  # new row
            # clear button
            self.btn_clear = ttk.Button(
                    self, text="清空選項", style="printNonc.TButton",
                    command=self.on_button_clear_clicked)
            self.btn_clear.grid(row=1, column=3, padx=5, pady=5)
            # last line
            self.cf["linePerPage"] = CompoundField(
                self, "spinbox", field, "normal", "每頁列印筆數")
            self.cf["linePerPage"].variable.set("20")
            self.cf["linePerPage"].label.grid(
                row=i, column=0, columnspan=2, sticky=tk.E)
            self.cf["linePerPage"].widget.grid(
                row=i, column=2, columnspan=2, sticky=tk.W)
            # Fetch suggested category from database
            connect, cursor = _getConnection(_default_database)
            sqlstr = ("select description from hvhnonc_category")
            rows = cursor.execute(sqlstr).fetchall()
            categories = [row[0] for row in rows if row[0]]
            self.cf["category"].widget.config(values=categories)
            # Hook combobox select callback
            self.cf["category"].widget.bind("<<ComboboxSelected>>",
                                            self.on_category_selected)
            self.on_category_selected(None)
            # Fetch other comboboxes' cache
            for key, cf in self.cf.items():
                if isinstance(cf.widget, ttk.Combobox):
                    if key not in ("category", "subcategory", "name"):
                        self.fetch_cache(cf)

        def fetch_cache(self, cf: CompoundField):
            connect, cursor = _getConnection(_default_database)
            sqlstr = ("select change_value "
                      "from hvhnonc_in_cache "
                      "where this_ID=:thisID "
                            "and this_value=:thisValue "
                            "and change_ID=:changeID "
                      "union all "
                      "select change_value "
                      "from hvhnonc_out_cache "
                      "where this_ID=:thisID "
                            "and this_value=:thisValue "
                            "and change_ID=:changeID;")
            params = {"thisID": getFieldIDByName("無"),
                      "thisValue": "none",
                      "changeID": getFieldIDByName(cf.description)}
            rows = cursor.execute(sqlstr, params).fetchall()
            cachehits = [row[0] for row in rows if row[0]]
            cf.widget.config(values=cachehits)

        def on_category_selected(self, event):
            # fetch suggested subcategory
            connect, cursor = _getConnection(_default_database)
            sqlstr = ("select description "
                      "from hvhnonc_subcategory "
                      "where parent_ID=("
                          "select ID "
                          "from hvhnonc_category "
                          "where description=?);")
            params = (self.cf["category"].variable.get(),)
            rows = cursor.execute(sqlstr, params).fetchall()
            subcategories = [row[0] for row in rows if row[0]]
            self.cf["subcategory"].widget.config(
                    values=subcategories)
            self.cf["subcategory"].widget.bind(
                    "<<ComboboxSelected>>", self.on_subcategory_selected)
            if (len(subcategories) and subcategories[0] not in (None, "")):
                self.cf["subcategory"].variable.set(subcategories[0])
            else:
                self.cf["name"].variable.set("")
            self.on_subcategory_selected(None)

        def on_subcategory_selected(self, event):
            # fetch suggested subcategory
            connect, cursor = _getConnection(_default_database)
            sqlstr = ("select change_value "
                      "from hvhnonc_in_cache "
                      "where this_ID=:thisID "
                            "and this_value=:thisValue "
                            "and change_ID=:changeID "
                      "union all "
                      "select change_value "
                      "from hvhnonc_out_cache "
                      "where this_ID=:thisID "
                            "and this_value=:thisValue "
                            "and change_ID=:changeID;")
            params = {"thisID": getFieldIDByName("物品細目"),
                      "thisValue": self.cf["subcategory"].variable.get(),
                      "changeID": getFieldIDByName("物品名稱")}
            rows = cursor.execute(sqlstr, params).fetchall()
            names = [row[0] for row in rows if row[0]]
            self.cf["name"].widget.config(values=names)
            if (len(names) and names[0] not in (None, "")):
                self.cf["name"].variable.set(names[0])
            else:
                self.cf["name"].variable.set("")

        # callback of button that clears the cat-subcat-name comboboxes
        def on_button_clear_clicked(self):
            self.cf["category"].variable.set("")
            self.cf["subcategory"].variable.set("")
            self.cf["name"].variable.set("")

    class BottomButtonsFrame(tk.Frame):
        def __init__(self, parent, *args, **kwargs):
            tk.Frame.__init__(self, parent, *args, **kwargs)
            self.parent = parent
            self.btn_quit = ttk.Button(self, text="返回",
                                       style="printNonc.TButton",
                                       command=parent.quitMe)
            self.btn_quit.grid(row=0, column=0, padx=5, pady=5)
            self.btn_quit = ttk.Button(
                    self, text="變更預設印表機", style="printNonc.TButton",
                    command=parent.on_change_default_printer_button_click)
            self.btn_quit.grid(row=0, column=1, padx=5, pady=5)
            self.btn_quit = ttk.Button(
                    self, text="預覽", style="printNonc.TButton",
                    command=parent.on_preview_button_click)
            self.btn_quit.grid(row=0, column=2, padx=5, pady=5)
            self.btn_quit = ttk.Button(
                    self, text="列印", style="printNonc.TButton",
                    command=parent.on_printer_print_button_click)
            self.btn_quit.grid(row=0, column=3, padx=5, pady=5)

    def on_change_default_printer_button_click(self):
        print(__name__)

    def on_preview_button_click(self):
        print(__name__)

    def on_printer_print_button_click(self):
        print(__name__)


class Maintenance(tk.Toplevel):
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
        # gui
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
    root.option_add("*Font", _default_font)
    root.option_add("*Label.Font", _default_font)
    test = Unregister(root)
    test.protocol("WM_DELETE_WINDOW", lambda: test.parent.destroy())
    root.mainloop()
    root.quit()


if __name__ == "__main__":
    main()
