# -*- coding: utf-8 -*-
"""
@author: alchenerd (alchenerd@gmail.com)
"""

from PyQt5 import QtWidgets
if __name__ == '__main__':
    from _login_skeleton import Ui_Dialog as LoginDialog
else:
    from myqtpy._login_skeleton import Ui_Dialog as LoginDialog


class Login(QtWidgets.QDialog, LoginDialog):
    def __init__(self, dialog):
        super(self.__class__, self).__init__(dialog)
        self.setupUi(dialog)

    def setupUi(self, Dialog):
        super(self.__class__, self).setupUi(Dialog)
        self.submitBtn.clicked.connect(lambda: self.on_submit(Dialog))

    def on_submit(self, Dialog):
        if self.authenticate():
            Dialog.accept()

    def authenticate(self):
        # TODO: Needs a more serious authentication
        if (self.username.text() == 'administrator'
                and self.password.text() == 'hualienveteranshome'):
            return True
        else:
            QtWidgets.QMessageBox.critical(self, u'錯誤', u'帳號或密碼不正確!')
            return False


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Login()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())