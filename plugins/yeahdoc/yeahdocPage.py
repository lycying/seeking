# coding:utf-8
#
# Copyright (c) 2010, guo.li <lycying@gmail.com>
# Site < http://code.google.com/p/seeking/ >
# All rights reserved.
# vim: set ft=python sw=2 ts=2 et:
#

from PyQt5.QtCore import QObject
from PyQt5.QtCore import SIGNAL
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QWidget

from plugins.yeahdoc.Ui_YeahdocPage import Ui_YeahdocPage
from plugins.yeahdoc.yeahdocsupport import YeahdocExtConfig
from sklib.ui.uimain import Seeking


class ConfigYeahdocPage(QWidget, Ui_YeahdocPage):
    def __init__(self, dlg):
        """
        Constructor
        """
        QWidget.__init__(self)
        self.setupUi(self)
        self.dlg = dlg

        self.config = YeahdocExtConfig()

        self.num.setText(self.config.getNumberPerPage())
        self.storedir.setText(self.config.getStoreDir())

        QObject.connect(self.num, SIGNAL("textChanged (const QString&)"), lambda: self.dlg.bufferMe(self))
        QObject.connect(self.storedir, SIGNAL("textChanged (const QString&)"), lambda: self.dlg.bufferMe(self))
        QObject.connect(self.brower, SIGNAL("clicked ()"), self.__evt_browser)

    def __evt_browser(self):
        directory = QFileDialog.getExistingDirectory(Seeking().new(), "Store Dir", self.config.getStoreDir(),
                                                     QFileDialog.ShowDirsOnly)
        if directory:
            self.storedir.setText(directory)

    def save(self):
        self.config.setNumberPerPage(self.num.text())
        self.config.setStoreDir(self.storedir.text())


def create(dlg):
    return ConfigYeahdocPage(dlg)
