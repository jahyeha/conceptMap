from bs4 import BeautifulSoup
import requests


class Mapping:
    """
    @ Mapping each concept to its Wikipedia URL
        + Updating...
    """
    
    def __init__(self):
        self.result = []

    def maping_Concept2Wiki(self, dictionary, concept_name):
        return dictionary[concept_name]

    def make_compelteDict(self):
        temp_dict = self.read_base_info()
        dictSet_lst = self.make_dicts(temp_dict)
        combined_dict= self.combine_dicts(dictSet_lst)
        return combined_dict

    
    def read_base_info(self):  #4
        ## Read a text file that contains Wikipedia pages which have information(list of Concepts) about Physics.
         # e.g. url_set = [url1, url2, url3], startEnd_set = [[start1, end1], [start2, end2], [start3, end3]]
         
        num_pages = 3
        info_set = open('info.txt').read().split('\n')
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

                #Removing unnecessary part of the title(concept) -such as '(physics)' in "Motion (physics)"
                if '(' in concept :
                    stopIdx = concept.find('(')
                    concept = concept[:stopIdx-1]
                    wiki_dict[concept] = base_url+ path

                wiki_dict[concept] = base_url+ path
            else:
                break
        return wiki_dict


def main():
    mapping = Mapping()
    dictionary = mapping.make_compelteDict()
    concept_name = input('Concept Name>')
    print(mapping.maping_Concept2Wiki(dictionary, concept_name))


if __name__ == "__main__":
    main()
