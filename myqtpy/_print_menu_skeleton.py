# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'printmenu.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(648, 421)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.rb_register = QtWidgets.QRadioButton(Dialog)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.rb_register.setFont(font)
        self.rb_register.setObjectName("rb_register")
        self.gridLayout.addWidget(self.rb_register, 0, 0, 1, 1)
        self.rb_unregister = QtWidgets.QRadioButton(Dialog)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.rb_unregister.setFont(font)
        self.rb_unregister.setObjectName("rb_unregister")
        self.gridLayout.addWidget(self.rb_unregister, 0, 1, 1, 1)
        self.rb_monthly = QtWidgets.QRadioButton(Dialog)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.rb_monthly.setFont(font)
        self.rb_monthly.setObjectName("rb_monthly")
        self.gridLayout.addWidget(self.rb_monthly, 1, 0, 1, 1)
        self.rb_full = QtWidgets.QRadioButton(Dialog)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.rb_full.setFont(font)
        self.rb_full.setObjectName("rb_full")
        self.gridLayout.addWidget(self.rb_full, 1, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label, 0, QtCore.Qt.AlignLeft)
        self.purchase_date_chk = QtWidgets.QCheckBox(Dialog)
        self.purchase_date_chk.setText("")
        self.purchase_date_chk.setObjectName("purchase_date_chk")
        self.horizontalLayout.addWidget(self.purchase_date_chk)
        self.purchase_date_min = QtWidgets.QDateEdit(Dialog)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.purchase_date_min.setFont(font)
        self.purchase_date_min.setCalendarPopup(True)
        self.purchase_date_min.setObjectName("purchase_date_min")
        self.horizontalLayout.addWidget(self.purchase_date_min, 0, QtCore.Qt.AlignLeft)
        self.label_2 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2, 0, QtCore.Qt.AlignLeft)
        self.purchase_date_max = QtWidgets.QDateEdit(Dialog)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.purchase_date_max.setFont(font)
        self.purchase_date_max.setCalendarPopup(True)
        self.purchase_date_max.setObjectName("purchase_date_max")
        self.horizontalLayout.addWidget(self.purchase_date_max, 0, QtCore.Qt.AlignLeft)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_4 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_2.addWidget(self.label_4, 0, QtCore.Qt.AlignLeft)
        self.edit_date_chk = QtWidgets.QCheckBox(Dialog)
        self.edit_date_chk.setText("")
        self.edit_date_chk.setObjectName("edit_date_chk")
        self.horizontalLayout_2.addWidget(self.edit_date_chk)
        self.edit_date_min = QtWidgets.QDateEdit(Dialog)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.edit_date_min.setFont(font)
        self.edit_date_min.setCalendarPopup(True)
        self.edit_date_min.setObjectName("edit_date_min")
        self.horizontalLayout_2.addWidget(self.edit_date_min, 0, QtCore.Qt.AlignLeft)
        self.label_5 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_2.addWidget(self.label_5, 0, QtCore.Qt.AlignLeft)
        self.edit_date_max = QtWidgets.QDateEdit(Dialog)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.edit_date_max.setFont(font)
        self.edit_date_max.setCalendarPopup(True)
        self.edit_date_max.setObjectName("edit_date_max")
        self.horizontalLayout_2.addWidget(self.edit_date_max, 0, QtCore.Qt.AlignLeft)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.line = QtWidgets.QFrame(Dialog)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.subcategory = QtWidgets.QComboBox(Dialog)
        self.subcategory.setMinimumSize(QtCore.QSize(200, 0))
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.subcategory.setFont(font)
        self.subcategory.setEditable(True)
        self.subcategory.setObjectName("subcategory")
        self.gridLayout_2.addWidget(self.subcategory, 0, 3, 1, 1)
        self.category = QtWidgets.QComboBox(Dialog)
        self.category.setMinimumSize(QtCore.QSize(200, 0))
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.category.setFont(font)
        self.category.setEditable(True)
        self.category.setObjectName("category")
        self.gridLayout_2.addWidget(self.category, 0, 1, 1, 1)
        self.label_7 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 0, 0, 1, 1)
        self.label_8 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.gridLayout_2.addWidget(self.label_8, 0, 2, 1, 1)
        self.clearBtn = QtWidgets.QPushButton(Dialog)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.clearBtn.setFont(font)
        self.clearBtn.setObjectName("clearBtn")
        self.gridLayout_2.addWidget(self.clearBtn, 1, 3, 1, 1)
        self.label_11 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.gridLayout_2.addWidget(self.label_11, 3, 0, 1, 1)
        self.label_10 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.gridLayout_2.addWidget(self.label_10, 2, 0, 1, 1)
        self.place = QtWidgets.QComboBox(Dialog)
        self.place.setMinimumSize(QtCore.QSize(200, 0))
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.place.setFont(font)
        self.place.setEditable(True)
        self.place.setObjectName("place")
        self.gridLayout_2.addWidget(self.place, 2, 1, 1, 1)
        self.use_department = QtWidgets.QComboBox(Dialog)
        self.use_department.setMinimumSize(QtCore.QSize(200, 0))
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.use_department.setFont(font)
        self.use_department.setEditable(True)
        self.use_department.setObjectName("use_department")
        self.gridLayout_2.addWidget(self.use_department, 3, 3, 1, 1)
        self.keep_department = QtWidgets.QComboBox(Dialog)
        self.keep_department.setMinimumSize(QtCore.QSize(200, 0))
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.keep_department.setFont(font)
        self.keep_department.setEditable(True)
        self.keep_department.setObjectName("keep_department")
        self.gridLayout_2.addWidget(self.keep_department, 3, 1, 1, 1)
        self.label_13 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.label_13.setFont(font)
        self.label_13.setObjectName("label_13")
        self.gridLayout_2.addWidget(self.label_13, 3, 2, 1, 1)
        self.name = QtWidgets.QComboBox(Dialog)
        self.name.setMinimumSize(QtCore.QSize(200, 0))
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.name.setFont(font)
        self.name.setEditable(True)
        self.name.setObjectName("name")
        self.gridLayout_2.addWidget(self.name, 1, 1, 1, 2)
        self.label_9 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.gridLayout_2.addWidget(self.label_9, 1, 0, 1, 1)
        self.label_12 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.gridLayout_2.addWidget(self.label_12, 4, 0, 1, 1)
        self.keeper = QtWidgets.QComboBox(Dialog)
        self.keeper.setMinimumSize(QtCore.QSize(200, 0))
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.keeper.setFont(font)
        self.keeper.setEditable(True)
        self.keeper.setObjectName("keeper")
        self.gridLayout_2.addWidget(self.keeper, 4, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.quitBtn = QtWidgets.QPushButton(Dialog)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.quitBtn.setFont(font)
        self.quitBtn.setObjectName("quitBtn")
        self.horizontalLayout_3.addWidget(self.quitBtn)
        self.previewBtn = QtWidgets.QPushButton(Dialog)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.previewBtn.setFont(font)
        self.previewBtn.setObjectName("previewBtn")
        self.horizontalLayout_3.addWidget(self.previewBtn)
        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.retranslateUi(Dialog)
        self.quitBtn.clicked.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.rb_register, self.rb_monthly)
        Dialog.setTabOrder(self.rb_monthly, self.rb_full)
        Dialog.setTabOrder(self.rb_full, self.rb_unregister)
        Dialog.setTabOrder(self.rb_unregister, self.purchase_date_chk)
        Dialog.setTabOrder(self.purchase_date_chk, self.purchase_date_min)
        Dialog.setTabOrder(self.purchase_date_min, self.purchase_date_max)
        Dialog.setTabOrder(self.purchase_date_max, self.edit_date_chk)
        Dialog.setTabOrder(self.edit_date_chk, self.edit_date_min)
        Dialog.setTabOrder(self.edit_date_min, self.edit_date_max)
        Dialog.setTabOrder(self.edit_date_max, self.category)
        Dialog.setTabOrder(self.category, self.subcategory)
        Dialog.setTabOrder(self.subcategory, self.name)
        Dialog.setTabOrder(self.name, self.clearBtn)
        Dialog.setTabOrder(self.clearBtn, self.place)
        Dialog.setTabOrder(self.place, self.keep_department)
        Dialog.setTabOrder(self.keep_department, self.use_department)
        Dialog.setTabOrder(self.use_department, self.keeper)
        Dialog.setTabOrder(self.keeper, self.quitBtn)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "列印報表"))
        self.rb_register.setText(_translate("Dialog", "[建帳]增加單"))
        self.rb_unregister.setText(_translate("Dialog", "[除帳]減損單"))
        self.rb_monthly.setText(_translate("Dialog", "統計月報表"))
        self.rb_full.setText(_translate("Dialog", "非消耗品清冊"))
        self.label.setText(_translate("Dialog", "購置日期範圍："))
        self.label_2.setText(_translate("Dialog", "~"))
        self.label_4.setText(_translate("Dialog", "建帳除帳日期："))
        self.label_5.setText(_translate("Dialog", "~"))
        self.label_7.setText(_translate("Dialog", "物品大項："))
        self.label_8.setText(_translate("Dialog", "物品細目："))
        self.clearBtn.setText(_translate("Dialog", "清空選項"))
        self.label_11.setText(_translate("Dialog", "保管單位："))
        self.label_10.setText(_translate("Dialog", "存置地點："))
        self.label_13.setText(_translate("Dialog", "使用單位："))
        self.label_9.setText(_translate("Dialog", "物品名稱："))
        self.label_12.setText(_translate("Dialog", "保管人："))
        self.quitBtn.setText(_translate("Dialog", "離開"))
        self.previewBtn.setText(_translate("Dialog", "產生並預覽表單"))

