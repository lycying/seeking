# coding:utf-8
#
# Copyright (c) 2010, guo.li <lycying@gmail.com>
# Site < http://code.google.com/p/seeking/ >
# All rights reserved.
# vim: set ft=python sw=2 ts=2 et:
#

from PyQt4.QtGui import QAction
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QToolBar 
from PyQt4.QtGui import QLineEdit
from PyQt4.QtGui import QMenu
from PyQt4.QtGui import QMovie
from PyQt4.QtGui import QLabel


from PyQt4.QtCore import QObject
from PyQt4.QtCore import QUrl
from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import QSize
from PyQt4.QtCore import QByteArray

from PyQt4.QtWebKit import QWebView
from PyQt4.QtWebKit import QWebPage

from PyQt4.QtNetwork import QNetworkReply

from ...config import getPath




class HtmlBrowser(QWidget):
    def __init__(self,parent=None):
        QWidget.__init__(self,parent)
        
        self.__toolBar = QToolBar(self)
        self.__toolBar.setIconSize(QSize(16,16))
        self.__htmlBrowserView = HtmlBrowserView(self)
        self.__addressinput = QLineEdit(self)
        self.__loadlabel = QLabel(self)

        layout=QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setMargin(0)
        layout.addWidget(self.__toolBar)
        layout.addWidget(self.__htmlBrowserView)
        
        self.__setupToolBarAction()
        
        QObject.connect(self.__addressinput, SIGNAL("returnPressed ()"),self.__evt_load)
        QObject.connect(self.__htmlBrowserView, SIGNAL("loadFinished (bool)"),lambda:self.__loadlabel.setMovie(None))
        QObject.connect(self.__htmlBrowserView, SIGNAL("loadStarted ()"),self.__evt_loadstarted)


    def __evt_loadstarted(self):
        if  not self.__loadlabel.movie():
            movie = QMovie(getPath('iconDir','loading.gif'), QByteArray(), self.__loadlabel)
            movie.setSpeed(50)
            self.__loadlabel.setMovie(movie)
            movie.start()

    
    def __evt_load(self):
        self.__htmlBrowserView.load(QUrl(self.__addressinput.text()))
        
    def setHtml(self,html):
        self.__htmlBrowserView.setHtml(html)
        
    def webview(self):
        return self.__htmlBrowserView
    def __setupToolBarAction(self):
        
        self.__toolBar.addAction(self.__htmlBrowserView.getActions()["pre"])
        self.__toolBar.addAction(self.__htmlBrowserView.getActions()["next"])
        self.__toolBar.addAction(self.__htmlBrowserView.getActions()["stop"])
        self.__toolBar.addAction(self.__htmlBrowserView.getActions()["reload"])
        self.__toolBar.addWidget(self.__loadlabel)
        self.__toolBar.addWidget(self.__addressinput)
        
        action = QAction(QIcon(getPath('iconDir','heditor/go.png')),"go",self,triggered=self.__evt_load)
        
        self.__toolBar.addAction(action)

        self.__toolBar.addAction(self.__htmlBrowserView.getActions()["zoomin"])
        self.__toolBar.addAction(self.__htmlBrowserView.getActions()["zoomreset"])
        self.__toolBar.addAction(self.__htmlBrowserView.getActions()["zoomout"])

