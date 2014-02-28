# coding:utf-8
#
# Copyright (c) 2010, guo.li <lycying@gmail.com>
# Site < http://code.google.com/p/seeking/ >
# All rights reserved.
# vim: set ft=python sw=2 ts=2 et:
#

from PyQt4.QtGui import QAction
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QApplication
from PyQt4.QtGui import QTabWidget
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QColorDialog
from PyQt4.QtGui import QTextEdit
from PyQt4.QtGui import QToolBar 
from PyQt4.QtGui import QLineEdit
from PyQt4.QtGui import QMenu
from PyQt4.QtGui import QPainter
from PyQt4.QtGui import QSplitter
from PyQt4.QtGui import QMovie
from PyQt4.QtGui import QLabel


from PyQt4.QtCore import QObject
from PyQt4.QtCore import QUrl
from PyQt4.QtCore import QMimeData
from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import Qt
from PyQt4.QtCore import QSize
from PyQt4.QtCore import QByteArray
from PyQt4.QtCore import QPoint
from PyQt4.QtCore import pyqtSignature

from PyQt4.QtWebKit import QWebView
from PyQt4.QtWebKit import QWebPage
from PyQt4.QtWebKit import QWebInspector

from PyQt4.QtNetwork import QNetworkReply

from ...htmlfilter import htmlclean
from ...config import getPath,getPrccisePath
from .widgets import RichHtmlColorSelectorAction,RichHtmlTableAction,SearchWidget,ImageDialog,LinkDialog,StyleDialog
from .syntax import Highlighter
from .editview import HtmlEditView,SouceView

