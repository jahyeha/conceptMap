import numpy as np
import math as m
import re
import itertools
from itertools import islice, cycle
import GetWikiFeature as WF

class WikiRotion:
    def __init__(self, nodes):
        self.nodes = nodes


    def get_rocation(self):
        degree_table = []
        words = {}

        for list in self.nodes:
            tmp = []
            for node in list:
                degree_list = []
                feature = WF.GetWikiFeature(node)
                if node not in words.keys():
                    # print("@",node)
                    InDegree = feature.getIndegree()  # 밖에서 들어오는거
                    OutDegree, links = feature.getOutdegree2()  # 문서 내에서 나가는 링크
                    degree_list.append(InDegree)
                    degree_list.append(OutDegree)
                    degree_list.append(links)
                    words[node] = degree_list
                    tmp.append(degree_list)
                else:
                    # print("#", node)
                    degree_list.append(words[node][0])
                    degree_list.append(words[node][1])
                    degree_list.append(words[node][2])
                    tmp.append(degree_list)
            degree_table.append(tmp)

        # print("degree_table: ",degree_table)

        # print(words.items())

        max_in = []
        max_out = []
        for node in degree_table:
            max_in.append(max(node))
            max_out.append(max(node, key=lambda item: item[1]))

        Max_in = max(max_in)
        Max_out = max(max_out, key=lambda item: item[1])
        # print("max_in : ", Max_in[0])
        # print("max_out: ", Max_out[1])

        for list in self.nodes:
            wordPair = []
            if len(list) >= 3:
                for i in range(len(list) - 1):
                    wordPair.append(list[i:i + 2])
                print("wordPair : ", wordPair)
                for i in wordPair:
                    concept_rocation(words, i, degree_table)
            else:
                wordPair = list
                print("wordPair : ", wordPair)
                concept_rocation(words, wordPair, degree_table)


def concept_rocation(words,wordPair,degree_table):
    sub = max_sub(degree_table)
    # C(i)의 진입링크 개수
    feature_i = words[wordPair[0]]
    feature_i_in = feature_i[0]
    feature_i_out = feature_i[1]
    links_i = feature_i[2]
    print("feature_i_out : ", feature_i_out)
    Wi = get_lank([feature_i_in,feature_i_out],sub)
    print("Wi",Wi)


    # C(j)의 진입링크 개수
    feature_j = words[wordPair[1]]
    feature_j_in = feature_j[0]
    feature_j_out = feature_j[1]
    links_j = feature_j[2]
    print("feature_j_out : ", feature_j_out)
    Wj = get_lank([feature_j_in, feature_j_out], sub)
    print("wj",Wj)


    # C(i), C(j) 교집합 개수
    cap_count = 0
    for node in links_i:
        if node in links_j:
            cap_count += 1

    # (단어i가 출현하는 문서 집합)에 단어j도 출현활 확률
    Hr_ij = cap_count / feature_j_in #* Wi
    Hr_ji = cap_count / feature_i_in #* Wj

    ABS_Hr = abs(Hr_ij - Hr_ji)

    if Hr_ij > Hr_ji:
        print("상위개념 : ", wordPair[0])
        print("하위개념 : ", wordPair[1])
    else:
        print("상위개념 : ", wordPair[1])
        print("하위개념 : ", wordPair[0])

    print("Hr_ij",Hr_ij)
    print("Hr_ji",Hr_ji)
    #print("ABS_Hr",ABS_Hr)


def get_lank(key, sub):
    '''
    lank 개념은 계층적 위상관계를 결정하는 데 있어서 일반성 정도에 대한 상대적인 순위의 의미를 갖는다
    :param word: in degree와 out degreee의 리스트
    :return: 정규화된 단어들의 가중치

    만약 가중치가 높다면 일반적인 의미 낮으면 구체적인 의 일반적인 강도를 판단한다
    '''

    c_log_indegree = m.log10(key[0])
    #print("c_log_indegree",c_log_indegree)
    c_log_outdegree = m.log10(key[1])
    #print("c_log_outdegree",c_log_outdegree)
    w = (c_log_indegree - c_log_outdegree) / sub

    return w

def max_sub(degree_table):
    for list in degree_table:
        sub = []

        c_log_indegree = []
        c_log_outdegree = []
        for count in range(0, len(list)):
            #print("count : ",count)
            i = m.log10(list[count][0])
            j = m.log10(list[count][1])
            c_log_indegree.append(i)
            c_log_outdegree.append(j)
            #print("i - j : ",i - j)
            sub.append(i - j)

        max_sub = max(sub)

    return max_sub

def main():
    nodes = [['acceleration', 'velocity']]
    WR = WikiRotion(nodes)
    WR.get_rocation()

if __name__ == "__main__":
    main()
