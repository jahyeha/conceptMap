import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
import html
import wikipedia

def mapping_first_page(concept):
    # 첫번째 검색결과랑 매핑
    # in : concept
    # out : url, title

    api_base_url = 'http://en.wikipedia.org/w/api.php'
    wiki_attr = {
        'action': 'query',
        'prop': 'info',
        'format': 'json',
        'titles': concept
    }

    json_page = requests.get(api_base_url, params=wiki_attr)
    data = json_page.json()

    wiki_id = list(data['query']['pages'].keys())[0] # wiki page id ex) 1556539
    # you can use wiki_id like this "https://en.wikipedia.org/?curid=1556539"
    wiki_title = data['query']['pages'][wiki_id]['title']  # concept's wiki title ex) Newton's first law


    if wiki_id == "-1": # page does not exist
        if len(wikipedia.search(wiki_title)) == 0:
            return 0
        else:
            new_title = wikipedia.search(wiki_title)[0]
            base_url = "https://en.wikipedia.org/wiki/"
            return new_title, base_url + new_title
    else:
        base_url = "https://en.wikipedia.org/wiki/"
        url = base_url + wiki_title
        html_page = urlopen(url)
        bs_obj = BeautifulSoup(html_page, "html.parser")
        new_title = bs_obj.select("h1#firstHeading")[0].get_text()
        url = base_url + new_title
        return new_title, url

def get_urls_from_concepts(concepts):
    # 첫번째 검색결과랑 매핑
    # in : [concept1, concept2, concept3 ... ]
    # out : {'concept1':'url1', 'concept2':'url2', ....}
    concept_page_list = {}
    for concept in concepts:
        mapped_page = mapping_first_page(concept)
        if mapped_page != 0:
            title = mapped_page[0]
            url = mapped_page[1]
            concept_page_list[title] = url
    return concept_page_list


# example
url_list = get_urls_from_concepts(["Supervised regression problem", "neural network", "machine learning"])
print(url_list)
