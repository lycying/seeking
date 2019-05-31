# coding:utf-8
#
# Copyright (c) 2010, guo.li <lycying@gmail.com>
# Site < http://code.google.com/p/seeking/ >
# All rights reserved.
# vim: set ft=python sw=2 ts=2 et:
#
import re
import os
import hashlib
from urllib.request import urlretrieve
import imghdr
from shutil import move

def cleanEmptyTagSub(html):
    html = re.sub("<span>\s*</span>","", html, flags=re.MULTILINE)
    html = re.sub("<SPAN>\s*</SPAN>","", html, flags=re.MULTILINE)
    html = re.sub("<font>\s*</font>","", html, flags=re.MULTILINE)
    html = re.sub("<FONT>\s*</FONT>","", html, flags=re.MULTILINE)
    return html
    
def cleanEmptyTag(html):
    return cleanEmptyTagSub(cleanEmptyTagSub(cleanEmptyTagSub(html)))
try:
    from lxml.html.clean import Cleaner
    from lxml import etree, html
    def htmlclean(value):
        cleaner = Cleaner(page_structure=False)
        value = cleanEmptyTag(cleaner.clean_html(value))
        try:
            document_root = html.document_fromstring(value)
            return etree.tostring(document_root, encoding='unicode', pretty_print=True)
        except Exception as e:
            raise e
            return value
except Exception as e:
    raise e

def downloadImages(value,baseUrl):
    if not os.path.exists(baseUrl):
        os.makedirs(baseUrl)
            
    number = 0
    if not baseUrl.endswith("/"):
        baseUrl = baseUrl+"/"
    try:
        document_root = html.document_fromstring(value)
        for link in document_root.xpath('//img'):
            if link.get("src").find("/") != -1:
                try:
                    uuidstr = str(hashlib.sha224(link.get("src").encode('utf-8')).hexdigest())
                    filename = baseUrl+uuidstr
                    urlretrieve(link.get('src'), filename)
                    imgType = imghdr.what(filename)
                    dstname = filename+"."+imgType
                    move(filename, dstname)
                    value = value.replace(link.get('src'),uuidstr+"."+imgType)
                    link.set("src",uuidstr+"."+imgType)
                    number = number+1
                except:
                    pass
        return  number,etree.tostring(document_root, encoding='unicode', pretty_print=True)
    except Exception as e:
        raise e
        return number,value
