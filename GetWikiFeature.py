#-*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

class GetWikiFeature:
    keyword = ""
    def __init__(self, keyword):
        self.keyword = keyword 

    def getIndegree(self):
        fullUrl = "https://en.wikipedia.org/w/index.php?title=Special:WhatLinksHere/"+str(self.keyword)+"&namespace=0&limit=500"
        req = requests.get(fullUrl)
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')

        get_list = soup.select(
            '#mw-whatlinkshere-list'
        )
        list = (get_list[0].text)
        get_list = list.split("\n")
        in_degree = len(get_list)
        print("indegree 수 : " + str(in_degree))
        return in_degree

    
    def getLanguageNum(self):
        fullUrl = "https://en.wikipedia.org/wiki/" +str(self.keyword)
        req = requests.get(fullUrl)
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')

        get_list = soup.select(
            '#p-lang > div.body'
                )
        
        list = str(get_list[0])
        get_list = list.split("<li ")
        numoflanguage = len(get_list)-1
        print("언어수 : " + str(numoflanguage))
        return numoflanguage

    def getCategoriesdegree(self):
        fullUrl = "https://en.wikipedia.org/wiki/" +str(self.keyword)
        req = requests.get(fullUrl)
        html = req.text 
        soup = BeautifulSoup(html, 'html.parser')

        get_list = soup.select(
             '#mw-normal-catlinks > ul > li'
             )
        print("category 수 : " + str(len(get_list)))
        return len(get_list)

    def getOutdegree(self):
        fullUrl = "https://en.wikipedia.org/wiki/" +str(self.keyword)
        req = requests.get(fullUrl)
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        get_list = soup.select(
            '.mw-parser-output'
            )
        getList = str(get_list[0]).split("\n")
        countOutDegree = 0
        for part in getList:
     #      print(part)
            if (int(part.find("<a")) >= 0):
                countOutDegree += 1
                continue
            if (int(part.find('id="toc"') != -1)):
                break
        print("outdegree 수 : " +str(countOutDegree ))
        return countOutDegree
        
        


#how to use

#keyword = "Artificial_neural_network"
#instance = GetWikiFeature(keyword)

#instance.getIndegree()
#instance.getLanguageNum()
#instance.getCategoriesdegree()
#instance.getOutdegree()






