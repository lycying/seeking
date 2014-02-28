# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PluginRequestDialog.ui'
#
# Created: Wed Mar 16 15:09:33 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_PluginRequestDialog(object):
    def setupUi(self, PluginRequestDialog):
        PluginRequestDialog.setObjectName(_fromUtf8("PluginRequestDialog"))
        PluginRequestDialog.resize(800, 600)
        PluginRequestDialog.setSizeGripEnabled(True)
        PluginRequestDialog.setModal(True)
        self.vboxlayout = QtGui.QVBoxLayout(PluginRequestDialog)
        self.vboxlayout.setObjectName(_fromUtf8("vboxlayout"))
        self.pluginList = QtGui.QTreeWidget(PluginRequestDialog)
        self.pluginList.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.pluginList.setRootIsDecorated(False)
        self.pluginList.setItemsExpandable(False)
        self.pluginList.setAllColumnsShowFocus(True)
        self.pluginList.setObjectName(_fromUtf8("pluginList"))
        self.vboxlayout.addWidget(self.pluginList)
        self.widget = QtGui.QWidget(PluginRequestDialog)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.progressBar = QtGui.QProgressBar(self.widget)
        self.progressBar.setProperty(_fromUtf8("value"), 0)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.verticalLayout.addWidget(self.progressBar)
        self.plugin_txt_url = QtGui.QLineEdit(self.widget)
        self.plugin_txt_url.setObjectName(_fromUtf8("plugin_txt_url"))
        self.verticalLayout.addWidget(self.plugin_txt_url)
        self.result_label = QtGui.QLabel(self.widget)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 85, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 85, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(190, 190, 190))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        self.result_label.setPalette(palette)
        self.result_label.setAutoFillBackground(True)
        self.result_label.setFrameShadow(QtGui.QFrame.Sunken)
        self.result_label.setText(_fromUtf8(""))
        self.result_label.setObjectName(_fromUtf8("result_label"))
        self.verticalLayout.addWidget(self.result_label)
        self.vboxlayout.addWidget(self.widget)
        self.widget_2 = QtGui.QWidget(PluginRequestDialog)
        self.widget_2.setObjectName(_fromUtf8("widget_2"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.widget_2)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(701, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.update = QtGui.QPushButton(self.widget_2)
        self.update.setObjectName(_fromUtf8("update"))
        self.horizontalLayout.addWidget(self.update)
        self.vboxlayout.addWidget(self.widget_2)

        self.retranslateUi(PluginRequestDialog)
        QtCore.QMetaObject.connectSlotsByName(PluginRequestDialog)

    def retranslateUi(self, PluginRequestDialog):
        PluginRequestDialog.setWindowTitle(QtGui.QApplication.translate("PluginRequestDialog", "Loaded Plugins", None, QtGui.QApplication.UnicodeUTF8))
        self.pluginList.setSortingEnabled(True)
        self.pluginList.headerItem().setText(0, QtGui.QApplication.translate("PluginRequestDialog", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.pluginList.headerItem().setText(1, QtGui.QApplication.translate("PluginRequestDialog", "Author", None, QtGui.QApplication.UnicodeUTF8))
        self.pluginList.headerItem().setText(2, QtGui.QApplication.translate("PluginRequestDialog", "Version", None, QtGui.QApplication.UnicodeUTF8))
        self.pluginList.headerItem().setText(3, QtGui.QApplication.translate("PluginRequestDialog", "Description", None, QtGui.QApplication.UnicodeUTF8))
        self.plugin_txt_url.setText(QtGui.QApplication.translate("PluginRequestDialog", "http://localhost/plugins.txt", None, QtGui.QApplication.UnicodeUTF8))
        self.update.setText(QtGui.QApplication.translate("PluginRequestDialog", "Update", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    PluginRequestDialog = QtGui.QDialog()
    ui = Ui_PluginRequestDialog()
    ui.setupUi(PluginRequestDialog)
    PluginRequestDialog.show()
    sys.exit(app.exec_())

