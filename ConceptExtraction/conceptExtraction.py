"""
@author: Jahye Ha
"""
import urllib
from urllib.parse import urlparse
from urllib.request import urlopen
from bs4 import BeautifulSoup
from lxml import etree
import requests

import re
import math
import nltk
# nltk.download('popular')
import operator
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

from ConceptExtraction import conceptMapping as CM


"""
@ Document Preprocessing for Concept Extraction
    1. Get all video URLs& IDs from an Education YouTube Channel(for Physics).
        ` Crash Course : https://www.youtube.com/playlist?list=PL8dPuuaLjXtN0ge7yDk_UA0ldZJdhwkoV
    2. Crawl and parse all video subtitles(documents).
    3. Clean up the documents by tokenizing and removing stop words.
    4. Use the Physics Dictionary from my module "conceptMapping" to not only easily map each concept to its Wikipedia page
       but to precisely distinguish which word is meaningful concept for Physics.
"""

class Preprocessor:

    def __init__(self, playlist_url):
        self.playlistUrl = playlist_url
        self.allUrls = self._get_allURLs()
        self.Cmap = CM.Mapping()
        self.physicsDict = self.Cmap._makeCompelteDict()
        # This list below contains all possible topics(concepts) of Physics based on Wikipedia
        self.physicsConcepts = list(self.physicsDict.keys())

    ## Get the result of Preprocessing
    def _getResult(self):
        video_IDs, titles = self._get_videoID_titles() #1#
        doc_set = self._getDocuments(video_IDs) #2#
        #bow_set = self._tokenizer(doc_set) - previous result
        bow_set = self._adv_tokenizer(doc_set) #3,4#
        return bow_set

    def _get_videoID_titles(self):
        URLs = self._get_allURLs()
        video_IDs = self._getVideoIDs(URLs)
        video_titles = self._get_videotitles()
        return video_IDs, video_titles
    #############################################################

    def _get_videotitles(self):
        URLs = self.allUrls
        video_titles = []
        for singleUrl in URLs:
            youtube = etree.HTML(urlopen(singleUrl).read())
            video_title = youtube.xpath("//span[@id='eow-title']/@title")
            title = video_title[0]

            if ':' in title:
                video_titles.append(title[:title.find(':')])
            else:
                video_titles.append(title)
        return video_titles

    def _get_allURLs(self):
        page = requests.get(self.playlistUrl)
        text = str(BeautifulSoup(page.content, 'html.parser'))
        URLs = []
        start_unique = '<td class="pl-video-title">'
        left_unique = 'href="'
        right = 0

        while True:
            start = text.find(start_unique, right)
            left = text.find(left_unique, start) + len(left_unique)
            right = text.find('"', left)

            if left >= 6 and right > left:
                candidate = text[left:right]
                URLs.append('https://www.youtube.com' + candidate)
            else:
                break
        return URLs

    def _getVideoIDs(self, URLs):
        video_IDs = []

        for url in URLs:
            url_data = urlparse(url)
            query = urllib.parse.parse_qs(url_data.query)
            video_IDs.append(query["v"][0])
        return video_IDs

    def _getDocuments(self, videoIDs):
        doc_set = []
        for ID in videoIDs:
            video_sub_url = 'http://video.google.com/timedtext?lang=en&v=' + ID
            page = requests.get(video_sub_url)
            soup = BeautifulSoup(page.content, "html.parser")
            doc = str(soup.get_text()).lower()
            doc = re.sub("[^-a-zA-Z]+", " ", doc)
            doc_set.append(doc)
        return doc_set


    ## NEW 2017-09-04 (복합명사 처리) ##
    """ Summary
        1. physics_glossary의 모든 단어들을 "singular noun"(단일명사)와 "compound noun"("2개 단어" 복합명사)로 나누기
            (physics_glossary: 위키피디아 페이지가 존재하는 Physics(물리학)의 단어 총 집합)
        2. 모든 문서(자막)에 대하여, 
            1) 토큰화 2) 모든 토큰들의 품사를 태깅 e.g.('apple', NN)
        3. 형태소 분석을 통한 심화 개념추출(기존: 단일명사만 취급, 현재: 단일& 복합명사)
    """
    def _adv_tokenizer(self, docSet):
        physics_glossary = self.physicsConcepts
        #1#
        one, two = [], []
        for word in physics_glossary:
            splitted = word.split()
            if len(splitted) == 1:
                one.append(word)
            elif len(splitted) == 2:
                two.append(word)
        #2#
        tagged_set = []
        for doc in docSet:
            tokenized = nltk.tokenize.word_tokenize(doc)
            tagged = nltk.pos_tag(tokenized)
            tagged_set.append(tagged)
        #3#
        concept_set = []
        for taggedDoc in tagged_set:
            concept_list = []

            for i in range(len(taggedDoc)-1):
                nowWord, nextWord = taggedDoc[i][0], taggedDoc[i+1][0]
                nowPos, nextPos = taggedDoc[i][1], taggedDoc[i+1][1]

                if (nowPos[0] == "J") and (nextPos[0] == "N"): ## Adj + N
                    candidate = nowWord + " " + nextWord
                    if nextPos == "NNS": # Plural Noun(-s, -es)
                        if candidate[:-2] in two:
                            concept_list.append(candidate[:-2])
                        elif candidate[:-1] in two:
                            concept_list.append(candidate[:-1])
                    elif candidate in two:  # Singular Noun
                        concept_list.append(candidate)

                elif (nowPos[0] == "N") and (nextPos[0] == "N"):  ## N + N
                    candidate = nowWord + " " + nextWord
                    if nextPos == "NNS":  # N + NNS
                        if candidate[:-2] in two:
                            concept_list.append(candidate[:-2])
                        elif candidate[:-1] in two:
                            concept_list.append(candidate[:-1])
                    elif candidate in two:  # N + N
                        concept_list.append(candidate)

                elif nowPos[0] == "N":
                    if nowPos == "NNS":
                        if candidate[:-2] in one:
                            concept_list.append(candidate[:-2])
                        elif candidate[:-1] in one:
                            concept_list.append(candidate[:-1])
                    elif nowWord in one:
                        concept_list.append(nowWord)
            concept_set.append(concept_list)

        return concept_set

    def _tokenizer(self, docSet): #previous tokenizer
        tokenizer = RegexpTokenizer(r'\w+')
        physics_glossary = self.physicsConcepts
        stop = set(stopwords.words('english'))
        bow_set = []

        for doc in docSet:
            tokens = tokenizer.tokenize(doc)
            stopped_tokens = [i for i in tokens if not i in stop and len(i) > 1]
            bow_set.append(stopped_tokens)

        filtered_bowSet = []
        for lst in bow_set:
            temp = []
            for item in lst:
                if item in physics_glossary:
                    temp.append(item)
            filtered_bowSet.append(temp)
        return filtered_bowSet


