import urllib
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests

import re
import math
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import pandas as pd


class Preprocessor:
    def __init__(self, playlist_url):
        self.playlist_url = playlist_url

    def get_result(self):
        playlist_url = self.playlist_url
        URLs = self.get_all_URLs()
        video_IDs = self.get_videoIDs(URLs)
        bow_set = self.tokenize(video_IDs)
        return bow_set

    def get_all_URLs(self):
        page = requests.get(self.playlist_url)
        text = str(BeautifulSoup(page.content, 'html.parser'))
        URLs = []
        unique = '<td class="pl-video-title">'
        right = 0

        while True:
            start = text.find(unique, right)
            left = text.find('href="', start) + 6
            right = text.find('"', left)

            if left >= 6 and right > left:
                candidate = text[left:right]
                URLs.append('https://www.youtube.com' + candidate)
            else:
                break
        return URLs

    def get_videoIDs(self, URLs):
        video_IDs = []

        for url in URLs:
            url_data = urlparse(url)
            query = urllib.parse.parse_qs(url_data.query)
            video_IDs.append(query["v"][0])
        return video_IDs

    def tokenize(self, video_IDs):
        doc_set = []
        #Importing & cleaning my documents
        for ID in video_IDs:
            video_sub_url = 'http://video.google.com/timedtext?lang=en&v=' + ID
            page = requests.get(video_sub_url)
            soup = BeautifulSoup(page.content, "html.parser")
            doc = str(soup.get_text()).lower()
            doc = re.sub("[^-a-zA-Z]+", " ", doc)
            doc_set.append(doc)

        tokenizer = RegexpTokenizer(r'\w+')
        bow_set = []

        #Tokenizing & stopwords
        for doc in doc_set:
            tokenizer.tokenize(doc)
            tokens = tokenizer.tokenize(doc)
            stop = set(stopwords.words('english'))

            stopped_tokens = [i for i in tokens if not i in stop and len(i) > 1]
            # p_stemmer = PorterStemmer
            # stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]
            bow_set.append(stopped_tokens)
        return bow_set


class ComputeTfIdf:
    def __init__(self, bow_set):
        self.bowSet = bow_set

    def RunTfIdf(self):
        DictSet = self.CreateDictSet()
        TF = self.ComputeTF(DictSet, self.bowSet)
        IDF = self.Compute_IDF(DictSet)
        result = self.Compute_TF_IDF(TF, IDF)
        return result

    def CreateDictSet(self):
        all_words = []
        for bow in self.bowSet:
            all_words += bow
        wordSet = set(all_words)

        dictSet = []
        for i in range(len(self.bowSet)):
            wordDict = dict.fromkeys(wordSet, 0)

            for bow in self.bowSet[i]:
                if bow in wordDict:
                    wordDict[bow] += 1

            dictSet.append(wordDict)
        return dictSet

    def ComputeTF(self, dictSet, bowSet):
        tfDictSet = []
        for i in range(len(dictSet)):
            tfDict = {}
            bowCount = len(bowSet[i])

            for word, count in dictSet[i].items():
                tfDict[word] = count / float(bowCount)
            tfDictSet.append(tfDict)
        return tfDictSet

    def Compute_IDF(self, dictSet):
        idfDict = {}
        N = len(dictSet)
        idfDict = dict.fromkeys(dictSet[0].keys(), 0)

        #Compute DF
        for wordDict in dictSet:
            for word, val in wordDict.items():
                if val > 0:
                    idfDict[word] += 1
        #Compute IDF
        for word, val in idfDict.items():
            idfDict[word] = math.log(N / float(val))
        return idfDict

    def Compute_TF_IDF(self, tfBowSet, idfs):
        tfidfSet = []
        for tfBow in tfBowSet:
            tfidf = {}
            for word, val in tfBow.items():
                tfidf[word] = val * idfs[word]
            tfidfSet.append(tfidf)
        return tfidfSet


def main():
    playlist_url = 'https://www.youtube.com/playlist?list=PL8dPuuaLjXtN0ge7yDk_UA0ldZJdhwkoV'
    pre = Preprocessor(playlist_url)
    preResult = pre.get_result()
    TFIDF = ComputeTfIdf(preResult)
    print(TFIDF.RunTfIdf())


if __name__ == "__main__":
    main()
