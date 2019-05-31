# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PortScanner.ui'
#
# Created: Mon Jan 20 10:45:58 2014
#      by: PyQt5 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui

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

class Ui_PortScanner(object):
    def setupUi(self, PortScanner):
        PortScanner.setObjectName(_fromUtf8("PortScanner"))
        PortScanner.resize(752, 573)
        PortScanner.setAutoFillBackground(True)
        self.horizontalLayout_3 = QtGui.QHBoxLayout(PortScanner)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.code = QtGui.QHBoxLayout()
        self.code.setObjectName(_fromUtf8("code"))
        self.bottomLayout = QtGui.QHBoxLayout()
        self.bottomLayout.setObjectName(_fromUtf8("bottomLayout"))
        self.label = QtGui.QLabel(PortScanner)
        self.label.setObjectName(_fromUtf8("label"))
        self.bottomLayout.addWidget(self.label)
        self.urlEdit = QtGui.QLineEdit(PortScanner)
        self.urlEdit.setObjectName(_fromUtf8("urlEdit"))
        self.bottomLayout.addWidget(self.urlEdit)
        self.Timeout = QtGui.QLabel(PortScanner)
        self.Timeout.setObjectName(_fromUtf8("Timeout"))
        self.bottomLayout.addWidget(self.Timeout)
        self.spinFrom = QtGui.QSpinBox(PortScanner)
        self.spinFrom.setMinimum(1)
        self.spinFrom.setMaximum(65534)
        self.spinFrom.setProperty("value", 1)
        self.spinFrom.setObjectName(_fromUtf8("spinFrom"))
        self.bottomLayout.addWidget(self.spinFrom)
        self.ThreadNumber = QtGui.QLabel(PortScanner)
        self.ThreadNumber.setObjectName(_fromUtf8("ThreadNumber"))
        self.bottomLayout.addWidget(self.ThreadNumber)
        self.spinTo = QtGui.QSpinBox(PortScanner)
        self.spinTo.setMinimum(2)
        self.spinTo.setMaximum(65535)
        self.spinTo.setProperty("value", 1000)
        self.spinTo.setObjectName(_fromUtf8("spinTo"))
        self.bottomLayout.addWidget(self.spinTo)
        self.code.addLayout(self.bottomLayout)
        self.verticalLayout.addLayout(self.code)
        self.progressBar = QtGui.QProgressBar(PortScanner)
        self.progressBar.setAutoFillBackground(True)
        self.progressBar.setMaximum(100)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.verticalLayout.addWidget(self.progressBar)
        self.controllayout = QtGui.QHBoxLayout()
        self.controllayout.setObjectName(_fromUtf8("controllayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.controllayout.addItem(spacerItem)
        self.label_2 = QtGui.QLabel(PortScanner)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.controllayout.addWidget(self.label_2)
        self.spinThreadSize = QtGui.QSpinBox(PortScanner)
        self.spinThreadSize.setMinimum(1)
        self.spinThreadSize.setMaximum(1000)
        self.spinThreadSize.setProperty("value", 20)
        self.spinThreadSize.setObjectName(_fromUtf8("spinThreadSize"))
        self.controllayout.addWidget(self.spinThreadSize)
        self.startBtn = QtGui.QPushButton(PortScanner)
        self.startBtn.setObjectName(_fromUtf8("startBtn"))
        self.controllayout.addWidget(self.startBtn)
        self.stopBtn = QtGui.QPushButton(PortScanner)
        self.stopBtn.setObjectName(_fromUtf8("stopBtn"))
        self.controllayout.addWidget(self.stopBtn)
        self.verticalLayout.addLayout(self.controllayout)
        self.textBrowser = QtGui.QTextBrowser(PortScanner)
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        self.verticalLayout.addWidget(self.textBrowser)
        self.horizontalLayout_3.addLayout(self.verticalLayout)

        self.retranslateUi(PortScanner)
        QtCore.QMetaObject.connectSlotsByName(PortScanner)

    def retranslateUi(self, PortScanner):
        PortScanner.setWindowTitle(_translate("PortScanner", "Form", None))
        self.label.setText(_translate("PortScanner", "Hostname", None))
        self.urlEdit.setText(_translate("PortScanner", "localhost", None))
        self.Timeout.setText(_translate("PortScanner", "From", None))
        self.ThreadNumber.setText(_translate("PortScanner", "To:", None))
        self.label_2.setText(_translate("PortScanner", "Thread Size(Max 100,BatchSize 10):", None))
        self.startBtn.setText(_translate("PortScanner", "Start", None))
        self.stopBtn.setText(_translate("PortScanner", "Stop", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    PortScanner = QtGui.QWidget()
    ui = Ui_PortScanner()
    ui.setupUi(PortScanner)
    PortScanner.show()
    sys.exit(app.exec_())

