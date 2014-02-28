# coding:utf-8
#
# Copyright (c) 2010, guo.li <lycying@gmail.com>
# Site < http://code.google.com/p/seeking/ >
# All rights reserved.
# vim: set ft=python sw=2 ts=2 et:
#


from PyQt4.QtGui import QGridLayout
from PyQt4.QtGui import QPlainTextEdit
from PyQt4.QtGui import QPushButton
from PyQt4.QtGui import QLineEdit

from PyQt4.QtGui import QWidget

        
class SKMainTabShow(QWidget): 
    
    def __init__(self,seeking,parent=None):
        super(SKMainTabShow,self).__init__(parent)
        self.seeking = seeking
        self.invoke()

    def invoke(self):
        searchInput = QLineEdit()
        normalInput = QPlainTextEdit()
        normalInput.setMaximumHeight(100)
        searchBtn = QPushButton("Search")
        sayBtn = QPushButton("Hmm..")
        
        
        listTops = QWidget()
        
        layoutWidget = QGridLayout()
        layoutWidget.addWidget(searchInput,1,0)
        layoutWidget.addWidget(searchBtn,1,1)
        layoutWidget.addWidget(normalInput,2,0)
        layoutWidget.addWidget(sayBtn,2,1)
        layoutWidget.addWidget(listTops,3,0,8,1)
        
        self.setLayout(layoutWidget)
