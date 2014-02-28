# coding:utf-8
#
# Copyright (c) 2010, guo.li <lycying@gmail.com>
# Site < http://code.google.com/p/seeking/ >
# All rights reserved.
# vim: set ft=python sw=2 ts=2 et:
#

import os

from PyQt4.QtGui import QAction
from PyQt4.QtGui import QWidgetAction
from PyQt4.QtGui import QCursor
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QColorDialog
from PyQt4.QtGui import QMenu
from PyQt4.QtGui import QPalette
from PyQt4.QtGui import QBrush
from PyQt4.QtGui import QColor
from PyQt4.QtGui import QPainter
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QToolTip
from PyQt4.QtGui import QDesktopWidget
from PyQt4.QtGui import QDialog
from PyQt4.QtGui import QDialogButtonBox

from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import Qt
from PyQt4.QtCore import QObject
from PyQt4.QtCore import pyqtSignature
from PyQt4.QtCore import QUrl

from ...config import getPath
from .Ui_SearchWidget import Ui_SearchWidget
from .Ui_Table import Ui_Table
from .Ui_Image import Ui_Image
from .Ui_Link import Ui_Link
from .Ui_StyleDialog import Ui_StyleDialog

class StyleDialog(QDialog,Ui_StyleDialog):
    def __init__(self,parent,ele):      
        QDialog.__init__(self,parent)
        self.setupUi(self)
        
        self.ele = ele 
        
        self.styleValue.setPlainText(self.ele.attribute("style",""))
        #center this window 
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)
        
        QObject.connect(self.btn, SIGNAL("clicked (QAbstractButton *)"),self.evt_btn_click)
        
    def evt_btn_click(self,btn):
        if btn == self.btn.button(QDialogButtonBox.Ok) :
            styleValue = self.styleValue.toPlainText()
            self.ele.setAttribute("style",styleValue)
            
class LinkDialog(QDialog,Ui_Link):
    def __init__(self,parent=None):
        QDialog.__init__(self,parent)
        self.setupUi(self)
        self.webview = parent
        #center this window 
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)
        
        QObject.connect(self.btn, SIGNAL("clicked (QAbstractButton *)"),self.evt_btn_click)
    
    def evt_btn_click(self,btn):
        if btn == self.btn.button(QDialogButtonBox.Ok) :
            #if web style url link
            if self.tab.currentIndex() is 0:
                urlStr  = self.url.text()
                if urlStr == "":return
                textStr = urlStr if ""==self.urltext.text() else self.urltext.text()
                linkStr = "<a href=\"%s\" %s>%s<\/a>"  % (urlStr,"" if ""==self.urlstyle.text() else "style=\"%s\""% self.urlstyle.text() , textStr)
                self.webview.emit(SIGNAL("insertHTML(QString &)"),linkStr)
        
class ImageDialog(QDialog,Ui_Image):
    def __init__(self,parent=None):
        QDialog.__init__(self,parent)
        self.setupUi(self)
        self.webview = parent
        #center this window 
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)
        
        self.preview.setHtml("<img src='../../images/logo.png'></img>",baseUrl=QUrl(os.getcwd()+"/support/image.html"))
        
        
        QObject.connect(self.btn, SIGNAL("clicked (QAbstractButton *)"),self.evt_btn_click)
        QObject.connect(self.uri,SIGNAL("textChanged (const QString&)"),self.evt_preview)
        QObject.connect(self.width,SIGNAL("valueChanged (const QString&)"),self.evt_preview)
        QObject.connect(self.height,SIGNAL("valueChanged (const QString&)"),self.evt_preview)
        QObject.connect(self.vspace,SIGNAL("valueChanged (const QString&)"),self.evt_preview)
        QObject.connect(self.hspace,SIGNAL("valueChanged (const QString&)"),self.evt_preview)
        QObject.connect(self.border,SIGNAL("valueChanged (const QString&)"),self.evt_preview)
        QObject.connect(self.alignment,SIGNAL("currentIndexChanged (int)"),self.evt_preview)
        
    def evt_preview(self, info=None):
        self.preview.setHtml(self.resultgen())
        
    def evt_btn_click(self,btn):
        rs = self.resultgen()
        if btn == self.btn.button(QDialogButtonBox.Ok) and rs is not "":
            self.webview.emit(SIGNAL("insertHTML(QString &)"),rs)
            
    def resultgen(self):
        widthStr = "" if self.width.value() is 0 else "width:%dpx;"%self.width.value()
        heightStr = "" if self.height.value() is 0 else "height:%dpx;"%self.height.value()
        borderStr = "" if self.border.value() is 0 else "border:%dpx solid #000;" %self.border.value()
        marginStr = "margin-left: %dpx; margin-right: %dpx;" % (self.vspace.value(),self.hspace.value())
        floatStr = "" if self.alignment.currentText() is "<not set>" else self.alignment.currentText()
            
        styleStr = "%s%s%s%s%s" %(widthStr,heightStr,borderStr,marginStr,floatStr)
            
        imgStr = "" if self.uri.text() == "" else "<img src=\"%s\" style=\"%s\" alt=\"%s\"></img>" % (self.uri.text(),styleStr,self.alt.text())
        
        return imgStr
        
