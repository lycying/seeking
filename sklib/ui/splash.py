# coding:utf-8
#
# Copyright (c) 2010, guo.li <lycying@gmail.com>
# Site < http://code.google.com/p/seeking/ >
# All rights reserved.
# vim: set ft=python sw=2 ts=2 et:
#

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QApplication
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QSplashScreen
from PyQt5.QtGui import QColor
from ..config import getPath


class SplashScreen(QSplashScreen):
    """
    Class implementing a splashscreen , Some ideas from  eric4 <http://eric-ide.python-projects.org/>.
    """
    def __init__(self):
        """
        Constructor
        """
        seeking = QPixmap(getPath('iconDir','splash.png'))
        self.labelAlignment = \
            Qt.Alignment(Qt.AlignBottom | Qt.AlignRight | Qt.AlignAbsolute)
        QSplashScreen.__init__(self, seeking)
        self.show()
        QApplication.flush()
        
    def showMessage(self, msg):
        """
        Public method to show a message in the bottom part of the splashscreen.
        
        @param msg message to be shown (string or QString)
        """
        QSplashScreen.showMessage(self, msg, self.labelAlignment, QColor(Qt.black))
        QApplication.processEvents()
        
    def clearMessage(self):
        """
        Public method to clear the message shown.
        """
        QSplashScreen.clearMessage(self)
        QApplication.processEvents()
