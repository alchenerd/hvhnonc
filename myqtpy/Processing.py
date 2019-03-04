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
        self.dialog.closeEvent = self.closeEvent
        super(self.__class__, self).__init__(dialog)
        self.worker = DocumentProcessThread()
        self.setupUi(dialog)
        self.cancelButton.clicked.connect(self.onclick_cancel)
        self.worker.finished.connect(self.on_thread_finished)
        self.worker.builder.status_update.connect(self.on_status_update)

    def on_status_update(self, max: int, current: int, msg: str):
        self.progressBar.setMaximum(max)
        self.progressBar.setValue(current)
        self.message.setText(msg)

    def on_thread_finished(self):
        self.dialog.reject()

    def closeEvent(self, evnt):
        self.worker.terminate()

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
