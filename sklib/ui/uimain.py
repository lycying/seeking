# coding:utf-8
#
# Copyright (c) 2010, guo.li <lycying@gmail.com>
# Site < http://code.google.com/p/seeking/ >
# All rights reserved.
# vim: set ft=python sw=2 ts=2 et:
#

from PyQt4.QtGui import QMainWindow
from PyQt4.QtGui import QStyleFactory
from PyQt4.QtGui import QAction
from PyQt4.QtGui import QActionGroup
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QApplication
from PyQt4.QtGui import QTabWidget
from PyQt4.QtGui import QMessageBox
from PyQt4.QtGui import QTabBar
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QMenu
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtGui import QPushButton

from PyQt4.QtCore import QObject
from PyQt4.QtCore import QTranslator
from PyQt4.QtCore import QDir
from PyQt4.QtCore import Qt
from PyQt4.QtCore import SIGNAL

from .overlay import Overlay
from .mshow import SKMainTabShow

from .uiconfig import ConfigurationDialog
from .uiplugin import PluginInfoDialog,PluginRequestDialog
from .utils import changeStyle
from ..config import Prefs, getPath,getPrccisePath




class Seeking(QMainWindow):
    """
    Main window . menu , toolbar , centerWidget ,statuts bar....
    Qt Signals:
    -    updateWindows(): update the 'Window' menu , you can call it such as "self.emit(SIGNAL('updateWindows()'))"
    Some access method :
    -    menuBar: Seeking.new().menuBar()
    -    toolBar: Seeking.new().addToolBar()
    -    menuBar: Seeking.new().menuBar()
    -    statusBar:Seeking.new().statusBar..
    """
    __instance =  None
    @staticmethod
    def new():
        if not Seeking.__instance:
            Seeking.__instance = Seeking()
        return Seeking.__instance
    
    
    def getActions(self):
        """
        get All actions
        """
        return self.__actions
    
    def getAction(self,name):
        """
        actions that can called by seeking.new() 
        -
        -    gotohome
        -    help
        -    perferences
        """
        try:
            return self.__actions[name]
        except:
            return None
    def regAction(self,name,action):
        """
        add new action to actions list
        """
        self.__actions[name]=action
    def getMenu(self,name):
        """
        menus that can called by seeking.new()
        -
        -    file
        -    edit
        -    window
        -    settings
        """
        return self.__menus[name]
    def regMenu(self,name,menu):
        """
        add new menu to menus list
        unless you have many menus , we do not recommend you to do this
        """
        self.__menus[name]=menu
    
        
        
    def __init__(self):
        """
        (1) Add a tabWidget
        (2) Setup the main Window
        (3) Some basic event slot
        (4) read datas(menus , actions) 
        """
        QMainWindow.__init__(self)
        
        # attrs 
        # Notice: These attributes can not be put outside init method 
        
        self.__actions = {}
        self.__menus = {}
        self.__globalActionGroup = QActionGroup(self)
        
        #the main widget(Tab) that show all things 
        self.tabs = MainTabWidget(self)
        self.setCentralWidget(self.tabs)
        
        view = SKMainTabShow(self,self.tabs)
        self.tabs.addTab(view,QIcon(getPath("iconDir",'main.png')),QApplication.translate("default", "MainTab"))
        
        QObject.connect(self, SIGNAL("updateWindows()"),self.__updateWindows)
        
        self.__addBasicMenus()
        self.__addBasicActions()
    
    
    def __updateWindows(self):
        """
        when we open a new window or close a exist window . this function will be called 
        we refresh the window menu according the tab's item
        """
        self.getMenu("window").clear()
        self.getMenu("window").addAction(self.getAction("close"))
        self.getMenu("window").addSeparator()
        
        actions = {}
        for i in range(self.tabs.count()):
            actions[i] = QAction(self.tabs.tabBar().tabIcon(i),self.tabs.tabBar().tabText(i),self,\
                                                     triggered=lambda re,i=i:self.tabs.setCurrentIndex(i))
            
        for key in actions.keys():
            actions[key].setIconVisibleInMenu(True)
            self.getMenu("window").addAction(actions[key])
        #if only maintab . disable the close action
        if self.tabs.count()<=1:
            self.getAction("close").setEnabled(False)
        else:
            self.getAction("close").setEnabled(True)

    def __addBasicMenus(self):
        """
        basic menus 
        """
        #menu bar that plugins can call
        self.regMenu("file",\
                     self.menuBar().addMenu(QApplication.translate("default", "&File")))
        self.regMenu("edit",\
                     self.menuBar().addMenu(QApplication.translate("default", "Edit")))
        self.regMenu("settings",\
                     self.menuBar().addMenu(QApplication.translate("default", "Settings")))
        self.regMenu("window",\
                     self.menuBar().addMenu(QApplication.translate("default", "Window")))
        self.regMenu("plugins",\
                     self.menuBar().addMenu(QApplication.translate("default", "Plugins")))
        self.regMenu("help",\
                     self.menuBar().addMenu(QApplication.translate("AboutSeeking", "Help")))
    def __addBasicActions(self):
        """
        basic action 
        """
        self.regAction("gotohome",\
            QAction(QIcon(getPath("iconDir",'home.png')),QApplication.translate("default", "MainTab"),self,triggered=self.__evt_home))
        self.regAction("close",\
            QAction(QIcon(getPath("iconDir",'close.png')),QApplication.translate("default", "Close"),self,triggered=self.__evt_close_tab))
        self.regAction("perferences",\
            QAction(QIcon(getPath("iconDir",'settings.png')),QApplication.translate("default", "Preferences..."),self,triggered=self.__evt_preferences))
        self.regAction("plguinInfos", \
            QAction(QApplication.translate("default","Plugin Infos..."),self,triggered=lambda : PluginInfoDialog(self).show()))
        self.regAction("plguinRequest", \
            QAction(QApplication.translate("default","Available plugins..."),self,triggered=lambda : PluginRequestDialog(self).show()))
        
        self.getAction("gotohome").setShortcut(Prefs.new().getShortcut("gotohome","Ctrl+H"))
        self.getAction("close").setShortcut(Prefs.new().getShortcut("close","Ctrl+W"))
        self.getAction("perferences").setShortcut(Prefs.new().getShortcut("perferences",""))
        self.getAction("plguinInfos").setShortcut(Prefs.new().getShortcut("plguinInfos",""))
        self.getAction("plguinRequest").setShortcut(Prefs.new().getShortcut("plguinRequest",""))
    

        
    def __evt_close_tab(self):
        """
        Just click one button instead click the tab's close button
        """
        self.__evt_close_tab_click(self.tabs.currentIndex())
        
        
    def __evt_close_tab_click(self,index):
        """
        because the first tab is the main window we'll show 
        so we never close it .
        If the tab's content need save , we also remind the user.
        """
        self.tabs.emit( SIGNAL("tabCloseRequested (int)"),index)
        
        
    def __evt_home(self):
        """
        go to home
        """
        self.tabs.setCurrentIndex(0)
        
    
    def __evt_preferences(self):
        ConfigurationDialog(self).show()
    
    def __evt_changeLanguage(self,locale):
        Prefs.new().setLanguage(locale)
        QMessageBox.information(self,"Success",QApplication.translate("default","Success , this Will take effect at the next time"))

    def resizeEvent(self, event):
        """
        When resize window . the overlay also will be resize
        """
        self.overlay.resize(event.size())
        event.accept()
    
    def closeEvent(self,event):
        """
        The event handle match the main window . 
        We looply use the __evt_close_tab_click method 
        """
        if self.tabs.count()>1:
            for i in range(self.tabs.count()):
                if  i is not 0:
                    if self.__evt_close_tab_click(self.tabs.count()-1)=="cancel":
                        event.ignore()
                        break
                    else:
                        pass
                if self.tabs.count()<=1:
                    event.accept()
           
           
                    
    def beginFinalInit(self):
        """
        @see: startup
        Notice the __init__ method . we just setup the basic widget.
        And after the language , style ,plugins etc had loaded .
        we call this method . 
        
        Never call it unless you know what's it
        """
        #when at linux platform . the icon is not visible at menu .
        for key in self.__actions.keys():
            self.__actions.get(key).setIconVisibleInMenu(True)
            
        #--------------->>Seeking init <<-----------------#
        # __init__ menu
        self.getMenu("settings").addAction(self.getAction("perferences"))
        
        
        #i18n , must restart program to make it in use
        action_languages = QAction(QIcon(getPath('iconDir','languages.png')),QApplication.translate("default", "Languages"),self)
        action_languages.setIconVisibleInMenu(True)
        menu_languages = QMenu(self)
        
        trans_dir = QDir(getPrccisePath("transDir","","coredir"))
        fileNames = trans_dir.entryList(['i18n*.qm'], QDir.Files,QDir.Name)
        qmFiles = [trans_dir.filePath(fn) for fn in fileNames]
    
        for qmf in qmFiles: 
            translator = QTranslator() 
            translator.load(qmf)
            action = menu_languages.addAction(translator.translate("default", "English"))
            action.triggered.connect(lambda re,locale=translator.translate("default", "locale"):self.__evt_changeLanguage(locale))
        
        action_languages.setMenu(menu_languages)
        self.getMenu("settings").addAction(action_languages)
        
        #style menu use signalmapper
        action_style = QAction(QIcon(getPath('iconDir','style.png')),QApplication.translate("default", "Style"),self)
        action_style.setIconVisibleInMenu(True)
        menu_style = QMenu(self)
        for style_item in QStyleFactory.keys():
            action = menu_style.addAction(style_item)
            action.triggered.connect(lambda re,style_item=style_item:changeStyle(style_item))
        action_style.setMenu(menu_style)
        self.getMenu("settings").addAction(action_style)
        
        menu_plugin = self.getMenu("plugins")
        
        menu_plugin.addAction(self.getAction("plguinInfos"))
        
        menu_plugin.addSeparator()
        menu_plugin.addAction(self.getAction("plguinRequest"))
        
        #--------------->>Seeking init <<-----------------#
        # __init__ toolbar
        toolBar = self.addToolBar(QApplication.translate("default","common"))
        
        toolBar.addAction(self.getAction("perferences"))
        toolBar.addAction(self.getAction("close"))
        toolBar.addAction(self.getAction("gotohome"))
        toolBar.addAction(self.getAction("help"))
        
        #--------------->>Seeking init <<-----------------#
        # __init__ status bar
        self.statusBar().showMessage("Seeking ...")
        
        
        #--------------->>Seeking init <<-----------------#
        #Effects of a loading progress .
        #Results appear in the tab of the interior, the window has no effect on the global
        self.overlay = Overlay(self.centralWidget())
        self.overlay.hide()

        #--------------->>Seeking init <<-----------------#
        #other
        self.emit(SIGNAL('updateWindows()'))
        

