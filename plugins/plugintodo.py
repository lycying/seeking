# coding:utf-8
#
# Copyright (c) 2010, guo.li <lycying@gmail.com>
# Site < http://code.google.com/p/seeking/ >
# All rights reserved.
# vim: set ft=python sw=2 ts=2 et:
#

import sqlite3 as sqlite

from sklib.ui.uimain import Seeking

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QHeaderView
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QTreeWidgetItem

from PyQt5.QtCore import QObject
from PyQt5.QtCore import QDateTime
from PyQt5.QtCore import SIGNAL
from PyQt5.QtCore import Qt

from sklib.ui.support import PluginBase
from sklib.ui.wysiwyg import HtmlWYSIWYG

from plugins.todo.Ui_TodoLists import Ui_TodoLists
from sklib.config import getPath

# Info ===
name = "TodoList Plugin"
author = "lycy < lycying@gmail.com >"
version = "0.1"
packageName = "__core_ext__"
description = "just another todolist"


# Info ===

def install():
    """
    The function that init the plugin . just once .
    core package ignore
    """
    pass


def uninstall():
    """
    core package ignore
    The method that remove the plugin .
    """
    pass


def activate():
    def _evt_list():
        list_view = AdapterTodoList()
        list_view.execute("Todo List")

    sk = Seeking.new()
    sk.regAction("__todolist",
                 QAction(QIcon(getPath('iconDir', 'todo/todolist.png')), "Show the todo list", Seeking.new(),
                         triggered=_evt_list))
    toolbar = sk.addToolBar("TODOLIST")
    toolbar.addAction(sk.getAction("__todolist"))
    sk.getMenu("file").addAction(sk.getAction("__todolist"))
    sk.getMenu("file").addSeparator()


def deactivate():
    """
    make this plugin disabled
    """
    pass


class AdapterTodoList(Ui_TodoLists, QWidget, PluginBase):
    """
    todoview
    """

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        PluginBase.__init__(self)

        # just mark it is the single one
        self.setKeepme("(__todolist__)")

    def invoke(self):
        self.setupUi(self)

        self.todonote = HtmlWYSIWYG()
        self.todonote.setMaximumWidth(300)
        self.todonote.setMinimumWidth(300)
        self.todolist.header().setResizeMode(0, QHeaderView.ResizeToContents)

        self.rightlayout.addWidget(self.todonote)

        self.readTodoData()
        self.setupAction()

    def readTodoData(self, parent=None, supplylist=None):

        todolist = TodoDatasSupply().read_todo_tree() if supplylist == None else supplylist

        for item in todolist:

            treeitem = QTreeWidgetItem()
            treeitem.setCheckState(0, Qt.Checked)
            treeitem.setText(0, item['title'])
            treeitem.setText(1, item['finishdate'])

            treeitem.setIcon(0, QIcon("Images/todo/flag/%s" % item['flag']))
            treeitem.setText(2, str(item['percent']))
            treeitem.setText(3, str(item['level']))
            treeitem.setText(4, item['desc'])

            if None == parent:
                self.todolist.addTopLevelItem(treeitem)
            else:
                parent.addChild(treeitem)
            if len(item['list']) > 0:
                self.readTodoData(treeitem, item['list'])

    def setupAction(self):
        QObject.connect(self.todonote.accessPoint(), SIGNAL("contentsChanged ()"), self.onbuffer)

        QObject.connect(self.todolist, SIGNAL("itemDoubleClicked (QTreeWidgetItem *,int)"), self.evt_dbclick)
        QObject.connect(self.todolist, SIGNAL("itemClicked (QTreeWidgetItem *,int)"), self.evt_click)
        QObject.connect(self.todolist, SIGNAL("itemActivated (QTreeWidgetItem *,int)"), self.evt_click)

    def evt_dbclick(self, item, pos):

        #        if 2==pos:
        #            colorSelecter = PercentQComboBox(item)
        #            self.todolist.setItemWidget(item,2,colorSelecter)

        pass

    def evt_click(self, item, pos):
        self.todonote.fill(item.text(4))
        self.titleeditor.setText(item.text(0))
        self.dateeditor.setDateTime(QDateTime.fromString(item.text(1), "yyyyMMddhhmmss"))
        self.percenteditor.setValue(int(item.text(2)))
        self.leveleditor.setValue(int(item.text(3)))

    def evt_new(self):
        pass

    def evt_save(self):
        pass

    def evt_delete(self):
        pass

    def evt_up(self):
        pass

    def evt_down(self):
        pass

    def evt_help(self):
        pass


class TodoDatasSupply(object):
    def __init__(self):
        self.DATAFILE = getPath("dataDir", "todo/default.db")

    def __dbBegin(self):
        """
        init connection and statement
        """
        self.conn = sqlite.connect(self.DATAFILE)
        self.stmt = self.conn.cursor()

    def __dbEnd(self):
        """
        close the db.
        """
        self.conn.commit()
        self.stmt.close()
        self.conn.close()

    def read_todo_tree(self, parent=-1):
        self.__dbBegin()
        re = self.__read_todo_tree()
        self.__dbEnd()
        return re

    def __read_todo_tree(self, parent=-1):
        todo_list = []

        sql = "select id,title,percent,level,createdate,finishdate,flag,clicked,desc from todo where parent=%d" % parent

        self.stmt.execute(sql)
        todolist = self.stmt.fetchall()
        for item in todolist:
            todo_list.append(
                {'list': self.__read_todo_tree(item[0]),
                 'title': item[1],
                 'percent': str(item[2]),
                 'level': str(item[3]),
                 'createdate': item[4],
                 'finishdate': item[5],
                 'flag': item[6],
                 'clicked': str(item[7]),
                 'desc': item[8]
                 })

        return todo_list
