# coding:utf-8
#
# Copyright (c) 2010, guo.li <lycying@gmail.com>
# Site < http://code.google.com/p/seeking/ >
# All rights reserved.
# vim: set ft=python sw=2 ts=2 et:
#
import tempfile
import zipfile
import sys

from PyQt5.QtGui import QDialog
from PyQt5.QtGui import QTreeWidgetItem
from PyQt5.QtGui import QMenu
from PyQt5.QtGui import QAction
from PyQt5.QtGui import QApplication
from PyQt5.QtGui import QDesktopWidget

from PyQt5.QtCore import QObject
from PyQt5.QtCore import SIGNAL
from PyQt5.QtCore import QUrl
from PyQt5.QtCore import QFile

from PyQt5.QtNetwork import QHttp 

from .Ui_PluginInfoDialog import Ui_PluginInfoDialog
from .Ui_PluginRequestDialog import Ui_PluginRequestDialog
from ..xplugin import PluginAdapter
from ..config import Prefs,getPrccisePath


class PluginInfoDialog(QDialog,Ui_PluginInfoDialog):
    """
    the plugin info dialog 
    """
    
    def __init__(self,parent=None):
        QDialog.__init__(self,parent)
        self.setupUi(self)

        #center this window 
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)
        
        for item in PluginAdapter().new().readInfos():
            itree = QTreeWidgetItem()
            for i in range(6):
                itree.setText(i,str(item[i]))
                
            self.pluginList.addTopLevelItem(itree)
            
        
        QObject.connect(self.pluginList, SIGNAL("customContextMenuRequested (const QPoint&)"),self.__evt_contextmenu)
        
    def __evt_contextmenu(self,point):
        """
        show the right menu
        """
        item = self.pluginList.currentItem()
        if item:
            menu = QMenu(self)
           
            
            if item.text(4)=="True":
                
                action = QAction(QApplication.translate("PluginInfoDialog", "DeActive"),self,\
                                 triggered=lambda re,name=item.text(0):self.__evt_toggle_active(name, False))
                #core plugin not allowed disabled
                action.setEnabled(not PluginAdapter.new().getPluginByName(item.text(0)).packageName == "__core__")
            else:
                action = QAction(QApplication.translate("PluginInfoDialog", "Active"),self,\
                                 triggered=lambda re,name=item.text(0):self.__evt_toggle_active(name, True))
                
            menu.addAction(action)
            menu.exec_(self.mapToGlobal(self.pluginList.mapTo(self,point)))
    
    def __evt_toggle_active(self,name,value):
        """
        make plugin active or deactive
        """
        item = self.pluginList.currentItem()
        item.setText(4,str(value))
        mod = PluginAdapter.new().getPluginByName(name)
        if mod and hasattr(mod,"deactivate"):
            mod.deactivate()
        Prefs.new().setPluginState(name,value)
        

class PluginRequestDialog(QDialog,Ui_PluginRequestDialog):
    """
    the plugin install dialog 
    """
    
    def __init__(self,parent=None):
        QDialog.__init__(self,parent)
        self.setupUi(self)
        
        #center this window 
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)
        
        QObject.connect(self.pluginList, SIGNAL("customContextMenuRequested (const QPoint&)"),self.__evt_contextmenu)
        QObject.connect(self.update,SIGNAL("clicked ()"),self.__evt_update)
        
        self.__http = None 
        self.__downloadFile = None
        self.__baseUrl = "http://localhost/"
        self.plugin_txt_url.setText("%splugins.txt"%self.__baseUrl)
        self.__evt_update()
        
    def __evt_update(self):
        self.progressBar.setValue(0)
        self.download(QUrl(self.plugin_txt_url.text()))
        
    def download(self,url):
        """
        download something
        """     
        if None == self.__http:
            self.__http = QHttp()
            QObject.connect(self.__http, SIGNAL("done(bool)"), self.__downloadFileDone)
            QObject.connect(self.__http, SIGNAL("dataReadProgress(int, int)"), self.__dataReadProgress) 
            
        if QUrl(url).scheme() == 'https':
            connectionMode = QHttp.ConnectionModeHttps
        else:
            connectionMode = QHttp.ConnectionModeHttp
        self.__http.setHost(url.host(),connectionMode,url.port(80))
        self.__downloadFile = QFile(tempfile.NamedTemporaryFile().name)
        self.__http.get(url.path(),self.__downloadFile)
        
    def __downloadFileDone(self, error):
        """
        Private method called, after the file has been downloaded
        from the internet.
        
        @param error flag indicating an error condition (boolean)
        """
        if self.__downloadFile.exists():
            filename = self.__downloadFile.fileName()
            #Notice must flush it first 
            self.__downloadFile.flush()
            if not zipfile.is_zipfile(filename):
            
                plugins_info = open(filename).readlines()
                
                self.pluginList.clear()
                
                for plugin_info in plugins_info:
                    try:
                        plugin_name = plugin_info.split('|')[0]
                        plugin_version = plugin_info.split('|')[1]
                        plugin_instruction = plugin_info.split('|')[2]
                        plugin_author = plugin_info.split('|')[3]
                        
                        itree = QTreeWidgetItem()
                        itree.setText(0,plugin_name)
                        itree.setText(1,plugin_author)
                        itree.setText(2,plugin_version)
                        itree.setText(3,plugin_instruction)
                        
                        self.pluginList.addTopLevelItem(itree)
                    except Exception as e:
                        raise e
            else:
                pluginDir = getPrccisePath("pluginsDir", "", "extdir")  if sys.platform.startswith("win") else  getPrccisePath("pluginsDir", "", "userdir") 
                tmpZip = zipfile.ZipFile(filename)
                for file in tmpZip.namelist():
                    tmpZip.extract(file,pluginDir)
                tmpZip.close()
                self.result_label.setText("Success install the plugin ")


    def __dataReadProgress(self, done, total):
        """
        Private slot to show the download progress.
        
        @param done number of bytes downloaded so far (integer)
        @param total total bytes to be downloaded (integer)
        """
        self.progressBar.setMaximum(total)
        self.progressBar.setValue(done)
    def __has_this_plugin(self,plugin_name):
        """
        Check if this plugin has installed 
        """
        for item in PluginAdapter().new().readInfos():
            if item[0]==plugin_name:
                return item
        return None
    def __evt_contextmenu(self,point):
        """
        show the right menu
        """
        item = self.pluginList.currentItem()
        if item:
            menu = QMenu(self)
            action = QAction(QApplication.translate("default","Install plugins..."),self,triggered=lambda:self.__evt_install_plugin(item))
            menu.addAction(action)
            action = QAction(QApplication.translate("default","Uninstall plugins..."),self)
            menu.addAction(action)
            menu.exec_(self.mapToGlobal(self.pluginList.mapTo(self,point)))
            
    def __evt_install_plugin(self,item):
        filename = "plugin-%s-%s.zip"%(item.text(0),item.text(2))
        if not None == self.__has_this_plugin(item.text(0)):
            self.download(QUrl("%s%s"%(self.__baseUrl,filename)))
        else:
            self.result_label.setText("This plugin '%s' had installed "%item.text(0))
