# coding:utf-8
#
# Copyright (c) 2010, guo.li <lycying@gmail.com>
# Site < http://code.google.com/p/seeking/ >
# All rights reserved.
# vim: set ft=python sw=2 ts=2 et:
#

from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import pyqtSignature

from .uimain import Seeking

class PluginBase(object):
    """
    Normally all the widget that added to the QTabWidget will implements this.
    This class has a PluginBase var to handle some infomation of the widget
    such as {"url":url,"title":title,"tree":tree}
    in some instance , url is used to mark if tabed or not
    and also title may need at some other sence
    and tree is the content of all the xml 
    """
    
    def __init__(self):
        """
        just add more info to PluginBase
        """
        self.__keepme = None
        self.__bufferon = False
        
        
    def setBufferon(self,value):
        """
        used to jude if need save or not
        """
        self.__bufferon = value
    
    def bufferon(self):
        return self.__bufferon
    
    def setKeepme(self,value):
        """
        used to remember the widget by flag
        """
        self.__keepme = value
    
    def keepme(self):
        return self.__keepme
    
    def sendCommand(self,command):
        """
        This will cause change if command is send
        """
        pass
    
    def hasTabOne(self,me):
        
        tabs = Seeking().new().tabs
        if tabs.count()>0:
            for i in range(tabs.count()):
                if  hasattr(tabs.widget(i),"keepme") and tabs.widget(i).keepme() == me:
                    tabs.setCurrentIndex(i)
                    return True
        return False
    
    def execute(self,title,icon=None):
        """
        This is used to determine whether the tab is there.
        By checking the tabs that already opened , see if there is no duplication of 
        data (we use the 'type + id' approach to identity). 
        If you already have the tab, then just jump directly to the appropriate page.
    
        Params:
        Title:The tab text 
        Icon: The tab icon
        """
        if not self.hasTabOne(self.keepme()):
            self.before()
            
            Seeking().new().overlay.show()
            #notice this function need overrider to avoid more expcel
            try:
                self.invoke()
                index = Seeking().new().tabs.addTab(self,title)
                Seeking().new().emit(SIGNAL('updateWindows()'))
                if icon:
                    Seeking().new().tabs.setTabIcon(index,icon)
                Seeking().new().tabs.setCurrentIndex(index)
                Seeking().new().overlay.hidestop()
            except Exception as e:
                raise e
                self.close()
                
            self.after()
            
    def before(self):
        """
        actions before in use
        """
        pass
    def after(self):
        """
        actions after in use
        """
        pass
            
    def invoke(self):
        """
        real setup function . children may implement this 
        """
        pass
    @pyqtSignature("")
    def onbuffer(self):
        """
        Typically, each open windows has a 'if you want to save' attribute, 
        some of the operations within these windows at any time to influence the value of the attribute.
        When we close the window ,the first judge to see is 'if the contents of the window has been altered'.
        This can prompt the user to customize options.
        """
        if  not self.bufferon():
            index = Seeking().new().tabs.indexOf(self)
            Seeking().new().tabs.setTabText(index,"*%s"%Seeking().new().tabs.tabText(index))
            self.setBufferon(True)