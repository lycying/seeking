# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'YeahdocList.ui'
#
# Created: Wed Jan 15 20:58:08 2014
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

class Ui_YeahdocList(object):
    def setupUi(self, YeahdocList):
        YeahdocList.setObjectName(_fromUtf8("YeahdocList"))
        YeahdocList.resize(631, 626)
        YeahdocList.setAcceptDrops(False)
        YeahdocList.setAutoFillBackground(True)
        self.horizontalLayout_2 = QtGui.QHBoxLayout(YeahdocList)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setContentsMargins(2, 0, 2, 0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.splitter = QtGui.QSplitter(YeahdocList)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.leftpart = QtGui.QWidget(self.splitter)
        self.leftpart.setObjectName(_fromUtf8("leftpart"))
        self.verticalLayout = QtGui.QVBoxLayout(self.leftpart)
        self.verticalLayout.setContentsMargins(0, 0, 0, -1)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.yeahdoclisttree = QtGui.QTreeWidget(self.leftpart)
        self.yeahdoclisttree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.yeahdoclisttree.setAutoFillBackground(True)
        self.yeahdoclisttree.setStyleSheet(_fromUtf8(""))
        self.yeahdoclisttree.setFrameShadow(QtGui.QFrame.Sunken)
        self.yeahdoclisttree.setLineWidth(1)
        self.yeahdoclisttree.setMidLineWidth(0)
        self.yeahdoclisttree.setAlternatingRowColors(True)
        self.yeahdoclisttree.setObjectName(_fromUtf8("yeahdoclisttree"))
        self.verticalLayout.addWidget(self.yeahdoclisttree)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.leftpart)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.searchEdit = QtGui.QLineEdit(self.leftpart)
        self.searchEdit.setObjectName(_fromUtf8("searchEdit"))
        self.horizontalLayout.addWidget(self.searchEdit)
        self.bytitle = QtGui.QCheckBox(self.leftpart)
        self.bytitle.setChecked(True)
        self.bytitle.setObjectName(_fromUtf8("bytitle"))
        self.horizontalLayout.addWidget(self.bytitle)
        self.bycontent = QtGui.QCheckBox(self.leftpart)
        self.bycontent.setChecked(True)
        self.bycontent.setObjectName(_fromUtf8("bycontent"))
        self.horizontalLayout.addWidget(self.bycontent)
        self.togglebtn = QtGui.QPushButton(self.leftpart)
        self.togglebtn.setMaximumSize(QtCore.QSize(20, 20))
        self.togglebtn.setText(_fromUtf8(""))
        self.togglebtn.setFlat(True)
        self.togglebtn.setObjectName(_fromUtf8("togglebtn"))
        self.horizontalLayout.addWidget(self.togglebtn)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.rightpart = QtGui.QWidget(self.splitter)
        self.rightpart.setMinimumSize(QtCore.QSize(200, 0))
        self.rightpart.setMaximumSize(QtCore.QSize(200, 16777215))
        self.rightpart.setObjectName(_fromUtf8("rightpart"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.rightpart)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.rightsplitter = QtGui.QSplitter(self.rightpart)
        self.rightsplitter.setOrientation(QtCore.Qt.Vertical)
        self.rightsplitter.setObjectName(_fromUtf8("rightsplitter"))
        self.yeahdoccategorylist = QtGui.QListWidget(self.rightsplitter)
        self.yeahdoccategorylist.setMinimumSize(QtCore.QSize(0, 300))
        self.yeahdoccategorylist.setMaximumSize(QtCore.QSize(200, 500))
        self.yeahdoccategorylist.setBaseSize(QtCore.QSize(0, 300))
        self.yeahdoccategorylist.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.yeahdoccategorylist.setStyleSheet(_fromUtf8(""))
        self.yeahdoccategorylist.setFrameShape(QtGui.QFrame.VLine)
        self.yeahdoccategorylist.setFrameShadow(QtGui.QFrame.Plain)
        self.yeahdoccategorylist.setLineWidth(0)
        self.yeahdoccategorylist.setAlternatingRowColors(True)
        self.yeahdoccategorylist.setViewMode(QtGui.QListView.ListMode)
        self.yeahdoccategorylist.setObjectName(_fromUtf8("yeahdoccategorylist"))
        self.preview = QtWebKit.QWebView(self.rightsplitter)
        self.preview.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.preview.setUrl(QtCore.QUrl(_fromUtf8("about:blank")))
        self.preview.setObjectName(_fromUtf8("preview"))
        self.verticalLayout_2.addWidget(self.rightsplitter)
        self.horizontalLayout_2.addWidget(self.splitter)

        self.retranslateUi(YeahdocList)
        QtCore.QMetaObject.connectSlotsByName(YeahdocList)

    def retranslateUi(self, YeahdocList):
        YeahdocList.setWindowTitle(_translate("YeahdocList", "Arcitle", None))
        self.yeahdoclisttree.setSortingEnabled(True)
        self.yeahdoclisttree.headerItem().setText(0, _translate("YeahdocList", "Title", None))
        self.yeahdoclisttree.headerItem().setText(1, _translate("YeahdocList", "CreateTime", None))
        self.yeahdoclisttree.headerItem().setText(2, _translate("YeahdocList", "Star", None))
        self.yeahdoclisttree.headerItem().setText(3, _translate("YeahdocList", "Lock", None))
        self.label.setText(_translate("YeahdocList", "Filter", None))
        self.bytitle.setText(_translate("YeahdocList", "by title", None))
        self.bycontent.setText(_translate("YeahdocList", "by content", None))
        self.yeahdoccategorylist.setSortingEnabled(False)

from PyQt5 import QtWebKit

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    YeahdocList = QtGui.QWidget()
    ui = Ui_YeahdocList()
    ui.setupUi(YeahdocList)
    YeahdocList.show()
    sys.exit(app.exec_())

