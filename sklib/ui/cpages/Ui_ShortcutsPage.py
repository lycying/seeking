# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ShortcutsPage.ui'
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

class Ui_ShortcutsPage(object):
    def setupUi(self, ShortcutsPage):
        ShortcutsPage.setObjectName(_fromUtf8("ShortcutsPage"))
        ShortcutsPage.resize(615, 394)
        self.verticalLayout_2 = QtGui.QVBoxLayout(ShortcutsPage)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(ShortcutsPage)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.searchEdit = QtGui.QLineEdit(ShortcutsPage)
        self.searchEdit.setObjectName(_fromUtf8("searchEdit"))
        self.horizontalLayout.addWidget(self.searchEdit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.shortcutsList = QtGui.QTreeWidget(ShortcutsPage)
        self.shortcutsList.setAlternatingRowColors(True)
        self.shortcutsList.setObjectName(_fromUtf8("shortcutsList"))
        self.verticalLayout.addWidget(self.shortcutsList)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.label.setBuddy(self.searchEdit)

        self.retranslateUi(ShortcutsPage)
        QtCore.QMetaObject.connectSlotsByName(ShortcutsPage)

    def retranslateUi(self, ShortcutsPage):
        ShortcutsPage.setWindowTitle(QtGui.QApplication.translate("ShortcutsPage", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("ShortcutsPage", "Filter", None, QtGui.QApplication.UnicodeUTF8))
        self.searchEdit.setToolTip(QtGui.QApplication.translate("ShortcutsPage", "Enter the regular expression that should be contained in the shortcut action", None, QtGui.QApplication.UnicodeUTF8))
        self.shortcutsList.setToolTip(QtGui.QApplication.translate("ShortcutsPage", "This list shows all keyboard shortcuts.", None, QtGui.QApplication.UnicodeUTF8))
        self.shortcutsList.setWhatsThis(QtGui.QApplication.translate("ShortcutsPage", "<b>Keyboard Shortcuts List</b>\n"
"<p>This list shows all keyboard shortcuts defined in the application. Double click an entry in order to change the respective shortcut. Alternatively, the shortcut might be changed by editing the key sequence in the respective column.</p>", None, QtGui.QApplication.UnicodeUTF8))
        self.shortcutsList.headerItem().setText(0, QtGui.QApplication.translate("ShortcutsPage", "Action", None, QtGui.QApplication.UnicodeUTF8))
        self.shortcutsList.headerItem().setText(1, QtGui.QApplication.translate("ShortcutsPage", "Shortcut", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ShortcutsPage = QtGui.QWidget()
    ui = Ui_ShortcutsPage()
    ui.setupUi(ShortcutsPage)
    ShortcutsPage.show()
    sys.exit(app.exec_())

