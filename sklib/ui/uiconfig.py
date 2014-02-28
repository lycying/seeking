# coding:utf-8
#
# Copyright (c) 2010, guo.li <lycying@gmail.com>
# Site < http://code.google.com/p/seeking/ >
# All rights reserved.
# vim: set ft=python sw=2 ts=2 et:
#

from PyQt4.QtGui import QDialog
from PyQt4.QtGui import QApplication
from PyQt4.QtGui import QTreeWidgetItem
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QDialogButtonBox
from PyQt4.QtGui import QDesktopWidget

from PyQt4.QtCore import QObject
from PyQt4.QtCore import SIGNAL


from .Ui_ConfigDialog import Ui_ConfigDialog
from ..config import getPath
from ..xplugin import PluginAdapter

class ConfigQTreeWidgetItem(QTreeWidgetItem):
    def __init__(self,modName):
        QTreeWidgetItem.__init__(self)
        self.__pageName = modName
        
    def getPageName(self):
        """
        Public method to get the name of the associated configuration page.
        """
        return self.__pageName
            
class ConfigurationDialog(QDialog,Ui_ConfigDialog):
    
    __willsavepages = []
    
    def __init__(self,parent = None):
        """
        Constructor
        """
        QDialog.__init__(self,parent)
        self.setupUi(self)


        #center this window 
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)
        
        self.baseConfigItem={
                    "applicationPage":[QApplication.translate("ApplicationPage","Application"),getPath("iconDir","preferences-application.png"),"sklib.ui.cpages.applicationPage",None],
                    "shortcutsPage":[QApplication.translate("ShortcutsPage","Shortcuts"),getPath("iconDir","preferences-shortcuts.png"),"sklib.ui.cpages.shortcutsPage","applicationPage"],
                    }
        #read from plugins 
        for plugin in PluginAdapter().new().getPlugins():
            if hasattr(plugin,"getConfigPages"):
                ptems = plugin.getConfigPages()
                for pkey in ptems.keys():
                    if not self.baseConfigItem.__contains__(pkey):
                        self.baseConfigItem[pkey]=ptems[pkey]
        #end plugin parse
        self.itmDict = {}
        self.setupTreeList()
        self.btn.button(QDialogButtonBox.Apply).setEnabled(False)
        QObject.connect(self.configItemList, SIGNAL("itemClicked (QTreeWidgetItem *,int)"),self.evt_click)
        QObject.connect(self.btn, SIGNAL("clicked (QAbstractButton *)"),self.evt_btn_click)

    
    def setupTreeList(self,parent=None):
        for key in self.baseConfigItem.keys():
            self.setupTreeListItem(key)
            
    def setupTreeListItem(self,key):
        if key in self.itmDict: return
        
        value = self.baseConfigItem.get(key)
        treeitem = ConfigQTreeWidgetItem(value[2])
        treeitem.setIcon(0,QIcon(value[1]))
        treeitem.setText(0,value[0])
        
        if value[3] is not None:
            if  value[3] not in self.itmDict is not None:
                self.setupTreeListItem(value[3])
            self.itmDict[value[3]].addChild(treeitem)
            self.itmDict[value[3]].setExpanded(True)
        else:
            self.configItemList.addTopLevelItem(treeitem)
        #put it to cache 
        self.itmDict[key] = treeitem
    def __findConfigureItem(self,pageName):
        for i in range(self.configpages.count()):
            if self.configpages.widget(i).windowTitle()==pageName:
                return self.configpages.widget(i)
        return None
    def evt_click(self,item):
        findW = self.__findConfigureItem(item.getPageName())
        if findW:
            self.configpages.setCurrentWidget(findW)
        else:
            wd = self.__obtainConfigurationPage(item.getPageName())
            wd.setWindowTitle(item.getPageName())
            self.configpages.addWidget(wd)
            self.configpages.setCurrentWidget(wd)
           
            
    def __obtainConfigurationPage(self, modName):
        """
        Private method to import a configuration page module.
        """
        try:
            mod = __import__(modName)
            components = modName.split('.')
            for comp in components[1:]:
                mod = getattr(mod, comp)
            return mod.create(self)
        except ImportError:
            return None
        
    def evt_btn_click(self,btn):
        if btn == self.btn.button(QDialogButtonBox.Apply):
            self.save()
            self.btn.button(QDialogButtonBox.Apply).setEnabled(False)
        elif btn == self.btn.button(QDialogButtonBox.Save):
            self.save()
            self.close()
        else:
            self.close()
    def bufferMe(self,wd):
        for wdi in self.__willsavepages:
            if wdi.windowTitle() == wd.windowTitle():
                self.__willsavepages.remove(wdi)
        self.__willsavepages.append(wd)
        self.btn.button(QDialogButtonBox.Apply).setEnabled(True)
    def save(self):
        for wd in self.__willsavepages:
            wd.save()
            self.__willsavepages.remove(wd)
