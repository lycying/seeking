# coding:utf-8
#
# Copyright (c) 2010, guo.li <lycying@gmail.com>
# Site < http://code.google.com/p/seeking/ >
# All rights reserved.
# vim: set ft=python sw=2 ts=2 et:
#

from PyQt5.QtCore import QObject
from PyQt5.QtCore import SIGNAL
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QInputDialog
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QWidget

from sklib.config import getPath, Prefs
from sklib.htmlfilter import downloadImages
from sklib.security import sk_decode
from sklib.ui.support import PluginBase
from sklib.ui.uimain import Seeking
from sklib.ui.wysiwyg import HtmlWYSIWYG
from .Ui_YeahdocEditor import Ui_YeahdocEditor
from .widgets import RichFlagButton
from .yeahdocsupport import YeahdocDatasSupply, getMyBaseUrl


class AdapterYeahdocItemViewerAndEditor(QWidget, Ui_YeahdocEditor, PluginBase):
    """
    When double click the yeahdoc list item , This will be shown 
    The basic layout has two tabs .
    One is used to show the yeahdoc in HTML
    Another one is used to edit it :)
    in order to make the interface more flexible, we are introducing a html editor.
    Of course, other elements such as tag or classification of these things,
    adjustments in the interface too.
    """
    __Y_MARK_SUBFIX = "~[__yeahdoc__]"

    __actions = {}

    def getActions(self):
        """
        This method is used by all the action can be configured and returns.
        """
        self.invoke()
        return self.__actions

    def __init__(self, idx=":new[yeahdoc]"):
        """
        Note that the url spelling.
        In order to ensure that it is only on the main interface,
        we use the id of each yeahdoc to spell out the string.
        Any action against in this instance will affect here.
        """

        QWidget.__init__(self)
        PluginBase.__init__(self)

        self.setKeepme(idx + self.__Y_MARK_SUBFIX)

    # Override#
    def invoke(self):

        self.setupUi(self)

        # our wysiwys editor
        self.__htmlWYSIWYG = HtmlWYSIWYG(self)
        self.layout().addWidget(self.__htmlWYSIWYG)

        self.passwordMore.setIcon(QIcon(getPath("iconDir", "yeahdoc/lock.png")))
        self.passwordWidget.setVisible(False)

        self.downloadBtn.setIcon(QIcon(getPath("iconDir", "yeahdoc/download.png")))
        self.saveBtn.setIcon(QIcon(getPath("iconDir", "yeahdoc/save.png")))

        self.__initData()
        self.__initAction()

    def __initData(self):
        """
        If the `url` is supplied , I will read datas from db and render it 
        otherwise , I just show a empty entry . and noramlly ,setHtml->"" to make it editable
        """

        # setup The classlist
        for item in YeahdocDatasSupply().bc_list():
            self.classlist.addItem(item['title'], item['id'])

        # the flag menu
        self.flagBtn = RichFlagButton(self)
        self.linelayout.insertWidget(0, self.flagBtn)

        # if not new .
        if self.keepme() and not self.keepme().startswith(":"):
            self.baseUrl = getMyBaseUrl() + "yeahdoc-images/" + self.keepme().split("~")[0]
            self.__htmlWYSIWYG.setBaseUrl(self.baseUrl)

            yeahdoc = YeahdocDatasSupply().bb_read1(self.keepme().split("~")[0])

            content = yeahdoc['content']

            if yeahdoc["lock"] == 1:
                password, ok = QInputDialog(self).getText(self, "", "", QLineEdit.Password, "")
                if ok:
                    try:
                        content = sk_decode(content, password)
                        self.password1.setText(password)
                        self.password2.setText(password)

                    except:
                        QMessageBox.warning(Seeking.new(), "error", "Error password")
                        raise Exception
                else:
                    raise Exception
            else:
                self.password1.setText("")
                self.password2.setText("")

            self.flagBtn.setIcon(QIcon(getPath("iconDir", "yeahdoc/flag/%s" % yeahdoc['img'])))
            self.flagBtn.setText(yeahdoc['img'])

            self.titleInput.setText(yeahdoc['title'])
            self.__htmlWYSIWYG.fill(content)

            # flag restore
            for i in range(self.classlist.count()):
                if self.classlist.itemData(i) == yeahdoc['categoryid']:
                    self.classlist.setCurrentIndex(i)
                    break

        else:

            self.titleInput.setText("")
            self.__htmlWYSIWYG.fill("")

    def __initAction(self):
        """
        set up the default action
        """

        self.__actions["__yeahdoc_save__"] = QAction(QApplication.translate("YeahdocEditor", "Save"), self, \
                                                     triggered=self.save)

        self.__actions["__yeahdoc_save__"].setShortcut(Prefs.new().getShortcut("__yeahdoc_save__", "Ctrl+S"))

        for key in self.__actions.keys():
            self.__actions[key].setIconVisibleInMenu(True)
            self.addAction(self.__actions[key])

        # save
        self.saveBtn.clicked.connect(self.save)
        self.downloadBtn.clicked.connect(self.download)
        # password
        self.passwordMore.clicked.connect(lambda: self.passwordWidget.setVisible(not self.passwordWidget.isVisible()))

        # change buffer
        QObject.connect(self.__htmlWYSIWYG.accessPoint(), \
                        SIGNAL("contentsChanged ()"), self.onbuffer)
        QObject.connect(self.flagBtn, SIGNAL("onbuffer ()"), self.onbuffer)
        QObject.connect(self.titleInput, SIGNAL("textChanged (const QString&)"), self.onbuffer)
        QObject.connect(self.password1, SIGNAL("textChanged (const QString&)"), self.onbuffer)
        QObject.connect(self.password2, SIGNAL("textChanged (const QString&)"), self.onbuffer)
        QObject.connect(self.tagsInput, SIGNAL("textChanged (const QString&)"), self.onbuffer)

    def download(self):
        """
        download the image of the document
        """
        self.save()

        Seeking.new().overlay.show()

        value = self.__htmlWYSIWYG.accessPoint().mainFrame().toHtml()
        number, value = downloadImages(value, self.baseUrl)
        if number != 0:
            self.__htmlWYSIWYG.fill(value)
            self.setBufferon(True)
            self.onbuffer()

        Seeking().new().overlay.hidestop()

    def save(self):
        """
        Handle save event . Before saved , checked if has password set . 
        The password is encrypt with pyDes
        """
        if self.bufferon():
            # get the password
            password = ""
            password1 = self.password1.text()
            password2 = self.password2.text()

            if not password1 == "" or not password2 == "":
                if password1 == password2:
                    password = password1
                else:
                    QMessageBox.warning(Seeking.new(), "error", "Not match")
                    return

            # loading effert
            Seeking.new().overlay.show()

            # if it's a new yeahdoc item instance
            if self.keepme() is "" or self.keepme().startswith(":"):
                idx = "~"
            # notice we contact the str at __init__ method
            else:
                idx = self.keepme().split('~')[0]

            # Values
            title = self.titleInput.text()
            content = self.__htmlWYSIWYG.accessPoint().mainFrame().toHtml()

            img = self.flagBtn.text()
            tags = self.tagsInput.text()
            categoryid = self.classlist.itemData(self.classlist.currentIndex())

            # Just save will change it , update opreation will just repeat it
            self.setKeepme(
                YeahdocDatasSupply().bb_save(categoryid.toString(), title, tags, img, content, password, idx) + \
                self.__Y_MARK_SUBFIX)

            # in order to make the suitable width of tab.
            title = "%s.." % title[0:8] if len(title) > 8 else title
            index = Seeking.new().tabs.indexOf(self)

            Seeking.new().tabs.setTabIcon(index, QIcon(getPath("iconDir", "yeahdoc/flag/%s" % img)))
            Seeking.new().tabs.setTabText(index, title)

            self.setBufferon(False)

            Seeking().new().overlay.hidestop()
        else:
            pass

        self.baseUrl = getMyBaseUrl() + "yeahdoc-images/" + self.keepme().split("~")[0]
        self.__htmlWYSIWYG.setBaseUrl(self.baseUrl)
