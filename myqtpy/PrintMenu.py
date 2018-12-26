# -*- coding: utf-8 -*-
"""
@author: alchenerd (alchenerd@gmail.com)
"""

from PyQt5 import QtWidgets
from typing import Dict
import sys
# These are mine
if __name__ == '__main__':
    sys.path.append('../')
else:
    sys.path.append('./myqtpy/')
from _print_menu_skeleton import Ui_Dialog as PrintMenuDialog
from myconnect import connect

class PrintMenu(QtWidgets.QDialog, PrintMenuDialog):
    def __init__(self, dialog):
        super(self.__class__, self).__init__(dialog)
        self.setupUi(dialog)
        self.init_fields()

    def init_fields(self):
        """This function is called once when the dialog ui is created."""
        # TODO: finish this function
        # Select the first radio button
        self.rb1.setChecked(True)
        # Disable dateEdits
        self.purchase_date_min.setEnabled(False)
        self.purchase_date_max.setEnabled(False)
        self.edit_date_min.setEnabled(False)
        self.edit_date_max.setEnabled(False)
        # load options for comboboxes
        self.load_options()

    def get_comboboxes(self) -> Dict[str, QtWidgets.QComboBox]:
        """returns the child comboboxes in dict(name, widget)"""
        for k, w in self.__dict__.items():
            if isinstance(w, QtWidgets.QComboBox):
                yield k, w

    def load_options(self):
        """load database data as combobox options"""
        con, cur = connect._get_connection()
        for name, cb in self.get_comboboxes():
            if name == 'category':
                sqlstr = 'select description from hvhnonc_category'
                cur.execute(sqlstr)
                for row in cur:
                    cb.addItem(row[0])
                cb.setEditText('')
            elif name == 'subcategory':
                pass
            else:
                sqlstr = ('select change_value '
                          'from hvhnonc_cache '
                          'where this_ID = 0 '
                          'and this_value = "" '
                          'and change_ID = ?')
                params = (connect.get_field_id(name),)
                cur.execute(sqlstr, params)
                rows = cur.fetchall()
                try:
                    for row in rows:
                        cb.addItem(row[0])
                except Exception as e:
                    print(e)
                cb.setEditText('')
        con.close()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QDialog()
    ui = PrintMenu(dialog)
    dialog.show()
    sys.exit(app.exec_())
