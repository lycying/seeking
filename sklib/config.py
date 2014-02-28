# coding:utf-8
#
# Copyright (c) 2010, guo.li <lycying@gmail.com>
# Site < http://code.google.com/p/seeking/ >
# All rights reserved.
# vim: set ft=python sw=2 ts=2 et:
#

"""
Module containing the default configuration 
"""
import sys
import os


from PyQt4.QtCore import QSettings
from PyQt4.QtCore import QCoreApplication
from PyQt4.QtCore import QVariant

from PyQt4.QtCore import QUrl
from PyQt4.QtGui import QPixmap
from PyQt4.QtWebKit import QWebSettings

"""
all path that will keep our execute files 
The first is user home dir
Second is the ext dir
The last is core dir
Any resources exists in these dirs will be found .
"""
__extpaths = { "userdir":os.path.join(os.path.abspath(os.path.expanduser('~')),".seeking"),
              "coredir":os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])),""), }

#method that used at startup.py
def initExtPaths():
    """
    Add the paths to runtime path. This function is called when startup
    Never call it more than two times . No need to do it !
    """
    sys.path.append(value for value in __extpaths.values())
    

"""
A simple way to access the dir
"""
_pkg_config = { 'iconDir' : 'images/',
    'dataDir' : "datas/",
    'transDir': 'trans/' ,
    'pluginsDir':'plugins/',
    'supportDir':'support/',}

    
def getPaths(name,file):
    """
    get all paths if exists
    """
    paths=[]
    for value in __extpaths.values():
        path = os.path.join(os.path.join(value , _pkg_config.get(name)),file)
        if os.path.exists(path): paths.append(path)
    return paths

def getPrccisePath(name,file,directory):
    """
    get path by especial dir name . Like `getPrccisePath("dataDir","","userdir")`
    """
    return os.path.join(os.path.join(__extpaths[directory], _pkg_config.get(name)),file)

def getPath(name,file):
    '''
    Module function to get a configuration value.
    '''
    for key in ["userdir","coredir"]:
        path = os.path.join( os.path.join(__extpaths.get(key), _pkg_config.get(name)),file)
        if os.path.exists(path) : return path
    return None

class Prefs(object):
    __instance =  None
    @staticmethod
    def new():
        if not Prefs.__instance:
            Prefs.__instance = Prefs()            
        return Prefs.__instance
    
    """
    The main config tool . AAA===
    """
    uiDefaults={ "Language" : "System",
               "Style" : "System",
               "QuitOnClose":False}
    def __init__(self):
        self.settings = QSettings(QSettings.IniFormat,QSettings.UserScope,"SuperMoon","Seeking")
        #core attrs
        QCoreApplication.setOrganizationName("SuperMoon")
        QCoreApplication.setApplicationName("Seeking")
        
        try:
            from base64 import b64encode
            #css file
            b64 = str(b64encode(bytes(open(getPrccisePath("supportDir", "sk.css", "coredir"),"r").read(),encoding = "utf8")),encoding = "utf-8")
            QWebSettings.globalSettings().setUserStyleSheetUrl(QUrl('data:text/css;charset=utf-8;base64,%s'% b64))
            #QWebSettings.globalSettings().setUserStyleSheetUrl(QUrl.fromLocalFile())
        except:
            pass

        QWebSettings.globalSettings().setAttribute(QWebSettings.AutoLoadImages,True)
        QWebSettings.globalSettings().setAttribute(QWebSettings.JavascriptEnabled,True)
        QWebSettings.globalSettings().setAttribute(QWebSettings.PluginsEnabled,False)
        QWebSettings.globalSettings().setAttribute(QWebSettings.PrivateBrowsingEnabled,True)
        QWebSettings.globalSettings().setAttribute(QWebSettings.JavascriptCanOpenWindows,False)
        QWebSettings.globalSettings().setAttribute(QWebSettings.JavascriptCanAccessClipboard,True)
        QWebSettings.globalSettings().setAttribute(QWebSettings.ZoomTextOnly,False)
        QWebSettings.globalSettings().setAttribute(QWebSettings.OfflineStorageDatabaseEnabled,False)
        QWebSettings.globalSettings().setAttribute(QWebSettings.OfflineWebApplicationCacheEnabled,False)
        QWebSettings.globalSettings().setAttribute(QWebSettings.LocalStorageEnabled,False)
        QWebSettings.globalSettings().setAttribute(QWebSettings.LocalContentCanAccessRemoteUrls,False)
        QWebSettings.globalSettings().setAttribute(QWebSettings.DeveloperExtrasEnabled,True)
        
        QWebSettings.globalSettings().setWebGraphic(QWebSettings.MissingImageGraphic,QPixmap(getPath('iconDir','404.jpg')))
        
        
        
    def getSettings(self):
        """
        export self.settings viewable
        """
        return self.settings
    
    def getLanguage(self):
        """
        Module function to retrieve the language for the user interface.
        """
        lang = self.settings.value("UI/Language",QVariant(Prefs.uiDefaults["Language"])).toString()
        
        return None if lang is "None" or lang is "" or lang is None else lang
    
    def setLanguage(self,lang):
        """
        Module function to store the language for the user interface.
        """
        self.settings.setValue("UI/Language", QVariant("None" if lang is None else lang))
    
    def getStyle(self):
        """
        Module function to retrieve the style for the user interface.
        """
        style = self.settings.value("UI/Style",QVariant(Prefs.uiDefaults["Style"])).toString() 
        
        return None if style is "None" or style is "" or style is None else style
        
    
    def setStyle(self,style):
        """
        Module function to store the style for the user interface.
        """
        self.settings.setValue("UI/Style", QVariant("None" if style is None else style))
        
    def getQuitOnClose(self):
        """
        QApplication.setQuitOnLastWindowClosed(Value)
        """
        return self.settings.value("UI/QuitOnClose",\
                QVariant(Prefs.uiDefaults["QuitOnClose"])).toBool()
        
    def setQuitOnClose(self,value):
        """
        QApplication.setQuitOnLastWindowClosed(Value)
        """
        self.settings.setValue("UI/QuitOnClose", QVariant(False if value is None else  value))
        
    
    def getPluginState(self,pluginName):
        """
        get the state of plugin by name
        """
        return self.settings.value("Plugin/x/%s"%pluginName,\
                QVariant(True).toBool())
        
    def setPluginState(self,pluginName,value):
        """
        set the state of plguin
        """
        self.settings.setValue("Plugin/x/%s"%pluginName, QVariant(True if value is None else value))
        
    def setShortCut(self,name,value):
        """
        set the config shortcut
        """
        if value is not None:
            self.settings.setValue("UI/Shortcut/%s"%name,QVariant(value))
            
    def getShortcut(self,name,default=None):
        """
        get The configure shortcut , if not supply , then return default
        """
        return self.settings.value("UI/Shortcut/%s"%name,\
                                    QVariant(default)).toString()