# coding:utf-8
#
# Copyright (c) 2010, guo.li <lycying@gmail.com>
# Site < http://code.google.com/p/seeking/ >
# All rights reserved.
# vim: set ft=python sw=2 ts=2 et:
#
import os,zipfile
import shutil
import logging
log=logging.getLogger("Log")
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
console.setFormatter(formatter)
filelog = logging.FileHandler("/tmp/tools.log")
filelog.setLevel(logging.DEBUG)
filelog.setFormatter(formatter)
log.addHandler(console)
log.addHandler(filelog)
log.setLevel(logging.DEBUG)

BASE_DIR = "../core/plugins/"
PUBLISH_DIR = "../doc/source/_static/"


shutil.copy("plugins.txt","%splugins.txt"%PUBLISH_DIR)
plugins_info = open("plugins.txt").readlines()

#change the dir .
os.chdir(BASE_DIR)
for plugin_info in plugins_info:

    log.debug("process for %s" % plugin_info)    

    plugin_name = plugin_info.split('|')[0]
    plugin_version = plugin_info.split('|')[1]
    plugin_instruction = plugin_info.split('|')[2]

    filelist = []
    filelist.append("plugin-%s.py"%plugin_name)
    for root,dirs,files in os.walk("%s"%plugin_name):
        for name in files:
            full_name = os.path.join(root, name)
            if not full_name.__contains__(".svn"):
                filelist.append(full_name)

    zf = zipfile.ZipFile('../%splugin-%s-%s.zip' %(PUBLISH_DIR,plugin_name,plugin_version),'w', zipfile.ZIP_DEFLATED)
    for i in filelist:
        log.debug("zip file %s" % i)    
        zf.write(i)
    zf.close()
    log.debug("zip done!\n")    
