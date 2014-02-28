# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ApplicationPage.ui'
#
# Created: Wed Nov 24 14:13:04 2010
#      by: PyQt4 UI code generator 4.8
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_ApplicationPage(object):
    def setupUi(self, ApplicationPage):
        ApplicationPage.setObjectName(_fromUtf8("ApplicationPage"))
        ApplicationPage.resize(507, 457)
        self.horizontalLayout = QtGui.QHBoxLayout(ApplicationPage)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.quitOnClose = QtGui.QCheckBox(ApplicationPage)
        self.quitOnClose.setObjectName(_fromUtf8("quitOnClose"))
        self.verticalLayout.addWidget(self.quitOnClose)
        self.errorLogChecker = QtGui.QCheckBox(ApplicationPage)
        self.errorLogChecker.setObjectName(_fromUtf8("errorLogChecker"))
        self.verticalLayout.addWidget(self.errorLogChecker)
        self.checkBox = QtGui.QCheckBox(ApplicationPage)
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.verticalLayout.addWidget(self.checkBox)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_2 = QtGui.QLabel(ApplicationPage)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        self.styleSelector = QtGui.QComboBox(ApplicationPage)
        self.styleSelector.setObjectName(_fromUtf8("styleSelector"))
        self.horizontalLayout_2.addWidget(self.styleSelector)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout)
        spacerItem1 = QtGui.QSpacerItem(275, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)

        self.retranslateUi(ApplicationPage)
        QtCore.QMetaObject.connectSlotsByName(ApplicationPage)

    def retranslateUi(self, ApplicationPage):
        ApplicationPage.setWindowTitle(QtGui.QApplication.translate("ApplicationPage", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.quitOnClose.setText(QtGui.QApplication.translate("ApplicationPage", "Quit when last window close", None, QtGui.QApplication.UnicodeUTF8))
        self.errorLogChecker.setText(QtGui.QApplication.translate("ApplicationPage", "Check error log at start", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox.setText(QtGui.QApplication.translate("ApplicationPage", "If show splash screen or not", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("ApplicationPage", "Style", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ApplicationPage = QtGui.QWidget()
    ui = Ui_ApplicationPage()
    ui.setupUi(ApplicationPage)
    ApplicationPage.show()
    sys.exit(app.exec_())

