# -*- coding: utf-8 -*-
"""
@author: alchenerd (alchenerd@gmail.com)
"""

from PyQt5 import QtGui, QtWidgets, QtCore, QtWebEngineWidgets
import os
# These are mine
if __name__ == '__main__':
    from _pdfpreview_skeleton import Ui_Dialog as PdfPreviewDialog
else:
    from myqtpy._pdfpreview_skeleton import Ui_Dialog as PdfPreviewDialog

# 2019/3/14: Now replaced by QtGui.QDesktopServices.openUrl
class PdfPreview(QtWidgets.QDialog, PdfPreviewDialog):
    def __init__(self, dialog):
        super(self.__class__, self).__init__(dialog)
        self.setupUi(dialog)
        # the viewer is at HVHNONC/pdfjs/web, so we need to get back
        path_to_pdfjs = ('file:///'
                         + os.getcwd().replace('\\', '/')
                         + '/pdfjs/web/viewer.html')
        path_to_file = ('file:///'
                        + os.getcwd().replace('\\', '/')
                        + '/result.pdf')
        full_path = path_to_pdfjs + '?file=' + path_to_file
        print(full_path)
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(path_to_file))
        """
        self.webEngineView.load(QtCore.QUrl(full_path))
        """

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QDialog()
    ui = PdfPreview(dialog)
    dialog.show()
    sys.exit(app.exec_())
