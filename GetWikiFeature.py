# -*- coding: utf-8 -*-
from os import replace

import requests
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup


class GetWikiFeature:
    keyword = ""

    def __init__(self, keyword):
        self.keyword = str(keyword).replace("–", "")
        self.fullUrl = "https://en.wikipedia.org/w/index.php?title=Special:WhatLinksHere/" + str(
            self.keyword) + "&namespace=0&limit=500"
        req = requests.get(self.fullUrl)
        html = req.text
        self.soup = BeautifulSoup(html, 'html.parser')

        print(self.keyword)

    def getIndegree(self):

        get_list = self.soup.select(
            '#mw-whatlinkshere-list'
        )
        list = (get_list[0].text)
        get_list = list.split("\n")
        in_degree = len(get_list)
        # print("Indegree 수 : " + str(in_degree))
        return in_degree

    def getLanguageNum(self):

        get_list = self.soup.select(
            '#p-lang > div.body'
        )
        list = str(get_list[0])
        get_list = list.split("<li ")
        numoflanguage = len(get_list) - 1
        # print("언어수 : " + str(numoflanguage))
        return numoflanguage

    def getCategoriesdegree(self):
        get_list = self.soup.select(
            '#mw-normal-catlinks > ul > li'
        )
        # print("category 수 : " + str(len(get_list)))
        return len(get_list)

    def getOutdegree(self):
        get_list = self.soup.select(
            '.mw-parser-output'
        )
        getList = str(get_list[0]).split("\n")
        countInDegree = 0
        for part in getList:
            if (int(part.find("<a")) >= 0):
                countInDegree += 1
                continue
            if (int(part.find('id="toc"') != -1)):
                break
        # print("Outdegree 수 : " +str(countInDegree ))
        return countInDegree

    def getOutdegree2(self):
        print("##")
        countInDegree = 0
        links = []
        for link in self.soup.find("div", {"id": "bodyContent"}).findAll("a", href=re.compile("^(/wiki/)((?!:).)*$")):
            if 'href' in link.attrs:
                if link.attrs['href'] not in links:
                    countInDegree += 1
                    links.append(link.attrs['href'])
                    # print(link.attrs['href']) #show name of links in pages
        # print("Outdegree 수 : " + str(countInDegree))
        return countInDegree, links
