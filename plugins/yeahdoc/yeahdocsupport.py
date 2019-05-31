# coding:utf-8
#
# Copyright (c) 2010, guo.li <lycying@gmail.com>
# Site < http://code.google.com/p/seeking/ >
# All rights reserved.
# vim: set ft=python sw=2 ts=2 et:
#
import os
import time
import sys
import sqlite3 as sqlite

from PyQt5.QtCore import QVariant


from sklib.config import Prefs, getPath, getPrccisePath
from sklib.security import sk_encode,sk_decode


            
def getMyBaseUrl():
        STOREDIR = ""
        
        userDefinedDir = YeahdocExtConfig().getStoreDir()
        
        if userDefinedDir == None or userDefinedDir ==  "":
            #QMessageBox.information(Seeking().new(), "Welcome", "This is the first time you run yeahdoc-plguin: please select your store dir . \n if you do not know what to do , Select cancel ")
            temp = getPath("dataDir", "yeahdoc.db")
            if temp is None:
                if sys.platform.startswith("win"):
                    STOREDIR = getPrccisePath("dataDir", "","coredir")
                else:
                    STOREDIR = getPrccisePath("dataDir", "","userdir")
                    
                STOREDIR = STOREDIR.replace("\\", "/")
                
            else:
                STOREDIR = temp.replace("yeahdoc.db","")
        return STOREDIR
        
