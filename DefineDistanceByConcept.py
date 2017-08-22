import urllib
from urllib.request import urlopen
from urllib.error import HTTPError

import itertools
from bs4 import BeautifulSoup
import re
import numpy as np
import queue

class DefineDistance :
        # A페이지 -> B페이지 의 거리degree를 구하는 함수 및 wordset안에서 거리 구하는 코드
        # get_def_links(page_url)함수
        # 위키 링크를 받아서 그 페이지의 첫 번째 문단에 존재하는 링크들을 리스트에 담아 리턴함
        # 입력 : page_url(위키 페이지 링크)를 받음
        # 리턴 : page_url의 첫번째 문단에 존재하는 링크들을 links리스트에 담아 리턴함

    def getConceptRelation(self, wordSet):
        regex = r'\>.+'
        All_nodes = []
        #exam)
        #wordSet = ["inertia", "Motion (physics)", "Rest (physics)", "Physical body", "Physical law"]
        #print(len(wordSet))

        for i in range(len(wordSet)):
            wordSet[i] = urllib.parse.quote_plus(wordSet[i])
            #print(wordSet[i])

        wordPair = list(itertools.product(wordSet, repeat=2))
        #print(wordPair)

        matrix = []
        submitCode = "1503212873%7Cc452a23b0c2794e8863b9a415367cea2"

        for words in wordPair:
            a1 = words[0]
            a2 = words[1]
            if a1 == a2:
                degree = 0
                print("a1:", a1, "---", degree, "--->", "a2:", a2)
                matrix.append(degree)
                continue

            searchingUrl = "http://degreesofwikipedia.com/?a1=" + a1 + "&linktype=1&a2=" + a2 + "&skips=&submit=" + submitCode + "&currentlang=en#"
            #print(searchingUrl)
            try:
                html = urlopen(searchingUrl)
            except HTTPError as e:
                print("페이지 찾을 수 없음", e)
                break
            bsObj = BeautifulSoup(html.read(), "html.parser")
            preTag = bsObj.pre
            node_list =[]
            if preTag == None:
                degree = 999
                print("a1:", a1, "---", degree, "--->", "a2:", a2)
                matrix.append(degree)
            else:
                linkText = preTag.get_text()  # Array를 텍스트로
                nodes = re.findall(regex, linkText)  # Array로 link뽑아냄
                for node in nodes:
                    x = re.sub('>.', '', node)
                    node_list.append(x)
                All_nodes.append(node_list)
                degree = len(node_list)
                print("a1:", a1, "---", degree-1, "--->", "a2:", a2)
                matrix.append(degree-1)


        start_pos = 0
        out = []
        while (start_pos < len(matrix)):
            out.append(matrix[start_pos:start_pos + len(wordSet)])
            start_pos += len(wordSet)
        #print(out)
        return np.array(out), np.array(All_nodes)