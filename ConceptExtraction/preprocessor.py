import urllib
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests

import re
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer


class Preprocessor:
    def __init__(self, playlist_url):
        self.playlist_url = playlist_url

    def get_all_URLs(self):
        page = requests.get(playlist_url)
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
        
        ## Importing & cleaning my documents ##
        for ID in video_IDs:
            video_sub_url = 'http://video.google.com/timedtext?lang=en&v=' + ID
            page = requests.get(video_sub_url)
            soup = BeautifulSoup(page.content, "html.parser")
            doc = str(soup.get_text()).lower()
            doc = re.sub("[^-a-zA-Z]+", " ", doc)
            doc_set.append(doc)

        tokenizer = RegexpTokenizer(r'\w+')
        bow_set = []

        ## Tokenizing & stopwords ##
        for doc in doc_set:
            tokenizer.tokenize(doc)
            tokens = tokenizer.tokenize(doc)
            stop = set(stopwords.words('english'))

            stopped_tokens = [i for i in tokens if not i in stop and len(i) > 1]
            # p_stemmer = PorterStemmer
            # stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]
            bow_set.append(stopped_tokens)
        return bow_set
