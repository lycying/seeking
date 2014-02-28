# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SearchWidget.ui'
#
# Created: Wed Feb 02 23:12:14 2011
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_SearchWidget(object):
    def setupUi(self, SearchWidget):
        SearchWidget.setObjectName("SearchWidget")
        SearchWidget.resize(718, 30)
        self.horizontalLayout = QtGui.QHBoxLayout(SearchWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtGui.QLabel(SearchWidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.input = QtGui.QLineEdit(SearchWidget)
        self.input.setObjectName("input")
        self.horizontalLayout.addWidget(self.input)
        self.findPrevButton = QtGui.QToolButton(SearchWidget)
        self.findPrevButton.setObjectName("findPrevButton")
        self.horizontalLayout.addWidget(self.findPrevButton)
        self.findNextButton = QtGui.QToolButton(SearchWidget)
        self.findNextButton.setObjectName("findNextButton")
        self.horizontalLayout.addWidget(self.findNextButton)
        self.caseCheckBox = QtGui.QCheckBox(SearchWidget)
        self.caseCheckBox.setObjectName("caseCheckBox")
        self.horizontalLayout.addWidget(self.caseCheckBox)
        self.wrapCheckBox = QtGui.QCheckBox(SearchWidget)
        self.wrapCheckBox.setObjectName("wrapCheckBox")
        self.horizontalLayout.addWidget(self.wrapCheckBox)
        self.infoLabel = QtGui.QLabel(SearchWidget)
        self.infoLabel.setMinimumSize(QtCore.QSize(200, 0))
        self.infoLabel.setText("")
        self.infoLabel.setObjectName("infoLabel")
        self.horizontalLayout.addWidget(self.infoLabel)
        self.closeButton = QtGui.QToolButton(SearchWidget)
        self.closeButton.setText("")
        self.closeButton.setObjectName("closeButton")
        self.horizontalLayout.addWidget(self.closeButton)

        self.retranslateUi(SearchWidget)
        QtCore.QMetaObject.connectSlotsByName(SearchWidget)
        SearchWidget.setTabOrder(self.caseCheckBox, self.wrapCheckBox)
        SearchWidget.setTabOrder(self.wrapCheckBox, self.findNextButton)
        SearchWidget.setTabOrder(self.findNextButton, self.findPrevButton)

    def retranslateUi(self, SearchWidget):
        SearchWidget.setWindowTitle(QtGui.QApplication.translate("SearchWidget", "Find", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("SearchWidget", "Find:", None, QtGui.QApplication.UnicodeUTF8))
        self.findPrevButton.setToolTip(QtGui.QApplication.translate("SearchWidget", "Press to find the previous occurrence", None, QtGui.QApplication.UnicodeUTF8))
        self.findNextButton.setToolTip(QtGui.QApplication.translate("SearchWidget", "Press to find the next occurrence", None, QtGui.QApplication.UnicodeUTF8))
        self.caseCheckBox.setText(QtGui.QApplication.translate("SearchWidget", "Match case", None, QtGui.QApplication.UnicodeUTF8))
        self.wrapCheckBox.setText(QtGui.QApplication.translate("SearchWidget", "Wrap around", None, QtGui.QApplication.UnicodeUTF8))
        self.closeButton.setToolTip(QtGui.QApplication.translate("SearchWidget", "Press to close the window", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    SearchWidget = QtGui.QWidget()
    ui = Ui_SearchWidget()
    ui.setupUi(SearchWidget)
    SearchWidget.show()
    sys.exit(app.exec_())

