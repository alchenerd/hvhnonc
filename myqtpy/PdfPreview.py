# -*- coding: utf-8 -*-
"""
@author: alchenerd (alchenerd@gmail.com)
"""

from PyQt5 import QtWidgets
# These are mine
if __name__ == '__main__':
    from _pdfpreview_skeleton import Ui_Dialog as PdfPreviewDialog
else:
    from myqtpy._pdfpreview_skeleton import Ui_Dialog as PdfPreviewDialog

class PdfPreview(QtWidgets.QDialog, PdfPreviewDialog):
    def __init__(self, dialog):
        super(self.__class__, self).__init__(dialog)
        self.setupUi(dialog)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QDialog()
    ui = PdfPreview(dialog)
    dialog.show()
    sys.exit(app.exec_())
