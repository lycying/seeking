# coding:utf-8
#
# Copyright (c) 2010, guo.li <lycying@gmail.com>
# Site < http://code.google.com/p/seeking/ >
# All rights reserved.
# vim: set ft=python sw=2 ts=2 et:
#

from PyQt4.QtGui import QSystemTrayIcon
from PyQt4.QtGui import QMenu
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QAction
from PyQt4.QtGui import qApp

from ..config import getPath
from .uimain import Seeking

class Trayer(QSystemTrayIcon):
    __instance =  None
    @staticmethod
    def new():
        if not Trayer.__instance:
            Trayer.__instance = Trayer()
        return Trayer.__instance
    
    def __init__(self):
        QSystemTrayIcon.__init__(self)

        self.trayIconMenu = QMenu(Seeking.new())
        self.trayIconMenu.addAction(QAction("Mi&nimize", self, triggered=Seeking.new().hide))
        self.trayIconMenu.addAction(QAction("Ma&ximize", self, triggered=Seeking.new().showMaximized))
        self.trayIconMenu.addAction(QAction("&Restore", self,  triggered=Seeking.new().showNormal))
        self.trayIconMenu.addSeparator()
        self.trayIconMenu.addAction(QAction("&Quit", self,triggered= qApp.quit))
        self.setContextMenu(self.trayIconMenu)
        
        self.setIcon(QIcon(getPath("iconDir","logo.png")))
        self.show()