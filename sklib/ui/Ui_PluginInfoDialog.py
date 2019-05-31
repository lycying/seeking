# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PluginInfoDialog.ui'
#
# Created: Wed Mar 16 15:09:32 2011
#      by: PyQt5 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_PluginInfoDialog(object):
    def setupUi(self, PluginInfoDialog):
        PluginInfoDialog.setObjectName(_fromUtf8("PluginInfoDialog"))
        PluginInfoDialog.resize(800, 600)
        PluginInfoDialog.setSizeGripEnabled(True)
        PluginInfoDialog.setModal(True)
        self.vboxlayout = QtGui.QVBoxLayout(PluginInfoDialog)
        self.vboxlayout.setObjectName(_fromUtf8("vboxlayout"))
        self.pluginList = QtGui.QTreeWidget(PluginInfoDialog)
        self.pluginList.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.pluginList.setRootIsDecorated(False)
        self.pluginList.setItemsExpandable(False)
        self.pluginList.setAllColumnsShowFocus(True)
        self.pluginList.setObjectName(_fromUtf8("pluginList"))
        self.vboxlayout.addWidget(self.pluginList)
        self.buttonBox = QtGui.QDialogButtonBox(PluginInfoDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.vboxlayout.addWidget(self.buttonBox)

        self.retranslateUi(PluginInfoDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), PluginInfoDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), PluginInfoDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(PluginInfoDialog)
        PluginInfoDialog.setTabOrder(self.pluginList, self.buttonBox)

    def retranslateUi(self, PluginInfoDialog):
        PluginInfoDialog.setWindowTitle(QtGui.QApplication.translate("PluginInfoDialog", "Loaded Plugins", None, QtGui.QApplication.UnicodeUTF8))
        self.pluginList.setSortingEnabled(True)
        self.pluginList.headerItem().setText(0, QtGui.QApplication.translate("PluginInfoDialog", "Module", None, QtGui.QApplication.UnicodeUTF8))
        self.pluginList.headerItem().setText(1, QtGui.QApplication.translate("PluginInfoDialog", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.pluginList.headerItem().setText(2, QtGui.QApplication.translate("PluginInfoDialog", "Author", None, QtGui.QApplication.UnicodeUTF8))
        self.pluginList.headerItem().setText(3, QtGui.QApplication.translate("PluginInfoDialog", "Version", None, QtGui.QApplication.UnicodeUTF8))
        self.pluginList.headerItem().setText(4, QtGui.QApplication.translate("PluginInfoDialog", "Active", None, QtGui.QApplication.UnicodeUTF8))
        self.pluginList.headerItem().setText(5, QtGui.QApplication.translate("PluginInfoDialog", "Description", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    PluginInfoDialog = QtGui.QDialog()
    ui = Ui_PluginInfoDialog()
    ui.setupUi(PluginInfoDialog)
    PluginInfoDialog.show()
    sys.exit(app.exec_())

