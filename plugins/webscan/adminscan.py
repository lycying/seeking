from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QIcon


from PyQt4.QtGui import QCheckBox
from PyQt4.QtCore import pyqtSignature
from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import QObject

import traceback
import threading
import os

from urllib.parse import urlparse

from plugins.webscan.Ui_Scanner import Ui_Scanner
from sklib.ui.support import PluginBase
from sklib.config import getPath
from http.client import HTTPConnection

class ScannerThread(threading.Thread):
    def __init__(self,scanner,total,preparedURL,lock):
        super(ScannerThread, self).__init__()
        self.stopEvent = threading.Event()
        self.scanner = scanner
        self.total = total
        self.preparedURL = preparedURL
        self.lock = lock
        self.batchSize = 10
    def stop(self):
        self.lock.acquire()                
        self.stopEvent.set()
        self.lock.release()

    def stopped(self):
        return self.stopEvent.isSet()
    
    def run(self):
        o = self.scanner.requestObject
        #conn = HTTPConnection(o.hostname,o.port,timeout=self.scanner.spinTimeout.value())

        while not self.stopped():
            if self.scanner.indexFlag > self.scanner.total:break
            self.lock.acquire()
            self.scanner.indexFlag = self.scanner.indexFlag+self.batchSize
            self.lock.release()
            for index in range(self.scanner.indexFlag,self.scanner.indexFlag+self.batchSize):
                if self.stopped():break
                if index>=self.total:
                    self.stop()
                    break
                        
                line = self.preparedURL[index] 
                
                self.lock.acquire()
                self.scanner.count = self.scanner.count+1
                self.lock.release()
                    
                if not line.startswith('/'):
                    line = "/"+line
                url = o.path+line
                try:
                    conn = HTTPConnection(o.hostname,o.port,timeout=self.scanner.spinTimeout.value())
                    conn.request("HEAD",url)
                    resp = conn.getresponse()
                    if (resp.status == 200 and self.scanner.cbx200.isChecked()) \
                        or (resp.status == 403 and self.scanner.cbx403.isChecked()) \
                        or (resp.status == 302 and self.scanner.cbx302.isChecked()):
                        self.scanner.emit(SIGNAL("feedback"),self.scanner.count*100/self.total, self.scanner.count, "<span style='color:green'>[%s]</span> <a href='%s'>%s</a>" % (str(resp.status),o.scheme+"://"+o.hostname+":"+str(o.port)+url,o.scheme+":"+o.hostname+":"+str(o.port)+url) )
            
                except:
                    pass
                else:
                    conn.close()
                #except UnicodeEncodeError as ex:
                #    pass
                #except Exception as ex:
                #    pass
                    #self.scanner.emit(SIGNAL("feedback"),0, 0, "<span style='color:red'>An error occured :</span>%s"%str(ex) )
                    #self.scanner.emit(SIGNAL("feedback"),0, 0, "<span style='color:red'>Exceptions :</span><pre>%s</pre>" % str(traceback.format_exc()) )
                    #self.scanner.startBtn.setDisabled(False)
                #else:
                #    conn.close()
                if index == self.total-1:
                    self.stop()
                    self.scanner.emit(SIGNAL("feedback"),100, self.scanner.count, "Scanning Completed!" )
                    self.stop()
                    self.scanner.startBtn.setEnabled(True)
                    self.scanner.stopBtn.setEnabled(False)
                    break
        #conn.close()
                    
class Scanner(QWidget,PluginBase,Ui_Scanner):
    def __init__(self):
        QWidget.__init__(self)
        PluginBase.__init__(self)
        
        self.setKeepme("__webadminscan_scanner__")
        self.setupUi(self)
        
        self.execute("Web Admin Scanner",QIcon(getPath('pluginsDir','webscan/admin.png')))
        
        
        self.txts = os.listdir(getPath('pluginsDir','webscan/txt'))
        if len(self.txts) is 0:
            self.emit(SIGNAL("feedback"),0, 0, "You need supply some dictionary")
        else:
            self.emit(SIGNAL("feedback"),0, 0, "I'm ready ! Input a URL to Scan...")
            for txt in self.txts:
                lines = self.readlinenumber(getPath('pluginsDir','webscan/txt')+"/"+txt)
                qcb = QCheckBox(txt+"("+str(lines)+")")
                qcb.setChecked(True)
                qcb.setWindowTitle(txt)
                self.txtLayout.addWidget(qcb)
    
           
    def readlinenumber(self,txt):
        return len(open(txt,"rb").readlines())
    #Override#
    def invoke(self):
        QObject.connect(self,SIGNAL("feedback"),self.feedback)
        QObject.connect(self.startBtn, SIGNAL("clicked ()"),self._evt_start)
        QObject.connect(self.stopBtn, SIGNAL("clicked ()"),self._evt_stop)
        
        
    @pyqtSignature("")
    def feedback(self,percent,number,text):
        """
        provide  feedback on progress
        """
        self.progressBar.setValue(percent)
        try:
            self.lblPercent.setText("<span style='color:blue'>"+str(number)+"</span>/<span style='color:green'>"+str(self.total)+"</span>")
        except:
            pass
        if text is not None:
            self.textBrowser.append(text)
        
    def _evt_start(self):
        self.textBrowser.setText("")
        self.startBtn.setDisabled(True)
        self.stopBtn.setDisabled(False)
        self.url = self.urlEdit.text()
        self.checks = []
        for index in range(self.txtLayout.count()):
            qcb = self.txtLayout.itemAt(index).widget()
            if qcb is not None and isinstance(qcb, QCheckBox) and qcb.isChecked():
                self.checks.append(qcb.windowTitle())
        
        if self.url == "":
            self.emit(SIGNAL("feedback"),0, 0, "Please supply a URL")
            self.startBtn.setDisabled(False)
            return
        if len(self.checks) is 0:
            self.emit(SIGNAL("feedback"),0, 0, "Please supply a dictionary")
            self.startBtn.setDisabled(False)
            return
        
        self.preparedURL = []
        for txt in self.checks:
            lines = open(getPath('pluginsDir','webscan/txt')+"/"+txt,"r").readlines()
            for line in lines:
                self.preparedURL.append(line.strip(' \t\n\r'))
        try:
            self.requestObject = urlparse(self.url)
        except Exception as ex:
            self.emit(SIGNAL("feedback"),0, 0, "<span style='color:red'>An error occured :</span>%s"%str(ex) )
            self.emit(SIGNAL("feedback"),0, 0, "<span style='color:red'>Exceptions :</span><pre>%s</pre>" % str(traceback.format_exc()) )
            self.startBtn.setDisabled(False)
            return
        self.total = len(self.preparedURL)
        self.count = 1
        
        self.lock = threading.Lock()
        self.threads = []
        self.indexFlag = -10
        
        for index in range(self.spinThreadNumber.value()):
            thread = ScannerThread(self,self.total,self.preparedURL,self.lock)
            thread.start()
            self.threads.append(thread)

    def _evt_stop(self):
        for thread in self.threads:
            thread.stop()
        self.startBtn.setEnabled(True)
        self.stopBtn.setEnabled(False)