class ConceptExtraction:

    def __init__(self, playlist_url):
        self.Pre = Preprocessor(playlist_url)
        self.bowSet = self.Pre._getResult()
        self.Tfidf_result = self._runTfIdf()

    ## Get the Result of Concept Extraction
        #  Get concept names without their weights
    def _get_onlyConcepts(self, max_concept, max_weight):
        candidate_set = self._get_conceptWeight(max_concept, max_weight)
        result = []
        for lst in candidate_set:
            temp = []
            for word in lst:
                temp.append(word[0])
            result.append(temp)
        return result

    ## Get concept names with their weights
    def _get_conceptWeight(self, max_concept, max_weight):
        candidate_set = []
        tfidf = self.Tfidf_result

        for dic in tfidf:
            candidate = {}
            for word, val in dic.items():
                if dic[word] >= max_weight:
                    candidate[word] = val

            candidate = sorted(candidate.items(), key=operator.itemgetter(1), reverse=True)
            candidate_set.append(candidate[:max_concept])
        return candidate_set
    #############################################################

    """ @ Computing TF-IDF
        1. Get ready to compute tf-idf : Convert tokenized(&cleaned) BOWs into numbers 
           by creating vectors of all possible words, and for each document how many times each word appears.
        2. Compute tf(w) = (Number of times the word appears in a document) / (Total number of words in the document)
        3. Compute idf(w) = log(Number of documents / Number of documents that contain word w)
        4. Compute TF*IDF """

    def _runTfIdf(self):
        dict_set = self._createDictSet()  #1
        tf = self._computeTf(dict_set, self.bowSet) #2
        idf = self._computeIdf(dict_set) #3
        result = self._computeTfIdf(tf, idf) #4
        return result

    def _createDictSet(self):
        all_words = []
        for bow in self.bowSet:
            all_words += bow
        word_set = set(all_words)

        dict_set = []
        for i in range(len(self.bowSet)):
            word_dict = dict.fromkeys(word_set, 0)
            for bow in self.bowSet[i]:
                if bow in word_dict:
                    word_dict[bow] += 1
            dict_set.append(word_dict)
        return dict_set

    def _computeTf(self, dictSet, bowSet):
        tf_dictSet = []

        for i in range(len(dictSet)):
            tf_dict = {}
            bow_count = len(bowSet[i])

            for word, count in dictSet[i].items():
                tf_dict[word] = count / float(bow_count)
            tf_dictSet.append(tf_dict)
        return tf_dictSet

    def _computeIdf(self, dictSet):
        idf_dict = {}
        N = len(dictSet)
        idf_dict = dict.fromkeys(dictSet[0].keys(), 0)

        # Computing df
        for wordDict in dictSet:
            for word, val in wordDict.items():
                if val > 0:
                    idf_dict[word] += 1

        # Computing idf
        for word, val in idf_dict.items():
            idf_dict[word] = math.log(N / float(val))
        return idf_dict

    def _computeTfIdf(self, tfBowSet, idfs):
        tfidf_set = []
        for tfBow in tfBowSet:
            tfidf = {}
            for word, val in tfBow.items():
                result = val * idfs[word]
                tfidf[word] = round(result, 5)
            tfidf_set.append(tfidf)
        return tfidf_set


