import wikipedia

def mapping_first_page(concept):
    # 첫번째 검색결과랑 매핑
    # in : concept
    # out : url, title

    candidate = wikipedia.search(concept, results=1)
    base_url = "https://en.wikipedia.org/wiki/"
    if len(candidate) == 0:
        return 0
    else:
        mapped_page = wikipedia.page(candidate[0])
        return mapped_page.title, mapped_page.url

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
