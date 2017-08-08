from urllib.request import urlopen

import itertools
from bs4 import BeautifulSoup
import re
import queue

class DefineDistance :
        # A페이지 -> B페이지 의 거리degree를 구하는 함수 및 wordset안에서 거리 구하는 코드
        # get_def_links(page_url)함수
        # 위키 링크를 받아서 그 페이지의 첫 번째 문단에 존재하는 링크들을 리스트에 담아 리턴함
        # 입력 : page_url(위키 페이지 링크)를 받음
        # 리턴 : page_url의 첫번째 문단에 존재하는 링크들을 links리스트에 담아 리턴함
    def getConceptRelation(self, word_list):
        # print(wordSet)
        word_pair = list(itertools.permutations(word_list, 2))
        for i in word_pair:
            print(i)
        degrees = dict()
        limit_degree = 2
        for a, b in word_pair:
            degrees[(a, b)] = self.bfs_search(a, b, limit_degree)
        for k in degrees.keys():
            print(k[0], " --->", k[1], degrees[k])
            # 이 아래로 그래프 그리는 부분
        return degrees


    def get_def_links(self,page_url):
        html = urlopen("https://en.wikipedia.org" + page_url)
        bs = BeautifulSoup(html, "html.parser")
        links = set()
        try:
            first_p = bs.find(id="mw-content-text").find_all("p")[0]
        except AttributeError:
            print("First <p> doesn't exist.")
        else:
            for link in first_p.find_all("a", href=re.compile("^(/wiki/)")):
                # print(link)
                links.add(link.attrs["href"])
        return links

    # bfs_search(start_url, end_url, limit_degree)함수
    # start_url로부터 end_url로 가는 거리를 구해 리턴함. 거리가 limit_degree를 넘을 경우 999를 넣고 중단
    # 입력 : start_url은 시작페이지 링크, end_url은 목표페이지 링크, limit_degree최대 거리
    # 리턴 : start_url에서 end_url로 가는 거리degree를 리턴함. limit_degree이상인 경우 999를 리턴
    #
    def bfs_search(self,start_url, end_url, limit_degree):
        # 함수 내의 print문들은 확인을 위해서 썼습니다. 안쓰는 경우 주석처리
        # print(">>>> 최초 탐색", start_url, "에서 ", end_url, "까지", limit_degree, "안에 가기")

        curr_degree = 1  # start_url애서 start_url로 가는 거리를 1로 설정
        q = queue.Queue()  # start_url의 이웃 링크를 저장할 큐 생성
        q.put(start_url)  # 큐에 start_url의 넣음
        while not q.empty():  # 큐가 비어있지 않은 동안 bfs로(visited체크는 안함) 탐색
            if curr_degree >= limit_degree:  # limit보다 현재 degree가 크다면 999리턴
                # print(curr_degree, ">=", limit_degree, "이므로 리턴 999")
                return 999
            current_url = q.get()  # 방문할 url을 current_url에 넣음(맨 처음엔 start_url이 나옴)
            # print("현재링크 : ", current_url)
            neighbor_links = self.get_def_links(current_url)  # current_url의 이웃 링크들을 리스트로 받음
            # print("현재링크의 이웃링크들 : ", len(neighbor_links), neighbor_links)
            if end_url not in neighbor_links:  # current_url의 이웃 링크 중 목적지인 end_url이 없는 경우
                # print("찾는 링크 없음.")
                # 이웃 중에 찾는 링크가 없다면 각각을 큐에 넣고 다시 반복해야함
                curr_degree += 1  # degree도 1 증가
                # current_url과 인접한 링크 중 방문하지 않은 곳에 전부 방문해야하므로 큐에 넣음
                for link in neighbor_links:
                    q.put(link)
            else:  # current_url의 이웃 링크 중 목적지인 end_url이 있는 경우
                # print(">>>>>>> 링크 찾음. 거리 : ", curr_degree)
                # 찾는 링크를 찾았다면 현재 거리 리턴
                return curr_degree
