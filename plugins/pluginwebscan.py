# coding:utf-8
#
# Copyright (c) 2010, guo.li <lycying@gmail.com>
# Site < http://code.google.com/p/seeking/ >
# All rights reserved.
# vim: set ft=python sw=2 ts=2 et:
#

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction

from plugins.webscan.adminscan import Scanner
from plugins.webscan.portscan import PortScanner
from sklib.config import getPath
from sklib.ui.uimain import Seeking

# Info ===
name = "Web Scanner"
author = "lycy < lycying@gmail.com >"
version = "0.1"
packageName = "__core_ext__"
description = "Web  For Security User"


# Info ===

def install(): pass  # pass


def uninstall(): pass  # pass


def activate():
    def evt_adminscan():
        Scanner()

    def evt_portscan():
        PortScanner()

    sk = Seeking.new()
    sk.regAction("__webadminscan",
                 QAction(QIcon(getPath('pluginsDir', 'webscan/admin.png')), "Admin Scan", Seeking.new(),
                         triggered=evt_adminscan))
    sk.regAction("__portscan", QAction(QIcon(getPath('pluginsDir', 'webscan/port.png')), "Port Scan", Seeking.new(),
                                       triggered=evt_portscan))
    toolbar = sk.addToolBar("WebScan")
    toolbar.addAction(sk.getAction("__webadminscan"))
    toolbar.addAction(sk.getAction("__portscan"))


def deactivate(): pass
