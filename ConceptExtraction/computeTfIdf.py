import urllib
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests

import re
import math
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import pandas as pd


class Preprocessor:
    """
    @Document preprocessing for computing TF-IDF
        1. Get all video URLs& IDs from an Education YouTube Channel(for Physics).
        2. Crawl and parse all video subtitles(documents).
        3. Clean up the documents by tokenizing, stemming& removing stop words.
    """

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

        #Tokenizing, Stemming & Removing stopwords
        for doc in doc_set:
            tokenizer.tokenize(doc)
            tokens = tokenizer.tokenize(doc)
            stop = set(stopwords.words('english'))

            stopped_tokens = [i for i in tokens if not i in stop and len(i) > 1]

        ''' stemming/ lemmatizing -- output is inaccurate!
            1. stemmer
            #p_stemmer = nltk.PorterStemmer()
            #stemmed = [p_stemmer.stem(token) for token in stopped_tokens]
            #bow_set.append(stemmed)

            2. lemmatizer
            #lemma = nltk.WordNetLemmatizer()
            #lemmatized = [lemma.lemmatize(token) for token in stopped_tokens]
            #bow_set.append(lemmatized)'''

            bow_set.append(stopped_tokens)
        return bow_set


class ComputeTfIdf:
    """
    @Computing TF-IDF
        1. Get ready to compute tf-idf
            . Convert tokenized(&cleaned) BOWs into numbers by creating vectors of all possible words, and for each document how many times each word appears.

        2. Compute tf-idf
            . Compute tf(w) = (Number of times the word appears in a document) / (Total number of words in the document)
            . Compute idf(w) = log(Number of documents / Number of documents that contain word w)
    """

    def __init__(self, bow_set):
        self.bowSet = bow_set

    def run_TfIdf(self):
        dict_set = self.create_dictSet()
        tf = self.compute_TF(dict_set, self.bowSet)
        idf = self.compute_IDF(dict_set)
        result = self.computeTF_IDF(tf, idf)
        return result

    def create_dictSet(self):
        all_words = []
        for bow in self.bowSet:
            all_words += bow
        word_set = set(all_words)

        dictSet = []
        for i in range(len(self.bowSet)):
            word_dict = dict.fromkeys(word_set, 0)

            for bow in self.bowSet[i]:
                if bow in word_dict:
                    word_dict[bow] += 1

            dictSet.append(word_dict)
        return dictSet

    def compute_TF(self, dictSet, bowSet):
        tf_dictSet = []

        for i in range(len(dictSet)):
            tf_dict = {}
            bow_count = len(bowSet[i])

            for word, count in dictSet[i].items():
                tf_dict[word] = count / float(bow_count)
            tf_dictSet.append(tf_dict)
        return tf_dictSet

    def compute_IDF(self, dictSet):
        idf_dict = {}
        N = len(dictSet)
        idf_dict = dict.fromkeys(dictSet[0].keys(), 0)

        #Computing df
        for wordDict in dictSet:
            for word, val in wordDict.items():
                if val > 0:
                    idf_dict[word] += 1

        #Computing idf
        for word, val in idf_dict.items():
            idf_dict[word] = math.log(N / float(val))
        return idf_dict

    def computeTF_IDF(self, tfBowSet, idfs):
        tfidf_set = []
        for tfBow in tfBowSet:
            tfidf = {}
            for word, val in tfBow.items():
                tfidf[word] = val * idfs[word]
            tfidf_set.append(tfidf)
        return tfidf_set


def main():
    playlist_url = input('playlist URL>').strip()
    #test URL : https://www.youtube.com/playlist?list=PL8dPuuaLjXtN0ge7yDk_UA0ldZJdhwkoV
    pre = Preprocessor(playlist_url)
    preResult = pre.get_result()
    TfIdf = ComputeTfIdf(preResult)
    Run_TfIdf = TfIdf.run_TfIdf()
    print(pd.DataFrame(Run_TfIdf))

if __name__ == "__main__":
    main()