class SearchWidget(QWidget, Ui_SearchWidget):
    """
    Class implementing the search bar for the web browser.
    """
    def __init__(self, page, parent = None):
        """
        Constructor
        
        @param mainWindow reference to the main window (QMainWindow)
        @param parent parent widget of this dialog (QWidget)
        """
        QWidget.__init__(self, parent)
        self.setupUi(self)
        
        self.__page = page
        
        
        self.wrapCheckBox.setChecked(True)
        self.closeButton.setIcon(QIcon(getPath('iconDir','heditor/close.png')))
        self.findPrevButton.setIcon(QIcon(getPath('iconDir','heditor/pre.png')))
        self.findNextButton.setIcon(QIcon(getPath('iconDir','heditor/next.png')))
        
        self.__defaultBaseColor = \
            self.input.palette().color(QPalette.Base)
        self.__defaultTextColor = \
            self.input.palette().color(QPalette.Text)
        
        self.findHistory = []
        self.havefound = False
        self.__findBackwards = False
        
        self.connect(self.input, SIGNAL("returnPressed()"), 
                     self.__findByReturnPressed)

    def on_findtextCombo_editTextChanged(self, txt):
        """
        Private slot to enable/disable the find buttons.
        """
        self.findPrevButton.setEnabled(not txt.isEmpty())
        self.findNextButton.setEnabled(not txt.isEmpty())

    def __findNextPrev(self):
        """
        Private slot to find the next occurrence of text.
        """
        self.infoLabel.clear()
        self.__setFindtextBackground(False)
        
        
        
        if not self.__page.findNextPrev(
                self.input.text(), 
                self.caseCheckBox.isChecked(), 
                self.__findBackwards, 
                self.wrapCheckBox.isChecked()):
            self.infoLabel.setText(self.trUtf8("Expression was not found."))
            self.__setFindtextBackground(True)
    @pyqtSignature("")
    def on_findNextButton_clicked(self):
        """
        Private slot to find the next occurrence.
        """
        
        self.__findBackwards = False
        self.__findNextPrev()
    
    def findNext(self):
        """
        Public slot to find the next occurrence.
        """
        self.on_findNextButton_clicked()

    @pyqtSignature("")
    def on_findPrevButton_clicked(self):
        """
        Private slot to find the previous occurrence.
        """
        self.__findBackwards = True
        self.__findNextPrev()
    
    def findPrevious(self):
        """
        Public slot to find the previous occurrence.
        """
        self.on_findPrevButton_clicked()
    
    def __findByReturnPressed(self):
        """
        Private slot to handle the returnPressed signal of the findtext combobox.
        """
        if self.__findBackwards:
            self.on_findPrevButton_clicked()
        else:
            self.on_findNextButton_clicked()



    @pyqtSignature("")
    def on_closeButton_clicked(self):
        """
        Private slot to close the widget.
        """
        self.close()
    
    def keyPressEvent(self, event):
        """
        Protected slot to handle key press events.
        
        @param event reference to the key press event (QKeyEvent)
        """
        if event.key() == Qt.Key_Escape:
            cb = self.__page
            if cb:
                cb.setFocus(Qt.ActiveWindowFocusReason)
            event.accept()
            self.close()
    
    def __setFindtextBackground(self, error):
        """
        Private slot to change the findtext combo background to indicate errors.
        
        @param error flag indicating an error condition (boolean)
        """
        le = self.input
        p = le.palette()
        if error:
            p.setBrush(QPalette.Base, QBrush(QColor("#FF6666")))
            p.setBrush(QPalette.Text, QBrush(QColor("#000000")))
        else:
            p.setBrush(QPalette.Base, self.__defaultBaseColor)
            p.setBrush(QPalette.Text, self.__defaultTextColor)
        le.setPalette(p)
        le.update()
        

