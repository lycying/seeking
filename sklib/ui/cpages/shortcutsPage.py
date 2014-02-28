# coding:utf-8
#
# Copyright (c) 2010, guo.li <lycying@gmail.com>
# Site < http://code.google.com/p/seeking/ >
# All rights reserved.
# vim: set ft=python sw=2 ts=2 et:
#

from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QTreeWidgetItem
from PyQt4.QtGui import QHeaderView
from PyQt4.QtGui import QKeySequence
from PyQt4.QtGui import QDialog
from PyQt4.QtGui import QDialogButtonBox
from PyQt4.QtGui import QApplication
from PyQt4.QtGui import QDesktopWidget

from PyQt4.QtCore import Qt
from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import QObject
from PyQt4.QtCore import QEvent

from .Ui_ShortcutsPage import Ui_ShortcutsPage
from .Ui_ShortcutDialog import Ui_ShortcutDialog
from ..uimain import Seeking
from ...xplugin import PluginAdapter
from ...config import Prefs


class ShortcutQTreeWidgetItem(QTreeWidgetItem):
    def __init__(self):
        QTreeWidgetItem.__init__(self)
        self.__shortcutmark = ""
        
    def setShorcutMark(self,value):
        self.__shortcutmark = value
        
    def getShorcutMark(self):
        """
        Public method to get the name of the associated configuration page.
        """
        return self.__shortcutmark
    
class ShortcutsPage(QWidget,Ui_ShortcutsPage):
    
    __buffer_keeper = []
    
    def __init__(self,dlg):
        """
        Constructor
        """
        QWidget.__init__(self)
        self.setupUi(self)


        #center this window 
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)
        self.shortcutsList.header().setResizeMode(0,QHeaderView.ResizeToContents)


        self.dlg = dlg
        
        self.shortcutDialog = ShortcutDialog()
        
        self.__setupActions(QApplication.translate("default","Global"),Seeking.new().getActions())
        self.__setupPlugins()
        
        QObject.connect(self.shortcutsList,\
                SIGNAL("itemDoubleClicked (QTreeWidgetItem *,int)"),\
                self.__evt_dbclick)
        QObject.connect(self.shortcutsList, SIGNAL("itemChanged (QTreeWidgetItem *,int)"),self.__has_change)
        QObject.connect(self.searchEdit,SIGNAL("textChanged (const QString&)"),self.__search)
        QObject.connect(self.shortcutDialog,SIGNAL("shortcutChanged"),self.__shortcut)
    
    def __shortcut(self,key):
        """
        shortcut
        """
        self.shortcutsList.currentItem().setText(1,key.toString())
    def __evt_dbclick(self,item,index):
        """
        double click
        """
        self.shortcutDialog.setKey(item.text(1))
        self.shortcutDialog.show()
        
    def __search(self,txt):
        """
        search match
        """
        for topIndex in range(self.shortcutsList.topLevelItemCount()):
            topItem = self.shortcutsList.topLevelItem(topIndex)
            childHiddenCount = 0
            for index in range(topItem.childCount()):
                itm = topItem.child(index)
                if  not itm.text(0).__contains__(txt):
                    itm.setHidden(True)
                    childHiddenCount += 1
                else:
                    itm.setHidden(False)
            topItem.setHidden(childHiddenCount == topItem.childCount())
    def __has_change(self,item,index):
        """
        pass other things . jus buffer me
        """
        self.dlg.bufferMe(self)
        
    def __setupActions(self,namespace,actions):
        """
        get the global shortcuts config and values
        """
        top = QTreeWidgetItem()
        top.setText(0,namespace)
        
        for key in actions.keys():
            action = actions.get(key)
            item = ShortcutQTreeWidgetItem()
            item.setShorcutMark(key)
            item.setText(0,action.text())
            item.setIcon(0,action.icon())
            
            skey = Prefs.new().getShortcut(key)
            if skey is None or skey == "":
                skey = action.shortcut().toString()
            item.setText(1,skey)
            top.addChild(item)
            
        self.shortcutsList.addTopLevelItem(top)
        top.setExpanded(True)
        
    def __setupPlugins(self):
        """
        setup the plugin's action
        """
        for plugin in PluginAdapter().new().getPlugins():
            
            
            if hasattr(plugin,"getActions"):
                actions_pe = plugin.getActions()
                self.__buffer_keeper.append(actions_pe)
                for key in actions_pe.keys():
                    self.__setupActions(key,actions_pe.get(key))
                   
                        
    def save(self):
        for item in self.shortcutsList.findItems(".*",Qt.MatchRegExp|Qt.MatchRecursive):
            if hasattr(item,"getShorcutMark"):
                Prefs.new().setShortCut(item.getShorcutMark(),item.text(1))


