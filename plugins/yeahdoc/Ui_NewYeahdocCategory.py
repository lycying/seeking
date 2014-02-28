# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'NewYeahdocCategory.ui'
#
# Created: Thu Dec 09 22:22:59 2010
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_NewYeahdocCategory(object):
    def setupUi(self, NewYeahdocCategory):
        NewYeahdocCategory.setObjectName("NewYeahdocCategory")
        NewYeahdocCategory.resize(400, 300)
        NewYeahdocCategory.setModal(True)
        self.verticalLayout_2 = QtGui.QVBoxLayout(NewYeahdocCategory)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.main = QtGui.QWidget(NewYeahdocCategory)
        self.main.setAutoFillBackground(True)
        self.main.setObjectName("main")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.main)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.linelayout = QtGui.QHBoxLayout()
        self.linelayout.setObjectName("linelayout")
        self.label_3 = QtGui.QLabel(self.main)
        self.label_3.setMinimumSize(QtCore.QSize(70, 0))
        self.label_3.setMaximumSize(QtCore.QSize(50, 16777215))
        self.label_3.setObjectName("label_3")
        self.linelayout.addWidget(self.label_3)
        self.verticalLayout_3.addLayout(self.linelayout)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtGui.QLabel(self.main)
        self.label.setMinimumSize(QtCore.QSize(70, 0))
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.title = QtGui.QLineEdit(self.main)
        self.title.setObjectName("title")
        self.horizontalLayout.addWidget(self.title)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.desclayout = QtGui.QHBoxLayout()
        self.desclayout.setObjectName("desclayout")
        self.label_2 = QtGui.QLabel(self.main)
        self.label_2.setMinimumSize(QtCore.QSize(70, 0))
        self.label_2.setObjectName("label_2")
        self.desclayout.addWidget(self.label_2)
        self.verticalLayout.addLayout(self.desclayout)
        self.verticalLayout_3.addLayout(self.verticalLayout)
        self.btn = QtGui.QDialogButtonBox(self.main)
        self.btn.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.btn.setObjectName("btn")
        self.verticalLayout_3.addWidget(self.btn)
        self.verticalLayout_2.addWidget(self.main)

        self.retranslateUi(NewYeahdocCategory)
        QtCore.QMetaObject.connectSlotsByName(NewYeahdocCategory)

    def retranslateUi(self, NewYeahdocCategory):
        NewYeahdocCategory.setWindowTitle(QtGui.QApplication.translate("NewYeahdocCategory", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("NewYeahdocCategory", "Flag", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("NewYeahdocCategory", "Title", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("NewYeahdocCategory", "Description", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    NewYeahdocCategory = QtGui.QDialog()
    ui = Ui_NewYeahdocCategory()
    ui.setupUi(NewYeahdocCategory)
    NewYeahdocCategory.show()
    sys.exit(app.exec_())

