from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QIcon


from PyQt4.QtCore import pyqtSignature
from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import QObject

import threading
import traceback
import socket


from sklib.ui.support import PluginBase
from sklib.config import getPath
from plugins.webscan.Ui_PortScanner import Ui_PortScanner

class ScannerThread(threading.Thread):
    def __init__(self,scanner,total,preparedPort,lock):
        super(ScannerThread, self).__init__()
        self.stopEvent = threading.Event()
        self.scanner = scanner
        self.total = total
        self.preparedPort = preparedPort
        self.lock = lock
        self.batchSize = 10
    def stop(self):
        self.lock.acquire()                
        self.stopEvent.set()
        self.lock.release()

    def stopped(self):
        return self.stopEvent.isSet()
    
    def run(self):
        while not self.stopped():
            if self.scanner.indexFlag >= self.scanner.total:break
            self.lock.acquire()
            self.scanner.indexFlag = self.scanner.indexFlag+self.batchSize
            self.lock.release()
            for index in range(self.scanner.indexFlag,self.scanner.indexFlag+self.batchSize):
                if self.stopped():break
                if index>=self.total:
                    self.stop()
                    break
                
                port = self.preparedPort[index]
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
                result = sock.connect_ex((self.scanner.remoteServerIP, port))
                
                self.lock.acquire()
                self.scanner.count = self.scanner.count+1
                self.lock.release()
                
                if result == 0:
                    self.scanner.emit(SIGNAL("feedback"),self.scanner.count*100/self.total, self.scanner.count, "Port {}: \t Open".format(port) )
                else:
                    self.scanner.emit(SIGNAL("feedback"),self.scanner.count*100/self.total, self.scanner.count,None)
                sock.close()

                if index == self.total-1:
                    self.stop()
                    self.scanner.emit(SIGNAL("feedback"),0, 0, "-" * 60 )
                    self.scanner.emit(SIGNAL("feedback"),100, self.scanner.count, "Scanning Completed!" )
                    self.scanner.startBtn.setEnabled(True)
                    self.scanner.stopBtn.setEnabled(False)
                    break
                    
class PortScanner(QWidget,PluginBase,Ui_PortScanner):
    def __init__(self):
        QWidget.__init__(self)
        PluginBase.__init__(self)
        
        self.setKeepme("__portscan_scanner__")
        self.setupUi(self)
        
        self.execute("Port Scanner",QIcon(getPath('pluginsDir','webscan/port.png')))
        
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
        
        self.lock = threading.Lock()
        self.threads = []
        self.indexFlag = -10
        
        begin = self.spinFrom.value()
        end = self.spinTo.value()
        if end<=begin:
            self.emit(SIGNAL("feedback"),0, 0, "Port error, 'To' Port must be larger than 'From' port!")
            return
        try:
            self.remoteServerIP  = socket.gethostbyname(self.urlEdit.text())
        except Exception as ex:
            self.emit(SIGNAL("feedback"),0, 0, "<span style='color:red'>An error occured :</span>%s"%str(ex) )
            self.emit(SIGNAL("feedback"),0, 0, "<span style='color:red'>Exceptions :</span><pre>%s</pre>" % str(traceback.format_exc()) )
            self.startBtn.setDisabled(False)
            return
        
        self.emit(SIGNAL("feedback"),0, 0, "-" * 60 )
        self.emit(SIGNAL("feedback"),0, 0, "Please wait, scanning remote host:"+self.remoteServerIP )
        self.emit(SIGNAL("feedback"),0, 0, "-" * 60 )
        
        self.preparedPort = []
        for port in range(begin,end+1):
            self.preparedPort.append(port)
        self.total = len(self.preparedPort)
        self.count = 0
        self.indexFlag = -10

        for index in range(self.spinThreadSize.value()):
            thread = ScannerThread(self,self.total,self.preparedPort,self.lock)
            thread.start()
            self.threads.append(thread)

    def _evt_stop(self):
        for thread in self.threads:
            thread.stop()
        self.startBtn.setEnabled(True)
        self.stopBtn.setEnabled(False)
        
    