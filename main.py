# -*- coding: utf-8 -*-
"""
Created on Sat Dec  8 14:04:58 2018

@author: menguan
"""

from window import Ui_mainwindow
from eval import EVAL
from crawler import *
import sys
import time
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QListWidgetItem 

class MAIN(EVAL,Ui_mainwindow):
    
    catalogurl=""
    is_root_catalog=True
    
    def setupButton(self):
        self.calprojectbtn.clicked.connect(self.calproject)
        self.calauthorbtn.clicked.connect(self.calauthor)
        self.calcodebtn.clicked.connect(self.calcode)
        
    def setprogress(self,num):
        self.progressbar.setValue(num)
        
    def calproject(self):
        if self.progressbar.value!=0:
            pass
        
        self.seturl(self.urledit.text())
        invalue=self.getinvalue()
        self.setprogress(40)
        outvalue=self.getoutvalue()
        self.setprogress(50)
        authorvalue=self.getauthorvalue()
        self.setprogress(60)
        self.invalueshow.setText(str(invalue))
        self.outvalueshow.setText(str(outvalue))
        self.authorvalueshow.setText(str(authorvalue))
        author=getauthor(self.URL)
        self.authoredit.setText(author)
        self.setprogress(70)
        authorinfo=getauthorinfo(author)
        self.authorinfoshow.setText(self.makeauthorinfo(authorinfo))
        self.setprogress(80)
        projectinfo=getprojectinfo(self.URL)
        self.projectinfoshow.setText(self.makeprojectinfo(projectinfo))
        self.setprogress(90)
        catalog=getcatalog(self.URL)
#        self.catalog=catalog
        self.catalogurl=self.URL#+"/tree/master/"
        self.is_root_catalog=True
        self.setcatalog(catalog,True)
        self.setprogress(100)
        time.sleep(1)
        self.setprogress(0)
    
    def calauthor(self):
        if self.progressbar.value!=0:
            pass
        author=self.authoredit.text()
        self.authoredit.setText(author)
        self.setprogress(50)
        authorinfo=getauthorinfo(author)
        self.authorinfoshow.setText(self.makeauthorinfo(authorinfo))
        self.setprogress(100)
        time.sleep(1)
        self.setprogress(0)
        
    def calcode(self):
        if self.progressbar.value!=0:
            pass

        codevalue=self.getcodevalue(self.codeview.toPlainText())
        self.codevalueshow.setText(str(round(codevalue,3)))
        self.setprogress(100)
        time.sleep(1)
        self.setprogress(0)
    
    ##之后三个函数都是用来处理项目目录
    def getcatalogurl(self,isup,profile_name=""):
        if isup==True:
            uu=self.catalogurl.split("/")
            if len(uu)<=8:
                return getcatalog(self.URL),self.URL,True
            else:
                catalogurl="/".join(uu[:len(uu)-1])
                return getcatalog(catalogurl),catalogurl,False
        else:
            if self.is_root_catalog==True:
                catalogurl=self.catalogurl+"/tree/master/"+profile_name
            else:
                catalogurl=self.catalogurl+profile_name
            print(catalogurl)
            return getcatalog(catalogurl),catalogurl,False
           
        
    def catalog_item_click(self,item):
        if item.font().italic()==True:
            catalog,self.catalogurl,self.is_root_catalog=self.getcatalogurl(True)
            self.setcatalog(catalog,self.is_root_catalog)
        elif item.font().bold()==False:
            self.codeview.setText(getrawcode(self.catalogurl,item.text()))#getrawcode(catalogurl+item.text())))
        else:
            catalog,self.catalogurl,self.is_root_catalog=self.getcatalogurl(False,item.text())
            self.setcatalog(catalog,self.is_root_catalog)
        
    def setcatalog(self,catalog,isroot):
        self.catalogshow.clear()
        font=self.catalogshow.font()
        if isroot==False: #返回上级 斜体省略号...
            item=QListWidgetItem()
            item.setText("...")
            tfont=font
            tfont.setBold(True)
            tfont.setItalic(True)
            item.setFont(tfont)
            self.catalogshow.addItem(item)
        for i in catalog:
            item=QListWidgetItem()
            item.setText(i[0])
            if i[1]!="blob":#目录进行加粗
                tfont=font
                tfont.setBold(True)
                item.setFont(tfont)
            self.catalogshow.addItem(item)
        self.catalogshow.itemDoubleClicked.connect(self.catalog_item_click)
    
    
    def makeauthorinfo(self,authorinfo):
        if len(authorinfo)==3:
            st="Repositories: "+authorinfo[0]+" People: "+authorinfo[1]+"\nProjects: "+authorinfo[2]
        elif len(authorinfo)==4:
            st="Repositories: "+authorinfo[0]+" Stars: "+authorinfo[1]+"\nFollowers: "+authorinfo[2]+" Following: "+authorinfo[1]
        return st
    
    def makeprojectinfo(self,projectinfo):
        st="Watch: "+projectinfo['Watch']+" Star: "+projectinfo['Star']+"\nFork: " \
            +projectinfo['Fork']+" Commits: "+projectinfo['Commits'] \
            +"\nBranchs: "+projectinfo['Branchs']+" Releases: "+projectinfo['Releases'] \
            +"\nContributors: "+projectinfo['Contributors']
        return st    
        
def main():
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    ui = MAIN()
    ui.setupUi(window)
    ui.setupButton()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
    

testurl="https://github.com/tianjin-university/lmis-tieics2017"