class RichHtmlTableAction(QAction):
    def __init__(self,parent):
        QAction.__init__(self,parent)
        self.webview = parent
        self.setIcon(QIcon(getPath('iconDir','heditor/table.png')))
        self.setIconVisibleInMenu(True)
        self.setText("table")
        
        self.infolabel = QLabel("Insert a table")
        menu = QMenu(self.webview)
        
        action = QWidgetAction(self)
        action.setDefaultWidget(self.infolabel)
        menu.addAction(action)
        
        
        action = QWidgetAction(self)
        action.setDefaultWidget(RichHtmlTableQWidget(self))
        menu.addAction(action)
        
        
        #action = QAction(QIcon(getPath('iconDir','heditor/table1.png')),"insert styled table",self)
        #action.setIconVisibleInMenu(True)
        #menu.addAction(action)
        
        action = QAction("insert table...",self,triggered=lambda:RichHtmlTableQDialog(self.webview).show())
        action.setIconVisibleInMenu(True)
        action.setIcon(QIcon(getPath('iconDir','heditor/table.png')))
        
        menu.addAction(action)
        
        self.setMenu(menu)
        
            
class RichHtmlTableQWidget(QWidget):
    def __init__(self, richaction):
        QWidget.__init__(self)
        self.setMouseTracking(True)
        self.setCursor(QCursor(Qt.CrossCursor))
        self.richaction = richaction
        
        self.squareSize = 25
        
        self.lastKey = [0,0]
        
        self.setMinimumWidth(250)
        self.setMaximumWidth(250)
        self.setMinimumHeight(200)
        self.setMaximumHeight(200)
        

        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(event.rect(), Qt.white)

        for row in range(0, 8):
            for column in range(0, 10):
                painter.setPen(Qt.black)
                painter.drawRect(column * self.squareSize+2,
                        row * self.squareSize+2, self.squareSize-5,
                        self.squareSize-5)
                painter.setPen(Qt.gray)
                painter.drawRect(column * self.squareSize+3,
                        row * self.squareSize+3, self.squareSize-7,
                        self.squareSize-7)
                
                key = [ row , column] 
                if key == self.lastKey:
                    painter.setPen(QColor("#ef4810"))
                    for r in range(0,row+1):
                        for c in range(0,column+1):
                            painter.drawRect(c* self.squareSize+2,
                                    r* self.squareSize+2, self.squareSize -4,
                                    self.squareSize-4)
        
    
    def mouseMoveEvent(self, event):
        self.lastKey = [int(event.y() / self.squareSize) , int(event.x() / self.squareSize)]
        
        info =  repr(self.lastKey[1]+1)+"x"+repr(self.lastKey[0]+1)
        QToolTip.showText(event.globalPos(),"<span style='font-size:24px'>size:" +info +"</span>",self)
        self.richaction.infolabel.setText("<b>"+info+"</b> Table")
        self.update()
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton :
            self.richaction.webview.emit(SIGNAL("insertHTML(QString &)"),self.makeTableHtml())
            self.richaction.menu().hide()
        else:
            self.richaction.menu().hide()
    def makeTableHtml(self):
        table = "<table border=\"1\" width=\"100%\">"
        for r in range(0,self.lastKey[0]+1):
            table += "<tr>"
            for c in range(0,self.lastKey[1]+1):
                table += "<td>&nbsp;</td>"
                r+c
            table +="</tr>"
        table += "</table>"

        return table
            
class RichHtmlTableQDialog(QDialog,Ui_Table):
    def __init__(self,parent=None):
        QDialog.__init__(self,parent)
        self.setupUi(self)
        self.webview = parent
        #center this window 
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)
        
        QObject.connect(self.btn, SIGNAL("clicked (QAbstractButton *)"),self.evt_btn_click)
        QObject.connect(self.widthtype, SIGNAL("currentIndexChanged (const QString&)"),self.evt_px_percent)
        
    def evt_px_percent(self,value):
        if value=="pixels":
            self.width.setMaximum(2000)
            self.width.setValue(500)
        else:
            self.width.setMaximum(100)
            self.width.setValue(100)
            
        
    def evt_btn_click(self,btn):
        if btn == self.btn.button(QDialogButtonBox.Ok):
            rows = self.rows.value()
            columns = self.columns.value()
            
            if rows is 0 or columns is 0 : return
            
            
            widthStr = "width=\"%d%s" % ( self.width.value(),"px\"" if self.widthtype.currentText()=="pixels" else "%\"")
            heightStr = "" if 0==self.height.value() else "height=\"%d\"" % self.height.value()
            borderStr = "border=\"%d\"" % self.border.value()
            cellStr = "cellpadding=\"%d\" cellspacing=\"%d\"" % (self.cellspacing.value(),self.cellpadding.value())
            idStr = "" if ""==self.id.text() else "id=\"%s\"" % self.id.text()
            style = "" if ""==self.style.text() else "style=\"%s\"" % self.style.text()
            
            
            table = "<table %s %s %s %s %s %s>" % (widthStr,heightStr,borderStr,cellStr,idStr,style)
            for r in range(0,rows):
                table += "<tr>"
                for c in range(0,columns):
                    table += "<td>&nbsp;</td>"
                    r+c
                table +="</tr>"
            table += "</table>"
            
            self.webview.emit(SIGNAL("insertHTML(QString &)"),table)
        else:
            pass
