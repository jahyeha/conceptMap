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
2. Crawl and parse all video subtitles(documents).
3. Clean up the documents by tokenizing and removing stop words.
4. Use the Physics Dictionary from my module "conceptMapping" to not only easily map each concept to its Wikipedia page
   but to precisely distinguish which word is meaningful concept for Physics.
"""

class Preprocessor:

    def __init__(self, playlist_url):
        self.playlist_url = playlist_url
        ## Import 'conceptMapping' Class(module) to get my Physics dictionary
        self.Cmap = CM.Mapping()
        self.physicsDict = self.Cmap._makeCompelteDict()
        # this list below contains all possible topics(concepts) of Physics based on Wikipedia
        self.physicsConcepts = list(self.physicsDict.keys())

    def _getResult(self):
        video_IDs, titles = self._get_videoID_titles()
        doc_set = self._getDocuments(video_IDs)
        bow_set = self._tokenizer(doc_set, self.physicsConcepts)
        return bow_set

    def _get_videoID_titles(self):
        playlist_url = self.playlist_url
        URLs = self._get_allURLs()
        video_IDs = self._getVideoIDs(URLs)
        video_titles = self._get_videotitles(URLs)
        return video_IDs, video_titles

    def _get_videotitles(self, URLs):
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
    #####################################################################

    def _get_allURLs(self):
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

    def _getVideoIDs(self, URLs):
        video_IDs = []

        for url in URLs:
            url_data = urlparse(url)
            query = urllib.parse.parse_qs(url_data.query)
            video_IDs.append(query["v"][0])
        return video_IDs

    def _getDocuments(self, videoIDs):
        doc_set = []
        # Importing & cleaning my documents
        for ID in videoIDs:
            video_sub_url = 'http://video.google.com/timedtext?lang=en&v=' + ID
            page = requests.get(video_sub_url)
            soup = BeautifulSoup(page.content, "html.parser")
            doc = str(soup.get_text()).lower()
            doc = re.sub("[^-a-zA-Z]+", " ", doc)
            doc_set.append(doc)
        return doc_set

    def _tokenizer(self, docSet, physics_glossary):
        # Tokenizing& removing stopwords
        tokenizer = RegexpTokenizer(r'\w+')
        bow_set = []
        stop = set(stopwords.words('english'))
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

    def _get_onlyConcepts(self, max_concept, max_weight):
        #### ONLY GET CONCEPT NAMES without their weights ####
        candidate_set = self._get_conceptWeight(max_concept, max_weight)
        result = []
        for lst in candidate_set:
            temp = []
            for word in lst:
                temp.append(word[0])
            result.append(temp)

            """result (e.g.)
            [['acceleration', 'velocity', 'displacement', 'motion', 'light'], 
             ['derivative', 'velocity', 'calculus', 'acceleration', 'power'], 
             ['integral', 'derivative', 'acceleration', 'velocity', 'displacement'], 
             ['vector', 'machine', 'velocity', 'dimension', 'motion'], 
             ['force', 'gravity', 'acceleration', 'mass', 'inertia'],...]"""
        return result

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

        """candidate_set(e.g.) : concept name with its weight
        [[('acceleration', 0.2855), ('velocity', 0.15526), ('displacement', 0.15062), ('motion', 0.0354), ('light', 0.03002)],
         [('derivative', 0.54908), ('velocity', 0.12148), ('calculus', 0.11439), ('acceleration', 0.11037), ('power', 0.05717)],
         [('integral', 0.41838), ('derivative', 0.26713), ('acceleration', 0.23131), ('velocity', 0.11552), ('displacement', 0.0523)]..]
        """
        return candidate_set

    ################################################################################
    """ NOTE
      @ Computing TF-IDF
        1. Get ready to compute tf-idf
         : Convert tokenized(&cleaned) BOWs into numbers by creating vectors of all possible words,
           and for each document how many times each word appears.
        2. Compute tf*idf
          2-1) Compute tf(w) = (Number of times the word appears in a document) / (Total number of words in the document)
          2-2) Compute idf(w) = log(Number of documents / Number of documents that contain word w)
    """

    def _runTfIdf(self):
        dict_set = self._createDictSet()
        tf = self._computeTf(dict_set, self.bowSet)
        idf = self._computeIdf(dict_set)
        result = self._computeTfIdf(tf, idf)
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
    URLs = Pre._get_allURLs()
    # print(URLs)
    print(Pre._get_videotitles(URLs))