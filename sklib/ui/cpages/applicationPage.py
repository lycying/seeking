# coding:utf-8
#
# Copyright (c) 2010, guo.li <lycying@gmail.com>
# Site < http://code.google.com/p/seeking/ >
# All rights reserved.
# vim: set ft=python sw=2 ts=2 et:
#

from PyQt5.QtGui import QWidget
from PyQt5.QtGui import QStyleFactory

from PyQt5.QtCore import QObject
from PyQt5.QtCore import SIGNAL

from .Ui_ApplicationPage import Ui_ApplicationPage
from ..utils import changeStyle
from ...config import Prefs
    
class ConfigApplicationPage(QWidget,Ui_ApplicationPage):    
    def __init__(self,dlg):
        """
        Constructor
        """
        QWidget.__init__(self)
        self.setupUi(self)
        self.dlg = dlg 
        
        self.styleSelector.addItem("System")
        for style_item in QStyleFactory.keys():
            self.styleSelector.addItem(style_item)
        for i in range(self.styleSelector.count()):
            if self.styleSelector.itemText(i)==Prefs.new().getStyle():
                self.styleSelector.setCurrentIndex(i)
                break
        self.quitOnClose.setChecked(Prefs.new().getQuitOnClose())
        
        QObject.connect(self.styleSelector, SIGNAL("currentIndexChanged (const QString&)"),self.__evt_style_change)
        QObject.connect(self.quitOnClose, SIGNAL("stateChanged (int)"),self.__evt_change)

    def __evt_change(self):
        self.dlg.bufferMe(self)
    def __evt_style_change(self,string):
        if Prefs.new().getStyle() == string:
            pass
        else:
            self.dlg.bufferMe(self)
            
    def save(self):
        changeStyle(self.styleSelector.currentText())
        Prefs.new().setQuitOnClose(self.quitOnClose.isChecked())
        
def create(dlg):
    return ConfigApplicationPage(dlg)
