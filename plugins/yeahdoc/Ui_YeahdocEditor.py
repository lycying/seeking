# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'YeahdocEditor.ui'
#
# Created: Thu Jan 23 11:59:09 2014
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

class Ui_YeahdocEditor(object):
    def setupUi(self, YeahdocEditor):
        YeahdocEditor.setObjectName(_fromUtf8("YeahdocEditor"))
        YeahdocEditor.resize(921, 27)
        YeahdocEditor.setAutoFillBackground(True)
        self.verticalLayout_2 = QtGui.QVBoxLayout(YeahdocEditor)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setContentsMargins(3, 2, 3, 0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.linelayout = QtGui.QHBoxLayout()
        self.linelayout.setSpacing(6)
        self.linelayout.setObjectName(_fromUtf8("linelayout"))
        self.label_2 = QtGui.QLabel(YeahdocEditor)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.linelayout.addWidget(self.label_2)
        self.titleInput = QtGui.QLineEdit(YeahdocEditor)
        self.titleInput.setMinimumSize(QtCore.QSize(0, 23))
        self.titleInput.setMaximumSize(QtCore.QSize(1000, 23))
        self.titleInput.setObjectName(_fromUtf8("titleInput"))
        self.linelayout.addWidget(self.titleInput)
        self.label = QtGui.QLabel(YeahdocEditor)
        self.label.setObjectName(_fromUtf8("label"))
        self.linelayout.addWidget(self.label)
        self.classlist = QtGui.QComboBox(YeahdocEditor)
        self.classlist.setObjectName(_fromUtf8("classlist"))
        self.linelayout.addWidget(self.classlist)
        self.taglabel = QtGui.QLabel(YeahdocEditor)
        self.taglabel.setObjectName(_fromUtf8("taglabel"))
        self.linelayout.addWidget(self.taglabel)
        self.tagsInput = QtGui.QLineEdit(YeahdocEditor)
        self.tagsInput.setMaximumSize(QtCore.QSize(200, 23))
        self.tagsInput.setObjectName(_fromUtf8("tagsInput"))
        self.linelayout.addWidget(self.tagsInput)
        self.downloadBtn = QtGui.QPushButton(YeahdocEditor)
        self.downloadBtn.setObjectName(_fromUtf8("downloadBtn"))
        self.linelayout.addWidget(self.downloadBtn)
        self.saveBtn = QtGui.QPushButton(YeahdocEditor)
        self.saveBtn.setObjectName(_fromUtf8("saveBtn"))
        self.linelayout.addWidget(self.saveBtn)
        self.passwordMore = QtGui.QPushButton(YeahdocEditor)
        self.passwordMore.setFlat(True)
        self.passwordMore.setObjectName(_fromUtf8("passwordMore"))
        self.linelayout.addWidget(self.passwordMore)
        self.passwordWidget = QtGui.QWidget(YeahdocEditor)
        self.passwordWidget.setEnabled(True)
        self.passwordWidget.setObjectName(_fromUtf8("passwordWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.passwordWidget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.password1 = QtGui.QLineEdit(self.passwordWidget)
        self.password1.setEchoMode(QtGui.QLineEdit.Password)
        self.password1.setObjectName(_fromUtf8("password1"))
        self.horizontalLayout.addWidget(self.password1)
        self.relabel = QtGui.QLabel(self.passwordWidget)
        self.relabel.setObjectName(_fromUtf8("relabel"))
        self.horizontalLayout.addWidget(self.relabel)
        self.password2 = QtGui.QLineEdit(self.passwordWidget)
        self.password2.setEchoMode(QtGui.QLineEdit.Password)
        self.password2.setObjectName(_fromUtf8("password2"))
        self.horizontalLayout.addWidget(self.password2)
        self.linelayout.addWidget(self.passwordWidget)
        self.verticalLayout_2.addLayout(self.linelayout)

        self.retranslateUi(YeahdocEditor)
        QtCore.QMetaObject.connectSlotsByName(YeahdocEditor)

    def retranslateUi(self, YeahdocEditor):
        self.label_2.setText(_translate("YeahdocEditor", "Title", None))
        self.titleInput.setToolTip(_translate("YeahdocEditor", "<h1>Input something as title</h1>", None))
        self.label.setText(_translate("YeahdocEditor", "Category", None))
        self.taglabel.setText(_translate("YeahdocEditor", "Tags", None))
        self.downloadBtn.setText(_translate("YeahdocEditor", "Download Images", None))
        self.saveBtn.setText(_translate("YeahdocEditor", "Save", None))
        self.passwordMore.setText(_translate("YeahdocEditor", "Encrypt", None))
        self.relabel.setText(_translate("YeahdocEditor", "Re", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    YeahdocEditor = QtGui.QWidget()
    ui = Ui_YeahdocEditor()
    ui.setupUi(YeahdocEditor)
    YeahdocEditor.show()
    sys.exit(app.exec_())

