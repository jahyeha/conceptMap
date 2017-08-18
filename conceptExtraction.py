import urllib
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests

import re
import math
import nltk
# nltk.download('popular')
import operator
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from ConceptExtraction import conceptMapping


class Preprocessor:
    """
    @"Document Preprocessing" for Concept Extraction
        1. Get all video URLs& IDs from an Education YouTube Channel(for Physics).
        2. Crawl and parse all video subtitles(documents).
        3. Clean up the documents by tokenizing, stemming& removing stop words.
        +++
        4. Use the Physics Dictionary from my module "conceptMapping" to not only easily map each concept to its Wikipedia page
            but to precisely distinguish which word is meaningful concept for Physics.
    """

    def __init__(self, playlist_url):
        self.playlist_url = playlist_url
        ## Import 'conceptMapping' Class(module) to get my Physics dictionary
        self.Cmap = conceptMapping.Mapping()
        self.physicsDict = self.Cmap.make_compelteDict()
        # this list below contains all possible topics(concepts) of Physics based on Wikipedia
        self.physicsConcepts = list(self.physicsDict.keys())

    def get_result(self):
        playlist_url = self.playlist_url
        URLs = self.get_all_URLs()
        video_IDs = self.get_videoIDs(URLs)
        doc_set = self.get_documents(video_IDs)
        bow_set = self.tokenize(doc_set, self.physicsConcepts)
        return bow_set
    ###########################################################

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

    def get_documents(self, videoIDs):
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

    def tokenize(self, docSet, conceptLst):
        # Tokenizing& removing stopwords
        tokenizer = RegexpTokenizer(r'\w+')
        bow_set = []
        stop = set(stopwords.words('english'))
        # (X) all_eng_words = words.words()

        physics_glossary = conceptLst

        for doc in docSet:
            tokens = tokenizer.tokenize(doc)
            stopped_tokens = [i for i in tokens if not i in stop and len(i) > 1]
            bow_set.append(stopped_tokens)

        # (X) Applying POS tagging to extract all Nouns & Checking English spelling
        # (X) tagged = [nltk.pos_tag(bow) for bow in bow_set]
        filtered_bowSet = []
        for lst in bow_set:
            temp = []
            for item in lst:
                if item in physics_glossary:
                    temp.append(item)
            filtered_bowSet.append(temp)
        return filtered_bowSet


class ConceptExtraction:  # ConputeTfIdf->ConceptExtraction
    def __init__(self, playlist_url):
        self.Pre = Preprocessor(playlist_url)
        self.bowSet = self.Pre.get_result()
        self.Tfidf_result = self.run_TfIdf()

    def get_Concepts(self, num_concept):
        # input: tfidf(the result of run_TfIdf)
        candidate_set = []
        tfidf = self.Tfidf_result

        for dic in tfidf:
            candidate = {}
            for word, val in dic.items():
                if dic[word] != 0:
                    candidate[word] = val
            candidate = sorted(candidate.items(), key=operator.itemgetter(1), reverse=True)
            candidate_set.append(candidate[:num_concept])

        """candidate_set  => CONCEPT NAME with its WEIGHT
        [[('acceleration', 0.2855), ('velocity', 0.15526), ('displacement', 0.15062), ('motion', 0.0354),
          ('light', 0.03002)],
         [('derivative', 0.54908), ('velocity', 0.12148), ('calculus', 0.11439), ('acceleration', 0.11037),
          ('power', 0.05717)],
         [('integral', 0.41838), ('derivative', 0.26713), ('acceleration', 0.23131), ('velocity', 0.11552),
          ('displacement', 0.0523)]..]
        """
        #### ONLY GET CONCEPT NAMES without their weights ####
        RESULT = []
        for lst in candidate_set:
            temp = []
            for word in lst:
                temp.append(word[0])
            RESULT.append(temp)
        return RESULT
    ################################################################################
    """
    @Computing TF-IDF
        1. Get ready to compute tf-idf
         : Convert tokenized(&cleaned) BOWs into numbers by creating vectors of all possible words,
           and for each document how many times each word appears.
        2. Compute tf*idf
          2-1) Compute tf(w) = (Number of times the word appears in a document) / (Total number of words in the document)
          2-2) Compute idf(w) = log(Number of documents / Number of documents that contain word w)
    """

    def run_TfIdf(self):
        dict_set = self.create_dictSet()
        tf = self.compute_Tf(dict_set, self.bowSet)
        idf = self.compute_Idf(dict_set)
        result = self.compute_TfIdf(tf, idf)
        return result

    def create_dictSet(self):
        all_words = []
        for bow in self.bowSet:
            all_words += bow
        word_set = set(all_words)
        # print('\nword_set>\n\t', word_set)

        dict_set = []
        for i in range(len(self.bowSet)):
            word_dict = dict.fromkeys(word_set, 0)
            for bow in self.bowSet[i]:
                if bow in word_dict:
                    word_dict[bow] += 1
            dict_set.append(word_dict)
        return dict_set

    def compute_Tf(self, dictSet, bowSet):
        tf_dictSet = []

        for i in range(len(dictSet)):
            tf_dict = {}
            bow_count = len(bowSet[i])

            for word, count in dictSet[i].items():
                tf_dict[word] = count / float(bow_count)
            tf_dictSet.append(tf_dict)
        return tf_dictSet

    def compute_Idf(self, dictSet):
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

    def compute_TfIdf(self, tfBowSet, idfs):
        tfidf_set = []
        for tfBow in tfBowSet:
            tfidf = {}
            for word, val in tfBow.items():
                result = val * idfs[word]
                tfidf[word] = round(result, 5)
            tfidf_set.append(tfidf)
        return tfidf_set
        ######################################################


def main():
    ############### Get the result ###############
    playlistURL = 'https://www.youtube.com/playlist?list=PL8dPuuaLjXtN0ge7yDk_UA0ldZJdhwkoV'
    Cextract = ConceptExtraction(playlistURL)  # OBJECT

    ### 1. Result of BOW(Bag of Words) /before applying TF-IDF ###
    num_topic = 5
    dictSet = Cextract.create_dictSet()
    sorted_dictSet = [sorted(dic.items(), key=operator.itemgetter(1), reverse=True) for dic in dictSet]
    BOW_result = [dic[:num_topic] for dic in sorted_dictSet]
    # print(BOW_result)

    ### 2. Result of applying TF-IDF ###
    Tfidf_result = Cextract.get_Concepts(num_topic)
    # [[('concept1 of first doc', weight),('concept2', weight)..,[('concept1 of second doc', weight)..],..]
    print(Tfidf_result, '\n')

    ################### TEST ###################
    """
    num_doc = len(Tfidf_result)

    print("###The Result of Concept to Wikipedia Mapping###")
    for i in range(num_doc):
        print("\nDocument {}".format(i+1))
        for concept in Tfidf_result[i]:
            url = physicsDict[concept[0]]
            print('\t',concept[0],'>', url)"""

    """
    print('###The Result of Topic Extraction###')
    for i in range(len(Tfidf_result)):
        print(' {}번 째 문서'.format(i+1))
        print('\tBOW   >', BOW_result[i])
        print('\tTF-IDF>', Tfidf_result[i],'\n')"""
    ############################################


if __name__ == "__main__":
    main()
