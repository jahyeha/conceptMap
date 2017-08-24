from bs4 import BeautifulSoup
import requests

"""NOTE 17-08-21
    @사전정보: 기본적으로는 2가지(Glossary of -, Outline of -)
    @Outline - 은 document slice하기 애매함 (physics와 비교한 뒤, 쓸 것인지 말 것인지 결정)

    playlistURL = 'https://www.youtube.com/playlist?list=PL8dPuuaLjXtN0ge7yDk_UA0ldZJdhwkoV'  #Physics
        - https://en.wikipedia.org/wiki/Glossary_of_physics#D
        - https://en.wikipedia.org/wiki/Outline_of_physics
        - https://en.wikipedia.org/wiki/List_of_physics_concepts_in_primary_and_secondary_education_curricula

    ############################TEST##############################
    V 8/22 테스트
    playlistURL1 = 'https://www.youtube.com/playlist?list=PL8dPuuaLjXtNdTKZkV_GiIYXpV9w4WxbX' #Ecology 
        - https://en.wikipedia.org/wiki/Glossary_of_ecology
        - https://en.wikipedia.org/wiki/Outline_of_ecology

    V 8/22 테스트
    playlistURL2 = 'https://www.youtube.com/playlist?list=PL8dPuuaLjXtPAJr1ysd5yGIyiSFuh0mIL' #Astronomy
        - https://en.wikipedia.org/wiki/Glossary_of_astronomy
        - https://en.wikipedia.org/wiki/Outline_of_astronomy
    ############################TEST##############################

    playlistURL3 = 'https://www.youtube.com/playlist?list=PL3EED4C1D684D3ADF' #biology
        - https://en.wikipedia.org/wiki/Glossary_of_biology
        - https://en.wikipedia.org/wiki/Outline_of_biology

    playlistURL4 = 'https://www.youtube.com/playlist?list=PL8dPuuaLjXtPHzzYuWy6fYEaX9mQQ8oGr' #Chemistry
        - https://en.wikipedia.org/wiki/Glossary_of_chemistry_terms 
        - https://en.wikipedia.org/wiki/Outline_of_chemistry
        - https://en.wikipedia.org/wiki/List_of_chemical_elements 원소

    V 8/22 테스트
    playlistURL5 = 'https://www.youtube.com/playlist?list=PL8dPuuaLjXtPNZwz5_o_5uirJ8gQXnhEO' #Economics
        - https://en.wikipedia.org/wiki/Glossary_of_economics
        - https://en.wikipedia.org/wiki/Outline_of_economics
"""


class Mapping:
    """
    @ linking each concept to its Wikipedia URL
    """
    def __init__(self):
        self.dictionary = self.make_compelteDict()

    def maping_Concept2Wiki(self, concept_name):
        return self.dictionary[concept_name]

    def make_compelteDict(self):
        temp_dict = self.read_base_info()
        dictSet_lst = self.make_dicts(temp_dict)
        combined_dict = self.combine_dicts(dictSet_lst)
        return combined_dict

    #####################################################
    """NOTE 17-08-22 new+ (TEMP)"""

    def temp_get_dict(self, subject_name):
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

    #####################################################
    def read_base_info(self):
        ## Read a text file that contains Wikipedia pages which have information(list of Concepts) about Physics.
        # e.g. url_set = [url1, url2, url3], startEnd_set = [[start1, end1], [start2, end2], [start3, end3]]
        num_pages = 3
        ###info_set 변경해야함###
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

    def make_dicts(self, baseInfo_dict):
        # input: a temporary dictionary that has only URLs info.  e.g. {url1 :[start1, end1],..}
        # output: a list containing three dictionaries  e.g. [{WordUrl_dict1}, {WordUrl_dict2}, {WordUrl_dict3}]

        urls = list(baseInfo_dict.keys())
        dictSet_lst = []

        for i in range(len(urls)):
            start, end = baseInfo_dict[urls[i]]
            text = self.get_page_doc(urls[i], start, end)
            wordUrl_dict = self.make_WordUrl_dict(text)
            dictSet_lst.append(wordUrl_dict)
        return dictSet_lst

    def combine_dicts(self, dict_set):
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

    ###############################################################################
    def get_page_doc(self, URL, start, end):
        ## Get the Wikipedia page(from input URL) and slice the document extracted from the page
        # start, end : input string that can be distinguished as starting&ending point to slice the Wikipedia page(document)
        page = requests.get(URL)
        text = str(BeautifulSoup(page.content, 'html.parser'))
        startIdx = text.find(start)
        endIdx = text.find(end)
        sliced_text = text[startIdx:endIdx]
        return sliced_text

    def make_WordUrl_dict(self, text):
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


def main():
    print('Running..')
    ##################TEST##################
    map = Mapping()
    concept_name = input('Concept Name>')
    print(map.maping_Concept2Wiki(concept_name))
    ########################################


if __name__ == "__main__":
    ##################TEST##################
    ## CC- Astronomy
    M1 = Mapping()
    temp_res1 = M1.temp_get_dict('astronomy')
    result1 = M1.make_dicts(temp_res1)
    # e.g. result1= [ {'zenith': 'https://en.wikipedia.org/wiki/Zenith','sun': 'https://en.wikipedia.org/wiki/Sun',..} ]
    print('Astronomy\n\t', result1)
    print(len(result1[0]))  # 160
    print('--------------------------------------')

    M2 = Mapping()
    temp_res2 = M2.temp_get_dict('economics')
    result2 = M2.make_dicts(temp_res2)
    print('Economics\n\t', result2)
    print(len(result2[0]))  # 208
    ########################################