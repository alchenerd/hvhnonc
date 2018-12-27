# -*- coding: utf-8 -*-
"""
@author: alchenerd (alchenerd@gmail.com)
"""

from PyQt5 import QtWidgets, QtCore
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
        # Select the first radio button
        self.rb1.setChecked(True)
        # initalize dateEdits
        self.init_date_edits()
        # load options for comboboxes
        self.load_options()
        # Connect onchange hooks
        self.category.currentTextChanged.connect(self.on_category_changed)
        self.subcategory.currentTextChanged.connect(
                self.on_subcategory_changed)
        # Callbacks for the checkbox -> enable dateedit
        self.purchase_date_chk.stateChanged.connect(self.on_pdchk_change)
        self.edit_date_chk.stateChanged.connect(self.on_edchk_change)
        # Connect button callbacks
        self.clearBtn.clicked.connect(self.on_clearBtn_clicked)
        self.previewBtn.clicked.connect(self.on_previewBtn_clicked)

    # QUESTION: When to create the document?
    def on_previewBtn_clicked(self):
        # TODO: finish this
        # find out what kind of document to create
        # Create the document(docx)
        # Convert into pdf
        # Open a preview dialog showing the pdf
        print('on_previewBtn_clicked')

    def init_date_edits(self):
        """Initalizes the date edits."""
        # Disable dateEdits
        self.purchase_date_min.setEnabled(False)
        self.purchase_date_max.setEnabled(False)
        self.edit_date_min.setEnabled(False)
        self.edit_date_max.setEnabled(False)
        # Set as today
        # init date
        date = QtCore.QDate.currentDate()
        self.purchase_date_min.setDate(date)
        self.purchase_date_max.setDate(date)
        self.edit_date_min.setDate(date)
        self.edit_date_max.setDate(date)

    def on_pdchk_change(self):
        """When checkbox is checked, enable purchase_date, vice versa."""
        self.purchase_date_min.setEnabled(self.purchase_date_chk.isChecked())
        self.purchase_date_max.setEnabled(self.purchase_date_chk.isChecked())
        # init date
        date = QtCore.QDate.currentDate()
        self.purchase_date_min.setDate(date)
        self.purchase_date_max.setDate(date)

    def on_edchk_change(self):
        """When checkbox is checked, enable edit_date, vice versa."""
        self.edit_date_min.setEnabled(self.edit_date_chk.isChecked())
        self.edit_date_max.setEnabled(self.edit_date_chk.isChecked())
        # init date
        date = QtCore.QDate.currentDate()
        self.edit_date_min.setDate(date)
        self.edit_date_max.setDate(date)

    def on_clearBtn_clicked(self):
        """Clear come fields when clearBtn is clicked."""
        widgetsToClear = ['category', 'subcategory', 'name', 'place',
                          'keep_department', 'use_department', 'keeper']
        for wname in widgetsToClear:
            w = getattr(self, wname)
            if isinstance(w, QtWidgets.QComboBox):
                w.setCurrentText('')

    def on_subcategory_changed(self):
        """When subcategory field is changed, load name options."""
        con, cur = connect._get_connection()
        sqlstr = ('select change_value '
                  'from hvhnonc_cache '
                  'where this_ID = ? '
                  'and this_value = ? '
                  'and change_ID = ?')
        params = (connect.get_field_id('subcategory'),
                  self.subcategory.currentText(),
                  connect.get_field_id('name'))
        try:
            cur.execute(sqlstr, params)
        except:
            QtWidgets.QMessageBox.critical(self, '錯誤',
                                           '取得名稱時出現未知錯誤')
        rows = cur.fetchall()
        con.close()
        self.name.clear()
        for row in rows:
            if row[0]:
                self.name.addItem(row[0])
        self.name.clearEditText()

    def on_category_changed(self):
        """When category field is changed, load subcategory options."""
        con, cur = connect._get_connection()
        sqlstr = ('select description '
                  'from hvhnonc_subcategory '
                  'where parent_ID = {0}')
        substr = ('(select ID from hvhnonc_category where description = ?)')
        sqlstr = sqlstr.format(substr)
        params = (self.category.currentText(),)
        try:
            cur.execute(sqlstr, params)
        except:
            QtWidgets.QMessageBox.critical(self, '錯誤',
                                           '取得細目時出現未知錯誤')
        rows = cur.fetchall()
        con.close()
        self.subcategory.clear()
        for row in rows:
            if row[0]:
                self.subcategory.addItem(row[0])
        self.subcategory.clearEditText()

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
                cb.clear()
                for row in cur:
                    cb.addItem(row[0])
                cb.setEditText('')
            elif name in ('subcategory', 'name'):
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
                    cb.clear()
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
