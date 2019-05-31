# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TodoLists.ui'
#
# Created: Mon Nov 22 20:54:44 2010
#      by: PyQt5 UI code generator 4.8
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_TodoLists(object):
    def setupUi(self, TodoList):
        TodoList.setObjectName(_fromUtf8("TodoList"))
        TodoList.setGeometry(QtCore.QRect(0, 0, 690, 553))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(TodoList.sizePolicy().hasHeightForWidth())
        TodoList.setSizePolicy(sizePolicy)
        TodoList.setAutoFillBackground(True)
        self.verticalLayout_3 = QtGui.QVBoxLayout(TodoList)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.mainlayout = QtGui.QVBoxLayout()
        self.mainlayout.setSizeConstraint(QtGui.QLayout.SetMaximumSize)
        self.mainlayout.setObjectName(_fromUtf8("mainlayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.pushButton = QtGui.QPushButton(TodoList)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.horizontalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtGui.QPushButton(TodoList)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.pushButton_3 = QtGui.QPushButton(TodoList)
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.horizontalLayout.addWidget(self.pushButton_3)
        self.titleeditor = QtGui.QLineEdit(TodoList)
        self.titleeditor.setObjectName(_fromUtf8("titleeditor"))
        self.horizontalLayout.addWidget(self.titleeditor)
        self.saveBtn = QtGui.QPushButton(TodoList)
        self.saveBtn.setObjectName(_fromUtf8("saveBtn"))
        self.horizontalLayout.addWidget(self.saveBtn)
        self.mainlayout.addLayout(self.horizontalLayout)
        self.splitlayout = QtGui.QHBoxLayout()
        self.splitlayout.setObjectName(_fromUtf8("splitlayout"))
        self.todolist = QtGui.QTreeWidget(TodoList)
        self.todolist.setMinimumSize(QtCore.QSize(500, 0))
        self.todolist.setAutoFillBackground(True)
        self.todolist.setAlternatingRowColors(True)
        self.todolist.setObjectName(_fromUtf8("todolist"))
        self.splitlayout.addWidget(self.todolist)
        self.rightlayout = QtGui.QVBoxLayout()
        self.rightlayout.setObjectName(_fromUtf8("rightlayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label = QtGui.QLabel(TodoList)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_2.addWidget(self.label)
        self.dateeditor = QtGui.QDateTimeEdit(TodoList)
        self.dateeditor.setMinimumSize(QtCore.QSize(100, 0))
        self.dateeditor.setMaximumSize(QtCore.QSize(200, 16777215))
        self.dateeditor.setCalendarPopup(True)
        self.dateeditor.setObjectName(_fromUtf8("dateeditor"))
        self.horizontalLayout_2.addWidget(self.dateeditor)
        self.rightlayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_2 = QtGui.QLabel(TodoList)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_3.addWidget(self.label_2)
        self.percenteditor = QtGui.QSpinBox(TodoList)
        self.percenteditor.setMinimumSize(QtCore.QSize(100, 0))
        self.percenteditor.setMaximumSize(QtCore.QSize(200, 16777215))
        self.percenteditor.setObjectName(_fromUtf8("percenteditor"))
        self.horizontalLayout_3.addWidget(self.percenteditor)
        self.rightlayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.label_3 = QtGui.QLabel(TodoList)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_4.addWidget(self.label_3)
        self.leveleditor = QtGui.QSpinBox(TodoList)
        self.leveleditor.setMinimumSize(QtCore.QSize(100, 0))
        self.leveleditor.setMaximumSize(QtCore.QSize(200, 16777215))
        self.leveleditor.setObjectName(_fromUtf8("leveleditor"))
        self.horizontalLayout_4.addWidget(self.leveleditor)
        self.rightlayout.addLayout(self.horizontalLayout_4)
        self.splitlayout.addLayout(self.rightlayout)
        self.mainlayout.addLayout(self.splitlayout)
        self.verticalLayout_3.addLayout(self.mainlayout)

        self.retranslateUi(TodoList)
        QtCore.QMetaObject.connectSlotsByName(TodoList)

    def retranslateUi(self, TodoList):
        TodoList.setWindowTitle(QtGui.QApplication.translate("TodoLists", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("TodoLists", "PushButton", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText(QtGui.QApplication.translate("TodoLists", "PushButton", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_3.setText(QtGui.QApplication.translate("TodoLists", "PushButton", None, QtGui.QApplication.UnicodeUTF8))
        self.saveBtn.setText(QtGui.QApplication.translate("TodoLists", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.todolist.setSortingEnabled(True)
        self.todolist.headerItem().setText(0, QtGui.QApplication.translate("TodoLists", "Title", None, QtGui.QApplication.UnicodeUTF8))
        self.todolist.headerItem().setText(1, QtGui.QApplication.translate("TodoLists", "EndTime", None, QtGui.QApplication.UnicodeUTF8))
        self.todolist.headerItem().setText(2, QtGui.QApplication.translate("TodoLists", "%", None, QtGui.QApplication.UnicodeUTF8))
        self.todolist.headerItem().setText(3, QtGui.QApplication.translate("TodoLists", "Important", None, QtGui.QApplication.UnicodeUTF8))
        self.todolist.headerItem().setText(4, QtGui.QApplication.translate("TodoLists", "Note", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("TodoLists", "Date:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("TodoLists", "Percent:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("TodoLists", "Level:", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    TodoList = QtGui.QWidget()
    ui = Ui_TodoLists()
    ui.setupUi(TodoList)
    TodoList.show()
    sys.exit(app.exec_())