class HtmlBrowserView(QWebView):
    def __init__(self,parent = None):
        QWebView.__init__(self,parent)
        
        self.__initActions()

        QObject.connect(self.page().networkAccessManager(),SIGNAL("finished (QNetworkReply *)"),self.__evt_networkfinished)
    
        
    def __evt_networkfinished(self,reply):
        errorTrans = {
            QNetworkReply.ConnectionRefusedError:"the remote server refused the connection (the server is not accepting requests)",
            QNetworkReply.RemoteHostClosedError:"the remote server closed the connection prematurely, before the entire reply was received and processed",
            QNetworkReply.HostNotFoundError:"the remote host name was not found (invalid hostname)",
            QNetworkReply.TimeoutError:" the connection to the remote server timed out",
            QNetworkReply.OperationCanceledError:"the operation was canceled via calls to abort() or close() before it was finished.",
            QNetworkReply.SslHandshakeFailedError:" the SSL/TLS handshake failed and the encrypted channel could not be established. The sslErrors() signal should have been emitted.",
            QNetworkReply.ProxyConnectionRefusedError:" the connection to the proxy server was refused (the proxy server is not accepting requests)",
            QNetworkReply.ProxyConnectionClosedError:" the proxy server closed the connection prematurely, before the entire reply was received and processed",
            QNetworkReply.ProxyNotFoundError:"the proxy host name was not found (invalid proxy hostname)",
            QNetworkReply.ProxyTimeoutError:"the connection to the proxy timed out or the proxy did not reply in time to the request sent",
            QNetworkReply.ProxyAuthenticationRequiredError:"the proxy requires authentication in order to honour the request but did not accept any credentials offered (if any)",
            QNetworkReply.ContentAccessDenied :"the access to the remote content was denied (similar to HTTP error 401)",
            QNetworkReply.ContentOperationNotPermittedError:"the operation requested on the remote content is not permitted",
            QNetworkReply.ContentNotFoundError:"the remote content was not found at the server (similar to HTTP error 404)",
            QNetworkReply.AuthenticationRequiredError :"the remote server requires authentication to serve the content but the credentials provided were not accepted (if any)",
            QNetworkReply.ContentReSendError:"the request needed to be sent again, but this failed for example because the upload data could not be read a second time.",
            QNetworkReply.ProtocolUnknownError:"the Network Access API cannot honor the request because the protocol is not known",
            QNetworkReply.ProtocolInvalidOperationError:"the requested operation is invalid for this protocol",
            QNetworkReply.UnknownNetworkError:"an unknown network-related error was detected",
            QNetworkReply.UnknownProxyError:"an unknown proxy-related error was detected",
            QNetworkReply.UnknownContentError:"an unknown error related to the remote content was detected",
            QNetworkReply.ProtocolFailure :"a breakdown in protocol was detected (parsing error, invalid or unexpected responses, etc.)"
        }

        code = reply.error()
        if not code == QNetworkReply.NoError:
            if QNetworkReply.ContentNotFoundError == code:
                self.setHtml(errorTrans[code])

        
    def getActions(self):
        """
        return all actions of html edit view
        """
        return self.__editActions
    
    def __evt_zoom(self,zoomin):
        if zoomin:
            zoom = self.zoomFactor()*100+20
            zoom = zoom if zoom <=300 else 300
            self.setZoomFactor(zoom/100)
        else:
            zoom = self.zoomFactor()*100-20
            zoom = zoom if zoom >= 30 else 30
            self.setZoomFactor(zoom/100)
        
    def __initActions(self):
        """
        put all actions to dict , so we can use them outside
        """
        self.__editActions = {}
        
        self.__editActions["pre"] = QAction(QIcon(getPath('iconDir','heditor/pre.png')),"back",
                                       self,triggered=lambda:self.page().triggerAction(QWebPage.Back,checked=True))
        self.__editActions["next"] = QAction(QIcon(getPath('iconDir','heditor/next.png')),"forward",
                                       self,triggered=lambda:self.page().triggerAction(QWebPage.Forward,checked=True))
        self.__editActions["stop"] = QAction(QIcon(getPath('iconDir','heditor/stop.png')),"stop",
                                       self,triggered=lambda:self.page().triggerAction(QWebPage.Stop,checked=True))
        self.__editActions["reload"] = QAction(QIcon(getPath('iconDir','heditor/reload.png')),"reload",
                                       self,triggered=lambda:self.page().triggerAction(QWebPage.Stop,checked=True))
        self.__editActions["zoomin"] = QAction(QIcon(getPath('iconDir','heditor/zoomin.png')),"zoomIn",
                                       self,triggered=lambda:self.__evt_zoom(True))
        self.__editActions["zoomreset"] = QAction(QIcon(getPath('iconDir','heditor/zoomreset.png')),"zoomReset",
                                       self,triggered=lambda:self.setZoomFactor(1.0))
        self.__editActions["zoomout"] = QAction(QIcon(getPath('iconDir','heditor/zoomout.png')),"zoomOut",
                                       self,triggered=lambda:self.__evt_zoom(False))
        
        
        
        #Make sure the menu can show their icons
        for key in self.__editActions.keys():
            self.__editActions[key].setIconVisibleInMenu(True)
    def contextMenuEvent (self, e):
        """
        right click
        """
        menu = QMenu(self)
        
        menu.addAction(self.__editActions["zoomin"])
        menu.addAction(self.__editActions["zoomreset"])
        menu.addAction(self.__editActions["zoomout"])
        menu.addAction(self.__editActions["reload"])
        
        menu.exec_(e.globalPos())