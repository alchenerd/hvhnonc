# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'searchbox.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        Dialog.resize(320, 90)
        Dialog.setMinimumSize(QtCore.QSize(320, 90))
        Dialog.setMaximumSize(QtCore.QSize(320, 90))
        Dialog.setModal(False)
        self.query = QtWidgets.QLineEdit(Dialog)
        self.query.setGeometry(QtCore.QRect(10, 10, 301, 33))
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.query.setFont(font)
        self.query.setObjectName("query")
        self.cancelBtn = QtWidgets.QPushButton(Dialog)
        self.cancelBtn.setGeometry(QtCore.QRect(60, 50, 125, 35))
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.cancelBtn.setFont(font)
        self.cancelBtn.setAutoDefault(False)
        self.cancelBtn.setObjectName("cancelBtn")
        self.searchBtn = QtWidgets.QPushButton(Dialog)
        self.searchBtn.setGeometry(QtCore.QRect(190, 50, 125, 35))
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.searchBtn.setFont(font)
        self.searchBtn.setObjectName("searchBtn")

        self.retranslateUi(Dialog)
        self.cancelBtn.clicked.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "搜尋"))
        self.cancelBtn.setText(_translate("Dialog", "取消"))
        self.searchBtn.setText(_translate("Dialog", "搜尋"))

