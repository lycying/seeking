# coding:utf-8
#
# Copyright (c) 2010, guo.li <lycying@gmail.com>
# Site < http://code.google.com/p/seeking/ >
# All rights reserved.
# vim: set ft=python sw=2 ts=2 et:
#


from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QAction
from PyQt4.QtGui import QApplication

from sklib.config import getPath, Prefs
from sklib.ui.uimain import Seeking

from plugins.yeahdoc.yeahdoceditor import AdapterYeahdocItemViewerAndEditor
from plugins.yeahdoc.yeahdoclist import AdapterMainYeahdocListView




#Info ===
name = "Yeahdoc Plugin"
author = "lycy < lycying@gmail.com >"
version = "0.1"
packageName = "__core__"
description = "Used to record you articals "
#Info ===

def install():
    """
    The function that init the plugin . just once .
    core package ignore
    """
    pass

def uninstall():
    """
    The method that remove the plugin .
    core package ignore
    """
    pass
def activate():
    """
    used to make use of the plugin
    """
    def __evt_new():
        """
        new yeahdoc evt 
        """
        yeahdoc = AdapterYeahdocItemViewerAndEditor(":new[Yeahdoc]")
        yeahdoc.setBufferon(True)
        yeahdoc.execute(":new[Yeahdoc]",QIcon(getPath('iconDir','yeahdoc/btn-new.png')))
        
    def __evt_list():
        """
        show yeahdoc list
        """
        yeahdoclist = AdapterMainYeahdocListView()
        yeahdoclist.execute(QApplication.translate("YeahdocList", "Yeahdoc"),QIcon(getPath('iconDir','yeahdoc/btn-list.png')))

    #setup the mainwindow UI 
    # New global action can be added to the list of global action
    sk = Seeking.new()
    
    sk.regAction("__yeahdoc_new",\
            QAction(QIcon(getPath('iconDir','yeahdoc/btn-new.png')),\
            QApplication.translate("YeahdocEditor","New Yeahdoc"),sk,\
            triggered=__evt_new))
    sk.regAction("__yeahdoc_list",\
            QAction(QIcon(getPath('iconDir','yeahdoc/btn-list.png')),\
            QApplication.translate("YeahdocList","Yeahdoc"),sk,\
            triggered=__evt_list))

    #set default shortcut
    sk.getAction("__yeahdoc_new").setShortcut(Prefs.new().getShortcut("__yeahdoc_new","Ctrl+N"))
    sk.getAction("__yeahdoc_list").setShortcut(Prefs.new().getShortcut("__yeahdoc_list","Ctrl+L"))

    #global toolbar
    toolbar = sk.addToolBar(QApplication.translate("Yeahdoc","Yeahdoc"))
    toolbar.addAction(sk.getAction("__yeahdoc_new"))
    toolbar.addAction(sk.getAction("__yeahdoc_list"))

    #global menu
    sk.getMenu("file").addAction(sk.getAction("__yeahdoc_new"))
    sk.getMenu("file").addAction(sk.getAction("__yeahdoc_list"))
    sk.getMenu("file").addSeparator()
    
def deactivate():
    """
    make this plugin disabled
    """
    pass
    
def getActions():
    """
    get All actions that will be config its shortcut
    """ 
    return {QApplication.translate("YeahdocList","Yeahdoc"):AdapterMainYeahdocListView().getActions(),\
            QApplication.translate("YeahdocEditor","Yeahdoc"):AdapterYeahdocItemViewerAndEditor().getActions()}

def getConfigPages():
    """
    The config page 
    """
    return {"yeahdocPage":[QApplication.translate("YeahdocPage","title"),\
            getPath("iconDir","yeahdoc/btn-list.png"),"plugins.yeahdoc.yeahdocPage",None],}
    