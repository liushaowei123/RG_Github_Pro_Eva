# -*- coding: utf-8 -*-
"""
Created on Thu Dec  6 13:46:14 2018

@author: menguan
"""


import pymysql
from crawler import *

class DB(object):
    
    def __init__(self):
        self.db = pymysql.connect("localhost","root","root","github" )#数据库配置
        self.cursor = self.db.cursor()
    
    def __del__(self):
        self.db.close()
    
    def exe(self,sql):
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            print(e)
            self.db.rollback()
            
    def init(self):#数据库初始化 需要加timestamp 目前还没有实现
        self.cursor.execute("DROP TABLE IF EXISTS FORK")
        self.cursor.execute("DROP TABLE IF EXISTS AUTHOR")
        self.cursor.execute("DROP TABLE IF EXISTS PROJECT")
        #作者
        sql = """CREATE TABLE AUTHOR (
             NAME CHAR(20) NOT NULL,
             REPOSITORIES CHAR(10) NOT NULL,
             STARS CHAR(10),
             FOLLOWERS CHAR(10),
             FOLLOWING CHAR(10),
             PEOPLE CHAR(10),
             PROJECTS CHAR(10),
             VALUE FLOAT,
             PRIMARY KEY (`NAME`)
             )ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;"""
        self.exe(sql)
        #项目
        sql = """CREATE TABLE PROJECT (
             PROJECTNAME CHAR(40) NOT NULL,
             AUTHOR CHAR(20) NOT NULL,
             Watch CHAR(10),
             Star CHAR(10),
             Fork CHAR(10),
             Commits CHAR(10),
             Branchs CHAR(10),
             Releases CHAR(10),
             Contributors CHAR(10),
             OutValue FLOAT DEFAULT '0' COMMENT '基于关联对项目的评价分数',
             InValue FLOAT DEFAULT '0' COMMENT '对项目本身的评价分数',
             IsFork INT NOT NULL DEFAULT '-1' COMMENT '是否fork了别的项目(0：不是，1：是)',
             PRIMARY KEY (`PROJECTNAME`,`AUTHOR`)
             )ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;"""
        self.exe(sql)
        #fork约束
        sql = """CREATE TABLE FORK (
             PROJECTNAME CHAR(40) NOT NULL,
             ORIAUTHOR CHAR(20) NOT NULL,
             FORKAUTHOR CHAR(20) NOT NULL,
             PRIMARY KEY (`PROJECTNAME`,`ORIAUTHOR`,`FORKAUTHOR`),
             CONSTRAINT `FORK_ibfk_1` FOREIGN KEY (`ORIAUTHOR`) REFERENCES `AUTHOR` (`NAME`),
             CONSTRAINT `FORK_ibfk_2` FOREIGN KEY (`FORKAUTHOR`) REFERENCES `AUTHOR` (`NAME`),
             CONSTRAINT `FORK_ibfk_3` FOREIGN KEY (`PROJECTNAME`) REFERENCES `PROJECT` (`PROJECTNAME`)
             )ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;"""
        self.exe(sql)
        
    def addauthor(self,name,info,value):#初始添加作者
        if len(info)==3:
            sql = "INSERT INTO AUTHOR \
                    VALUES ('%s','%s', '-1', '-1' ,'-1','%s','%s',%f)" % \
                    (name, info[0], info[1] , info[2] , value)
            self.exe(sql)
        elif len(info)==4:
            sql = "INSERT INTO AUTHOR \
                    VALUES ('%s','%s', '%s','%s' , '%s' , '-1', '-1' ,%f)" % \
                    (name, info[0], info[1] , info[2],info[3],value)
            self.exe(sql)
        
    def addproject(self,dic):#初始添加项目
        sql = "INSERT INTO PROJECT \
                    VALUES ('%s','%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s',-1.0,-1.0,%d )" % \
                    (dic['Name'], dic['Author'], dic['Watch'],dic['Star'],
                     dic['Fork'],dic['Commits'],dic['Branchs'],
                     dic['Releases'],dic['Contributors'],dic['Isfork'])
        self.exe(sql)
        
    def addfork(self,proname,oriauthor,forkauthor):#添加fork并自动
        sql = "INSERT INTO FORK \
                    VALUES ('%s','%s','%s')" % \
                    (proname,oriauthor,forkauthor)
        self.exe(sql)
#        更新 前后两个项目的 isfork属性 并不需要
#        sql = "UPDATE PROJECT SET IsFork = 0 WHERE PROJECTNAME = '%s' AND AUTHOR = '%s' " % (proname,oriauthor)
#        self.exe(sql)
#        sql = "UPDATE PROJECT SET IsFork = 1 WHERE PROJECTNAME = '%s' AND AUTHOR = '%s' " % (proname,forkauthor)
#        self.exe(sql)
    
    def get_author_value(self,author):
        sql = "SELECT * FROM AUTHOR \
                WHERE NAME= '%s' " % (author)
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            if len(results)==0:
                return -1.0
            else:
                return results[0][7]                
        except Exception as e:
            print(e)
            self.db.rollback()
        return -1.0     
    
    def get_project_invalue(self,proname,author):
        sql = "SELECT * FROM PROJECT \
                WHERE PROJECTNAME = '%s' AND AUTHOR = '%s' " % (proname,author)
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            if len(results)==0:
                self.addproject(getprojectinfo(geturl(author,proname)))
                return -1.0
            else:
                return results[0][10]                
        except Exception as e:
            print(e)
            self.db.rollback()
        return -1.0     
        
    def get_project_outvalue(self,proname,author):
        sql = "SELECT * FROM PROJECT \
                WHERE PROJECTNAME = '%s' AND AUTHOR = '%s' " % (proname,author)
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            if len(results)==0:
                self.addproject(getprojectinfo(geturl(author,proname)))
                return -1.0
            else:
                return results[0][9]                
        except Exception as e:
            print(e)
            self.db.rollback()
        return -1.0
    
    
    def update_project_with_invalue(self,proname,author,invalue):
        sql = "UPDATE PROJECT SET InValue= %f  \
                WHERE PROJECTNAME = '%s' AND AUTHOR = '%s' " % \
                (invalue,proname,author)
        self.exe(sql)
    
    def update_project_with_outvalue(self,proname,author,outvalue):
        sql = "UPDATE PROJECT SET OutValue= %f  \
                WHERE PROJECTNAME = '%s' AND AUTHOR = '%s' " % \
                (outvalue,proname,author)
        self.exe(sql)
    
    #实际上只能一次更新一个值
    def updateproject(self,proname,author,outvalue,invalue):
        sql = "UPDATE PROJECT SET OutValue= %f AND InValue = %f \
                WHERE PROJECTNAME = '%s' AND AUTHOR = '%s' " % \
                (outvalue,invalue,proname,author)
        self.exe(sql)
        
    def deleteproject(self):
        pass
    
    def deleteauthor(self):
        pass
    
    def deletefork(self):
        pass
    
a=DB() #数据库初始化
a.init()