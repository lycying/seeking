# coding:utf-8
#
# Copyright (c) 2010, guo.li <lycying@gmail.com>
# Site < http://code.google.com/p/seeking/ >
# All rights reserved.
# vim: set ft=python sw=2 ts=2 et:
#


import sys

from cx_Freeze import setup, Executable


base = None
if sys.platform == "win32":
    base = "Win32GUI"

buildOptions = dict(
        compressed = True,
        #path = sys.path + ["plugins"],
        excludes = ['cookielib', 'getpass', 'urllib2', 'ssl', 'termios', 'matplotlib', "Tkconstants", "Tkinter", "tcl", "_imagingtk",
                    "ImageTk", "FixTk", 'wx', 'PyQt5.QtAssistant', 'PyQt5.QtOpenGL',
                    'PyQt5.QtScript', 'PyQt5.QtSql', 'PyQt5.QtTest', 'qt'
            ],
        includes = ["pyDes","inspect","lxml", "lxml._elementpath", "lxml.etree",\
                    'PyQt5.QtWebKit',\
                'PyQt5.QtNetwork',
                'sqlite3',\
                'sklib.security',\
                'sklib.ui.support',\
                'sklib.ui.wysiwyg',\
                'sklib.ui.wysiwyg.browserview',\
                'sklib.ui.wysiwyg.editview',\
                'sklib.htmlfilter',\
                'sklib.ui.cpages.applicationPage'],
        include_files = [
                         "plugins",
                         "images",
                         "support",
                         "datas",
                         "trans/i18n_en_US.qm",
                         "trans/i18n_zh_CN.qm"
                         ]
        )

setup(
        name = "Seeking",
        version = "0.1",
        description = "Seeking",
        options = dict(build_exe = buildOptions),
        executables=[
            Executable("Seeking.pyw", base = base,icon="images/logo.ico")
        ])


