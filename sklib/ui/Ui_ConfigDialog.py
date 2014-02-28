# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ConfigDialog.ui'
#
# Created: Wed Mar 16 15:09:32 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_ConfigDialog(object):
    def setupUi(self, ConfigDialog):
        ConfigDialog.setObjectName(_fromUtf8("ConfigDialog"))
        ConfigDialog.resize(632, 468)
        ConfigDialog.setModal(True)
        self.horizontalLayout_2 = QtGui.QHBoxLayout(ConfigDialog)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.configItemList = QtGui.QTreeWidget(ConfigDialog)
        self.configItemList.setMaximumSize(QtCore.QSize(200, 16777215))
        self.configItemList.setObjectName(_fromUtf8("configItemList"))
        self.configItemList.headerItem().setText(0, _fromUtf8("1"))
        self.configItemList.header().setVisible(False)
        self.horizontalLayout.addWidget(self.configItemList)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.configpages = QtGui.QStackedWidget(ConfigDialog)
        self.configpages.setObjectName(_fromUtf8("configpages"))
        self.verticalLayout.addWidget(self.configpages)
        self.btn = QtGui.QDialogButtonBox(ConfigDialog)
        self.btn.setStandardButtons(QtGui.QDialogButtonBox.Apply|QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Save)
        self.btn.setObjectName(_fromUtf8("btn"))
        self.verticalLayout.addWidget(self.btn)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi(ConfigDialog)
        QtCore.QMetaObject.connectSlotsByName(ConfigDialog)

    def retranslateUi(self, ConfigDialog):
        ConfigDialog.setWindowTitle(QtGui.QApplication.translate("ConfigDialog", "Config Dialog", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ConfigDialog = QtGui.QDialog()
    ui = Ui_ConfigDialog()
    ui.setupUi(ConfigDialog)
    ConfigDialog.show()
    sys.exit(app.exec_())