if __name__ == "__main__":
    playlistURL = "https://www.youtube.com/playlist?list=PL8dPuuaLjXtN0ge7yDk_UA0ldZJdhwkoV"
    Pre = Preprocessor(playlistURL)
    Con = ConceptExtraction(playlistURL)
    video_titles = Pre._get_videotitles()

    ############ TEST : Preprocessor ############
    pre_result = Pre._getResult()
    print('> 전처리 결과(문서추출& 토큰화& 불용어 제거)\n')
    for i in range(len(pre_result)):
        print('\t{}강 강의: {}'.format(i+1, video_titles[i]),'\n\t',pre_result[i],'\n')

    ############ TEST : ConceptExtraction #######
    max_concept, max_weight = 5, 0.07
    ce_tfidf_result = Con._runTfIdf()
    print('\n> TF-IDF 결과 (가중치 내림차순)\n')
    #print(ce_tfidf_result,'\n')
    for i in range(len(ce_tfidf_result)):
        sorted_dict = sorted(ce_tfidf_result[i].items(), key=operator.itemgetter(1),reverse=True)
        print('\t{}강 강의: {}'.format(i+1, video_titles[i]),'\n\t', sorted_dict,'\n')

    ce_result = Con._get_conceptWeight(max_concept, max_weight)
    print('\n> 개념추출 결과(TF-IDF 결과를 기반으로 추출된 개념)')
    print('\t - 조건: 가중치 0.07 이상, 강의 당 최대 개념 수 5개\n')
    for i in range(len(ce_result)):
        print('\t{}강 강의: {} (개념 수: {}개)'.format(i+1, video_titles[i], len(ce_result[i])),'\n\t',ce_result[i],'\n')