class ShortcutDialog(QDialog, Ui_ShortcutDialog):
    """
    Class implementing a dialog for the configuration of a keyboard shortcut.
    
    @signal shortcutChanged(QKeySequence) emitted 
        after the OK button was pressed
    """
    def __init__(self, parent = None, name = None, modal = False):
        """
        Constructor
        """
        QDialog.__init__(self, parent)
        if name:
            self.setObjectName(name)
        self.setModal(modal)
        self.setupUi(self)

        #center this window 
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)
        
        self.keyIndex = 0
        self.keys = [0, 0, 0, 0]
        
        self.objectType = None
        
        self.connect(self.primaryClearButton, SIGNAL("clicked()"), self.__clear)

        
        self.shortcutsGroup.installEventFilter(self)

        
        self.primaryClearButton.installEventFilter(self)
        
        
        self.buttonBox.button(QDialogButtonBox.Ok).installEventFilter(self)
        self.buttonBox.button(QDialogButtonBox.Cancel).installEventFilter(self)

    def setKey(self, key):
        """
        set key 
        """
        self.keyIndex = 0
        self.keys = [0, 0, 0, 0]
        self.keyLabel.setText(key)
        
       
        
    def on_buttonBox_accepted(self):
        """
        Private slot to handle the OK button press.
        """
        self.hide()
        self.emit(SIGNAL('shortcutChanged'), 
                  QKeySequence(self.keyLabel.text()))

    def __clear(self):
        """
        Private slot to handle the Clear button press.
        """
        self.keyIndex = 0
        self.keys = [0, 0, 0, 0]
        self.__setKeyLabelText("")
        
        
    def __setKeyLabelText(self, txt):
        """
        Private method to set the text of a key label.
        """
        
        self.keyLabel.setText(txt)
        
        
    def eventFilter(self, watched, event):
        """
        Method called to filter the event queue.
        """
        if event.type() == QEvent.KeyPress:
            self.keyPressEvent(event)
            return True
            
        return False
        
    def keyPressEvent(self, evt):
        """
        Private method to handle a key press event.        
        """
        if evt.key() == Qt.Key_Control:
            return
        if evt.key() == Qt.Key_Meta:
            return
        if evt.key() == Qt.Key_Shift:
            return
        if evt.key() == Qt.Key_Alt:
            return
        if evt.key() == Qt.Key_Menu:
            return
    
        if self.keyIndex == 4:
            self.keyIndex = 0
            self.keys = [0, 0, 0, 0]
    
        if evt.key() == Qt.Key_Backtab and evt.modifiers() & Qt.ShiftModifier:
            self.keys[self.keyIndex] = Qt.Key_Tab
        else:
            self.keys[self.keyIndex] = evt.key()
        
        if evt.modifiers() & Qt.ShiftModifier:
            self.keys[self.keyIndex] += Qt.SHIFT
        if evt.modifiers() & Qt.ControlModifier:
            self.keys[self.keyIndex] += Qt.CTRL
        if evt.modifiers() & Qt.AltModifier:
            self.keys[self.keyIndex] += Qt.ALT
        if evt.modifiers() & Qt.MetaModifier:
            self.keys[self.keyIndex] += Qt.META
        
        self.keyIndex += 1
        
        if self.keyIndex == 1:
            self.__setKeyLabelText(QKeySequence(self.keys[0]).toString())
        elif self.keyIndex == 2:
            self.__setKeyLabelText(QKeySequence(self.keys[0], self.keys[1]).toString())
        elif self.keyIndex == 3:
            self.__setKeyLabelText(QKeySequence(self.keys[0], self.keys[1],
                self.keys[2]).toString())
        elif self.keyIndex == 4:
            self.__setKeyLabelText(QKeySequence(self.keys[0], self.keys[1],
                self.keys[2], self.keys[3]).toString())
              
def create(dlg):
    return ShortcutsPage(dlg)
