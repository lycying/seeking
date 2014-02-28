# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ShortcutDialog.ui'
#
# Created: Wed Nov 24 14:13:05 2010
#      by: PyQt4 UI code generator 4.8
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_ShortcutDialog(object):
    def setupUi(self, ShortcutDialog):
        ShortcutDialog.setObjectName(_fromUtf8("ShortcutDialog"))
        ShortcutDialog.resize(539, 147)
        ShortcutDialog.setModal(True)
        self.vboxlayout = QtGui.QVBoxLayout(ShortcutDialog)
        self.vboxlayout.setObjectName(_fromUtf8("vboxlayout"))
        self.shortcutsGroup = QtGui.QGroupBox(ShortcutDialog)
        self.shortcutsGroup.setTitle(_fromUtf8(""))
        self.shortcutsGroup.setObjectName(_fromUtf8("shortcutsGroup"))
        self.gridlayout = QtGui.QGridLayout(self.shortcutsGroup)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.primaryClearButton = QtGui.QPushButton(self.shortcutsGroup)
        self.primaryClearButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.primaryClearButton.setObjectName(_fromUtf8("primaryClearButton"))
        self.gridlayout.addWidget(self.primaryClearButton, 0, 0, 1, 1)
        self.keyLabel = QtGui.QLabel(self.shortcutsGroup)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.keyLabel.sizePolicy().hasHeightForWidth())
        self.keyLabel.setSizePolicy(sizePolicy)
        self.keyLabel.setToolTip(_fromUtf8(""))
        self.keyLabel.setFrameShape(QtGui.QFrame.StyledPanel)
        self.keyLabel.setFrameShadow(QtGui.QFrame.Sunken)
        self.keyLabel.setText(_fromUtf8(""))
        self.keyLabel.setObjectName(_fromUtf8("keyLabel"))
        self.gridlayout.addWidget(self.keyLabel, 0, 1, 1, 1)
        self.vboxlayout.addWidget(self.shortcutsGroup)
        self.buttonBox = QtGui.QDialogButtonBox(ShortcutDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.vboxlayout.addWidget(self.buttonBox)

        self.retranslateUi(ShortcutDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ShortcutDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ShortcutDialog)

    def retranslateUi(self, ShortcutDialog):
        ShortcutDialog.setWindowTitle(QtGui.QApplication.translate("ShortcutDialog", "Edit Shortcut", None, QtGui.QApplication.UnicodeUTF8))
        ShortcutDialog.setWhatsThis(QtGui.QApplication.translate("ShortcutDialog", "Press your shortcut keys and select OK", None, QtGui.QApplication.UnicodeUTF8))
        self.primaryClearButton.setToolTip(QtGui.QApplication.translate("ShortcutDialog", "Press to clear the key sequence buffer.", None, QtGui.QApplication.UnicodeUTF8))
        self.primaryClearButton.setText(QtGui.QApplication.translate("ShortcutDialog", "Clear", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ShortcutDialog = QtGui.QDialog()
    ui = Ui_ShortcutDialog()
    ui.setupUi(ShortcutDialog)
    ShortcutDialog.show()
    sys.exit(app.exec_())

