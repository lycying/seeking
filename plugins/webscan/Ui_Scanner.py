# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Scanner.ui'
#
# Created: Fri Jan 17 17:53:02 2014
#      by: PyQt4 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Scanner(object):
    def setupUi(self, Scanner):
        Scanner.setObjectName(_fromUtf8("Scanner"))
        Scanner.resize(752, 573)
        Scanner.setAutoFillBackground(True)
        self.horizontalLayout_3 = QtGui.QHBoxLayout(Scanner)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.extoption = QtGui.QVBoxLayout()
        self.extoption.setObjectName(_fromUtf8("extoption"))
        self.mainlayout = QtGui.QHBoxLayout()
        self.mainlayout.setObjectName(_fromUtf8("mainlayout"))
        self.label_2 = QtGui.QLabel(Scanner)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.mainlayout.addWidget(self.label_2)
        self.urlEdit = QtGui.QLineEdit(Scanner)
        self.urlEdit.setObjectName(_fromUtf8("urlEdit"))
        self.mainlayout.addWidget(self.urlEdit)
        self.threadlayout = QtGui.QHBoxLayout()
        self.threadlayout.setObjectName(_fromUtf8("threadlayout"))
        self.ThreadNumber = QtGui.QLabel(Scanner)
        self.ThreadNumber.setObjectName(_fromUtf8("ThreadNumber"))
        self.threadlayout.addWidget(self.ThreadNumber)
        self.spinThreadNumber = QtGui.QSpinBox(Scanner)
        self.spinThreadNumber.setMinimum(1)
        self.spinThreadNumber.setProperty("value", 5)
        self.spinThreadNumber.setObjectName(_fromUtf8("spinThreadNumber"))
        self.threadlayout.addWidget(self.spinThreadNumber)
        self.Timeout = QtGui.QLabel(Scanner)
        self.Timeout.setObjectName(_fromUtf8("Timeout"))
        self.threadlayout.addWidget(self.Timeout)
        self.spinTimeout = QtGui.QSpinBox(Scanner)
        self.spinTimeout.setMinimum(2)
        self.spinTimeout.setProperty("value", 5)
        self.spinTimeout.setObjectName(_fromUtf8("spinTimeout"))
        self.threadlayout.addWidget(self.spinTimeout)
        self.mainlayout.addLayout(self.threadlayout)
        self.extoption.addLayout(self.mainlayout)
        self.verticalLayout.addLayout(self.extoption)
        self.txtLayout = QtGui.QHBoxLayout()
        self.txtLayout.setObjectName(_fromUtf8("txtLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.txtLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.txtLayout)
        self.code = QtGui.QHBoxLayout()
        self.code.setObjectName(_fromUtf8("code"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.code.addItem(spacerItem1)
        self.label_3 = QtGui.QLabel(Scanner)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.code.addWidget(self.label_3)
        self.cbx200 = QtGui.QCheckBox(Scanner)
        self.cbx200.setChecked(True)
        self.cbx200.setObjectName(_fromUtf8("cbx200"))
        self.code.addWidget(self.cbx200)
        self.cbx302 = QtGui.QCheckBox(Scanner)
        self.cbx302.setObjectName(_fromUtf8("cbx302"))
        self.code.addWidget(self.cbx302)
        self.cbx403 = QtGui.QCheckBox(Scanner)
        self.cbx403.setObjectName(_fromUtf8("cbx403"))
        self.code.addWidget(self.cbx403)
        self.bottomLayout = QtGui.QHBoxLayout()
        self.bottomLayout.setObjectName(_fromUtf8("bottomLayout"))
        self.lblPercent = QtGui.QLabel(Scanner)
        self.lblPercent.setObjectName(_fromUtf8("lblPercent"))
        self.bottomLayout.addWidget(self.lblPercent)
        self.progressBar = QtGui.QProgressBar(Scanner)
        self.progressBar.setAutoFillBackground(True)
        self.progressBar.setMaximum(100)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.bottomLayout.addWidget(self.progressBar)
        self.code.addLayout(self.bottomLayout)
        self.verticalLayout.addLayout(self.code)
        self.controllayout = QtGui.QHBoxLayout()
        self.controllayout.setObjectName(_fromUtf8("controllayout"))
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.controllayout.addItem(spacerItem2)
        self.startBtn = QtGui.QPushButton(Scanner)
        self.startBtn.setObjectName(_fromUtf8("startBtn"))
        self.controllayout.addWidget(self.startBtn)
        self.stopBtn = QtGui.QPushButton(Scanner)
        self.stopBtn.setObjectName(_fromUtf8("stopBtn"))
        self.controllayout.addWidget(self.stopBtn)
        self.verticalLayout.addLayout(self.controllayout)
        self.textBrowser = QtGui.QTextBrowser(Scanner)
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        self.verticalLayout.addWidget(self.textBrowser)
        self.horizontalLayout_3.addLayout(self.verticalLayout)

        self.retranslateUi(Scanner)
        QtCore.QMetaObject.connectSlotsByName(Scanner)

    def retranslateUi(self, Scanner):
        Scanner.setWindowTitle(_translate("Scanner", "Form", None))
        self.label_2.setText(_translate("Scanner", "URL:", None))
        self.urlEdit.setText(_translate("Scanner", "http://", None))
        self.ThreadNumber.setText(_translate("Scanner", "Thread Number:", None))
        self.Timeout.setText(_translate("Scanner", "Time Out(sec):", None))
        self.label_3.setText(_translate("Scanner", "HTTP Code:", None))
        self.cbx200.setText(_translate("Scanner", "200 OK", None))
        self.cbx302.setText(_translate("Scanner", "302 Found", None))
        self.cbx403.setText(_translate("Scanner", "403 Forbidden", None))
        self.lblPercent.setText(_translate("Scanner", "0/0", None))
        self.startBtn.setText(_translate("Scanner", "Start", None))
        self.stopBtn.setText(_translate("Scanner", "Stop", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Scanner = QtGui.QWidget()
    ui = Ui_Scanner()
    ui.setupUi(Scanner)
    Scanner.show()
    sys.exit(app.exec_())

