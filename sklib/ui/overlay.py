# coding:utf-8
#
# Copyright (c) 2010, guo.li <lycying@gmail.com>
# Site < http://code.google.com/p/seeking/ >
# All rights reserved.
# vim: set ft=python sw=2 ts=2 et:
#

import math

from PyQt5.QtGui import QWidget
from PyQt5.QtGui import QPainter
from PyQt5.QtGui import QPalette
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QBrush
from PyQt5.QtGui import QPen

from PyQt5.QtCore import Qt


class Overlay(QWidget):
    """
    Open a large file or some more time-consuming operation, there will be a wait for results, and this is that widget
    """
    def __init__(self, parent = None):

        QWidget.__init__(self, parent)
        palette = QPalette(self.palette())
        palette.setColor(palette.Background, Qt.transparent)
        self.setPalette(palette)
        self.MINCOUNTER = 10

        self.minloopkeep = False
    def paintEvent(self, event):

        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(event.rect(), QBrush(QColor(255, 255, 255, 127)))
        painter.setPen(QPen(Qt.NoPen))

        for i in range(6):
            if (self.counter / 5) % 6 == i:
                painter.setBrush(QBrush(QColor(127 + (self.counter % 5)*32, 127, 127)))
            else:
                painter.setBrush(QBrush(QColor(127, 127, 127)))
            painter.drawEllipse(
                self.width()/2 + 30 * math.cos(2 * math.pi * i / 6.0) - 10,
                self.height()/2 + 30 * math.sin(2 * math.pi * i / 6.0) - 10, 20, 20)

        painter.end()
        
    def showEvent(self, event):

        self.timer = self.startTimer(20)
        self.counter = 0

    def timerEvent(self, event):

        self.counter += 1
        self.update()
        
        if self.minloopkeep:
            if self.counter == self.MINCOUNTER:
                self.killTimer(self.timer)
                self.hide()
    def hidestop(self):
        if self.counter <= self.MINCOUNTER:
            self.minloopkeep = True
        else:
            self.killTimer(self.timer)
            self.hide()
        
    def resizeEvent(self, event):
        self.parent().resize(event.size())
        event.accept()
