# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'register.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        Dialog.resize(850, 470)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        Dialog.setFont(font)
        self.layoutWidget = QtWidgets.QWidget(Dialog)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 832, 452))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_24 = QtWidgets.QLabel(self.layoutWidget)
        self.label_24.setMinimumSize(QtCore.QSize(105, 33))
        self.label_24.setMaximumSize(QtCore.QSize(105, 33))
        self.label_24.setObjectName("label_24")
        self.gridLayout.addWidget(self.label_24, 0, 0, 1, 1)
        self.category = QtWidgets.QComboBox(self.layoutWidget)
        self.category.setEnabled(False)
        self.category.setMinimumSize(QtCore.QSize(300, 33))
        self.category.setMaximumSize(QtCore.QSize(300, 33))
        self.category.setEditable(False)
        self.category.setObjectName("category")
        self.gridLayout.addWidget(self.category, 0, 1, 1, 1)
        self.label_25 = QtWidgets.QLabel(self.layoutWidget)
        self.label_25.setMinimumSize(QtCore.QSize(105, 33))
        self.label_25.setMaximumSize(QtCore.QSize(105, 33))
        self.label_25.setObjectName("label_25")
        self.gridLayout.addWidget(self.label_25, 0, 2, 1, 1)
        self.subcategory = QtWidgets.QComboBox(self.layoutWidget)
        self.subcategory.setEnabled(False)
        self.subcategory.setMinimumSize(QtCore.QSize(300, 33))
        self.subcategory.setMaximumSize(QtCore.QSize(300, 33))
        self.subcategory.setObjectName("subcategory")
        self.gridLayout.addWidget(self.subcategory, 0, 3, 1, 1)
        self.label_23 = QtWidgets.QLabel(self.layoutWidget)
        self.label_23.setMinimumSize(QtCore.QSize(105, 33))
        self.label_23.setMaximumSize(QtCore.QSize(105, 33))
        self.label_23.setObjectName("label_23")
        self.gridLayout.addWidget(self.label_23, 1, 0, 1, 1)
        self.name = QtWidgets.QComboBox(self.layoutWidget)
        self.name.setEnabled(False)
        self.name.setMinimumSize(QtCore.QSize(300, 33))
        self.name.setMaximumSize(QtCore.QSize(300, 33))
        self.name.setEditable(True)
        self.name.setInsertPolicy(QtWidgets.QComboBox.InsertAtTop)
        self.name.setObjectName("name")
        self.gridLayout.addWidget(self.name, 1, 1, 1, 1)
        self.label_22 = QtWidgets.QLabel(self.layoutWidget)
        self.label_22.setMinimumSize(QtCore.QSize(105, 33))
        self.label_22.setMaximumSize(QtCore.QSize(105, 33))
        self.label_22.setObjectName("label_22")
        self.gridLayout.addWidget(self.label_22, 1, 2, 1, 1)
        self.unit = QtWidgets.QComboBox(self.layoutWidget)
        self.unit.setEnabled(False)
        self.unit.setMinimumSize(QtCore.QSize(300, 33))
        self.unit.setMaximumSize(QtCore.QSize(300, 33))
        self.unit.setEditable(True)
        self.unit.setInsertPolicy(QtWidgets.QComboBox.InsertAtTop)
        self.unit.setObjectName("unit")
        self.gridLayout.addWidget(self.unit, 1, 3, 1, 1)
        self.label_27 = QtWidgets.QLabel(self.layoutWidget)
        self.label_27.setMinimumSize(QtCore.QSize(105, 33))
        self.label_27.setMaximumSize(QtCore.QSize(105, 33))
        self.label_27.setObjectName("label_27")
        self.gridLayout.addWidget(self.label_27, 2, 0, 1, 1)
        self.brand = QtWidgets.QComboBox(self.layoutWidget)
        self.brand.setEnabled(False)
        self.brand.setMinimumSize(QtCore.QSize(300, 33))
        self.brand.setMaximumSize(QtCore.QSize(300, 33))
        self.brand.setEditable(True)
        self.brand.setInsertPolicy(QtWidgets.QComboBox.InsertAtTop)
        self.brand.setObjectName("brand")
        self.gridLayout.addWidget(self.brand, 2, 1, 1, 1)
        self.label_26 = QtWidgets.QLabel(self.layoutWidget)
        self.label_26.setMinimumSize(QtCore.QSize(105, 33))
        self.label_26.setMaximumSize(QtCore.QSize(105, 33))
        self.label_26.setObjectName("label_26")
        self.gridLayout.addWidget(self.label_26, 2, 2, 1, 1)
        self.spec = QtWidgets.QComboBox(self.layoutWidget)
        self.spec.setEnabled(False)
        self.spec.setMinimumSize(QtCore.QSize(300, 33))
        self.spec.setMaximumSize(QtCore.QSize(300, 33))
        self.spec.setEditable(True)
        self.spec.setInsertPolicy(QtWidgets.QComboBox.InsertAtTop)
        self.spec.setObjectName("spec")
        self.gridLayout.addWidget(self.spec, 2, 3, 1, 1)
        self.label_28 = QtWidgets.QLabel(self.layoutWidget)
        self.label_28.setMinimumSize(QtCore.QSize(105, 37))
        self.label_28.setMaximumSize(QtCore.QSize(105, 37))
        self.label_28.setObjectName("label_28")
        self.gridLayout.addWidget(self.label_28, 3, 0, 1, 1)
        self.object_ID = QtWidgets.QLineEdit(self.layoutWidget)
        self.object_ID.setEnabled(False)
        self.object_ID.setMinimumSize(QtCore.QSize(300, 33))
        self.object_ID.setMaximumSize(QtCore.QSize(300, 33))
        self.object_ID.setReadOnly(True)
        self.object_ID.setObjectName("object_ID")
        self.gridLayout.addWidget(self.object_ID, 3, 1, 1, 1)
        self.label_29 = QtWidgets.QLabel(self.layoutWidget)
        self.label_29.setMinimumSize(QtCore.QSize(105, 37))
        self.label_29.setMaximumSize(QtCore.QSize(105, 37))
        self.label_29.setObjectName("label_29")
        self.gridLayout.addWidget(self.label_29, 3, 2, 1, 1)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.serial_ID = QtWidgets.QLineEdit(self.layoutWidget)
        self.serial_ID.setEnabled(False)
        self.serial_ID.setMinimumSize(QtCore.QSize(180, 33))
        self.serial_ID.setMaximumSize(QtCore.QSize(180, 33))
        self.serial_ID.setReadOnly(True)
        self.serial_ID.setObjectName("serial_ID")
        self.horizontalLayout_8.addWidget(self.serial_ID)
        self.lookupSerialBtn = QtWidgets.QPushButton(self.layoutWidget)
        self.lookupSerialBtn.setMinimumSize(QtCore.QSize(113, 35))
        self.lookupSerialBtn.setMaximumSize(QtCore.QSize(113, 35))
        self.lookupSerialBtn.setObjectName("lookupSerialBtn")
        self.horizontalLayout_8.addWidget(self.lookupSerialBtn)
        self.gridLayout.addLayout(self.horizontalLayout_8, 3, 3, 1, 1)
        self.label_30 = QtWidgets.QLabel(self.layoutWidget)
        self.label_30.setMinimumSize(QtCore.QSize(105, 33))
        self.label_30.setMaximumSize(QtCore.QSize(105, 33))
        self.label_30.setObjectName("label_30")
        self.gridLayout.addWidget(self.label_30, 4, 0, 1, 1)
        self.purchase_date = QtWidgets.QDateEdit(self.layoutWidget)
        self.purchase_date.setEnabled(False)
        self.purchase_date.setMinimumSize(QtCore.QSize(301, 33))
        self.purchase_date.setMaximumSize(QtCore.QSize(301, 33))
        self.purchase_date.setCalendarPopup(True)
        self.purchase_date.setObjectName("purchase_date")
        self.gridLayout.addWidget(self.purchase_date, 4, 1, 1, 1)
        self.label_31 = QtWidgets.QLabel(self.layoutWidget)
        self.label_31.setMinimumSize(QtCore.QSize(105, 33))
        self.label_31.setMaximumSize(QtCore.QSize(105, 33))
        self.label_31.setObjectName("label_31")
        self.gridLayout.addWidget(self.label_31, 4, 2, 1, 1)
        self.acquire_date = QtWidgets.QDateEdit(self.layoutWidget)
        self.acquire_date.setEnabled(False)
        self.acquire_date.setMinimumSize(QtCore.QSize(301, 33))
        self.acquire_date.setMaximumSize(QtCore.QSize(301, 33))
        self.acquire_date.setCalendarPopup(True)
        self.acquire_date.setObjectName("acquire_date")
        self.gridLayout.addWidget(self.acquire_date, 4, 3, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_32 = QtWidgets.QLabel(self.layoutWidget)
        self.label_32.setMinimumSize(QtCore.QSize(63, 27))
        self.label_32.setMaximumSize(QtCore.QSize(63, 27))
        self.label_32.setObjectName("label_32")
        self.horizontalLayout.addWidget(self.label_32)
        self.source = QtWidgets.QComboBox(self.layoutWidget)
        self.source.setEnabled(False)
        self.source.setMinimumSize(QtCore.QSize(201, 33))
        self.source.setMaximumSize(QtCore.QSize(201, 33))
        self.source.setEditable(False)
        self.source.setInsertPolicy(QtWidgets.QComboBox.InsertAtTop)
        self.source.setObjectName("source")
        self.horizontalLayout.addWidget(self.source)
        self.label_33 = QtWidgets.QLabel(self.layoutWidget)
        self.label_33.setMinimumSize(QtCore.QSize(63, 27))
        self.label_33.setMaximumSize(QtCore.QSize(63, 27))
        self.label_33.setObjectName("label_33")
        self.horizontalLayout.addWidget(self.label_33)
        self.price = QtWidgets.QLineEdit(self.layoutWidget)
        self.price.setEnabled(False)
        self.price.setMinimumSize(QtCore.QSize(201, 33))
        self.price.setMaximumSize(QtCore.QSize(201, 33))
        self.price.setObjectName("price")
        self.horizontalLayout.addWidget(self.price)
        self.label_34 = QtWidgets.QLabel(self.layoutWidget)
        self.label_34.setMinimumSize(QtCore.QSize(63, 27))
        self.label_34.setMaximumSize(QtCore.QSize(63, 27))
        self.label_34.setObjectName("label_34")
        self.horizontalLayout.addWidget(self.label_34)
        self.amount = QtWidgets.QLineEdit(self.layoutWidget)
        self.amount.setEnabled(False)
        self.amount.setMinimumSize(QtCore.QSize(201, 33))
        self.amount.setMaximumSize(QtCore.QSize(201, 33))
        self.amount.setObjectName("amount")
        self.horizontalLayout.addWidget(self.amount)
        self.gridLayout.addLayout(self.horizontalLayout, 5, 0, 1, 4)
        self.label_37 = QtWidgets.QLabel(self.layoutWidget)
        self.label_37.setMinimumSize(QtCore.QSize(105, 35))
        self.label_37.setMaximumSize(QtCore.QSize(105, 35))
        self.label_37.setObjectName("label_37")
        self.gridLayout.addWidget(self.label_37, 6, 0, 1, 1)
        self.place = QtWidgets.QComboBox(self.layoutWidget)
        self.place.setEnabled(False)
        self.place.setMinimumSize(QtCore.QSize(300, 33))
        self.place.setMaximumSize(QtCore.QSize(300, 33))
        self.place.setEditable(True)
        self.place.setInsertPolicy(QtWidgets.QComboBox.InsertAtTop)
        self.place.setObjectName("place")
        self.gridLayout.addWidget(self.place, 6, 1, 1, 1)
        self.label_36 = QtWidgets.QLabel(self.layoutWidget)
        self.label_36.setMinimumSize(QtCore.QSize(105, 35))
        self.label_36.setMaximumSize(QtCore.QSize(105, 35))
        self.label_36.setObjectName("label_36")
        self.gridLayout.addWidget(self.label_36, 6, 2, 1, 1)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.keep_year = QtWidgets.QLineEdit(self.layoutWidget)
        self.keep_year.setEnabled(False)
        self.keep_year.setMinimumSize(QtCore.QSize(267, 33))
        self.keep_year.setMaximumSize(QtCore.QSize(267, 33))
        self.keep_year.setObjectName("keep_year")
        self.horizontalLayout_5.addWidget(self.keep_year)
        self.label_21 = QtWidgets.QLabel(self.layoutWidget)
        self.label_21.setMinimumSize(QtCore.QSize(26, 33))
        self.label_21.setMaximumSize(QtCore.QSize(26, 33))
        self.label_21.setObjectName("label_21")
        self.horizontalLayout_5.addWidget(self.label_21)
        self.gridLayout.addLayout(self.horizontalLayout_5, 6, 3, 1, 1)
        self.label_38 = QtWidgets.QLabel(self.layoutWidget)
        self.label_38.setMinimumSize(QtCore.QSize(105, 33))
        self.label_38.setMaximumSize(QtCore.QSize(105, 33))
        self.label_38.setObjectName("label_38")
        self.gridLayout.addWidget(self.label_38, 7, 0, 1, 1)
        self.keep_department = QtWidgets.QComboBox(self.layoutWidget)
        self.keep_department.setEnabled(False)
        self.keep_department.setMinimumSize(QtCore.QSize(300, 33))
        self.keep_department.setMaximumSize(QtCore.QSize(300, 33))
        self.keep_department.setEditable(True)
        self.keep_department.setInsertPolicy(QtWidgets.QComboBox.InsertAtTop)
        self.keep_department.setObjectName("keep_department")
        self.gridLayout.addWidget(self.keep_department, 7, 1, 1, 1)
        self.label_35 = QtWidgets.QLabel(self.layoutWidget)
        self.label_35.setMinimumSize(QtCore.QSize(105, 33))
        self.label_35.setMaximumSize(QtCore.QSize(105, 33))
        self.label_35.setObjectName("label_35")
        self.gridLayout.addWidget(self.label_35, 7, 2, 1, 1)
        self.use_department = QtWidgets.QComboBox(self.layoutWidget)
        self.use_department.setEnabled(False)
        self.use_department.setMinimumSize(QtCore.QSize(300, 33))
        self.use_department.setMaximumSize(QtCore.QSize(300, 33))
        self.use_department.setEditable(True)
        self.use_department.setInsertPolicy(QtWidgets.QComboBox.InsertAtTop)
        self.use_department.setObjectName("use_department")
        self.gridLayout.addWidget(self.use_department, 7, 3, 1, 1)
        self.label_39 = QtWidgets.QLabel(self.layoutWidget)
        self.label_39.setMinimumSize(QtCore.QSize(105, 33))
        self.label_39.setMaximumSize(QtCore.QSize(105, 33))
        self.label_39.setObjectName("label_39")
        self.gridLayout.addWidget(self.label_39, 8, 0, 1, 1)
        self.keeper = QtWidgets.QComboBox(self.layoutWidget)
        self.keeper.setEnabled(False)
        self.keeper.setMinimumSize(QtCore.QSize(300, 33))
        self.keeper.setMaximumSize(QtCore.QSize(300, 33))
        self.keeper.setEditable(True)
        self.keeper.setInsertPolicy(QtWidgets.QComboBox.InsertAtTop)
        self.keeper.setObjectName("keeper")
        self.gridLayout.addWidget(self.keeper, 8, 1, 1, 1)
        self.label_40 = QtWidgets.QLabel(self.layoutWidget)
        self.label_40.setMinimumSize(QtCore.QSize(105, 37))
        self.label_40.setMaximumSize(QtCore.QSize(105, 37))
        self.label_40.setObjectName("label_40")
        self.gridLayout.addWidget(self.label_40, 9, 0, 1, 1)
        self.remark = QtWidgets.QComboBox(self.layoutWidget)
        self.remark.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.remark.sizePolicy().hasHeightForWidth())
        self.remark.setSizePolicy(sizePolicy)
        self.remark.setMinimumSize(QtCore.QSize(411, 37))
        self.remark.setMaximumSize(QtCore.QSize(411, 37))
        self.remark.setEditable(True)
        self.remark.setInsertPolicy(QtWidgets.QComboBox.InsertAtTop)
        self.remark.setObjectName("remark")
        self.gridLayout.addWidget(self.remark, 9, 1, 1, 2)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.searchBtn = QtWidgets.QPushButton(self.layoutWidget)
        self.searchBtn.setMinimumSize(QtCore.QSize(147, 35))
        self.searchBtn.setMaximumSize(QtCore.QSize(147, 35))
        self.searchBtn.setObjectName("searchBtn")
        self.horizontalLayout_6.addWidget(self.searchBtn)
        self.saveBtn = QtWidgets.QPushButton(self.layoutWidget)
        self.saveBtn.setMinimumSize(QtCore.QSize(146, 35))
        self.saveBtn.setMaximumSize(QtCore.QSize(146, 35))
        self.saveBtn.setObjectName("saveBtn")
        self.horizontalLayout_6.addWidget(self.saveBtn)
        self.gridLayout.addLayout(self.horizontalLayout_6, 9, 3, 1, 1)
        self.line_2 = QtWidgets.QFrame(self.layoutWidget)
        self.line_2.setMinimumSize(QtCore.QSize(0, 5))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout.addWidget(self.line_2, 10, 0, 1, 4)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.returnBtn = QtWidgets.QPushButton(self.layoutWidget)
        self.returnBtn.setObjectName("returnBtn")
        self.horizontalLayout_7.addWidget(self.returnBtn)
        self.getPreviousBtn = QtWidgets.QPushButton(self.layoutWidget)
        self.getPreviousBtn.setObjectName("getPreviousBtn")
        self.horizontalLayout_7.addWidget(self.getPreviousBtn)
        self.getNextBtn = QtWidgets.QPushButton(self.layoutWidget)
        self.getNextBtn.setObjectName("getNextBtn")
        self.horizontalLayout_7.addWidget(self.getNextBtn)
        self.deleteBtn = QtWidgets.QPushButton(self.layoutWidget)
        self.deleteBtn.setObjectName("deleteBtn")
        self.horizontalLayout_7.addWidget(self.deleteBtn)
        self.formBtn = QtWidgets.QPushButton(self.layoutWidget)
        self.formBtn.setObjectName("formBtn")
        self.horizontalLayout_7.addWidget(self.formBtn)
        self.createBtn = QtWidgets.QPushButton(self.layoutWidget)
        self.createBtn.setObjectName("createBtn")
        self.horizontalLayout_7.addWidget(self.createBtn)
        self.gridLayout.addLayout(self.horizontalLayout_7, 11, 0, 1, 4)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "入帳"))
        self.label_24.setText(_translate("Dialog", "物品大項："))
        self.label_25.setText(_translate("Dialog", "物品細目："))
        self.label_23.setText(_translate("Dialog", "物品名稱："))
        self.label_22.setText(_translate("Dialog", "單位："))
        self.label_27.setText(_translate("Dialog", "品牌："))
        self.label_26.setText(_translate("Dialog", "規格："))
        self.label_28.setText(_translate("Dialog", "物品編號："))
        self.label_29.setText(_translate("Dialog", "流水號"))
        self.lookupSerialBtn.setText(_translate("Dialog", "流水號總覽"))
        self.label_30.setText(_translate("Dialog", "購置日期："))
        self.purchase_date.setDisplayFormat(_translate("Dialog", "yyyy-MM-dd"))
        self.label_31.setText(_translate("Dialog", "取得日期："))
        self.acquire_date.setDisplayFormat(_translate("Dialog", "yyyy-MM-dd"))
        self.label_32.setText(_translate("Dialog", "來源："))
        self.label_33.setText(_translate("Dialog", "單價："))
        self.label_34.setText(_translate("Dialog", "數量："))
        self.label_37.setText(_translate("Dialog", "存置地點："))
        self.label_36.setText(_translate("Dialog", "保管年限："))
        self.label_21.setText(_translate("Dialog", "年 "))
        self.label_38.setText(_translate("Dialog", "保管單位："))
        self.label_35.setText(_translate("Dialog", "使用單位："))
        self.label_39.setText(_translate("Dialog", "保管人：    "))
        self.label_40.setText(_translate("Dialog", "備註事項："))
        self.searchBtn.setText(_translate("Dialog", "檢索"))
        self.saveBtn.setText(_translate("Dialog", "本筆存入"))
        self.returnBtn.setText(_translate("Dialog", "返回"))
        self.getPreviousBtn.setText(_translate("Dialog", "上一筆"))
        self.getNextBtn.setText(_translate("Dialog", "下一筆"))
        self.deleteBtn.setText(_translate("Dialog", "刪除本筆"))
        self.formBtn.setText(_translate("Dialog", "表單"))
        self.createBtn.setText(_translate("Dialog", "新增一筆"))

