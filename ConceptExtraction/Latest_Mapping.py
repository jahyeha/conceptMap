from bs4 import BeautifulSoup
import requests

class Mapping:
    """
    @ Mapping each concept to its Wikipedia URL
        + Updating...
    """

    def __init__(self):
        #This URL below has a list of definitions about physics
        self.wiki_url = "https://en.wikipedia.org/wiki/Glossary_of_physics#D"

    def get_page(self):
        #get the page of "Glossary of physics" and slice it
        page = requests.get(self.wiki_url)
        text = str(BeautifulSoup(page.content, 'html.parser'))
        startIdx = text.find('<h2><span class="mw-headline" id="A">')
        endIdx = text.find('<h2><span class="mw-headline" id="See_also">')
        sliced_text = text[startIdx:endIdx]
        return sliced_text

    def get_dict(self, text): #text <= sliced_text(the output of "get_page" method)
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

                #removing unnecessary part of the title(concept) such as '(physics)' in "Motion (physics)"
                if '(' in concept :
                    stopIdx = concept.find('(')
                    concept = concept[:stopIdx-1]

                wiki_dict[concept] = base_url+ path
            else:
                break

        #adding some Concept(concept name& url) that the Glossary page don't have but are important, on manual
        candidate = ['Motion (physics)', 'Mass', 'Collision', 'Gas', 'Engine', 'Metal', 'Voltage', 'Lens (anatomy)', 'Radiation']
        for word in candidate:
            full_url = base_url + '/' + word

            if '(' in word:
                stopIdx = word.find('(')
                title = word[:stopIdx - 1].lower()
                wiki_dict[title] = full_url

            wiki_dict[word] = full_url
        return wiki_dict

    def maping_Concept2Wiki(self, info_dict, concept_name):
        return info_dict[concept_name]


def main():
    """
    Updating..
    """
    mapping = Mapping()
    text = mapping.get_page()
    concept_dict = mapping.get_dict(text) #concept_dict : {concept name : URL}
    all_possible_concept = list(concept_dict.keys()) #"keys" only(all possible concept list)
    #print(all_possible_concept)
    #print(concept_dict)
    result = mapping.maping_Concept2Wiki(concept_dict, concept_name=str(input('Concept name>')))
    print(result)
    
    """
    https://en.wikipedia.org/Motion (physics) ## Error: 내일 오류고치기
    """

if __name__ == "__main__":
    main()
