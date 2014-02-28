# coding:utf-8
#
# Copyright (c) 2010, guo.li <lycying@gmail.com>
# Site < http://code.google.com/p/seeking/ >
# All rights reserved.
# vim: set ft=python sw=2 ts=2 et:
#

import sys

from PyQt4.QtGui import QApplication
from PyQt4.QtGui import QIcon
from PyQt4.QtCore import QTranslator
from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import SLOT
from PyQt4.QtCore import QLocale
from PyQt4.QtCore import QDir

from .xplugin import PluginAdapter
from .ui.splash import SplashScreen
from .ui.uimain import Seeking
from .ui.utils import changeStyle
from .config import Prefs, getPath, getPaths
from .ui.tray import Trayer
from .config import initExtPaths

splash = None
mainWin = None
translators =  []
trayer = None

def __startupMainWindow():
    """
    startup default mainWindow
    """
    global splash,mainWin
    splash.showMessage("Startup main window")
    mainWin = Seeking.new()
    splash.showMessage("read the default windows style")
    
def __startupPlugins():
    """
    load all plugins and setup them .
    they may add toolbars or menus and other goodaddones
    """
    global splash
    splash.showMessage("load plugins ...")
    PluginAdapter.new().finalizeActivate()
    
def __startupLanguage0(locale):
    global translators
    for dirname in getPaths("transDir",""):
        trans_dir = QDir(dirname)
        fileNames = trans_dir.entryList(['*%s.qm'%locale], QDir.Files,QDir.Name)
        qmFiles = [trans_dir.filePath(fn) for fn in fileNames]
        for qmf in qmFiles:
            translator =  QTranslator()
            translator.load(qmf)
            translators.append(translator)
    
def __startupLanguage():
    """
    Function to load all required translations qm files.
    defaut we use system langages . If no this file , we just set 
    it to english.
    If user have set the language , we just load what it is 
    """
    global splash,translators
    splash.showMessage("load default languages ...")
    
    prefs = Prefs.new()
        
    if prefs.getLanguage()=="System":
        try:
            __startupLanguage0(QLocale.system().name())
        except:
            __startupLanguage0("en_US")
    else:
        try:
            __startupLanguage0(prefs.getLanguage())
        except:
            __startupLanguage0("en_US")
    # install this trans file to global
    for translator in translators:
        QApplication.installTranslator(translator) 
def __startupConfigureStyle():
    """
    Get the saved config values from ini file and make use of them
    """
    global splash
    prefs = Prefs.new()
    
    #setup windows style
    try:
        if prefs.getStyle()=="System":
            pass
        else:
            splash.showMessage("load default style ...")
            changeStyle(prefs.getStyle())
    except Exception:
        pass
def __startupTrayer():
    """
    setup trayer icon
    """
    global trayer
    trayer = Trayer.new()
    
def main():
    global splash,mainWin
    
    initExtPaths()

    
    # the app will be start first 
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(getPath("iconDir","logo.png")))
    #if close the window from tray icon
    if Prefs.new().getQuitOnClose():
        app.setQuitOnLastWindowClosed(True)
        app.connect(app, SIGNAL("lastWindowClosed()"), app, SLOT("quit()"))
    else:
        app.setQuitOnLastWindowClosed(False)        
        
    #read the public qss style file
    #file_t = open(getPath("iconDir","theme/public.qss"),"r")
    #app.setStyleSheet(file_t.read())
    #file_t.close()

    #the splash instance
    splash = SplashScreen()
    
    #set the language first
    __startupLanguage()
    #just start the main window , and do nothing at all
    __startupMainWindow()
    #read plugins and setup many things such as menus , toolbar , actions etc
    __startupPlugins()
    #after all finished . we now start add some goodness to the main window
    mainWin.beginFinalInit()
    #make default the style 
    __startupConfigureStyle()
    
    __startupTrayer()
    #stop the splash window and close it 
    splash.clearMessage()
    splash.close()
    splash.destroy()
    splash = None
    
    #now we can make the mainwindow visualable. you may really like maximize it 
    mainWin.show()
        
    
    mainWin.showMaximized()
    
    sys.exit(app.exec_())
