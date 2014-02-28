# coding:utf-8
#
# Copyright (c) 2010, guo.li <lycying@gmail.com>
# Site < http://code.google.com/p/seeking/ >
# All rights reserved.
# vim: set ft=python sw=2 ts=2 et:
#


import os


from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import pyqtSignature
from PyQt4.QtGui import QAction
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QMenu
from PyQt4.QtGui import QPushButton

from sklib.config import getPath


class RichFlagButton(QPushButton):
    """
    This will send an event self.emit(SIGNAL("onbuffer()"))
    """
    def __init__(self, parent=None):
        QPushButton.__init__(self, parent)
        self.setMenu(self.__richflag())
        # flag
        self.setIcon(QIcon(getPath("iconDir", "yeahdoc/flag/default.png")))
        self.setText("default.png")
        
    def __richflag(self):
        """
        Show many many colorfull icon to make the yeahdoc flag . 
        """
        menu = QMenu(self)
        
        for item in os.listdir(getPath("iconDir", "yeahdoc/flag")):
            if item.endswith("png"):
                action = QAction(QIcon(getPath("iconDir", "yeahdoc/flag/%s" % item)), item, self, \
                        triggered=lambda re, item=item:self.__evt_richflag_menu_click(item))
                action.setIconVisibleInMenu(True)
                menu.addAction(action)
        return menu
        
    @pyqtSignature("")
    def __evt_richflag_menu_click(self, item):
        """
        IF ICON CHANGED , save flag will be active .
        """
        self.setIcon(QIcon(getPath("iconDir", "yeahdoc/flag/%s" % item)))
        self.setText(item)
        self.emit(SIGNAL("onbuffer()"))
        