class YeahdocDatasSupply(object):
    """
    The yeahdoc datas supply . 
    read , update or delete datas use sqlite3
    """
    def __init__(self):
        self.STOREDIR = getMyBaseUrl()
        
        self.DATAFILE = "%s/yeahdoc.db" % self.STOREDIR
        if not  os.path.exists(self.STOREDIR):
            os.makedirs(self.STOREDIR)
        if not  os.path.exists(self.DATAFILE):
            self.__install()
            
                
        self.MAXLINE = int(YeahdocExtConfig().getNumberPerPage())
    def __install(self):
        """
        init db file
        """
        self.__dbBegin()
        self.stmt.execute("CREATE TABLE yeahdoc (star NUMERIC, lock NUMERIC, categoryid NUMERIC, desc TEXT, createdate varchar(20), img varchar(100), tags varchar(500), id INTEGER PRIMARY KEY, title varchar(200), content TEXT);")
        self.stmt.execute("CREATE TABLE category (img varchar(100), id INTEGER PRIMARY KEY, title varchar(100), desc TEXT, yeahdocnum NUMERIC,lock NUMERIC, createdate varchar(20));")
        self.stmt.execute("INSERT INTO category VALUES('default.png',1,'Default','<html><head></head><body>Default</body></html>',0,0,2010101010101010);")
        self.__dbEnd()

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

    def bb_list(self,categoryid=None):
        """
        Read the Data/item files . the return structs is :
        """
        yeahdoc_list = []
        sql = "select id,img,createdate,desc,title,star,lock from yeahdoc order by id desc limit %d offset 0" % self.MAXLINE
        if categoryid!=None:
            sql =  "select id,img,createdate,desc,title,star,lock from yeahdoc where categoryid=%s order by id desc  " % categoryid
        
        self.__dbBegin()
        
        self.stmt.execute(sql)
        yeahdoclist = self.stmt.fetchall()
        for item in yeahdoclist:
            yeahdoc_list.append({
                    "title":item[4], \
                    "img":item[1], \
                    "createdate":item[2], \
                    "id":str(item[0]),\
                    "star":item[5],\
                    "lock":item[6]
                    })
        
        self.__dbEnd()
    
        return yeahdoc_list
    def bb_lock(self,idx,password):
        request = self.bb_read1(idx)["content"]
        result = sk_encode(request, password)
        sql = "update  yeahdoc set lock=1,desc='',content=? where id=%s" % idx
        self.__dbBegin()
        self.stmt.execute(sql,(result,))
        self.__dbEnd()
    def bb_unlock(self,idx,password):
        request = self.bb_read1(idx)["content"]
        result = sk_decode(request, password)
        sql = "update  yeahdoc set lock=0,content=? where id=%s" % idx
        self.__dbBegin()
        self.stmt.execute(sql,(result,))
        self.__dbEnd()
    def bb_read1_simple(self,idx):
        """
        avoid large datas, just simple infomation
        """
        
        sql = "select id,img,createdate,title,categoryid,desc,lock from yeahdoc where id=%s"%idx
        self.__dbBegin()
        
        self.stmt.execute(sql)

        rs      = self.stmt.fetchone()
        title   = rs[3]
        icon    = rs[1]
        categoryid = rs[4]
        desc    = rs[5]
        lock    = rs[6]
        
        self.__dbEnd()
        
        title = "%s.." % title[0:8] if len(title)>8 else title
        return {"title":title,"img":icon,"categoryid":categoryid,"desc":desc,"lock":lock}
    
    def bb_read1(self,idx):
        """
        get the yeahdoc infomation and display it 
        """
        sql = "select id,img,createdate,title,desc,content,categoryid,lock from yeahdoc where id= %s" %idx
        self.__dbBegin()
        
        self.stmt.execute(sql)
        rs      = self.stmt.fetchone()
        title   = rs[3]
        icon    = rs[1]
        content = rs[5]
        desc    = rs[4]
        categoryid = rs[6]
        createdate=rs[2]
        lock    = rs[7]
        
        self.__dbEnd()
        
        return {"title":title,"img":icon,"content":content,"desc":desc,"createdate":createdate,"categoryid":categoryid,"lock":lock}
    
    def bb_save(self,categoryid,title,tags,img,content,password,idx):
        """
        save or update the yeahdoc
        """
        lock = 0 if password=="" else 1
        createdate = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
        insert_sql = "insert into yeahdoc (categoryid,title,img,tags,createdate,star,content,desc,lock) values(%s,'%s','%s','%s','%s',0,?,?,%d)" % (categoryid,title,img,tags,createdate,lock)
        update_sql = "update  yeahdoc set categoryid=%s,title='%s',img='%s',tags='%s',content=?,desc=?,lock=%s where id=%s" % (categoryid,title,img,tags,lock,idx)
        self.__dbBegin()
        
        desc  = ""
        #encode the content .
        if not password=="":
            content = sk_encode(content, password)
        else:
            desc  = "%s.." % content[0:500] if len(content)>500 else content
            
        if idx == "~":
            #next seq 
            self.stmt.execute("select max(id) as n from yeahdoc ")
            try:
                idx = self.stmt.fetchone()[0]+1
            except:
                idx = 1
            self.stmt.execute(insert_sql,(content,desc,))
        else:
            self.stmt.execute(update_sql,(content,desc,))
            
        self.__dbEnd()
        
        return str(idx)

    def bb_delete(self,idx):
        """
        delete yeahdoc item from db
        """
        sql = "delete from yeahdoc where id=%s" % idx
        self.__dbBegin()
        
        self.stmt.execute(sql)
        self.stmt.execute("VACUUM")
        
        self.__dbEnd()
        return True

    
    def bb_update_title(self,value,idx):
        """
        this may used when rename a yeahdoc
        """
        sql = "update  yeahdoc set title='%s'where id=%s" %(value,idx)
        
        self.__dbBegin()
        
        self.stmt.execute(sql)
        
        self.__dbEnd()
        return True
    
    def bb_update_class(self,value,idx):
        """
        change the yeahdoc class
        """
        
        sql = "update  yeahdoc set categoryid=%s where id=%s" %(value,idx)
        
        self.__dbBegin()
        
        self.stmt.execute(sql)
        
        self.__dbEnd()
        return True
    
    def bb_toggle_star(self,idx):
        """
        toggle star flag
        """
        selectsql = "select star from yeahdoc where id=%s"%idx
        sql = "update  yeahdoc set star=? where id=%s"%idx
        
        self.__dbBegin()
        
        self.stmt.execute(selectsql)
        fx = self.stmt.fetchone()[0]
        if 0==fx:
            self.stmt.execute(sql,(1,))
        else:
            self.stmt.execute(sql,(0,))
            
        self.__dbEnd()
        return fx
    
    def bc_list(self):
        """
        read class list datas
        """
        yeahdoc_class_list = []
        sql = "select id,img,createdate,desc,title,lock from category order by id desc"
        self.__dbBegin()
        
        self.stmt.execute(sql)
        yeahdoclist = self.stmt.fetchall()
        for item in yeahdoclist:
            yeahdoc_class_list.append({"id":item[0],"title":item[4], "img":item[1], "createdate":item[2],"lock":item[5]})
            
        self.__dbEnd()
    
        return yeahdoc_class_list

    def bc_save(self,title,img,desc,idx):
        """
        save yeahdoc class item
        """
        createdate = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
        insert_sql = "insert into category (title,img,createdate,desc) values('%s','%s','%s',?)" %(title,img,createdate)
        update_sql = "update  category set title='%s',img='%s',desc=? where id=%s" %(title,img,idx)
        
        self.__dbBegin()
        
        if idx == "~":
            self.stmt.execute("select max(id) as n from category ")
            try:
                idx = self.stmt.fetchone()[0]+1
            except:
                idx = 1
            self.stmt.execute(insert_sql,(desc,))
        else:
            self.stmt.execute(update_sql,(desc,))
            
        self.__dbEnd()
        return str(idx)
    
    def bc_read1(self,idx):
        """ read yeahdoc class item data """
        sql = "select id,img,createdate,title,desc,lock from category where id=%s" % idx
        
        self.__dbBegin()
        
        self.stmt.execute(sql)
        rs      = self.stmt.fetchone()
        idx      = rs[0]
        title   = rs[3]
        icon    = rs[1]
        desc    = rs[4]
        createdate=rs[2]
        lock    = rs[5]
        
        self.__dbEnd()
        
        return {"id":idx,"title":title,"img":icon,"desc":desc,"createdate":createdate,"lock":lock}
    
    def bc_update_title(self,value,idx):
        """
        this may used when rename a yeahdoc
        """
        sql = "update  category set title='%s'where id=%s" %(value,idx)
        
        self.__dbBegin()
        
        self.stmt.execute(sql)
        
        self.__dbEnd()
        return True
    def bc_delete(self,idx):
        """
        delete yeahdoc class item
        """
        sql = "delete from category where id=%s"%idx
        sql2 = "delete from yeahdoc where categoryid=%s"%idx
        
        self.__dbBegin()
        self.stmt.execute(sql)
        self.stmt.execute(sql2);
        self.stmt.execute("VACUUM")
        self.__dbEnd()
        return True

    def bc_merge(self,idx,id2id):
        """
        merge the id into id2id
        """
        sql = "update yeahdoc set categoryid=%s where categoryid=%s" % (str(id2id),str(idx))
        self.__dbBegin()
        self.stmt.execute(sql)
        self.__dbEnd()

    def bc_clear(self,idx):
        """
        clear the datas of this category
        """
        sql = "delete from yeahdoc where categoryid=%s"%idx
        self.__dbBegin()
        self.stmt.execute(sql)
        self.__dbEnd()
    
    
class YeahdocExtConfig(object):
    """
    yeahdoc config
    """
    def __init__(self):
        self.settings = Prefs.new().getSettings()
    
    
    def getNumberPerPage(self):
        """
        number per page show
        """
        return self.settings.value("UI/Plugin/yeahdoc/numberperpage",
                QVariant(100)).toString()
    
    def setNumberPerPage(self,num):
        """
        number per page show
        """
        value = QVariant(50)
        if isinstance(num,int) or num.isdigit():
            value = QVariant(num)
        self.settings.setValue("UI/Plugin/yeahdoc/numberperpage", value)
        
    def getStoreDir(self):
        """
        Module function to retrieve the language for the user interface.
        """
        storedir = self.settings.value("UI/Plugin/yeahdoc/storedir",QVariant("")).toString()
        
        return None if storedir is "None" or storedir is "" or storedir is None else storedir
    
    def setStoreDir(self,storedir):
        """
        Module function to store the language for the user interface.
        """
        self.settings.setValue("UI/Plugin/yeahdoc/storedir", QVariant("" if storedir is None else storedir))