class  HtmlWYSIWYG(QTabWidget):
    def __init__(self,parent=None):
        QTabWidget.__init__(self,parent)
        #some default value is needed
        self.setTabPosition(QTabWidget.South)
        self.setTabShape(QTabWidget.Triangular)
        self.setDocumentMode(True)
        
        self.__toolBar = QToolBar(self)
        self.__toolBar.setIconSize(QSize(16,16))
        self.__htmlEditorArea = HtmlEditView(self)
        #self.__htmlEditorArea.setBaseUrl(baseURL)
        self.__sourceView = SouceView(self)
        self.__searchBarForEditor = SearchWidget(self.__htmlEditorArea,self)
        self.__searchBarForEditor.setVisible(False)
        
        self.__inspector = None
        self.__inspectorSplitter = QSplitter(self)
        self.__inspectorSplitter.setOrientation(Qt.Vertical)
        
        self.__inspectorSplitter.addWidget(self.__htmlEditorArea)
        #tab1
        layout=QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setMargin(0)
        layout.addWidget(self.__toolBar)
        layout.addWidget(self.__searchBarForEditor)
        layout.addWidget(self.__inspectorSplitter)
        
        
        the_editor_tab=QWidget(self)
        the_editor_tab.setLayout(layout)
        the_editor_tab.setAutoFillBackground(True)

        self.addTab(the_editor_tab, "Edit")

        #tab2
        self.addTab(self.__sourceView, "Source")
        
        
        QObject.connect(self, SIGNAL("currentChanged (int)"),self.__evt_currentTabChange)
        #actions
        self.__setupToolBarAction()

    def accessPoint(self):
        return self.__htmlEditorArea.page()

    def __evt_currentTabChange(self,index):
        """
        change tab event
        """
        {
            0:lambda:self.__reloadHtmlFromSource(),
            1:lambda:self.__loadSourceFromEditView()
        }[index]()
    def __reloadHtmlFromSource(self):
        """
        load html from soruce edit . this used to edit your page directly
        """
        self.fill(self.__sourceView.toPlainText())
        
    def fill(self,value):
        """
        Fill html value 
        """
        self.__htmlEditorArea.fill(value)
    def setBaseUrl(self,baseURL):
        """
        set base url of the edit view
        """
        self.__htmlEditorArea.setBaseUrl(baseURL)
        
    def __loadSourceFromEditView(self):
        """
        load your source content from html view
        """
        value = self.__htmlEditorArea.page().mainFrame().toHtml()
        self.__sourceView.setPlainText(value)
    
    def __evt_inspector(self):
        if self.__inspector is None:
            self.__inspector = QWebInspector()
            self.__inspector.setPage(self.__htmlEditorArea.page())
            self.__inspectorSplitter.insertWidget(0,self.__inspector)
        else:
            self.__inspector.setVisible(not self.__inspector.isVisible())
        
    def __evt_find(self):
        self.__searchBarForEditor.setVisible(not self.__searchBarForEditor.isVisible()) 
        if self.__searchBarForEditor.isVisible():self.__searchBarForEditor.input.setFocus()
        
    def __setupToolBarAction(self):
        #find action
        findAction = QAction(QIcon(getPath('iconDir','heditor/find.png')),"Find",
                        self,triggered=self.__evt_find)
        findAction.setIconVisibleInMenu(True)
        findAction.setShortcut("Ctrl+F")

        self.__toolBar.addAction(self.__htmlEditorArea.editActions()["undo"])
        self.__toolBar.addAction(self.__htmlEditorArea.editActions()["redo"])
        self.__toolBar.addAction(self.__htmlEditorArea.editActions()["selectall"])
        self.__toolBar.addAction(self.__htmlEditorArea.editActions()["copy"])
        self.__toolBar.addAction(self.__htmlEditorArea.editActions()["cut"])
        self.__toolBar.addAction(self.__htmlEditorArea.editActions()["paste"])
        self.__toolBar.addSeparator()
        
        self.__toolBar.addAction(self.__htmlEditorArea.editActions()["bold"])
        self.__toolBar.addAction(self.__htmlEditorArea.editActions()["italic"])
        self.__toolBar.addAction(self.__htmlEditorArea.editActions()["underline"])
        self.__toolBar.addAction(self.__htmlEditorArea.editActions()["subscript"])
        self.__toolBar.addAction(self.__htmlEditorArea.editActions()["superscript"])
        self.__toolBar.addAction(self.__htmlEditorArea.editActions()["strikethrough"])
        
        self.__toolBar.addAction(self.__htmlEditorArea.editActions()["justify"])
        self.__toolBar.addAction(self.__htmlEditorArea.editActions()["left"])
        self.__toolBar.addAction(self.__htmlEditorArea.editActions()["center"])
        self.__toolBar.addAction(self.__htmlEditorArea.editActions()["right"])
        self.__toolBar.addAction(self.__htmlEditorArea.editActions()["orderedlist"])
        self.__toolBar.addAction(self.__htmlEditorArea.editActions()["unorderedlist"])
        self.__toolBar.addAction(self.__htmlEditorArea.editActions()["indent"])
        self.__toolBar.addAction(self.__htmlEditorArea.editActions()["outdent"])
        self.__toolBar.addAction(self.__htmlEditorArea.editActions()["h1"])
        self.__toolBar.addAction(self.__htmlEditorArea.editActions()["h2"])
        self.__toolBar.addAction(self.__htmlEditorArea.editActions()["h3"])

        self.__toolBar.addAction(self.__htmlEditorArea.editActions()["fgcolor"])
        self.__toolBar.addAction(self.__htmlEditorArea.editActions()["bgcolor"]) 
        self.__toolBar.addAction(self.__htmlEditorArea.editActions()["removeformat"])
        self.__toolBar.addSeparator()
        
        self.__toolBar.addAction(self.__htmlEditorArea.editActions()["image"])
        self.__toolBar.addAction(self.__htmlEditorArea.editActions()["linkpage"])
        self.__toolBar.addAction(self.__htmlEditorArea.editActions()["table"])
         
        
        self.__toolBar.addSeparator()
        action = QAction(QIcon(getPath('iconDir','heditor/inspector.png')),"WebInspector",
                                       self,triggered=self.__evt_inspector)

        action.setIconVisibleInMenu(True)
        self.__toolBar.addAction(action) 
        self.__toolBar.addAction(findAction)
        
        self.__toolBar.addSeparator()
        self.__toolBar.addAction(self.__htmlEditorArea.editActions()["htmlclean"])
        
    
