# -*- coding: utf-8 -*-
"""
Created on Thu Dec  6 18:46:39 2018

@author: menguan
"""

from crawler import *
from database import *

class EVAL(object):
    
    URL=""
    
    def __init__(self):
        self.DB=DB()
#        self.crawler=CRAWLER()
        
    def seturl(self,url):
        self.URL=url
    
    def geteps(self,LIST):
        if len(LIST)!=0:     
            eps=1.0/len(LIST)
        else:
            eps=0
        return eps
        
    def _getauthorvalue(self,author):       
        value=self.DB.get_author_value(author) #检查数据库中是否已经有结果
        if value>0:
            return value
        repositories=getrepositories(author)
        eps=self.geteps(repositories)     
        value=0.0000001
        for i in repositories:
            value=value+eps*self._getinvalue(geturl(author,i))
        
        self.DB.addauthor(author,getauthorinfo(author),value)
        return value
    
    def getauthorvalue(self):
        author=getauthor(self.URL)
        print(author)
        return self._getauthorvalue(author)
            
    def _getinvalue(self,url):
        print(url)
        proname=getproname(url)
        author=getauthor(url)
        invalue=self.DB.get_project_invalue(proname,author) #检查数据库中是否已经有结果 若没有同时进行初始添加项目
        if invalue>0:
            return invalue
        
        invalue=0.0000001
        #可以在这预留出接口评价项目本身的接口
#        codelist=getsomecode(url)
#        eps=self.geteps(codelist)
#        for i in codelist:
#            invalue=invalue+self.getcodevalue(i)*eps
        import random
        invalue=random.uniform(60, 80)
        self.DB.update_project_with_invalue(proname,author,invalue)
        return invalue
    
    def getinvalue(self):
        return self._getinvalue(self.URL)
        
    def _getoutvalue(self,url):
        proname=getproname(url)
        author=getauthor(url)
        outvalue=self.DB.get_project_outvalue(proname,author) #检查数据库中是否已经有结果 若没有同时进行初始添加项目
        if outvalue>0:
            return outvalue
        
        forkers=getforkers(url)
        stars=getstars(url)
        
        forkvalue=0
        eps=self.geteps(forkers)    
        for i in forkers:
            forkvalue=forkvalue+eps*self._getauthorvalue(i)
        
#        for i in forkers:
#            self.DB.addfork(proname,author,i)
            
        starvalue=0
        eps=self.geteps(stars)    
        for i in stars:
            starvalue=starvalue+eps*self._getauthorvalue(i)
        
        outvalue=max(forkvalue,starvalue)+0.0000001
        self.DB.update_project_with_outvalue(proname,author,outvalue)
        return outvalue
    
    def getoutvalue(self):
        return self._getoutvalue(self.URL)
    
    def getcodevalue(self,str):
        line=str.split("\n")
        #arrangeline=getdifferent(line)
        #按照缩进划分代码段 未实现
        #对不同层次的代码段分别进行聚类
        #检查相似代码段，并按照比例进行不同层次上的评分
        #from sklearn.cluster import SpectralClustering
        #ans = SpectralClustering(n_clusters=K, random_state=0)
        import random
        return random.uniform(60, 80)
            