class RichHtmlColorSelectorAction(QAction):
    def __init__(self,parent,attr="forecolor"):
        QAction.__init__(self,parent)
        self.webview = parent
        self.attr = attr
        self.setIcon(QIcon(getPath('iconDir','heditor/paintbrush.png')))
        self.setIconVisibleInMenu(True)
        self.setText("fgcolor")
        
        menu = QMenu(self.webview)
        
        action = QWidgetAction(self)
        action.setDefaultWidget(RichHtmlColorSelectorQWidget(self,self.webview))
        
        menu.addAction(action)
        
        action = QAction("more...",self,triggered = self.__evt_color)
        menu.addAction(action)
        
        self.setMenu(menu)
        
    def __evt_color(self):
        color = QColorDialog().getColor(Qt.green, self.webview)
        if color.isValid():
            self.webview.emit(SIGNAL("changeColor(QString &,QString &)"),self.attr,color.name())
class RichHtmlColorSelectorQWidget(QWidget):
    def __init__(self, richaction,webview):
        QWidget.__init__(self)
        self.setMouseTracking(True)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.richaction = richaction
        self.webview = webview
        self.lastKey = "-1-1"
        
        self.squareSize = 24
        self.basiccolors = {
                    "00":"#000000","10":"#800000","20":"#8b4513","30":"#2f4f4f",
                    "40":"#008080","50":"#000080","60":"#4b0082","70":"#696969",
                    "01":"#b22222","11":"#a52a2a","21":"#daa520","31":"#006400",
                    "41":"#40e0d0","51":"#0000cd","61":"#800080","71":"#808080",
                    "02":"#ff0000","12":"#ff8c00","22":"#ffd700","32":"#008000",
                    "42":"#00ffff","52":"#0000ff","62":"#ee82ee","72":"#a9a9a9",
                    "03":"#ffa07a","13":"#ffa500","23":"#ffff00","33":"#00ff00",
                    "43":"#afeeee","53":"#add8e6","63":"#dda0dd","73":"#d3d3d3",
                    "04":"#fff0f5","14":"#faebd7","24":"#ffffe0","34":"#f0fff0",
                    "44":"#f0ffff","54":"#f0f8ff","64":"#e6e6fa","74":"#ffffff"}

        self.setMinimumHeight(self.squareSize*5)
        self.setMaximumHeight(self.squareSize*5)
        self.setMinimumWidth(self.squareSize*8)
        self.setMaximumWidth(self.squareSize*8)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(event.rect(), Qt.white)
        
        for row in range(0, 5):
            for column in range(0, 8):
                key = repr(column)+repr(row)
                painter.fillRect(column * self.squareSize+5,
                        row * self.squareSize+5, self.squareSize-9,
                        self.squareSize-9,QColor(self.basiccolors[key]))
                
                painter.setPen(Qt.darkGray)
                painter.drawRect(column * self.squareSize+3,
                        row * self.squareSize+3, self.squareSize-6,
                        self.squareSize-6)
                if key == self.lastKey:
                    painter.setPen(Qt.blue)
                    painter.drawRect(column * self.squareSize+1,
                        row * self.squareSize+1, self.squareSize-2,
                        self.squareSize-2)
                
    def mouseMoveEvent(self, event):
        self.lastKey = repr( event.x() / self.squareSize)+repr(event.y() / self.squareSize)
        self.update()
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.richaction.webview.emit(SIGNAL("changeColor(QString &,QString &)"),self.richaction.attr,self.basiccolors[repr( int(event.x() / self.squareSize))+repr(int(event.y() / self.squareSize))])
            self.richaction.menu().hide()
        else:
            self.richaction.menu().hide()
