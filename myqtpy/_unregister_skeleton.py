# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'unregister.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(620, 601)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.category = QtWidgets.QComboBox(Dialog)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.category.setFont(font)
        self.category.setEditable(True)
        self.category.setObjectName("category")
        self.gridLayout.addWidget(self.category, 0, 1, 1, 1)
        self.label_13 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.label_13.setFont(font)
        self.label_13.setObjectName("label_13")
        self.gridLayout.addWidget(self.label_13, 0, 2, 1, 1)
        self.subcategory = QtWidgets.QComboBox(Dialog)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.subcategory.setFont(font)
        self.subcategory.setEditable(True)
        self.subcategory.setObjectName("subcategory")
        self.gridLayout.addWidget(self.subcategory, 0, 3, 1, 1)
        self.label_2 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.name = QtWidgets.QComboBox(Dialog)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.name.setFont(font)
        self.name.setEditable(True)
        self.name.setObjectName("name")
        self.gridLayout.addWidget(self.name, 1, 1, 1, 1)
        self.label_12 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.gridLayout.addWidget(self.label_12, 1, 2, 1, 1)
        self.unit = QtWidgets.QComboBox(Dialog)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.unit.setFont(font)
        self.unit.setEditable(True)
        self.unit.setObjectName("unit")
        self.gridLayout.addWidget(self.unit, 1, 3, 1, 1)
        self.label_3 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.brand = QtWidgets.QComboBox(Dialog)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.brand.setFont(font)
        self.brand.setEditable(True)
        self.brand.setObjectName("brand")
        self.gridLayout.addWidget(self.brand, 2, 1, 1, 1)
        self.label_11 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.gridLayout.addWidget(self.label_11, 2, 2, 1, 1)
        self.spec = QtWidgets.QComboBox(Dialog)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.spec.setFont(font)
        self.spec.setEditable(True)
        self.spec.setObjectName("spec")
        self.gridLayout.addWidget(self.spec, 2, 3, 1, 1)
        self.label_4 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.object_ID = QtWidgets.QLineEdit(Dialog)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.object_ID.setFont(font)
        self.object_ID.setObjectName("object_ID")
        self.gridLayout.addWidget(self.object_ID, 3, 1, 1, 1)
        self.label_10 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.gridLayout.addWidget(self.label_10, 3, 2, 1, 1)
        self.serial_ID = QtWidgets.QLineEdit(Dialog)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.serial_ID.setFont(font)
        self.serial_ID.setObjectName("serial_ID")
        self.gridLayout.addWidget(self.serial_ID, 3, 3, 1, 1)
        self.label_5 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 1)
        self.acquire_date = QtWidgets.QDateEdit(Dialog)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.acquire_date.setFont(font)
        self.acquire_date.setCalendarPopup(True)
        self.acquire_date.setObjectName("acquire_date")
        self.gridLayout.addWidget(self.acquire_date, 4, 1, 1, 1)
        self.label_14 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.label_14.setFont(font)
        self.label_14.setObjectName("label_14")
        self.gridLayout.addWidget(self.label_14, 4, 2, 1, 1)
        self.keep_year = QtWidgets.QLineEdit(Dialog)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.keep_year.setFont(font)
        self.keep_year.setObjectName("keep_year")
        self.gridLayout.addWidget(self.keep_year, 4, 3, 1, 1)
        self.label_6 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 5, 0, 1, 1)
        self.price = QtWidgets.QLineEdit(Dialog)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.price.setFont(font)
        self.price.setObjectName("price")
        self.gridLayout.addWidget(self.price, 5, 1, 1, 1)
        self.label_15 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.label_15.setFont(font)
        self.label_15.setObjectName("label_15")
        self.gridLayout.addWidget(self.label_15, 5, 2, 1, 1)
        self.amount = QtWidgets.QLineEdit(Dialog)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.amount.setFont(font)
        self.amount.setObjectName("amount")
        self.gridLayout.addWidget(self.amount, 5, 3, 1, 1)
        self.label_7 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 6, 0, 1, 1)
        self.keep_department = QtWidgets.QComboBox(Dialog)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.keep_department.setFont(font)
        self.keep_department.setEditable(True)
        self.keep_department.setObjectName("keep_department")
        self.gridLayout.addWidget(self.keep_department, 6, 1, 1, 1)
        self.label_16 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.label_16.setFont(font)
        self.label_16.setObjectName("label_16")
        self.gridLayout.addWidget(self.label_16, 6, 2, 1, 1)
        self.place = QtWidgets.QComboBox(Dialog)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.place.setFont(font)
        self.place.setEditable(True)
        self.place.setObjectName("place")
        self.gridLayout.addWidget(self.place, 6, 3, 1, 1)
        self.label_8 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 7, 0, 1, 1)
        self.keeper = QtWidgets.QComboBox(Dialog)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.keeper.setFont(font)
        self.keeper.setEditable(True)
        self.keeper.setObjectName("keeper")
        self.gridLayout.addWidget(self.keeper, 7, 1, 1, 1)
        self.label_17 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.label_17.setFont(font)
        self.label_17.setObjectName("label_17")
        self.gridLayout.addWidget(self.label_17, 7, 2, 1, 1)
        self.use_department = QtWidgets.QComboBox(Dialog)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.use_department.setFont(font)
        self.use_department.setEditable(True)
        self.use_department.setObjectName("use_department")
        self.gridLayout.addWidget(self.use_department, 7, 3, 1, 1)
        self.label_9 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 8, 0, 1, 1)
        self.remark = QtWidgets.QLineEdit(Dialog)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.remark.setFont(font)
        self.remark.setObjectName("remark")
        self.gridLayout.addWidget(self.remark, 8, 1, 1, 3)
        self.verticalLayout.addLayout(self.gridLayout)
        self.line = QtWidgets.QFrame(Dialog)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.line.setFont(font)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_18 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.label_18.setFont(font)
        self.label_18.setObjectName("label_18")
        self.horizontalLayout.addWidget(self.label_18)
        self.last_unregister_date = QtWidgets.QDateEdit(Dialog)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.last_unregister_date.setFont(font)
        self.last_unregister_date.setCalendarPopup(True)
        self.last_unregister_date.setObjectName("last_unregister_date")
        self.horizontalLayout.addWidget(self.last_unregister_date)
        self.label_19 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.label_19.setFont(font)
        self.label_19.setObjectName("label_19")
        self.horizontalLayout.addWidget(self.label_19)
        self.unregistered_count = QtWidgets.QLineEdit(Dialog)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.unregistered_count.setFont(font)
        self.unregistered_count.setObjectName("unregistered_count")
        self.horizontalLayout.addWidget(self.unregistered_count)
        self.label_20 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.label_20.setFont(font)
        self.label_20.setObjectName("label_20")
        self.horizontalLayout.addWidget(self.label_20)
        self.unregistered_amount = QtWidgets.QLineEdit(Dialog)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.unregistered_amount.setFont(font)
        self.unregistered_amount.setObjectName("unregistered_amount")
        self.horizontalLayout.addWidget(self.unregistered_amount)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.line_4 = QtWidgets.QFrame(Dialog)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.line_4.setFont(font)
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.verticalLayout.addWidget(self.line_4)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_21 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.label_21.setFont(font)
        self.label_21.setObjectName("label_21")
        self.horizontalLayout_2.addWidget(self.label_21)
        self.unregister_date = QtWidgets.QDateEdit(Dialog)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.unregister_date.setFont(font)
        self.unregister_date.setCalendarPopup(True)
        self.unregister_date.setObjectName("unregister_date")
        self.horizontalLayout_2.addWidget(self.unregister_date)
        self.label_22 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.label_22.setFont(font)
        self.label_22.setObjectName("label_22")
        self.horizontalLayout_2.addWidget(self.label_22)
        self.unregister_amount = QtWidgets.QLineEdit(Dialog)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.unregister_amount.setFont(font)
        self.unregister_amount.setObjectName("unregister_amount")
        self.horizontalLayout_2.addWidget(self.unregister_amount)
        self.label_23 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.label_23.setFont(font)
        self.label_23.setObjectName("label_23")
        self.horizontalLayout_2.addWidget(self.label_23)
        self.remain_amount = QtWidgets.QLineEdit(Dialog)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.remain_amount.setFont(font)
        self.remain_amount.setObjectName("remain_amount")
        self.horizontalLayout_2.addWidget(self.remain_amount)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_24 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.label_24.setFont(font)
        self.label_24.setObjectName("label_24")
        self.gridLayout_2.addWidget(self.label_24, 0, 0, 1, 1)
        self.unregister_place = QtWidgets.QComboBox(Dialog)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.unregister_place.setFont(font)
        self.unregister_place.setEditable(True)
        self.unregister_place.setObjectName("unregister_place")
        self.gridLayout_2.addWidget(self.unregister_place, 0, 3, 1, 1)
        self.reason = QtWidgets.QComboBox(Dialog)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.reason.setFont(font)
        self.reason.setEditable(True)
        self.reason.setObjectName("reason")
        self.gridLayout_2.addWidget(self.reason, 0, 1, 1, 1)
        self.label_25 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.label_25.setFont(font)
        self.label_25.setObjectName("label_25")
        self.gridLayout_2.addWidget(self.label_25, 0, 2, 1, 1)
        self.label_26 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.label_26.setFont(font)
        self.label_26.setObjectName("label_26")
        self.gridLayout_2.addWidget(self.label_26, 1, 0, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.searchBtn = QtWidgets.QPushButton(Dialog)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.searchBtn.setFont(font)
        self.searchBtn.setAutoDefault(False)
        self.searchBtn.setObjectName("searchBtn")
        self.horizontalLayout_3.addWidget(self.searchBtn)
        self.saveBtn = QtWidgets.QPushButton(Dialog)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.saveBtn.setFont(font)
        self.saveBtn.setAutoDefault(False)
        self.saveBtn.setObjectName("saveBtn")
        self.horizontalLayout_3.addWidget(self.saveBtn)
        self.gridLayout_2.addLayout(self.horizontalLayout_3, 1, 3, 1, 1)
        self.unregister_remark = QtWidgets.QLineEdit(Dialog)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.unregister_remark.setFont(font)
        self.unregister_remark.setObjectName("unregister_remark")
        self.gridLayout_2.addWidget(self.unregister_remark, 1, 1, 1, 2)
        self.verticalLayout.addLayout(self.gridLayout_2)
        self.line_3 = QtWidgets.QFrame(Dialog)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.line_3.setFont(font)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.verticalLayout.addWidget(self.line_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.returnBtn = QtWidgets.QPushButton(Dialog)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.returnBtn.setFont(font)
        self.returnBtn.setDefault(False)
        self.returnBtn.setObjectName("returnBtn")
        self.horizontalLayout_4.addWidget(self.returnBtn)
        self.getPreviousBtn = QtWidgets.QPushButton(Dialog)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.getPreviousBtn.setFont(font)
        self.getPreviousBtn.setObjectName("getPreviousBtn")
        self.horizontalLayout_4.addWidget(self.getPreviousBtn)
        self.getNextBtn = QtWidgets.QPushButton(Dialog)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.getNextBtn.setFont(font)
        self.getNextBtn.setObjectName("getNextBtn")
        self.horizontalLayout_4.addWidget(self.getNextBtn)
        self.deleteBtn = QtWidgets.QPushButton(Dialog)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.deleteBtn.setFont(font)
        self.deleteBtn.setObjectName("deleteBtn")
        self.horizontalLayout_4.addWidget(self.deleteBtn)
        self.formBtn = QtWidgets.QPushButton(Dialog)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.formBtn.setFont(font)
        self.formBtn.setObjectName("formBtn")
        self.horizontalLayout_4.addWidget(self.formBtn)
        self.selectRecordBtn = QtWidgets.QPushButton(Dialog)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.selectRecordBtn.setFont(font)
        self.selectRecordBtn.setObjectName("selectRecordBtn")
        self.horizontalLayout_4.addWidget(self.selectRecordBtn)
        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.retranslateUi(Dialog)
        self.returnBtn.clicked.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.category, self.subcategory)
        Dialog.setTabOrder(self.subcategory, self.name)
        Dialog.setTabOrder(self.name, self.unit)
        Dialog.setTabOrder(self.unit, self.brand)
        Dialog.setTabOrder(self.brand, self.spec)
        Dialog.setTabOrder(self.spec, self.object_ID)
        Dialog.setTabOrder(self.object_ID, self.serial_ID)
        Dialog.setTabOrder(self.serial_ID, self.acquire_date)
        Dialog.setTabOrder(self.acquire_date, self.keep_year)
        Dialog.setTabOrder(self.keep_year, self.price)
        Dialog.setTabOrder(self.price, self.amount)
        Dialog.setTabOrder(self.amount, self.keep_department)
        Dialog.setTabOrder(self.keep_department, self.place)
        Dialog.setTabOrder(self.place, self.keeper)
        Dialog.setTabOrder(self.keeper, self.use_department)
        Dialog.setTabOrder(self.use_department, self.remark)
        Dialog.setTabOrder(self.remark, self.last_unregister_date)
        Dialog.setTabOrder(self.last_unregister_date, self.unregistered_count)
        Dialog.setTabOrder(self.unregistered_count, self.unregistered_amount)
        Dialog.setTabOrder(self.unregistered_amount, self.unregister_date)
        Dialog.setTabOrder(self.unregister_date, self.unregister_amount)
        Dialog.setTabOrder(self.unregister_amount, self.remain_amount)
        Dialog.setTabOrder(self.remain_amount, self.reason)
        Dialog.setTabOrder(self.reason, self.unregister_place)
        Dialog.setTabOrder(self.unregister_place, self.unregister_remark)
        Dialog.setTabOrder(self.unregister_remark, self.searchBtn)
        Dialog.setTabOrder(self.searchBtn, self.saveBtn)
        Dialog.setTabOrder(self.saveBtn, self.returnBtn)
        Dialog.setTabOrder(self.returnBtn, self.getPreviousBtn)
        Dialog.setTabOrder(self.getPreviousBtn, self.getNextBtn)
        Dialog.setTabOrder(self.getNextBtn, self.deleteBtn)
        Dialog.setTabOrder(self.deleteBtn, self.formBtn)
        Dialog.setTabOrder(self.formBtn, self.selectRecordBtn)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "物品大項："))
        self.label_13.setText(_translate("Dialog", "物品細目："))
        self.label_2.setText(_translate("Dialog", "物品名稱："))
        self.label_12.setText(_translate("Dialog", "單位："))
        self.label_3.setText(_translate("Dialog", "品牌："))
        self.label_11.setText(_translate("Dialog", "規格："))
        self.label_4.setText(_translate("Dialog", "物品編號："))
        self.label_10.setText(_translate("Dialog", "流水號："))
        self.label_5.setText(_translate("Dialog", "取得日期："))
        self.label_14.setText(_translate("Dialog", "保存年限："))
        self.label_6.setText(_translate("Dialog", "單價："))
        self.label_15.setText(_translate("Dialog", "數量："))
        self.label_7.setText(_translate("Dialog", "保管單位："))
        self.label_16.setText(_translate("Dialog", "存置地點："))
        self.label_8.setText(_translate("Dialog", "保管人："))
        self.label_17.setText(_translate("Dialog", "使用單位："))
        self.label_9.setText(_translate("Dialog", "備註："))
        self.label_18.setText(_translate("Dialog", "上次除帳："))
        self.label_19.setText(_translate("Dialog", "除帳次數："))
        self.label_20.setText(_translate("Dialog", "除帳數量："))
        self.label_21.setText(_translate("Dialog", "除帳日期："))
        self.label_22.setText(_translate("Dialog", "除帳數量："))
        self.label_23.setText(_translate("Dialog", "剩餘數量："))
        self.label_24.setText(_translate("Dialog", "除帳原因："))
        self.label_25.setText(_translate("Dialog", "繳存地點："))
        self.label_26.setText(_translate("Dialog", "備註事項："))
        self.searchBtn.setText(_translate("Dialog", "檢索"))
        self.saveBtn.setText(_translate("Dialog", "本筆存入"))
        self.returnBtn.setText(_translate("Dialog", "退回"))
        self.getPreviousBtn.setText(_translate("Dialog", "上一筆"))
        self.getNextBtn.setText(_translate("Dialog", "下一筆"))
        self.deleteBtn.setText(_translate("Dialog", "刪除本筆"))
        self.formBtn.setText(_translate("Dialog", "除帳表單"))
        self.selectRecordBtn.setText(_translate("Dialog", "選取資料"))

