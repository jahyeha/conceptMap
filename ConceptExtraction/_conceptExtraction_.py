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
from ConceptExtraction import _conceptMapping_ as CM


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
        self.Cmap = CM.Mapping()
        self.physicsDict = self.Cmap.make_compelteDict()
        # this list below contains all possible topics(concepts) of Physics based on Wikipedia
        self.physicsConcepts = list(self.physicsDict.keys())

    def get_result(self):
        video_IDs, titles = self.get_videoID_titles()
        doc_set = self.get_documents(video_IDs)
        bow_set = self.tokenizer(doc_set)
        filtered_bowSet = self.adv_tokenizer(bow_set, self.physicsConcepts)
        return filtered_bowSet

    #############################################################
    #17-08-22 03:05 new+
    def temp_get_result(self, subject_name):
        video_IDs, titles = self.get_videoID_titles()
        doc_set = self.get_documents(video_IDs)
        bow_set = self.tokenizer(doc_set)
        temp_conceptList = self.temp_matching_dict(subject_name)
        filtered_bowSet = self.adv_tokenizer(bow_set, temp_conceptList)
        return filtered_bowSet

    #NOTE 17-08-22 02:50 new+ (TEMP)
    def temp_matching_dict(self, subject_name):
        if subject_name == "physics":
            return self.physicsConcepts

        else:
            temp = self.Cmap.temp_get_dict(subject_name)
            res_dict = self.Cmap.make_dicts(temp)[0]
            return list(res_dict.keys())
        # [motion, power, electricity, zenith,...]
    #############################################################

    """NOTE 2017-08-20 new+ """
    def get_videoID_titles(self):
        playlist_url = self.playlist_url
        URLs = self.get_all_URLs()
        video_IDs = self.get_videoIDs(URLs)
        video_titles = self.get_video_title(URLs)
        return video_IDs, video_titles
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
    #####################################################################
    """NOTE 17-08-20 new+ (Optional)"""
    def get_video_title(self, URLs):
        #Input: a list which contains all video URLs from the input playlist (page)
        #Output: a list of titles from the videos(lectures)
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

    def tokenizer(self, docSet):
        # Tokenizing& removing stopwords
        tokenizer = RegexpTokenizer(r'\w+')
        bow_set = []
        stop = set(stopwords.words('english'))

        for doc in docSet:
            tokens = tokenizer.tokenize(doc)
            stopped_tokens = [i for i in tokens if not i in stop and len(i) > 1]
            bow_set.append(stopped_tokens)
        """
        bow_set = [['want', 'video', 'istalk', 'difference', 'vectors',..],
                   ['direction', 'talking', 'velocity', 'talking',..],...]
        """
        return bow_set

    """
    NOTE 17-08-22 new+ 
    """
    def adv_tokenizer(self, bowSet, concept_list):
        physics_glossary = concept_list
        filtered_bowSet = []

        for lst in bowSet:
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

    ##########(기존) k만큼 컨셉 뽑기##########
    def get_Kconcept(self, num_concept):
        candidate_set = []
        tfidf = self.Tfidf_result

        for dic in tfidf:
            candidate = {}
            for word, val in dic.items():
                if dic[word] != 0:
                    candidate[word] = val
            candidate = sorted(candidate.items(), key=operator.itemgetter(1), reverse=True)
            candidate_set.append(candidate[:num_concept])

        result = []
        for lst in candidate_set:
            temp = []
            for word in lst:
                temp.append(word[0])
            result.append(temp)
        return result
        ########################################

    def get_only_concepts(self, max_concept, max_weight):
        #### ONLY GET CONCEPT NAMES without their weights ####
        candidate_set = self.get_concept_weight(max_concept, max_weight)
        result = []

        for lst in candidate_set:
            temp = []
            for word in lst:
                temp.append(word[0])
            result.append(temp)

            """
            [['acceleration', 'velocity', 'displacement', 'motion', 'light'], 
            ['derivative', 'velocity', 'calculus', 'acceleration', 'power'], 
            ['integral', 'derivative', 'acceleration', 'velocity', 'displacement'], 
            ['vector', 'machine', 'velocity', 'dimension', 'motion'], 
            ['force', 'gravity', 'acceleration', 'mass', 'inertia'],...] 
            """
        return result

    def get_concept_weight(self, max_concept, max_weight): #parameter num_concepts 삭제
        # input: tfidf(the result of run_TfIdf)
        # 가중치(일정 가중치 이상의 단어)와 최대 컨셉 개수를 고려하여 개념 추출
        candidate_set = []
        tfidf = self.Tfidf_result

        for dic in tfidf: # dic: each lecture
            candidate = {}
            for word, val in dic.items():
                # if dic[word] != 0:  NOTE 수정이전(수정일시 17-08-23)
                # max_weight 이상인 단어만 candidate에 추가
                if dic[word] >= max_weight:
                    candidate[word] = val

            ## candidate : {'motion': 0.7(weight), 'power': 0.3,..}
            candidate = sorted(candidate.items(), key=operator.itemgetter(1), reverse=True)
            ## candidate(after sorted) : [('motion', 0.7), ('power', 0.3),..]

            #candidate_set.append(candidate[:num_concept])
            #하나의 강의에 대해 끝났으면, 가중치로 내림차순으로 정렬된 상태에서
            #max_concept만큼 슬라이스해서 candidate_set에 추가합니다.
            candidate_set.append(candidate[:max_concept])

        """candidate_set  => CONCEPT NAME with its WEIGHT
        [[('acceleration', 0.2855), ('velocity', 0.15526), ('displacement', 0.15062), ('motion', 0.0354),
          ('light', 0.03002)],
         [('derivative', 0.54908), ('velocity', 0.12148), ('calculus', 0.11439), ('acceleration', 0.11037),
          ('power', 0.05717)],
         [('integral', 0.41838), ('derivative', 0.26713), ('acceleration', 0.23131), ('velocity', 0.11552),
          ('displacement', 0.0523)]..]
        """
        return candidate_set

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
    #Physics
    playlistURL = "https://www.youtube.com/playlist?list=PL8dPuuaLjXtN0ge7yDk_UA0ldZJdhwkoV"
    Pre = Preprocessor(playlistURL)
    URLs = Pre.get_all_URLs()
    #print(URLs)
    #print(Pre.get_videoID_titles())
    IDs = Pre.get_videoIDs(URLs)
    doc = Pre.get_documents(IDs)
    #print(Pre.tokenizer(doc))

    Con = ConceptExtraction(playlistURL)
    #print(Con.get_concept_weight(5))
    max_concept, max_weight = 5, 0.08 #카테고리에서 컨셉 뽑는 것과 가중치 다름
    final_concept = Con.get_only_concepts(max_concept, max_weight)
    #for i in range(len(final_concept)):
        #print('{}번 강의의 컨셉({}개) : '.format(i+1, len(final_concept[i])), final_concept[i])

    ########TEST 08-24 (기존 컨셉추출 방법)
    temp_res = Con.get_Kconcept(num_concept=5)
    for x in temp_res:
        print(x)

        """
        1번 강의의 컨셉(3개) :  ['acceleration', 'velocity', 'displacement']
        2번 강의의 컨셉(4개) :  ['derivative', 'velocity', 'calculus', 'acceleration']
        3번 강의의 컨셉(4개) :  ['integral', 'derivative', 'acceleration', 'velocity']
        4번 강의의 컨셉(4개) :  ['vector', 'machine', 'velocity', 'dimension']
        5번 강의의 컨셉(5개) :  ['force', 'gravity', 'acceleration', 'mass', 'inertia']
        6번 강의의 컨셉(3개) :  ['force', 'gravity', 'acceleration']
        7번 강의의 컨셉(2개) :  ['circle', 'acceleration']
        8번 강의의 컨셉(4개) :  ['acceleration', 'gravity', 'mass', 'force']
        9번 강의의 컨셉(2개) :  ['energy', 'pendulum']
        10번 강의의 컨셉(3개) :  ['momentum', 'mass', 'pendulum']
        11번 강의의 컨셉(4개) :  ['velocity', 'motion', 'circle', 'acceleration']
        12번 강의의 컨셉(5개) :  ['inertia', 'torque', 'mass', 'energy', 'momentum']
        13번 강의의 컨셉(5개) :  ['stress', 'torque', 'force', 'statics', 'length']
        14번 강의의 컨셉(5개) :  ['pressure', 'fluid', 'density', 'volume', 'force']
        15번 강의의 컨셉(5개) :  ['fluid', 'density', 'pressure', 'viscosity', 'volume']
        16번 강의의 컨셉(4개) :  ['amplitude', 'motion', 'energy', 'frequency']
        17번 강의의 컨셉(5개) :  ['wave', 'pulse', 'amplitude', 'crest', 'sound']
        18번 강의의 컨셉(5개) :  ['sound', 'wave', 'watt', 'pressure', 'decibel']
        19번 강의의 컨셉(4개) :  ['wave', 'wavelength', 'frequency', 'sound']
        20번 강의의 컨셉(5개) :  ['temperature', 'volume', 'pressure', 'kelvin', 'length']
        21번 강의의 컨셉(4개) :  ['temperature', 'liquid', 'pressure', 'kelvin']
        22번 강의의 컨셉(5개) :  ['heat', 'temperature', 'convection', 'phase', 'radiation']
        23번 강의의 컨셉(5개) :  ['entropy', 'heat', 'thermodynamics', 'volume', 'temperature']
        24번 강의의 컨셉(3개) :  ['engine', 'heat', 'temperature']
        25번 강의의 컨셉(5개) :  ['coulomb', 'electron', 'atom', 'force', 'ground']
        26번 강의의 컨셉(2개) :  ['coulomb', 'force']
        27번 강의의 컨셉(5개) :  ['capacitor', 'capacitance', 'voltage', 'energy', 'dielectric']
        28번 강의의 컨셉(5개) :  ['voltage', 'ohm', 'battery', 'power', 'light']
        29번 강의의 컨셉(5개) :  ['voltage', 'battery', 'ohm', 'resistor', 'light']
        30번 강의의 컨셉(4개) :  ['resistor', 'ohm', 'voltage', 'voltmeter']
        31번 강의의 컨셉(5개) :  ['voltage', 'capacitor', 'capacitance', 'battery', 'resistor']
        32번 강의의 컨셉(5개) :  ['force', 'radiation', 'vector', 'magnetism', 'tesla']
        33번 강의의 컨셉(3개) :  ['circle', 'integral', 'ampere']
        34번 강의의 컨셉(1개) :  ['flux']
        35번 강의의 컨셉(5개) :  ['voltage', 'transformer', 'electricity', 'inductance', 'flux']
        36번 강의의 컨셉(4개) :  ['voltage', 'inductor', 'inductance', 'flux']
        37번 강의의 컨셉(5개) :  ['flux', 'wave', 'permittivity', 'density', 'energy']
        38번 강의의 컨셉(4개) :  ['refraction', 'light', 'reflection', 'length']
        39번 강의의 컨셉(5개) :  ['wave', 'light', 'diffraction', 'interference', 'wavelength']
        40번 강의의 컨셉(5개) :  ['light', 'interference', 'wave', 'diffraction', 'phase']
        41번 강의의 컨셉(3개) :  ['light', 'focus', 'diffraction']
        42번 강의의 컨셉(3개) :  ['light', 'speed', 'length']
        43번 강의의 컨셉(5개) :  ['light', 'photon', 'wave', 'energy', 'frequency']
        44번 강의의 컨셉(5개) :  ['electron', 'quantum', 'probability', 'momentum', 'wavelength']
        45번 강의의 컨셉(5개) :  ['mass', 'atom', 'energy', 'proton', 'electron']
        46번 강의의 컨셉(5개) :  ['universe', 'radiation', 'light', 'redshift', 'plasma']
        """

if __name__ == "__main__":
    main()