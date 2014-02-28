# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'StyleDialog.ui'
#
# Created: Wed Feb 02 23:12:16 2011
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_StyleDialog(object):
    def setupUi(self, StyleDialog):
        StyleDialog.setObjectName("StyleDialog")
        StyleDialog.resize(448, 172)
        StyleDialog.setModal(True)
        self.verticalLayout_2 = QtGui.QVBoxLayout(StyleDialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.styleValue = QtGui.QTextEdit(StyleDialog)
        self.styleValue.setObjectName("styleValue")
        self.verticalLayout.addWidget(self.styleValue)
        self.btn = QtGui.QDialogButtonBox(StyleDialog)
        self.btn.setOrientation(QtCore.Qt.Horizontal)
        self.btn.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.btn.setObjectName("btn")
        self.verticalLayout.addWidget(self.btn)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(StyleDialog)
        QtCore.QObject.connect(self.btn, QtCore.SIGNAL("accepted()"), StyleDialog.accept)
        QtCore.QObject.connect(self.btn, QtCore.SIGNAL("rejected()"), StyleDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(StyleDialog)

    def retranslateUi(self, StyleDialog):
        StyleDialog.setWindowTitle(QtGui.QApplication.translate("StyleDialog", "StyleDialog", None, QtGui.QApplication.UnicodeUTF8))
        self.styleValue.setHtml(QtGui.QApplication.translate("StyleDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    StyleDialog = QtGui.QDialog()
    ui = Ui_StyleDialog()
    ui.setupUi(StyleDialog)
    StyleDialog.show()
    sys.exit(app.exec_())

