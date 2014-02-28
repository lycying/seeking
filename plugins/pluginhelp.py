# coding:utf-8
#
# Copyright (c) 2010, guo.li <lycying@gmail.com>
# Site < http://code.google.com/p/seeking/ >
# All rights reserved.
# vim: set ft=python sw=2 ts=2 et:
#

import sys
import os

from PyQt4.QtGui import QDialog
from PyQt4.QtGui import QAction
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QApplication
from PyQt4.QtGui import qApp
from PyQt4.QtGui import QWhatsThis
from PyQt4.QtGui import QDesktopWidget

from PyQt4.QtCore import qVersion
from PyQt4.QtCore import PYQT_VERSION_STR
from PyQt4.QtCore import QUrl

from plugins.help.Ui_AboutSeeking import Ui_AboutSeeking
from sklib.ui.support import PluginBase
from sklib.ui.uimain import Seeking
from sklib.config import getPath
from sklib.ui.wysiwyg.browserview import HtmlBrowser

#Info ===
name = "Help"
author = "lycy < lycying@gmail.com >"
version = "0.1"
packageName = "__core__"
description = "Help and about infomations "
#Info ===

def install(): pass#pass
def uninstall(): pass#pass
def activate():
    def _evt_help(self):
        """
        Help event
        """
        Help().execute(QApplication.translate("AboutSeeking", "Help"),QIcon(getPath("iconDir",'help.png')))
        
    def _evt_checkupdate(self):
        """
        Check update
        """
        Update().execute(QApplication.translate("AboutSeeking", "Check for Updates..."),QIcon(getPath("iconDir",'help.png')))


    def _evt_bug(self):
        """
        Bug event
        """
        Bug().execute(QApplication.translate("AboutSeeking", "Report bug"),QIcon(getPath("iconDir",'help.png')))
        

    def _evt_showversions(self):
        """
        Show versions
        """
        ShowVersions().execute(QApplication.translate("AboutSeeking", "Show Versions"),QIcon(getPath("iconDir",'help.png')))
        
        
    def _evt_aboutseeking(self):
        """
        About Seeking
        """  
        About(Seeking.new()).show()
    
        
    
    sk = Seeking.new()
    sk.regAction("help",\
            QAction(QIcon(getPath("iconDir",'help.png')),QApplication.translate("AboutSeeking", "Help"),sk,triggered=_evt_help))
     
    menu_about = sk.getMenu("help")
    menu_about.addAction(QAction(QApplication.translate("AboutSeeking","About Seeking"),sk,\
                triggered=_evt_aboutseeking))
    menu_about.addAction(QAction(QApplication.translate("AboutSeeking","About Qt"),sk,\
                triggered=qApp.aboutQt))
    menu_about.addAction(QAction(QApplication.translate("AboutSeeking","Show Versions"),sk,\
                triggered=_evt_showversions))
    menu_about.addSeparator()
    menu_about.addAction(QAction(QApplication.translate("AboutSeeking","Check for Updates..."),sk,\
                triggered=_evt_checkupdate))
    menu_about.addAction(QAction(QApplication.translate("AboutSeeking","Report bug"),sk,\
                triggered=_evt_bug))
    menu_about.addSeparator()
    menu_about.addAction(QAction(QApplication.translate("AboutSeeking","What's This?"),sk,
                triggered=QWhatsThis.enterWhatsThisMode))
    menu_about.addAction(sk.getAction("help"))

def deactivate(): pass


Name="Seeking"
Homepage="http://code.google.com/p/seeking/"
Issuespage="http://code.google.com/p/seeking/issues/list"
Version="0.1 (r244)"
Feadback="guo.li <lycying@gmail.com>"
Copyright="Copyright (c) 2010, guo.li <lycying@gmail.com>"
UpdateSite="http://code.google.com/p/seeking/downloads/list"

class Help(HtmlBrowser,PluginBase):
    def __init__(self,parent=None):
        HtmlBrowser.__init__(self)
        PluginBase.__init__(self)
        self.setKeepme("[about]help")
        
    def invoke(self):
        url = os.path.join(os.path.dirname(sys.argv[0]),"../doc/build/html/index.html")
        url = url.replace("\\\\", "/").replace("\\", "/")
        if not os.path.exists(url):
            url = Homepage
            
        self.webview().setUrl(QUrl(url))

class Bug(HtmlBrowser,PluginBase):
    def __init__(self,parent=None):
        HtmlBrowser.__init__(self)
        PluginBase.__init__(self)
        
        self.setKeepme("[about]bug")
        
    def invoke(self):
        self.webview().setUrl(QUrl(Issuespage))
        
class Update(HtmlBrowser,PluginBase):
    def __init__(self,parent=None):
        HtmlBrowser.__init__(self)
        PluginBase.__init__(self)
        
        self.setKeepme("[about]update")
    
    #Override#
    def invoke(self):
        self.webview().setUrl(QUrl(UpdateSite))
          
class ShowVersions(HtmlBrowser,PluginBase):
    def __init__(self,parent=None):
        HtmlBrowser.__init__(self)
        PluginBase.__init__(self)
        
        self.setKeepme("[about]showversions")
    
    #Override#
    def invoke(self):
        sip_version_str = "sip version is not available"
        try :
            import sipconfig
            sip_version_str = sipconfig.Configuration().sip_version_str
        except:
            pass
        vstr = "<h1>Versions</h1>"
        
        vstr += "<table border='1' width='100%'><tr><td><b>Name</b></td><td><b>Version</b></td></tr>"
        
        vstr += ("<tr><td>Python</td><td>"+sys.version.split()[0]+"</td></tr>")
        vstr += ("<tr><td>Qt</td><td>"+qVersion()+"</td></tr>")
        vstr += ("<tr><td>PyQt</td><td>"+PYQT_VERSION_STR+"</td></tr>")
        vstr += ("<tr><td>sip</td><td>"+sip_version_str+"</td></tr>")
        vstr += ("<tr><td>Seeking</td><td>"+Version+"</td></tr>")
        
        vstr += "</table>"
        
        self.setHtml(vstr)
        
class About(QDialog,Ui_AboutSeeking):
    def __init__(self,parent=None):
        QDialog.__init__(self,parent)
        self.setupUi(self)
        
        #center this window 
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)
        
        self.title.setText("<img width='48' src='%s'/><b>%s-%s</b>" % (getPath("iconDir","logo.png"),Name,Version))
