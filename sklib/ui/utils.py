# coding:utf-8
#
# Copyright (c) 2010, guo.li <lycying@gmail.com>
# Site < http://code.google.com/p/seeking/ >
# All rights reserved.
# vim: set ft=python sw=2 ts=2 et:
#

from PyQt5.QtGui import QApplication
from PyQt5.QtGui import QStyleFactory

from ..config import Prefs

def changeStyle(style_name):
    QApplication.setStyle(QStyleFactory.create(style_name))
    QApplication.setPalette(QApplication.style().standardPalette())
    Prefs.new().setStyle(style_name)
