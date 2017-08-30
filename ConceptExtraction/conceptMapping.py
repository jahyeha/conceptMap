"""
@author: Jahye Ha
"""
from bs4 import BeautifulSoup
import requests

""" 
Mapping(Linking) Class that links each concept to its Wikipedia page 
e.g. inertia -> https://en.wikipedia.org/wiki/Inertia
@sources: Glossary of Physics & Outline of Physics (wikipedia pages)
"""

class Mapping:
    def __init__(self):
        self.dictionary = self._makeCompelteDict()

    def _mapingConcept2Wiki(self, concept_name):
        return self.dictionary[concept_name]

    def _makeCompelteDict(self):
        temp_dict = self._readBaseInfo()
        dictSet_lst = self._makeDicts(temp_dict)
        combined_dict = self._combineDicts(dictSet_lst)
        return combined_dict

    def _readBaseInfo(self):
        ## Read a text file that contains Wikipedia pages which have information(list of Concepts) about Physics.
        # e.g. url_set = [url1, url2, url3], startEnd_set = [[start1, end1], [start2, end2], [start3, end3]]
        num_pages = 3
        info_set = ['https://en.wikipedia.org/wiki/Glossary_of_physics#D',
                    'https://en.wikipedia.org/wiki/Outline_of_physics',
                    'https://en.wikipedia.org/wiki/List_of_physics_concepts_in_primary_and_secondary_education_curricula',
                    '<h2><span class="mw-headline" id="A">', '<h2><span class="mw-headline" id="See_also">',
                    '<table class="wikitable">', '<h3><span class="mw-headline" id="Concepts_by_field">',
                    '<h2><span class="mw-headline" id="Motion_and_forces">',
                    '<h2><span class="mw-headline" id="See_also">']

        url_set = info_set[:num_pages]
        startEnd = info_set[num_pages:]

        startEnd_set = []
        for i in range(0, len(startEnd), 2):
            startEnd_set.append([startEnd[i], startEnd[i + 1]])

        ## Make a temporary dictionary that has only URLs(&distinguishable starting&ending point) info.
        # e.g. temp_dict = {url1 :[start1, end1],..}
        temp_dict = {}
        for i in range(len(url_set)):
            temp_dict[url_set[i]] = startEnd_set[i]
        return temp_dict

    def _makeDicts(self, baseInfo_dict):
        # input: a temporary dictionary that has only URLs info.  e.g. {url1 :[start1, end1],..}
        # output: a list containing three dictionaries  e.g. [{WordUrl_dict1}, {WordUrl_dict2}, {WordUrl_dict3}]

        urls = list(baseInfo_dict.keys())
        dictSet_lst = []

        for i in range(len(urls)):
            start, end = baseInfo_dict[urls[i]]
            text = self._getPageDoc(urls[i], start, end)
            wordUrl_dict = self._makeWord2Url(text)
            dictSet_lst.append(wordUrl_dict)
        return dictSet_lst

    def _combineDicts(self, dict_set):
        ## Combine a base dictionary with the others
        # input: a list containing three dictionaries
        # output: one base dictionary combined with the others

        base_dict = dict_set[0]
        for i in range(1, len(dict_set)):
            word_set = list(dict_set[i].keys())
            for word in word_set:
                if word not in base_dict:
                    base_dict[word] = dict_set[i][word]
        return base_dict

    def _getPageDoc(self, URL, start, end):
        ## Get the Wikipedia page(from input URL) and slice the document extracted from the page
        # start, end : input string that can be distinguished as starting&ending point to slice the Wikipedia page(document)
        page = requests.get(URL)
        text = str(BeautifulSoup(page.content, 'html.parser'))
        startIdx = text.find(start)
        endIdx = text.find(end)
        sliced_text = text[startIdx:endIdx]
        return sliced_text

    def _makeWord2Url(self, text):
        wiki_dict = {}
        # wiki_dict : {title : url}
        # e.g.  {'motion' : https://en.wikipedia.org/wiki/Motion, 'inertia': https://en.wikipedia.org/wiki/Inertia, ..}
        base_url = 'https://en.wikipedia.org'
        right = 0

        while True:
            left = text.find('<a href="/wiki/', right) + 9
            right = text.find('"', left)

            if left >= 9 and right > left:
                path = text[left:right]
                start = text.find('title="', right) + 7
                end = text.find('"', start)
                concept = text[start:end].lower()

                # Removing unnecessary part of the title(concept) -such as '(physics)' in "Motion (physics)"
                if '(' in concept:
                    stopIdx = concept.find('(')
                    concept = concept[:stopIdx - 1]
                    wiki_dict[concept] = base_url + path

                wiki_dict[concept] = base_url + path
            else:
                break
        return wiki_dict

    """ for other subjects(Astronomy, economics, etc.)
    def _tempGetDict(self, subject_name):
        # pos = {페이지 특징 이름 : [start, end]}
        pos = {'glossary': ['<h2><span class="mw-headline" id="A">', '<h2><span class="mw-headline" id="See_also">'],
               'outline': ['<table class="wikitable">', '<h3><span class="mw-headline" id="Concepts_by_field">'],
               'other': ['<h2><span class="mw-headline" id="Motion_and_forces">',
                         '<h2><span class="mw-headline" id="See_also">']}

        base_url = 'https://en.wikipedia.org/wiki/'
        subject_url = {'astronomy': base_url + 'Glossary_of_astronomy',
                       'economics': base_url + 'Glossary_of_economics'}
        url = subject_url[subject_name]
        base_info_dict = {url: pos['glossary']}
        return base_info_dict
    """

if __name__ == "__main__":
    print('Running..')
    ##################TEST##################
    map = Mapping()
    concept_name = input('Concept Name>')
    print(map._mapingConcept2Wiki(concept_name))
    ########################################