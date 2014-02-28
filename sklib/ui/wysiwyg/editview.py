# coding:utf-8
#
# Copyright (c) 2010, guo.li <lycying@gmail.com>
# Site < http://code.google.com/p/seeking/ >
# All rights reserved.
# vim: set ft=python sw=2 ts=2 et:
#
import sys

from PyQt4.QtGui import QAction
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QTextEdit
from PyQt4.QtGui import QMenu


from PyQt4.QtCore import QObject
from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import pyqtSignature
from PyQt4.QtCore import QUrl


from PyQt4.QtWebKit import QWebView
from PyQt4.QtWebKit import QWebPage


from ...htmlfilter import htmlclean
from ...config import getPath,getPrccisePath
from .widgets import RichHtmlColorSelectorAction,RichHtmlTableAction,ImageDialog,LinkDialog,StyleDialog
from .syntax import Highlighter
class HtmlEditView(QWebView):
    @pyqtSignature("QString")
    def clicked_buttons(self, msg):
        """Open a message box and display the specified message."""
        for action in self.__editActions.values():
            action.setChecked(False)
            action.setEnabled(True)
            
        if ""==msg:
            pass
        else:
            try:
                for actionName in msg.split(","):
                    if not "" == actionName:
                        if actionName in self.__editActions:
                            self.__editActions[actionName].setChecked(True)
            except Exception as e:
                print(e)
                pass
        #disable some actions
        selectedText = self.page().selectedText()
        if None == selectedText or  ""==selectedText:
            self.__editActions["copy"].setEnabled(False)
            self.__editActions["bold"].setEnabled(False)
            self.__editActions["cut"].setEnabled(False)
            self.__editActions["italic"].setEnabled(False)
            self.__editActions["underline"].setEnabled(False)
            self.__editActions["strikethrough"].setEnabled(False)
            self.__editActions["removeformat"].setEnabled(False)
            self.__editActions["superscript"].setEnabled(False)
            self.__editActions["subscript"].setEnabled(False)
            self.__editActions["fgcolor"].setEnabled(False)
            self.__editActions["bgcolor"].setEnabled(False)
            
        self.__editActions["redo"].setEnabled(self.page().undoStack().canRedo())
        self.__editActions["undo"].setEnabled(self.page().undoStack().canUndo())
            
    def __init__(self,parent = None):
        QWebView.__init__(self,parent)
        self.page().setLinkDelegationPolicy(QWebPage.DontDelegateLinks)
        self.page().setContentEditable(True)
        

        QObject.connect(self, SIGNAL("loadFinished(bool)"), self.__evt_loadFinished)
        QObject.connect(self, SIGNAL("insertHTML(QString &)"), self.__evt_self_insert)
        QObject.connect(self, SIGNAL("changeColor(QString &,QString &)"), self.__evt_self_changecolor)
        
        self.__initActions()
        
        
    def __evt_loadFinished(self):
        # load jquery in global javascript env 
        self.page().mainFrame().addToJavaScriptWindowObject("wysiwyg", self)
        
        #jQuerySource = open(getPrccisePath("supportDir", "jquery.js","coredir")).read()
        #self.page().mainFrame().evaluateJavaScript(jQuerySource)
        jQuerySource = open(getPrccisePath("supportDir", "sk.editor.js","coredir")).read()
        self.page().mainFrame().evaluateJavaScript(jQuerySource)
        self.__evt_update_toolbar_signal()
        
            
        
    def editActions(self):
        """
        return all actions of html edit view
        """
        return self.__editActions
    def __initActions(self):
        """
        put all actions to dict , so we can use them outside
        """
        self.__editActions = {}
        
        
        self.__editActions["undo"] = QAction(QIcon(getPath('iconDir','heditor/undo.png')),"undo",
                                       self,triggered=lambda:self.__evt_webpage_emit(QWebPage.Undo))
        

        self.__editActions["redo"] = QAction(QIcon(getPath('iconDir','heditor/redo.png')),"redo",
                                       self,triggered=lambda:self.__evt_webpage_emit(QWebPage.Redo))

        self.__editActions["copy"] = QAction(QIcon(getPath('iconDir','heditor/copy.png')),"copy",
                                       self,triggered=lambda:self.__evt_webpage_emit(QWebPage.Copy))
        
        self.__editActions["selectall"] = QAction(QIcon(getPath('iconDir','heditor/selectall.png')),"Select All",
                                       self,triggered=lambda:self.__evt_webpage_emit(QWebPage.SelectAll))

        self.__editActions["cut"]  = QAction(QIcon(getPath('iconDir','heditor/cut.png')),"cut",
                                       self,triggered=lambda:self.__evt_webpage_emit(QWebPage.Cut))
        

        self.__editActions["paste"]  = QAction(QIcon(getPath('iconDir','heditor/paste_plain.png')),"paste",
                                       self,triggered=lambda:self.__evt_webpage_emit(QWebPage.PasteAndMatchStyle))
       

        self.__editActions["removeformat"]  = QAction(QIcon(getPath('iconDir','heditor/removeformat.png')),"removeformat",
                                       self,triggered=lambda:self.__evt_webpage_emit(QWebPage.RemoveFormat))
        
        self.__editActions["bold"]  = QAction(QIcon(getPath('iconDir','heditor/text_bold.png')),"bold",
                                       self,triggered=lambda:self.__evt_webpage_emit(QWebPage.ToggleBold))
        
        self.__editActions["italic"]  = QAction(QIcon(getPath('iconDir','heditor/text_italic.png')),"italic",
                                       self,triggered=lambda:self.__evt_webpage_emit(QWebPage.ToggleItalic))
        
        self.__editActions["underline"]  = QAction(QIcon(getPath('iconDir','heditor/text_underline.png')),"underline",
                                       self,triggered=lambda:self.__evt_webpage_emit(QWebPage.ToggleUnderline))
       
        self.__editActions["strikethrough"] = QAction(QIcon(getPath("iconDir", "heditor/strikethrough.png")),"strikethrough",\
                                        self,triggered=lambda:self.__evt_webpage_emit(QWebPage.ToggleStrikethrough))
        
        self.__editActions["subscript"] = QAction(QIcon(getPath("iconDir", "heditor/subscript.png")),"subscript",\
                                        self,triggered=lambda:self.__evt_webpage_emit(QWebPage.ToggleSubscript))
        
        self.__editActions["superscript"] = QAction(QIcon(getPath("iconDir", "heditor/superscript.png")),"superscript",\
                                        self,triggered=lambda:self.__evt_webpage_emit(QWebPage.ToggleSuperscript))
        
        self.__editActions["left"]  = QAction(QIcon(getPath('iconDir','heditor/text_align_left.png')),"left",
                                       self,triggered=lambda:self.__evt_webpage_emit(QWebPage.AlignLeft))
  
        self.__editActions["center"]  = QAction(QIcon(getPath('iconDir','heditor/text_align_center.png')),"center",
                                       self,triggered=lambda:self.__evt_webpage_emit(QWebPage.AlignCenter))
        

        self.__editActions["right"]  = QAction(QIcon(getPath('iconDir','heditor/text_align_right.png')),"right",
                                       self,triggered=lambda:self.__evt_webpage_emit(QWebPage.AlignRight))
       
        self.__editActions["justify"]  = QAction(QIcon(getPath('iconDir','heditor/text_align_justify.png')),"justify",
                                       self,triggered=lambda:self.__evt_webpage_emit(QWebPage.AlignJustified))
        
        self.__editActions["indent"]  = QAction(QIcon(getPath('iconDir','heditor/text_indent.png')),"indent",
                                       self,triggered=lambda:self.__evt_webpage_emit(QWebPage.Indent))
        
        self.__editActions["outdent"]  = QAction(QIcon(getPath('iconDir','heditor/text_indent_remove.png')),"outdent",
                                       self,triggered=lambda:self.__evt_webpage_emit(QWebPage.Outdent))
        
        self.__editActions["linkpage"] = QAction(QIcon(getPath('iconDir','heditor/linkpage.png')),"link page",
                                       self,triggered=lambda:LinkDialog(self).show())
        
        self.__editActions["image"] = QAction(QIcon(getPath('iconDir','heditor/image.png')),"insert image",
                                       self,triggered=lambda:ImageDialog(self).show())
        
        self.__editActions["orderedlist"] = QAction(QIcon(getPath('iconDir','heditor/orderedlist.png')),"InsertOrderedList",
                                       self,triggered=lambda:self.__evt_webpage_emit(QWebPage.InsertOrderedList))
        
        self.__editActions["unorderedlist"] = QAction(QIcon(getPath('iconDir','heditor/unorderedlist.png')),"InsertUnorderedList",
                                       self,triggered=lambda:self.__evt_webpage_emit(QWebPage.InsertUnorderedList) )
        
        self.__editActions["h1"] = QAction(QIcon(getPath('iconDir','heditor/h1.png')),"H1",
                                       self,triggered=lambda:self.__evt_formatblock(1))
        
        self.__editActions["h2"] = QAction(QIcon(getPath('iconDir','heditor/h2.png')),"H2",
                                       self,triggered=lambda:self.__evt_formatblock(2))
        
        self.__editActions["h3"] = QAction(QIcon(getPath('iconDir','heditor/h3.png')),"H3",
                                       self,triggered=lambda:self.__evt_formatblock(3))
        
        self.__editActions["htmlclean"] = QAction(QIcon(getPath('iconDir','heditor/html.png')),"Clean HTML",
                                       self,triggered=self.__evt_cleanhtml)
    
        
        self.__editActions["table"] = RichHtmlTableAction(self)
        
        self.__editActions["fgcolor"] = RichHtmlColorSelectorAction(self)
        
        action = RichHtmlColorSelectorAction(self,"backcolor")
        action.setIcon(QIcon(getPath('iconDir','heditor/paintcan.png')))
        action.setText("bgcolor")
        self.__editActions["bgcolor"] = action
        
        
        #Make sure the menu can show their icons
        for key in self.__editActions.keys():
            self.__editActions[key].setIconVisibleInMenu(True)
            self.__editActions[key].setCheckable(True)
        #below actions are not checkable
        for key in ["table","fgcolor","bgcolor","image","linkpage"]:
            self.__editActions[key].setCheckable(False)
    def __evt_cleanhtml(self):
        """
        clean up the html 
        """
        value = self.page().mainFrame().toHtml()
        value = htmlclean(value)
        self.fill(value)
        self.page().emit(SIGNAL("contentsChanged ()"))
        self.__editActions["htmlclean"].setChecked(False)
    
 
    def fill(self,html):
        if hasattr(self, "baseUrl"):
            if sys.platform.startswith("win"):
                self.page().mainFrame().setHtml(html,baseUrl=QUrl("file:///"+self.baseUrl))
            else:
                self.page().mainFrame().setHtml(html,baseUrl=QUrl("file://"+self.baseUrl))
        
    def setBaseUrl(self,baseURL):
        if baseURL is not None:
            self.baseUrl = baseURL.replace("\\","/")
            if not self.baseUrl.endswith("/"):
                self.baseUrl = self.baseUrl+"/"
        
        
    def __evt_formatblock(self,size):
        self.page().mainFrame().evaluateJavaScript("document.execCommand('formatblock','true','h%d')" % size)
        self.__evt_update_toolbar_signal()
        
    def __evt_self_insert(self,html):
        """
        common insert command use html5
        """
        self.page().mainFrame().evaluateJavaScript("document.execCommand('inserthtml','true','%s')" % html)
        self.page().emit(SIGNAL("contentsChanged ()"))
        
    
    def __evt_self_changecolor(self,attr,color):
        
        self.page().mainFrame().evaluateJavaScript("document.execCommand('%s','true','%s')"%(attr,color))
        self.page().emit(SIGNAL("contentsChanged ()"))
        
        
    def __evt_linkpage(self):
        """
        link another page . can access directly
        """ 
    def __evt_update_toolbar_signal(self):
        #Just send a javascript signal to make in use of it . And update the toolbar's states 
        self.page().mainFrame().evaluateJavaScript("$(document).trigger('click');")
        
    def __evt_webpage_emit(self,webaction):
        self.page().triggerAction(webaction,checked=True)
        self.__evt_update_toolbar_signal()
        
    def hasSelection(self):
        """
        return if has select text
        """
        return self.selectedText() is None
    
    def findNextPrev(self, txt, case, backwards, wrap):
        """
        Public slot to find the next occurrence of a text.
        """
        findFlags = QWebPage.FindFlags()
        if case:
            findFlags |= QWebPage.FindCaseSensitively
        if backwards:
            findFlags |= QWebPage.FindBackward
        if wrap:
            findFlags |= QWebPage.FindWrapsAroundDocument
        return self.findText(txt, findFlags)
    
    
    def _table_tr_movedown(self,tag):
        tr = tag.parent()
        tr.nextSibling().appendOutside(tr.takeFromDocument())
    def _table_tr_moveup(self,tag):
        tr = tag.parent()
        tr.appendOutside(tr.previousSibling().takeFromDocument())
    def _table_tr_insert_above(self,tag):
        tr = tag.parent()
        tr.prependOutside(tr.clone())
        
    def _table_tr_insert_below(self,tag):
        tr = tag.parent()
        tr.appendOutside(tr.clone())
    
    def _table_tr_remove(self,tag):
        tr = tag.parent()
        tr.removeFromDocument()
    def _table_delete(self,tag):
        table = tag.parent().parent()
        #this exists because the tbody 
        if not table.tagName().lower() == "table":
            table = table.parent()
        table.removeFromDocument()
    def _hit_column_counter(self,tag):
        count = 0
        hitElement = tag.previousSibling()
        while hitElement.tagName().lower()=="td":
            hitElement = hitElement.previousSibling()
            count += 1
        return count 
    def _table_column_left(self,tag):
        thisCol = self._hit_column_counter(tag)
        table = tag.parent().parent()
        #this exists because the tbody 
        if not table.tagName().lower() == "table":
            table = table.parent()
        for ele in table.findAll("td"):
            if thisCol == self._hit_column_counter(ele):
                ele.prependOutside("<td>&nbsp;</td>")
    def _table_column_right(self,tag):
        thisCol = self._hit_column_counter(tag)
        table = tag.parent().parent()
        #this exists because the tbody 
        if not table.tagName().lower() == "table":
            table = table.parent()
        for ele in table.findAll("td"):
            if thisCol == self._hit_column_counter(ele):
                ele.appendOutside("<td>&nbsp;</td>")
    def _table_column_remove(self,tag):
        cols = []
        thisCol = self._hit_column_counter(tag)
        table = tag.parent().parent()
        #this exists because the tbody 
        if not table.tagName().lower() == "table":
            table = table.parent()
        
        #avoid muti delete
        for ele in table.findAll("td"):
            if thisCol == self._hit_column_counter(ele):
                cols.append(ele)
        for ele in cols:
            ele.removeFromDocument()
    
    def _table_style_change(self,tag):
        table = tag.parent().parent()
        #this exists because the tbody 
        if not table.tagName().lower() == "table":
            table = table.parent()
        
        StyleDialog(self,table).show()
        
    def contextMenuEvent (self, e):
        """
        right click . table oprerators etc...
        """
        menu = QMenu(self)
        
        tag = self.page().mainFrame().hitTestContent(e.pos()).element()
        
        #some table operations
        if tag and tag.tagName().lower() == "td":
            hasPre =  tag.parent().previousSibling().tagName().lower()=="tr"
            hasNext =  tag.parent().nextSibling().tagName().lower()=="tr"
            #move up
            action = QAction(QIcon(getPath('iconDir','heditor/row_up.png')),"Move row up",self,triggered=lambda :self._table_tr_moveup(tag))
            action.setDisabled(not hasPre)
            action.setIconVisibleInMenu(True)
            menu.addAction(action)
            #move down
            action = QAction(QIcon(getPath('iconDir','heditor/row_down.png')),"Move row down",self,triggered=lambda :self._table_tr_movedown(tag))
            action.setDisabled(not hasNext)
            action.setIconVisibleInMenu(True)
            menu.addAction(action)
    
            
            menu.addAction(QAction("Copy row to above",self,triggered=lambda :self._table_tr_insert_above(tag)))
            menu.addAction(QAction("Copy row to below",self,triggered=lambda :self._table_tr_insert_below(tag)))
            menu.addAction(QAction(QIcon(getPath('iconDir','heditor/col_left.png')),"Insert column left",self,triggered=lambda :self._table_column_left(tag)))
            menu.addAction(QAction(QIcon(getPath('iconDir','heditor/col_right.png')),"Insert column right",self,triggered=lambda :self._table_column_right(tag)))
            
            action = QAction("Delete row",self,triggered=lambda :self._table_tr_remove(tag))
            action.setDisabled(not hasPre and not hasNext)
            menu.addAction(action)
            
            menu.addAction(QAction("Delete column",self,triggered=lambda :self._table_column_remove(tag)))
            
            action = QAction("Set Table Style",self,triggered=lambda :self._table_style_change(tag))
            menu.addAction(action)
            
            action = QAction(QIcon(getPath('iconDir','heditor/delete.png')),"Delete table",self,triggered=lambda :self._table_delete(tag))
            action.setIconVisibleInMenu(True)
            menu.addAction(action)
            
            menu.addSeparator()
             
        #Common content menu
        menu.addAction(self.__editActions["selectall"])
        menu.addAction(self.__editActions["copy"])
        menu.addAction(self.__editActions["cut"])
        menu.addAction(self.__editActions["paste"])
        menu.addSeparator()
        
        menuEdit = QMenu("Edit")
        menuEdit.addAction(self.__editActions["bold"])
        menuEdit.addAction(self.__editActions["italic"])
        menuEdit.addAction(self.__editActions["underline"])
        menuEdit.addAction(self.__editActions["strikethrough"])
        menuEdit.addAction(self.__editActions["removeformat"])
        menuEdit.addSeparator()
        menuEdit.addAction(self.__editActions["left"])
        menuEdit.addAction(self.__editActions["center"])
        menuEdit.addAction(self.__editActions["right"])
        menuEdit.addAction(self.__editActions["justify"])
        menuEdit.addSeparator()
        menuEdit.addAction(self.__editActions["indent"])
        menuEdit.addAction(self.__editActions["outdent"]) 
        menuEdit.addAction(self.__editActions["subscript"])
        menuEdit.addAction(self.__editActions["superscript"])
        
        
        menu.addMenu(menuEdit)
        menu.addSeparator()
        
        menuInsert = QMenu("Insert")
        menuInsert.addAction(self.__editActions["image"])
        menuInsert.addAction(self.__editActions["table"])
        menuInsert.addAction(self.__editActions["linkpage"])
        
        menu.addMenu(menuInsert)
        
            
        menu.exec_(e.globalPos())
        
        

class SouceView(QTextEdit):
    def __init__(self,parent = None):
        super(SouceView, self).__init__(parent)
        self.setAcceptRichText(False)
        self.highlighter = Highlighter(self.document())
