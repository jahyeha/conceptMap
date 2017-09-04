"""
@author: Jahye Ha
"""
from ConceptExtraction import clustering as CL
from ConceptExtraction import conceptExtraction as CE
from ConceptExtraction import conceptMapping as CM

"""
Step 1. Extract concepts from each cluster    
Step 2. Recommend lectures based on weights 
"""
class Recommendation:
    def __init__(self):
        self.url = 'https://www.youtube.com/playlist?list=PL8dPuuaLjXtN0ge7yDk_UA0ldZJdhwkoV'
        self.Pre = CE.Preprocessor(self.url)
        self.bowSet = self.Pre._getResult()
        self.Con = CE.ConceptExtraction(self.url)
        self.Clu = CL.HClustering(self.url)
        self.titles = self.Pre._get_videoID_titles()[1]

    def _recommendLec(self, max_concept, max_weight, concept_name):
        Concept2Lec = self._linkWord2Lec(max_concept, max_weight, self.bowSet)
        res = sorted(Concept2Lec[concept_name], reverse=True)
        all_url = self.Pre._get_allURLs()
        wikiPage = CM.Mapping()._mapingConcept2Wiki(concept_name)
        result = [wikiPage]

        for i in range(len(res)):
            lecTitle = res[i][1][1]
            lecNum = res[i][1][0]
            lecUrl = all_url[lecNum-1]
            result.append(('{}: {}'.format(lecNum, lecTitle), lecUrl))

        return result


    def _linkWord2Lec(self, max_concept, max_weight, bowSet):
        playlistURL = "https://www.youtube.com/playlist?list=PL8dPuuaLjXtN0ge7yDk_UA0ldZJdhwkoV"
        Con = CE.ConceptExtraction(playlistURL)
        Pre = CE.Preprocessor(playlistURL)
        final_concept_weight = Con._get_conceptWeight(bowSet, max_concept, max_weight)
        titles = Pre._get_videoID_titles()[1]

        lec_title = {}
        # e.g. {1:'Motion in a Straight Line', 2: 'Derivatives', 3: 'Integrals',..}
        for i in range(len(titles)):
            lec_title[i+1] = titles[i]

        ConceptToLec = {}
        for i in range(len(final_concept_weight)):
            for word, val in final_concept_weight[i]:
                if word in ConceptToLec:
                    ConceptToLec[word].append((val, (i+1, lec_title[i+1])))
                else:
                    ConceptToLec[word] = [(val, (i+1, lec_title[i+1]))]
        return ConceptToLec


    def _getCluVideos(self):
        cluster_videos = {}
        cos = self.Clu._getCosMatrix()
        titles = self.titles
        Z, labels = self.Clu._Hclustering(cos, num_cluster=5)
        #H = CL.HClustering(self.url)
        #Z, labels = H._Hclustering(cos, num_cluster=5)

        for i in range(len(titles)):
            if labels[i] not in cluster_videos:
                cluster_videos[labels[i]] = [(i+1, titles[i])]
            else:
                cluster_videos[labels[i]].append((i+1, titles[i]))
        return cluster_videos


    def _cluMainConcepts(self, max_concept, max_weight):
        # 카테고리(클러스터)별 주요 개념 추출
        # e.g. clu_main_concepts == {1: ['voltmeter','resistor',..], 2: [], 3: [],..}
        main_concepts = {}
        cluster_videos = self._getCluVideos()
        lec_conceptsDic = self._lecMainConcepts(max_concept, max_weight)
        for i in range(1, len(cluster_videos) + 1):
            tempForSet = []
            for lec in cluster_videos[i]:
                lecNum = lec[0]
                tempForSet += lec_conceptsDic[lecNum]
            main_concepts[i] = list(set(tempForSet))
        return main_concepts


    def _lecMainConcepts(self, max_concept, max_weight):
        # 강의(lecture)별 주요 개념 추출, 총 46개 강의
        only_concepts = self.Con._get_onlyConcepts(self.bowSet, max_concept, max_weight)
        lec_conceptDic = {}
        for i in range(len(self.titles)):
            lec_conceptDic[i+1] = only_concepts[i]
        return lec_conceptDic
