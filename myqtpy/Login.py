# -*- coding: utf-8 -*-
"""
@author: alchenerd (alchenerd@gmail.com)
"""

import hashlib
import sqlite3
from PyQt5 import QtWidgets
from typing import Dict
# These modules are mine
if __name__ == '__main__':
    from _login_skeleton import Ui_Dialog as LoginDialog
    import sys
    sys.path.append('../')
    from myconnect.connect import _get_connection
else:
    from myqtpy._login_skeleton import Ui_Dialog as LoginDialog
    from myconnect.connect import _get_connection

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

    def authenticate(self) -> bool:
        credential = {'username': self.username.text(),
                      'password': self.password.text()}
        if self.correct_hash(credential):
            return True
        else:
            QtWidgets.QMessageBox.critical(self, u'錯誤', u'帳號或密碼不正確!')
            return False

    def correct_hash(self, credential: Dict[str, str]) -> bool:
        # The symbol <= means 'is subset of'
        if not set(('username', 'password')) <= credential.keys():
            return False
        (username, password) = (credential.get('username'),
                                credential.get('password'))
        con = _get_connection()
        con.row_factory = sqlite3.Row
        sqlstr = ("select {hash}, {salt} from {table} where {username}=?;")
        sqlstr = sqlstr.format(**{'hash': 'hash_SHA256',
                                  'salt': 'salt',
                                  'table': 'hvhnonc_users',
                                  'username': 'username'})
        params = (username,)
        result = con.execute(sqlstr, params).fetchone()
        con.close()
        try:
            dbHash = result['hash_SHA256']
            dbSalt = result['salt']
        except:
            return False
        # SHA256 hash the dbSalt + password
        sha256 = hashlib.sha256()
        data = dbSalt + password
        sha256.update(data.encode("utf-8"))
        localHash = sha256.hexdigest()
        return localHash == dbHash


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Login(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
