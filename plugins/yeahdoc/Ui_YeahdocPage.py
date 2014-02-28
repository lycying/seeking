# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'YeahdocPage.ui'
#
# Created: Fri Dec 31 14:37:11 2010
#      by: PyQt4 UI code generator 4.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_YeahdocPage(object):
    def setupUi(self, YeahdocPage):
        YeahdocPage.setObjectName(_fromUtf8("YeahdocPage"))
        YeahdocPage.resize(557, 466)
        self.verticalLayout_5 = QtGui.QVBoxLayout(YeahdocPage)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.localtiongroup = QtGui.QGroupBox(YeahdocPage)
        self.localtiongroup.setObjectName(_fromUtf8("localtiongroup"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.localtiongroup)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.storedir = QtGui.QLineEdit(self.localtiongroup)
        self.storedir.setEnabled(False)
        self.storedir.setMinimumSize(QtCore.QSize(0, 0))
        self.storedir.setObjectName(_fromUtf8("storedir"))
        self.horizontalLayout.addWidget(self.storedir)
        self.brower = QtGui.QToolButton(self.localtiongroup)
        self.brower.setEnabled(True)
        self.brower.setObjectName(_fromUtf8("brower"))
        self.horizontalLayout.addWidget(self.brower)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_3.addLayout(self.verticalLayout)
        self.verticalLayout_2.addWidget(self.localtiongroup)
        self.groupBox = QtGui.QGroupBox(YeahdocPage)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.num = QtGui.QLineEdit(self.groupBox)
        self.num.setMinimumSize(QtCore.QSize(0, 0))
        self.num.setMaximumSize(QtCore.QSize(30, 16777215))
        self.num.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.num.setObjectName(_fromUtf8("num"))
        self.verticalLayout_4.addWidget(self.num)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        self.verticalLayout_5.addLayout(self.verticalLayout_3)
        spacerItem = QtGui.QSpacerItem(20, 309, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem)

        self.retranslateUi(YeahdocPage)
        QtCore.QMetaObject.connectSlotsByName(YeahdocPage)

    def retranslateUi(self, YeahdocPage):
        YeahdocPage.setWindowTitle(QtGui.QApplication.translate("YeahdocPage", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.localtiongroup.setTitle(QtGui.QApplication.translate("YeahdocPage", "Store Location", None, QtGui.QApplication.UnicodeUTF8))
        self.brower.setText(QtGui.QApplication.translate("YeahdocPage", "brower...", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("YeahdocPage", "Number Per Page", None, QtGui.QApplication.UnicodeUTF8))
        self.num.setText(QtGui.QApplication.translate("YeahdocPage", "50", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    YeahdocPage = QtGui.QWidget()
    ui = Ui_YeahdocPage()
    ui.setupUi(YeahdocPage)
    YeahdocPage.show()
    sys.exit(app.exec_())

