from ConceptExtraction import conceptExtraction as CE
from ConceptExtraction import conceptMapping as CM
from ConceptExtraction import clustering as CL
from ConceptExtraction import recommendation as RC

# TEST #

""" Process
    1. Preprocessing(전처리)
        - 필요한 문서(강의 자막)추출, 문서의 토큰화& 형태소 분석 및 불용어제거

    2. Concept Extraction(개념추출) : 문서에서 개념추출
        - 각 문서(강의)별로 해당 강의에서 중요한 개념을 추출(각 문서에서 가중치가 높은 단어추출)
        - 알고리즘 : TF-IDF(Term Frequency Inverse Document Frequency)
        
    3. Clustering(Categorization)
        - 문서(강의)별 유사도를 구해 비슷한 강의들끼리 군집(카테고리)생성
        - 알고리즘 : Hierarchical Clustering
      
    4. Recommendation : 카테고리에서 개념추출& 강의추천
        - 3번 군집화 결과를 기반, 군집(카테고리)별로 개념추출& 모르는 개념에 대한 정보제공"""


#### Base Information (YouTube Crash Course -"Physics")
playlist_url = "https://www.youtube.com/playlist?list=PL8dPuuaLjXtN0ge7yDk_UA0ldZJdhwkoV"


#### 1.Preprocessing ####
'''
parameters
    1) urls: playlist 내에 존재하는 모든 비디오 강의 URLs
    2) ids: 비디오강의들의 고유 IDs
    3) docs: 각 비디오강의들의 자막들(문서)
    4) *bows: 토큰화 및 형태소 분석으로 불용어를 제거한 결과(*전처리 결과)
'''

Pre = CE.Preprocessor(playlist_url)
urls = Pre._get_allURLs()
ids = Pre._getVideoIDs(urls)
docs = Pre._getDocuments(ids)
bows = Pre._adv_tokenizer(docs)

print('\n\n1. Preprocessing 결과..')
# 1)urls
print('\n1) urls>\n', urls)
# 2)ids
print('\n2) ids>\n', ids)
# 3)docs
print('\n3) docs[0]>\n', docs[0])
# 4)bows
print('\n4) bows[0]>\n', bows[0])


#### 2.Concept Extraction ####
'''
parameters
    1) dicSet: Term-Document Dictionary(각 문서의 "Term Frequency" 계산 결과)
    2) tfidf: TF-IDF 알고리즘을 계산한 최종 결과
    3) *getConcept: 개념추출 결과
        - 조건: 가중치(weight) 0.07 이상, 강의 별 최대 컨셉 수 5개
'''

Con = CE.ConceptExtraction(playlist_url)
lecMaxConcept, lecMaxWeight = 5, 0.07
bowSet = Pre._getResult()

dictSet = Con._createDictSet(bowSet)
tfidf = Con._runTfIdf(bowSet)
getConcept = Con._get_conceptWeight(bowSet, lecMaxConcept, lecMaxWeight)

print('\n\n2. Concept Extraction 결과..')
# 1)dicSet
print('\n1) dicSet[0]>\n', dictSet[0])
# 2)tfidf
print('\n2) tfidf[0]>\n', tfidf[0])
# 3)getConcept
print('\n1) getConcept[0]>\n', getConcept[0])


#### 3.Clustering(Categorizing) ####
'''
parameters
    1) cos: TF-IDF Matrix(가중치)를 가지고, 강의(문서)별 유사도(Cosine Similarity)를 구한 결과
    2) Hierarchical Clustering(계층적 군집화)
        2-1) Z: 계층적 군집화 결과 (linkage matrix, 문서별 거리측정: ward distance)
        2-2) labels: 각 문서가 어느 군집에 속하는지에 대한 레이블
    3) *plot: 계층적 군집화 결과의 시각화
'''

H = CL.HClustering(playlist_url)
cos = H._getCosMatrix()
Z, labels = H._Hclustering(cos, num_cluster=5)
plot = H._plotClusters(Z, labels)

print('\n\n3. Clustering(Categorization) 결과..')
# 1)cos
print('\n1) cos>\n', cos)
# 2)Z
print('\n2) Z>\n', Z)
# 3)labels
print('\n3) labels>\n', labels)
#print(plot)


#### 4.Recommendation ####
'''
parameters
    1) clusterVideos: 각 군집에 속하는 강의들의 집합
    2) clusterConcepts: 카테고리에서 개념추출(군집 또는 카테고리를 대표하는 개념)
    3) *recommendLec: 모르는 개념에 대한 정보제공
                    (해당 개념의 위키피디아 페이지& 가중치를 기반으로 해당 개념과 가장 유사한 강의추천)
'''

R = RC.Recommendation()
clusterVideos = R._getCluVideos()
cluMaxConcept, cluMaxWeight = 4, 0.1

clusterConcepts = R._cluMainConcepts(cluMaxConcept, cluMaxWeight)
conceptName = "integral"
recommendLec = R._recommendLec(cluMaxConcept, cluMaxWeight, conceptName)

print('\n\n4. Recommendation 결과..')
# 1) clusterVideos
print('\n1) clusterVideos>\n', clusterVideos)
# 2) clusterConcepts
print('\n2) clusterConcepts>\n', clusterConcepts)
# 3) recommendLec
print('\n3) recommendLec>\n', recommendLec)