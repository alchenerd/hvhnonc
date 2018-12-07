# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'index.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(640, 320)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.welcomeImage = QtWidgets.QLabel(self.centralwidget)
        self.welcomeImage.setGeometry(QtCore.QRect(10, 10, 400, 300))
        self.welcomeImage.setObjectName("welcomeImage")
        self.addBtn = QtWidgets.QPushButton(self.centralwidget)
        self.addBtn.setGeometry(QtCore.QRect(430, 10, 200, 60))
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.addBtn.setFont(font)
        self.addBtn.setObjectName("addBtn")
        self.removeBtn = QtWidgets.QPushButton(self.centralwidget)
        self.removeBtn.setGeometry(QtCore.QRect(430, 70, 200, 60))
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.removeBtn.setFont(font)
        self.removeBtn.setObjectName("removeBtn")
        self.maintenanceBtn = QtWidgets.QPushButton(self.centralwidget)
        self.maintenanceBtn.setGeometry(QtCore.QRect(430, 190, 200, 60))
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.maintenanceBtn.setFont(font)
        self.maintenanceBtn.setObjectName("maintenanceBtn")
        self.printBtn = QtWidgets.QPushButton(self.centralwidget)
        self.printBtn.setGeometry(QtCore.QRect(430, 130, 200, 60))
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.printBtn.setFont(font)
        self.printBtn.setObjectName("printBtn")
        self.quitBtn = QtWidgets.QPushButton(self.centralwidget)
        self.quitBtn.setGeometry(QtCore.QRect(430, 250, 200, 60))
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.quitBtn.setFont(font)
        self.quitBtn.setObjectName("quitBtn")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.addBtn, self.removeBtn)
        MainWindow.setTabOrder(self.removeBtn, self.printBtn)
        MainWindow.setTabOrder(self.printBtn, self.maintenanceBtn)
        MainWindow.setTabOrder(self.maintenanceBtn, self.quitBtn)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "花蓮榮家非消耗品管理系統"))
        self.welcomeImage.setText(_translate("MainWindow", "<html><head/><body><p><img src=\":/index/kaiba.gif\"/></p></body></html>"))
        self.addBtn.setText(_translate("MainWindow", "入帳"))
        self.removeBtn.setText(_translate("MainWindow", "除帳"))
        self.maintenanceBtn.setText(_translate("MainWindow", "維護"))
        self.printBtn.setText(_translate("MainWindow", "列印"))
        self.quitBtn.setText(_translate("MainWindow", "離開"))

import myqtpy_rc
