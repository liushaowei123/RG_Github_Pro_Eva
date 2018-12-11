# -*- coding: utf-8 -*-
"""
Created on Mon Nov 19 19:31:22 2018

@author: menguan
"""

from pyquery import PyQuery as pq
import requests
#class CRAWLER(object):
    
#testURL = "https://github.com/YadiraF/GAN"

def getcatalog(url):#,isroot,step): #获取项目目录
    nowlist=[]
    doc = pq(url)
    content=doc('.content .js-navigation-open').items()
    for i in content:
        addr=i.attr('href')
        addr=addr.split('/')
        typ=addr[3]
#        nam="/".join(addr[5:len(addr)])
        nam=addr[len(addr)-1]
        res=[]
        res.append(nam)
        res.append(typ)
        nowlist.append(res)
            
#        else: #递归查找子目录 耗时且可能会被限制ip
#            if isroot==True:
#                nowlist.append(getcatalog(url+"/tree/master/"+nam,False,step+1))
#            else:
#                nowlist.append(getcatalog(url+"/"+nam,False,step+1))
    return nowlist

def getrawcode(url,str):
    uu=url.split('/')
    if len(uu)>6:
        uu.pop(5)
    else: 
        uu.append("master")
    uu[2]="raw.githubusercontent.com"
    uu.append(str)
    url="/".join(uu)
    res = requests.get(url)
    res.encoding = 'utf-8'
    return res.text  

def getsomecode(url):#随机抽取一些项目中的代码 这里测试版本只抽取主目录的一个代码
    res=[]
    catalog=getcatalog(url)
    for i in catalog:
        if i[1] == "blob":
            res.append(getrawcode(url,i[0]))
            break;#这里只取一个
    return res
    
def geturl(author,projectname):
    return "https://github.com/"+author+"/"+projectname
    
def getproname(url):
    tmp=url.split("/")
    return tmp[len(tmp)-1]

def getauthor(url):
    doc = pq(url)
    author=doc('.author').text()
    return author

def getprojectinfo(url): #return dict
    doc = pq(url)
    WSF = doc('.social-count').items() 
    tmp=[]
    for i in WSF:
        tmp.append(i.text().replace(',', ''))
    CBRC = doc('.numbers-summary li a span').items()  
    for i in CBRC:
        tmp.append(i.text().replace(',', ''))
    dic={}
    dic['Name']=getproname(url)
    dic['Author']=getauthor(url)
    dic['Watch']=tmp[0]
    dic['Star']=tmp[1]
    dic['Fork']=tmp[2]
    dic['Commits']=tmp[3]
    dic['Branchs']=tmp[4]
    dic['Releases']=tmp[5]
    dic['Contributors']=tmp[6]
    isfork=doc('.fork-flag').items()
    dic['Isfork']=0
    for i in isfork:
        dic['Isfork']=1
    return dic

def getauthorinfo(author): 
    #return list 4个代表Repositories Stars Followers Following 3个代表Repositories People Projects
    url="https://github.com/"+author
    doc = pq(url)
    proper = doc('.Counter').items() 
    res=[]
    for i in proper:
        tmp=i.text()
        res.append(tmp)
    return res

def getstars(url): #获取收藏人列表
    page=1
    res=[]
    while True:
        turl=url+"/stargazers?page="+str(page)
        doc=pq(turl)
        stname=doc('.follow-list-name').items()
        for i in stname:
            tmp=i.text()
            res.append(tmp)
        pa=doc('.pagination') 
        if len(pa)==0:
            break
        pa=doc('.pagination .disabled').text()
        if pa=="Next":
            break
        page=page+1
    return res

def getforkers(url): #获取fork的人列表 第一个是自己 只能取出1000左右 这里只做评价用 还可以通过作者的资料进行补充 
    url=url+"/network/members"
    res=[]
    doc=pq(url)
    forkers=doc('.repo').items()
    for i in forkers:
        res.append(i.text().split(' ')[0])
    return res

def getfollowers(author):
    return 0

def getfollowing(author):
    return 0
    
def getrepositories(author): # return list获取仓库列表
    page=1
    res=[]
    while True:
        url="https://github.com/"+str(author)+"?page="+str(page)+"&tab=repositories"
        doc=pq(url)
        rename=doc('.d-inline-block.mb-1').items()
        for i in rename:
            tmp=i.text().split('\n')
            res.append(tmp[0])
            
        pa=doc('.pagination') 
        if len(pa)==0:
            break
        pa=doc('.next_page.disabled')
        if len(pa)!=0:
            break
        page=page+1
        
    return res

#testURL = "https://github.com/tianjin-university/lmis-tieics2017/tree/master/db"
#uu=testURL.split("/")
#uu.pop(5)
#aa=getrawcode(testURL,"logistics.sql")