# -*- coding: utf-8 -*-
"""
@author: alchenerd (alchenerd@gmail.com)
"""

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QThread
# These are mine
if __name__ == '__main__':
    from _processing_skeleton import Ui_Dialog as ProcessingDialog
else:
    from myqtpy._processing_skeleton import Ui_Dialog as ProcessingDialog
from mydocbuilder.DocBuilder import DocBuilder

class DocumentProcessThread(QThread):
    def __init__(self):
        QThread.__init__(self)
        self.builder = DocBuilder()

    def __del__(self):
        self.wait()

    def run(self):
        self.builder.construct()


class Processing(QtWidgets.QDialog, ProcessingDialog):
    def __init__(self, dialog):
        self.dialog = dialog
        super(self.__class__, self).__init__(dialog)
        self.worker = DocumentProcessThread()
        self.setupUi(dialog)
        self.cancelButton.clicked.connect(self.onclick_cancel)

    def onclick_cancel(self):
        print('onclick_cancel')
        self.worker.terminate()  # dangerous but dunno better
        self.dialog.reject()

    def configurate_doc_worker(self, doctype, filledFields):
        self.worker.builder.set_type(doctype)
        self.worker.builder.set_kwargs(**filledFields)

    def run_thread(self):
        self.worker.start()

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QDialog()
    ui = Processing(dialog)
    dialog.show()
    sys.exit(app.exec_())
