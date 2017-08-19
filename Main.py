#import ExtractConcept as EX
from ConceptExtraction import _conceptExtraction_ as CE
from ConceptExtraction import conceptMapping as CM

import DefineDistanceByConcept as DD
import GetWikiFeature as GF
import MakeGraph as MG
import os


def main():
    ##################Concept Extraction##################
    originURL ="PLmhKTejvqnoOrQOcTY-pxN00BOZTGSWc3"#:로마 역사  # "PL8dPuuaLjXtN0ge7yDk_UA0ldZJdhwkoV" :물리학
    playlistURL = 'https://www.youtube.com/playlist?list='+ originURL
    print(playlistURL)
    c_extraction = CE.ConceptExtraction(playlistURL)
    defineConcept = DD.DefineDistance()
    makeGraph = MG.MakeGraph()

    testIndex = 0
    index = 1
    num_topic = 5

    Result = c_extraction.get_Concepts(num_topic)
    #print(Result)
    #######################################################
    """e.g. of Result    ## 46개 문서(강의)에 대하여 각각 5개씩 뽑힌 컨셉리스트 입니다. ##
    [['acceleration', 'velocity', 'displacement', 'motion', 'light'],
    ['derivative', 'velocity', 'calculus', 'acceleration', 'power'],
    ['integral', 'derivative', 'acceleration', 'velocity', 'displacement'],
    ['vector', 'machine', 'velocity', 'dimension', 'motion'],
    ['force', 'gravity', 'acceleration', 'mass', 'inertia'],
    ......
    ['universe', 'radiation', 'light', 'redshift', 'plasma']]
    """
    ##################Concept Mapping##################
    """
    NOTE (e.g.)
    Input(concept) : 'inertia'
    Output(URL) : https://en.wikipedia.org/wiki/Inertia
    """
    Cmap = CM.Mapping()

    ##TEST##
    print('[첫 번째 문서(강의)에 대한 컨셉-위키피디아 URL 매핑 결과]')
    for concept in Result[index]:
        URL = Cmap.maping_Concept2Wiki(concept)
        print('\t{}의 위키피디아 URL> '.format(concept), URL)

    ##URL의 고유 path name(e.g. "Motion_(physics)")을 알고 싶을 경우##
    for concept in Result[testIndex]:
        URL = Cmap.maping_Concept2Wiki(concept)
        idx = URL.find('/wiki/') + 6
        print('\t{}의 위키피디아 URL> '.format(URL[idx:]), URL)
    ##################################################

    #### NOTE ####
    #### 임시로 밑에 getConceptRelation2 파라미터-> Result[1]으로 해놓았습니다.
    #### Result[doc_num]   0 <= doc_num < 47
    print (Result[index])
    conceptRelation = defineConcept.getConceptRelation2(Result[index])
    print(conceptRelation)

    graphSource = makeGraph.py2json(Result[index], conceptRelation)
    sourceName = originURL+".json"
    sourceLoc = os.path.join("./Web/conceptproto/play/static/play/data/" +sourceName)
    print(sourceLoc)
    with open(sourceLoc, "w") as f:
        f.write(graphSource)


def testFeature(concept):
    for c in concept:
        c = c.replace("/wiki/", "")
        #print(c)
        feature = GF.GetWikiFeature(c)

        feature.getCategoriesdegree()
        feature.getIndegree()
        feature.getOutdegree()
        feature.getLanguageNum()


def testGraph():
    originURL = "PLmhKTejvqnoOrQOcTY-pxN00BOZTGSWc3"#:로마 역사  # "PL8dPuuaLjXtN0ge7yDk_UA0ldZJdhwkoV" :물리학
    playlistURL = 'https://www.youtube.com/playlist?list=' + originURL
    #c_extraction = CE.ConceptExtraction(playlistURL)
    #defineConcept = DD.DefineDistance()

    makeGraph = MG.MakeGraph()
    Result = ['derivative', 'velocity', 'calculus', 'acceleration', 'power']
    conceptRelation = [[0, 1, 1, 1, 2],
                       [2, 0, 2, 1, 2],
                       [1, 1, 0, 1, 2],
                       [1, 1, 1, 0, 1],
                       [2, 2, 2, 2, 0]]

    graphSource = makeGraph.py2json(Result, conceptRelation)
    sourceLoc = os.path.join("./Web/conceptproto/play/static/play/data/" + originURL + ".json")
    print(sourceLoc)
    with open(sourceLoc, "w") as f:
        f.write(graphSource)


if __name__ == "__main__":
    main()
    #testGraph()