class MainTabWidget(QTabWidget):
    """
    The main tabWidget
    """
    def __init__(self,parent=None):
        QTabWidget.__init__(self,parent)
        self.setTabBar(TabBarSupport(self))
        self.setMovable(False)
        self.setTabsClosable(True)
        self.setDocumentMode(False)
        
        
        self.navigationButton = QPushButton(QIcon(getPath('iconDir','navigation.png')),"",self)
        self.navigationButton.setFlat(True)
        
        self.closeButton = QPushButton(QIcon(getPath('iconDir','navclose.png')),"",self)
        self.closeButton.setFlat(True)
        
        self.rightCornerWidget = QWidget(self)
        self.rightCornerWidgetLayout = QHBoxLayout(self.rightCornerWidget)
        self.rightCornerWidgetLayout.setMargin(0)
        self.rightCornerWidgetLayout.setSpacing(0)
        self.rightCornerWidgetLayout.addWidget(self.navigationButton)
        self.rightCornerWidgetLayout.addWidget(self.closeButton)
        self.setCornerWidget(self.rightCornerWidget, Qt.TopRightCorner)
        
        QObject.connect(self.navigationButton, SIGNAL("pressed()"),self.__evt_navigation)
        QObject.connect(self.closeButton, SIGNAL("clicked(bool)"),lambda:self.emit(SIGNAL("tabCloseRequested (int)"),self.currentIndex()))
        QObject.connect(self, SIGNAL("tabCloseRequested (int)"),self.__evt_close_tab_click)
        QObject.connect(self.tabBar(), SIGNAL('customContextMenuRequested(const QPoint &)'),self.__evt_showContextMenu)
        
    def __evt_contextMenuCloseOthers(self,index):
        """
        Private method to close the other tabs.
        """
        for i in range(self.count() - 1, index, -1) :
            self.__evt_close_tab_click(i)
        for i in range(index - 1, -1, -1):
            self.__evt_close_tab_click(i)
                
    def __evt_showContextMenu(self,point):
        _tabbar = self.tabBar()
        for index in range(_tabbar.count()):
            rect = _tabbar.tabRect(index)
            if rect.contains(point):
                menu = QMenu(self)
                action = QAction("close",self,triggered=lambda:self.__evt_close_tab_click(index))
                action.setEnabled(self.count()>1 and index is not 0)
                menu.addAction(action)
                
                action = QAction("close others",self,triggered=lambda:self.__evt_contextMenuCloseOthers(index))
                action.setEnabled(self.count()>1)
                menu.addAction(action)
                
                action = QAction("close all",self,triggered=lambda:self.__evt_contextMenuCloseOthers(0))
                action.setEnabled(self.count()>1)
                menu.addAction(action)
                
                menu.exec_(self.mapToGlobal(point))
    def __evt_navigation(self):
        menu = QMenu()
        actions = {}
        for i in range(self.count()):
            actions[i] = QAction(self.tabBar().tabIcon(i),self.tabBar().tabText(i),self,\
                            triggered=lambda re,i=i:self.setCurrentIndex(i) and self.navigationButton)
        for key in actions.keys():
            actions[key].setIconVisibleInMenu(True)
            menu.addAction(actions[key])
        self.navigationButton.setMenu(menu)
        self.navigationButton.showMenu()
        menu.clear()
    def __evt_close_tab_click(self,index):
        """
        because the first tab is the main window we'll show 
        so we never close it .
        If the tab's content need save , we also remind the user.
        """
        if 0 == index :return
        
        if hasattr(self.widget(index),"bufferon") and  self.widget(index).bufferon():
            
                reply = QMessageBox.question(self, "Save or not?",
                    "Save your content first?\n%s" % self.tabText(index),
                    QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
                if reply == QMessageBox.Yes:
                    if hasattr(self.widget(index),"save"):
                        self.widget(index).save()
                        self.removeTab(index)
                        Seeking().new().emit(SIGNAL('updateWindows()'))
                        return "yes"
                elif reply == QMessageBox.No:
                    self.removeTab(index)
                    Seeking().new().emit(SIGNAL('updateWindows()'))
                    return "no"
                elif reply == QMessageBox.Cancel:
                    return "cancel"
        else:
                self.removeTab(index)
                Seeking().new().emit(SIGNAL('updateWindows()'))
                return "yes"
        
class TabBarSupport(QTabBar):
    """
    Class implementing a tab bar class substituting QTabBar to support wheel events.
    """
    def __init__(self, parent = None):
        """
        Constructor
        
        @param parent reference to the parent widget (QWidget)
        """
        QTabBar.__init__(self, parent)
        self._tabWidget = parent
        self.setContextMenuPolicy(Qt.CustomContextMenu)
    
    def wheelEvent(self, event):
        """
        Protected slot to support wheel events.
        
        @param reference to the wheel event (QWheelEvent)
        """
        try:
            if event.delta() > 0:
                self._tabWidget.prevTab()
            else:
                self._tabWidget.nextTab()
            
            event.accept()
        except AttributeError:
            pass
