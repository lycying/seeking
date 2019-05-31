# coding:utf-8
#
# Copyright (c) 2010, guo.li <lycying@gmail.com>
# Site < http://code.google.com/p/seeking/ >
# All rights reserved.
# vim: set ft=python sw=2 ts=2 et:
#

from PyQt5.QtCore import QObject
from PyQt5.QtCore import QSize
from PyQt5.QtCore import SIGNAL
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QDialogButtonBox
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QHeaderView
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QListView
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtWidgets import QMenu
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QSpacerItem
from PyQt5.QtWidgets import QToolBar
from PyQt5.QtWidgets import QToolButton
from PyQt5.QtWidgets import QTreeWidgetItem
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QWidgetAction

from sklib.config import getPath, Prefs
from sklib.ui.support import PluginBase
from sklib.ui.uimain import Seeking
from sklib.ui.wysiwyg import HtmlWYSIWYG
from .Ui_NewYeahdocCategory import Ui_NewYeahdocCategory
from .Ui_YeahdocList import Ui_YeahdocList
from .widgets import RichFlagButton
from .yeahdoceditor import AdapterYeahdocItemViewerAndEditor
from .yeahdocsupport import YeahdocDatasSupply


class AdapterMainYeahdocListView(Ui_YeahdocList, QWidget, PluginBase):
    """
    This will be added to mainlayout as tab!
    We have both the class list and yeahdoclist in the same viewer
    """

    __actions = {}

    def getActions(self):
        self.invoke()
        return self.__actions

    class __NewBCWidget(QDialog, Ui_NewYeahdocCategory):
        """
        This is a inner class used to add a new yeahdoc class.
        This will show a widget that recive inputs 
        And will make effect to its parent 
        """

        def __init__(self, parent=None, id="~"):
            """
            init
            """
            QWidget.__init__(self, parent)
            self.setupUi(self)

            # center this window
            screen = QDesktopWidget().screenGeometry()
            size = self.geometry()
            self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

            self.id = id
            self.flagBtn = RichFlagButton(self)
            self.linelayout.addWidget(self.flagBtn)
            self.desc = HtmlWYSIWYG()
            self.desc.setMinimumHeight(200)
            self.desclayout.addWidget(self.desc)

            if not self.id == "~":
                restore = YeahdocDatasSupply().bc_read1(self.id)
                self.flagBtn.setIcon(QIcon(getPath("iconDir", "yeahdoc/flag/%s" % str(restore['img']))))
                self.flagBtn.setText(restore['img'])
                self.title.setText(restore['title'])
                self.desc.fill(restore['desc'])

            QObject.connect(self.btn, SIGNAL("clicked (QAbstractButton *)"), self.__evt_btn_click)

        def __evt_btn_click(self, btn):
            """
            save or cancel
            """
            if btn == self.btn.button(QDialogButtonBox.Ok):
                self.save()
            elif btn == self.btn.button(QDialogButtonBox.Cancel):
                self.close()

        def save(self):
            """
            save the yeahdoc 
            """
            title = self.title.text()
            desc = self.desc.accessPoint().mainFrame().toHtml()
            img = self.flagBtn.text()

            if title == None or title == "" or desc == None or desc == "":
                QMessageBox.warning(self, "Warn", "title and desc can not be null")
                return

            YeahdocDatasSupply().bc_save(title, img, desc, self.id)

            self.parent().refreshClasslist()
            self.close()

    class __YeahdocQTreeWidgetItem(QTreeWidgetItem):
        """
        used to record extend data
        every tree item will use this
        """

        def __init__(self):
            QTreeWidgetItem.__init__(self)
            # used to record the yeahdoc item
            self.__mark = None

        def getMark(self):
            return self.__mark

        def setMark(self, mark):
            self.__mark = mark

    class __YeahdocCategoryQListWidgetItem(QListWidgetItem):
        """
        the yeahdoc class list item 
        """

        def __init__(self):
            QListWidgetItem.__init__(self)
            # used to record the yeahdoc item
            self.__mark = None

        def getMark(self):
            return self.__mark

        def setMark(self, mark):
            self.__mark = mark

    def __init__(self, parent=None):
        """
        Just init ... supply a url mark sure
        """
        QWidget.__init__(self, parent)
        PluginBase.__init__(self)
        # just mark it is the single one
        self.setKeepme("(__yeahdoc_list__)")

    # Override
    def invoke(self):
        """
        the real setup function to show someting.
        """
        self.setupUi(self)

        # make sure the first col show full
        self.yeahdoclisttree.header().setResizeMode(0, QHeaderView.ResizeToContents)

        self.__initAction()

        # toolbar .
        classToolbar = QToolBar()
        classToolbar.setIconSize(QSize(16, 16))
        classToolbar.setMovable(False)
        self.rightsplitter.insertWidget(0, classToolbar)

        classToolbar.addAction(self.__actions["__yeahdoc_c_new__"])
        classToolbar.addAction(self.__actions["__yeahdoc_c_edit__"])
        classToolbar.addAction(self.__actions["__yeahdoc_c_rename__"])
        classToolbar.addAction(self.__actions["__yeahdoc_c_delete__"])
        classToolbar.addWidget(self.__evt_category_view())

        # More useful gadgets
        self.togglebtn.setIcon(QIcon(getPath("iconDir", "yeahdoc/right.png")))

        # read datas from db .
        self.__setupYeahdocCategoryDatas()
        self.__setupyeahdoclisttreeDatas()

    # Override
    def after(self):
        # tour
        # if self.yeahdoclisttree.topLevelItemCount() <=0 :
        #    QMessageBox.information(self, "Info", "Current No items now . You may want import some datas")
        pass

    def __initAction(self):
        """
        action that handle the event
        """
        # open
        self.__actions["__yeahdoc_open__"] = \
            QAction(QIcon(getPath("iconDir", "yeahdoc/open.png")), QApplication.translate("YeahdocList", "Open"), self, \
                    triggered=self.__evt_yeahdoc_Xopen0)
        # edit
        self.__actions["__yeahdoc_edit__"] = \
            QAction(QIcon(getPath("iconDir", "yeahdoc/edit.png")), QApplication.translate("YeahdocList", "Edit"), self, \
                    triggered=self.__evt_yeahdoc_Xopen0)
        # star
        self.__actions["__yeahdoc_star__"] = \
            QAction(QIcon(getPath("iconDir", "yeahdoc/star.png")), QApplication.translate("YeahdocList", "Toggle Star"),
                    self, \
                    triggered=self.__evt_yeahdoc_star)
        # rename
        self.__actions["__yeahdoc_rename__"] = \
            QAction(QIcon(getPath("iconDir", "yeahdoc/rename.png")), QApplication.translate("YeahdocList", "Rename"),
                    self, \
                    triggered=self.__evt_yeahdoc_rename)
        # delete
        self.__actions["__yeahdoc_delete__"] = \
            QAction(QIcon(getPath("iconDir", "yeahdoc/delete.png")), QApplication.translate("YeahdocList", "Delete"),
                    self, \
                    triggered=self.__evt_yeahdoc_delete_item)
        # new
        self.__actions["__yeahdoc_c_new__"] = \
            QAction(QIcon(getPath("iconDir", "yeahdoc/categorynew.png")),
                    QApplication.translate("YeahdocList", "new category"), self, \
                    triggered=self.__evt_category_new)
        # edit
        self.__actions["__yeahdoc_c_edit__"] = \
            QAction(QIcon(getPath("iconDir", "yeahdoc/categoryedit.png")),
                    QApplication.translate("YeahdocList", "Edit"), self, \
                    triggered=self.__evt_category_edit)
        # rename
        self.__actions["__yeahdoc_c_rename__"] = \
            QAction(QIcon(getPath("iconDir", "yeahdoc/rename.png")), QApplication.translate("YeahdocList", "Rename"),
                    self, \
                    triggered=self.__evt_category_rename)
        # delete
        self.__actions["__yeahdoc_c_delete__"] = \
            QAction(QIcon(getPath("iconDir", "yeahdoc/categorydelete.png")),
                    QApplication.translate("YeahdocList", "Delete"), self, \
                    triggered=self.__evt_category_delete)
        # clear datas
        self.__actions["__yeahdoc_c_cleardatas__"] = \
            QAction(QIcon(getPath("iconDir", "yeahdoc/cleardatas.png")), QApplication.translate("YeahdocList", "Clear"),
                    self, \
                    triggered=self.__evt_category_cleardatas)

        self.__actions["__yeahdoc_open__"].setShortcut(Prefs.new().getShortcut("__yeahdoc_open__", "Ctrl+O"))
        self.__actions["__yeahdoc_edit__"].setShortcut(Prefs.new().getShortcut("__yeahdoc_edit__", "Ctrl+E"))
        self.__actions["__yeahdoc_star__"].setShortcut(Prefs.new().getShortcut("__yeahdoc_star__", "Alt+M"))
        self.__actions["__yeahdoc_rename__"].setShortcut(Prefs.new().getShortcut("__yeahdoc_rename__", "F2"))
        self.__actions["__yeahdoc_delete__"].setShortcut(Prefs.new().getShortcut("__yeahdoc_delete__", "Delete"))

        self.__actions["__yeahdoc_c_new__"].setShortcut(Prefs.new().getShortcut("__yeahdoc_c_new__", ""))
        self.__actions["__yeahdoc_c_edit__"].setShortcut(Prefs.new().getShortcut("__yeahdoc_c_edit__", ""))
        self.__actions["__yeahdoc_c_rename__"].setShortcut(Prefs.new().getShortcut("__yeahdoc_c_rename__", ""))
        self.__actions["__yeahdoc_c_delete__"].setShortcut(Prefs.new().getShortcut("__yeahdoc_c_delete__", ""))

        for key in self.__actions.keys():
            self.__actions[key].setIconVisibleInMenu(True)
            self.addAction(self.__actions[key])

        # toggle buttion
        QObject.connect(self.togglebtn, \
                        SIGNAL("clicked ()"), \
                        self.__evt_toggle_view)

        # double click the yeahdoc tree list,open a new window at main tab
        QObject.connect(self.yeahdoclisttree, \
                        SIGNAL("itemDoubleClicked (QTreeWidgetItem *,int)"), \
                        self.__evt_yeahdoc_Xopen)

        QObject.connect(self.yeahdoclisttree, \
                        SIGNAL("itemChanged (QTreeWidgetItem *,int)"), \
                        self.__evt_yeahdoc_rename_done)

        QObject.connect(self.yeahdoclisttree, \
                        SIGNAL("currentItemChanged (QTreeWidgetItem *,QTreeWidgetItem *)"), \
                        self.__evt_yeahdoc_currentItemChanged)

        QObject.connect(self.yeahdoccategorylist, \
                        SIGNAL("itemChanged (QListWidgetItem *)"), \
                        self.__evt_category_rename_done)

        QObject.connect(self.yeahdoccategorylist, \
                        SIGNAL("currentItemChanged (QListWidgetItem *,QListWidgetItem *)"), \
                        self.__evt_category_currentItemChanged)
        # right click the yeahdoc tree list and show a context menu
        QObject.connect(self.yeahdoclisttree, \
                        SIGNAL("customContextMenuRequested (const QPoint&)"), \
                        self.__evt_yeahdoc_contextMenu)

        QObject.connect(self.yeahdoccategorylist, \
                        SIGNAL("customContextMenuRequested (const QPoint&)"), \
                        self.__evt_category_contextMenu)
        # double click the yeahdoc class list
        QObject.connect(self.yeahdoccategorylist, \
                        SIGNAL("itemDoubleClicked (QListWidgetItem *)"), \
                        self.__evt_category_dbclick)

        QObject.connect(self.searchEdit, SIGNAL("textChanged (const QString&)"), self.__search)

    def __search(self, txt):
        """
        search match
        """
        for topIndex in range(self.yeahdoclisttree.topLevelItemCount()):
            topItem = self.yeahdoclisttree.topLevelItem(topIndex)

            if not topItem.text(0).__contains__(txt):
                topItem.setHidden(True)
            else:
                topItem.setHidden(False)

    def refreshClasslist(self):
        """
        call me outside
        """
        self.__setupYeahdocCategoryDatas()

    def __setupYeahdocCategoryDatas(self):
        """
        Read class list .
        """
        self.yeahdoccategorylist.clear()
        # read
        yeahdoccategorylist = YeahdocDatasSupply().bc_list()
        for item in yeahdoccategorylist:
            newItem = self.__YeahdocCategoryQListWidgetItem()
            newItem.setMark(str(item["id"]))
            newItem.setText(item['title'])
            newItem.setIcon(QIcon(getPath("iconDir", "yeahdoc/flag/%s" % str(item["img"]))))
            self.yeahdoccategorylist.addItem(newItem)

    def __setupyeahdoclisttreeDatas(self, categoryid=None):
        """
        Set up the yeahdoc's datas 
        By default 
        """
        # clear first
        self.yeahdoclisttree.clear()
        # read datas
        for item in YeahdocDatasSupply().bb_list(categoryid):
            treeitem = self.__YeahdocQTreeWidgetItem()

            treeitem.setText(0, item["title"])
            treeitem.setIcon(0, QIcon(getPath("iconDir", "yeahdoc/flag/%s" % item["img"])))

            treeitem.setText(1, item["createdate"])

            treeitem.setMark(str(item['id']))

            if 1 == item['star']: treeitem.setIcon(2, QIcon(getPath("iconDir", "yeahdoc/star.png")))
            if 1 == item['lock']: treeitem.setIcon(3, QIcon(getPath("iconDir", "yeahdoc/lock.png")))

            self.yeahdoclisttree.addTopLevelItem(treeitem)

    def __evt_toggle_view(self):
        """
        show or hide the right part
        """
        if self.rightpart.isVisible():
            self.rightpart.setVisible(False)
            self.togglebtn.setIcon(QIcon(getPath("iconDir", "yeahdoc/left.png")))
        else:
            self.rightpart.setVisible(True)
            self.togglebtn.setIcon(QIcon(getPath("iconDir", "yeahdoc/right.png")))

    def __evt_category_view(self):
        """
        view by 
        """
        btn = QToolButton()
        btn.setIcon(QIcon(getPath("iconDir", "yeahdoc/view.png")))

        menu = QMenu(btn)
        menu.addAction(QAction("ListMode", self, \
                               triggered=lambda: self.yeahdoccategorylist.setViewMode(QListView.ListMode)))
        menu.addAction(QAction("IconMode", self, \
                               triggered=lambda: self.yeahdoccategorylist.setViewMode(QListView.IconMode)))

        btn.setMenu(menu)

        return btn

    def __evt_category_contextMenu(self, p):
        """
        yeahdoc class context menu
        """
        item = self.yeahdoccategorylist.currentItem()

        if item and item.getMark():

            menu = QMenu()

            action = QAction(QIcon(getPath("iconDir", "yeahdoc/item.png")), item.text(), self)
            action.setIconVisibleInMenu(True)
            menu.addAction(action)

            menu.addSeparator()

            action = QAction(QIcon(getPath("iconDir", "yeahdoc/open.png")),
                             QApplication.translate("YeahdocList", "Open"), self, \
                             triggered=lambda re, id=item.getMark(): self.__setupyeahdoclisttreeDatas(id))
            action.setIconVisibleInMenu(True)
            menu.addAction(action)

            action = QAction(QIcon(getPath("iconDir", "yeahdoc/refresh.png")),
                             QApplication.translate("YeahdocList", "Refresh"), self, \
                             triggered=self.refreshClasslist)
            action.setIconVisibleInMenu(True)
            menu.addAction(action)

            menu.addSeparator()

            # merge class
            merge_class_menu = QMenu()
            current_categoryid = item.getMark()
            for class_item in YeahdocDatasSupply().bc_list():
                if not str(class_item['id']) == current_categoryid:
                    action = QAction(class_item["title"], self, \
                                     triggered=lambda re, item=item, categoryid=str(class_item["id"]): \
                                         YeahdocDatasSupply().bc_merge(current_categoryid, categoryid))
                    action.setIcon(QIcon(getPath("iconDir", "yeahdoc/flag/%s" % str(class_item["img"]))))
                    action.setIconVisibleInMenu(True)
                    merge_class_menu.addAction(action)

            action = QAction(QIcon(getPath("iconDir", "yeahdoc/merge.png")),
                             QApplication.translate("YeahdocList", "Merge"), self)
            action.setIconVisibleInMenu(True)
            action.setMenu(merge_class_menu)
            menu.addAction(action)
            menu.addAction(self.__actions["__yeahdoc_c_cleardatas__"])
            menu.addSeparator()

            menu.addAction(self.__actions["__yeahdoc_c_new__"])
            menu.addAction(self.__actions["__yeahdoc_c_edit__"])
            menu.addAction(self.__actions["__yeahdoc_c_rename__"])
            menu.addAction(self.__actions["__yeahdoc_c_delete__"])

            menu.exec_(self.mapToGlobal(self.yeahdoccategorylist.mapTo(self, p)))

    def __evt_yeahdoc_contextMenu(self, p):
        """
        context menu
        """
        item = self.yeahdoclisttree.currentItem()
        if item == None or item.isDisabled():
            pass
        else:
            menu = QMenu()

            # menu top
            action = QWidgetAction(self)
            title = item.text(0)
            if len(title) < 25:
                for i in range(len(title), 25):
                    title = title + "  &nbsp;"
            action.setDefaultWidget(
                QLabel("&nbsp;&nbsp;<img  src='%s'/>  &nbsp;%s" % (getPath("iconDir", "yeahdoc/item.png"), title)))
            menu.addAction(action)

            menu.addSeparator()

            menu.addAction(self.__actions["__yeahdoc_open__"])
            menu.addAction(self.__actions["__yeahdoc_edit__"])

            # change class
            change_class_menu = QMenu()
            entry = YeahdocDatasSupply().bb_read1_simple(item.getMark())
            current_categoryid = entry['categoryid']
            for class_item in YeahdocDatasSupply().bc_list():
                action = QAction(class_item["title"], self, \
                                 triggered=lambda re, item=item, categoryid=str(class_item["id"]): \
                                     self.__evt_change_category(categoryid, item))
                action.setIcon(QIcon(getPath("iconDir", "yeahdoc/flag/%s" % str(class_item["img"]))))
                action.setIconVisibleInMenu(True)
                # mark current class id menu checked
                if class_item['id'] == current_categoryid:
                    action.setCheckable(True)
                    action.setChecked(True)
                    action.setDisabled(True)
                change_class_menu.addAction(action)

            action = QAction(QIcon(getPath("iconDir", "yeahdoc/change.png")),
                             QApplication.translate("YeahdocList", "Change Category"), self)
            action.setIconVisibleInMenu(True)
            action.setMenu(change_class_menu)

            menu.addAction(action)

            menu.addAction(self.__actions["__yeahdoc_star__"])
            menu.addAction(self.__actions["__yeahdoc_rename__"])
            menu.addAction(self.__actions["__yeahdoc_delete__"])

            menu.addSeparator()

            setmode = True if entry['lock'] == 0 else False
            action = QWidgetAction(self)
            widget = QWidget()
            layout = QHBoxLayout()
            layout.setSpacing(0)
            layout.setMargin(0)
            widget.setLayout(layout)
            widgetMore = QWidget()
            widgetMore.setVisible(False)
            layoutMore = QHBoxLayout()
            layoutMore.setSpacing(0)
            layoutMore.setMargin(0)
            widgetMore.setLayout(layoutMore)

            layout.addWidget(QLabel("<img src='%s'/>" % getPath("iconDir", "yeahdoc/password.png")))
            passwordMore = QPushButton(
                QApplication.translate("YeahdocEditor", "Encrypt") if setmode else QApplication.translate(
                    "YeahdocEditor", "Decrypt"))
            passwordMore.setFlat(True)
            layout.addWidget(passwordMore)

            passwordInput = QLineEdit()
            passwordInput.setEchoMode(QLineEdit.Password)
            passwordInput.setMaximumWidth(70)

            layoutMore.addWidget(passwordInput)

            if setmode:
                passwordInputAgain = QLineEdit()
                passwordInputAgain.setEchoMode(QLineEdit.Password)
                passwordInputAgain.setMaximumWidth(70)
                layoutMore.addWidget(QLabel(QApplication.translate("YeahdocEditor", "Re")))
                layoutMore.addWidget(passwordInputAgain)

            passwordSubmit = QPushButton("OK")
            passwordSubmit.setFlat(True)
            layoutMore.addWidget(passwordSubmit)

            layout.addWidget(widgetMore)
            layout.addItem(QSpacerItem(0, 20, QSizePolicy.Expanding, QSizePolicy.Expanding))

            action.setDefaultWidget(widget)
            QObject.connect(passwordSubmit, SIGNAL("clicked ()"),
                            lambda: self.__evt_password(setmode, passwordInput.text(),
                                                        passwordInputAgain.text() if setmode else ""))
            QObject.connect(passwordMore, SIGNAL("clicked ()"),
                            lambda: widgetMore.setVisible(not widgetMore.isVisible()))

            menu.addAction(action)

            # show it.
            menu.exec_(self.mapToGlobal(self.yeahdoclisttree.mapTo(self, p)))

    def __evt_change_category(self, categoryid, item):
        """
        change the category of the item
        """
        YeahdocDatasSupply().bb_update_class(categoryid, item.getMark())
        item.setHidden(True)

    def __evt_password(self, setmode, password, repassword):
        """
        set the password of the item.
        """
        item = self.yeahdoclisttree.currentItem()
        if item and password:
            try:
                d = YeahdocDatasSupply().bb_read1(item.getMark())["content"]
                if setmode:
                    if password == repassword:
                        YeahdocDatasSupply().bb_lock(item.getMark(), password)
                        QMessageBox.information(Seeking.new(), "Success",
                                                "%s Success" % QApplication.translate("YeahdocEditor", "Encrypt"))
                        item.setIcon(3, QIcon(getPath("iconDir", "yeahdoc/lock.png")))
                    else:
                        QMessageBox.warning(Seeking.new(), "error", "Not match")
                else:
                    YeahdocDatasSupply().bb_unlock(item.getMark(), password)
                    QMessageBox.information(Seeking.new(), "Success",
                                            "%s Success" % QApplication.translate("YeahdocEditor", "Decrypt"))
                    item.setIcon(3, QIcon(None))
            except Exception as e:
                raise e
                QMessageBox.warning(Seeking.new(), "error", "Error password")

    def __evt_category_rename(self):
        """
        rename
        """
        item = self.yeahdoccategorylist.currentItem()
        if item:
            self.yeahdoccategorylist.openPersistentEditor(item)
            self.yeahdoccategorylist.editItem(item)

    def __evt_category_cleardatas(self):
        """
        clear the datas contains in this category
        """
        item = self.yeahdoccategorylist.currentItem()
        if item:
            reply = QMessageBox.question(self, "Clear Data?",
                                         "Really Clear ? \n %s" % item.text(), QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                YeahdocDatasSupply().bc_clear(item.getMark())
            elif reply == QMessageBox.No:
                pass
            else:
                pass

    def __evt_category_delete(self):
        """
        delete current item
        """
        item = self.yeahdoccategorylist.currentItem()
        if item:
            reply = QMessageBox.question(self, "Delete!",
                                         "Really Delete? %s" % item.text(), QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                if YeahdocDatasSupply().bc_delete(item.getMark()):
                    self.refreshClasslist()
            elif reply == QMessageBox.No:
                pass
            else:
                pass

    def __evt_category_rename_done(self, item):
        """
        do rename
        """
        YeahdocDatasSupply().bc_update_title(item.text(), str(item.getMark()))
        self.yeahdoccategorylist.openPersistentEditor(item)

    def __evt_category_new(self):
        """
        just append a yeahdoc class item
        """
        newclass = self.__NewBCWidget(self)
        newclass.show()

    def __evt_category_edit(self):
        """
        edit yeahdoc class item
        """
        item = self.yeahdoccategorylist.currentItem()
        if item:
            newclass = self.__NewBCWidget(self, item.getMark())
            newclass.show()

    def __evt_category_currentItemChanged(self, item1, item2):
        """
        just set the rename state off
        """
        self.yeahdoccategorylist.closePersistentEditor(item1)
        self.yeahdoccategorylist.closePersistentEditor(item2)
        if item1 and item1.getMark():
            self.preview.setHtml(YeahdocDatasSupply().bc_read1(item1.getMark())["desc"])

    def __evt_yeahdoc_currentItemChanged(self, item1, item2):
        """
        just set the rename state off
        """
        self.yeahdoclisttree.closePersistentEditor(item1)
        self.yeahdoclisttree.closePersistentEditor(item2)

        if item1 and item1.getMark():
            self.preview.setHtml(YeahdocDatasSupply().bb_read1_simple(item1.getMark())["desc"])

    def __evt_category_dbclick(self, item):
        """
        setup treelist by class id
        """
        self.__setupyeahdoclisttreeDatas(item.getMark())

    def __evt_yeahdoc_Xopen0(self):
        """
        defaut
        """
        self.__evt_yeahdoc_Xopen(self.yeahdoclisttree.currentItem(), 0)

    def __evt_yeahdoc_Xopen(self, item, index):
        """
        real open the item . 
        """
        if item == None or item.isDisabled():
            pass
        else:
            id = item.getMark()
            simple_info = YeahdocDatasSupply().bb_read1_simple(id)
            editor = AdapterYeahdocItemViewerAndEditor(id)
            editor.execute(simple_info['title'], \
                           QIcon(getPath("iconDir", "yeahdoc/flag/%s" % simple_info['img'])))

    def __evt_yeahdoc_star(self):
        """
        star it 
        TODO:
        """
        item = self.yeahdoclisttree.currentItem()
        if 0 == YeahdocDatasSupply().bb_toggle_star(item.getMark()):
            item.setIcon(2, QIcon(getPath("iconDir", "yeahdoc/star.png")))
        else:
            item.setIcon(2, QIcon(None))

    def __evt_yeahdoc_rename(self):
        """
        rename evt
        """
        item = self.yeahdoclisttree.currentItem()
        self.yeahdoclisttree.openPersistentEditor(item, 0)
        self.yeahdoclisttree.editItem(item, 0)

    def __evt_yeahdoc_rename_done(self, item, index):
        """
        do rename
        """
        YeahdocDatasSupply().bb_update_title(item.text(0), item.getMark())
        self.yeahdoclisttree.closePersistentEditor(item)

    # Delete it from db , and more , make it disabled
    def __evt_yeahdoc_delete_item(self):
        """
        delete item
        """
        item = self.yeahdoclisttree.currentItem()
        reply = QMessageBox.question(self, "Delete!",
                                     "Really Delete? \n %s" % item.text(0), QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            if YeahdocDatasSupply().bb_delete(item.getMark()):
                item.setDisabled(True)
                item.setHidden(True)
        elif reply == QMessageBox.No:
            pass
        else:
            pass
