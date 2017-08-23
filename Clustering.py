from ConceptExtraction import _conceptExtraction_ as CE
import operator
import numpy as np

from sklearn.metrics.pairwise import cosine_similarity
from scipy.cluster.hierarchy import ward, dendrogram, fcluster
import matplotlib.pyplot as plt

"""NOTE 17-08-24 04:00
메인이랑 연결해야함. _conceptExtraction_.py 에 get_concept_only -> 메인의 getConcept 틀림
강의별 개념추출할 때도 weight 커트라인(max_weight)& max_concept을 정해서 추출할건지?
-> 결정 후, Main.py line 23 수정, _conceptExtraction_.py & main() COMMIT
"""
##############################
# 카테고리(클러스터)별 개념추출 #
##############################
class ConceptFromCluster:
    def __init__(self):
        self.playlist_url = 'https://www.youtube.com/playlist?list=PL8dPuuaLjXtN0ge7yDk_UA0ldZJdhwkoV'
        self.Clu = Clustering(self.playlist_url)
        self.Pre = CE.Preprocessor(self.playlist_url)
        self.Con = CE.ConceptExtraction(self.playlist_url)
        self.cos = self.Clu.get_cosMatrix()
        self.Z, labels = self.Clu.Hclustering(self.cos, num_cluster=5)
        self.titles = self.Pre.get_video_title(self.playlist_url)[1]

        """
        # labels
            = [4 4 4 4 4 4 4 4 4 4 4 4 4 3 3 4 2 2 2 3,..] 
        # titles 
            = ['Motion in a Straight Line', 'Derivatives', 'Integrals', 
                'Vectors and 2D Motion',"Newton's Laws", 'Friction'..]
        """

    def get_clu_concept(self, max_concept, max_weight):
        clu_main_concepts = {}
        clu_videos = self.get_clu_videos()
        lec_concepts_dic = self.get_conceptByweight(max_concept, max_weight)
        for i in range(1, len(clu_videos) + 1):
            temp_for_set = []
            for lec in clu_videos[i]:
                lec_num = lec[0]
                temp_for_set += lec_concepts_dic[lec_num]
            clu_main_concepts[i] = list(set(temp_for_set))
        return clu_main_concepts
    #########################################################################

    def get_clu_videos(self):
        clu_videos = {}
        for i in range(len(self.titles)):
            if labels[i] not in clu_videos:
                clu_videos[labels[i]] = [(i + 1, self.titles[i])]
            else:
                clu_videos[labels[i]].append((i + 1, self.titles[i]))
        return clu_videos

    """clu_videos
    {1: [(27, 'Voltage, Electric Energy, and Capacitors'), (28, 'Electric Current'), 
         (29, 'DC Resistors & Batteries'), (30, 'Circuit Analysis'), ...], 2: [..], ..}"""

    def get_conceptByweight(self, max_concept, max_weight):
        #max_concept = 5, max_weight = 0.1
        #concepts = self.Con.get_concept_weight(max_concept,max_weight)
        only_concepts = self.Con.get_only_concepts(max_concept, max_weight)
        """only_concepts
        [['acceleration', 'velocity', 'displacement'],  #1st lecture's Concepts
        ['derivative', 'velocity', 'calculus', 'acceleration'], #2nd
        ['integral', 'derivative', 'acceleration', 'velocity'], #3rd ..
        """
        lec_concepets_dic = {}
        for i in range(len(self.titles)):
            lec_concepets_dic[i+1] = only_concepts[i]

        """lec_concepts_dic
        {1 : ['acceleration', 'velocity', 'displacement'], 
         2 : ['derivative', 'velocity', 'calculus', 'acceleration'],..}
        """
        return lec_concepets_dic


class Clustering:
    def __init__(self, playlistURL):
        self.playlist_url = playlistURL
        self.Pre = CE.Preprocessor(self.playlist_url)      #module1
        self.all_urls = self.Pre.get_all_URLs()
        self.video_titles = self.Pre.get_video_title(self.all_urls)

        self.Con = CE.ConceptExtraction(self.playlist_url) #module2
        self.dict_set = self.Con.create_dictSet()

    def get_cosMatrix(self):
        num_concept = 5
        tfidf_dicSet = self.get_tfidf_result(num_concept)
        cosine = self.cosine_similarity(tfidf_dicSet)
        return cosine
        ##########################################################################

    def get_tfidf_result(self, num_concept):
        sorted_dictSet = [sorted(dic.items(), key=operator.itemgetter(1), reverse=True) for dic in self.dict_set]
        BOW_result = [dic[:num_concept] for dic in sorted_dictSet]
            # BOW_result = [[('acceleration',30), ('velocity',28),..],['pressure',41),.."num_concept" 만큼],..]
        Tfidf_dicSet = self.Con.run_TfIdf()
            # Tfidf_dictSet = [{'motion':0.0, 'capacitor':0.15, 'mass':0.0},
            #                  {'motion':0.35, 'capacitor':0.0, 'mass':0.01}..]
        return Tfidf_dicSet

    def cosine_similarity(self,Tfidf_dicSet):
        tfidf_weights = np.array([list(dict.values()) for dict in Tfidf_dicSet])
        """ NOTE #shape is (46, 122) == (doc num, word num)
            e.g.
                      w1(weight)    w2  ...   w122
             doc1 [[      0.        0.  ...    0.2   ],
             doc2  [      0.1       0.  ...    0.8   ],
             ...          ..            ...
             doc46 [      0.        0.  ...    0.    ]]"""

        cos = cosine_similarity(tfidf_weights)
        """ NOTE #shape is (46, 46), "doc-doc similarity"
            e.g.
                  doc1    doc2    doc3  ...  doc46
            doc1   1      0.95    0.451      0.095
            doc2            1
            doc3                    1
            ...                         ...
            doc46                              1   """
        return cos

    def Hclustering(self, cos, num_cluster):
        dist = 1 - cos
        #linkage_matrix = hier.linkage(dist, method='single')  #singleprint(Z, labels)-linkage
        linkage_matrix = ward(dist)
        cluster_id = fcluster(linkage_matrix, num_cluster, criterion='maxclust')
        #print(cluster_id)
        return linkage_matrix, cluster_id

    def plot_clusters(self, Z, labels):
        ##### Plotting #####
        video_titles = self.video_titles
        titles = ['{}: {}'.format(i+1, video_titles[i]) for i in range(len(video_titles))]

        dflt_col = "#808080"
        #if num_clusters > 5, this below has to be changed(adding colors)
        assign_col = {1: "#58C9B9", 2: "#A593E0", 3: "#566270", 4: "#e94e77",5: "#4f953b"}
        D_leaf_colors = {}

        for i in range(len(titles)):
            D_leaf_colors[titles[i]] = assign_col[labels[i]]

        link_cols = {}
        for i, i12 in enumerate(Z[:, :2].astype(int)):
            c1, c2 = (link_cols[x] if x > len(Z) else D_leaf_colors["{}: ".format(x+1)+video_titles[x]] for x in i12)
            link_cols[i + 1 + len(Z)] = c1 if c1 == c2 else dflt_col

        ax = dendrogram(Z=Z,
                        orientation="left",
                        labels=titles,
                        link_color_func=lambda x: link_cols[x],
                        leaf_font_size=8.,
                        show_leaf_counts=4)

        plt.tick_params(
            axis='x',
            which='both',
            bottom='on',
            top='on',
            labelbottom='on')

        plt.tight_layout()
        plt.savefig('ward_clusters.png', dpi=200)
        plt.show()


if __name__ == "__main__":
    playlistURL = 'https://www.youtube.com/playlist?list=PL8dPuuaLjXtN0ge7yDk_UA0ldZJdhwkoV'
    C = Clustering(playlistURL)
    cos = C.get_cosMatrix()
    num_cluster = 5 #color : max = 5
    Z, labels = C.Hclustering(cos, num_cluster)
    #print(Z, '\n', labels)
    C.plot_clusters(Z, labels)

    ########TEST 08/24########
    CC = ConceptFromCluster()
    max_concept = 5
    max_weight = 0.1
    result = CC.get_clu_concept(max_concept, max_weight)
    clu_main_concepts = CC.get_clu_concept(max_concept, max_weight)
    for i in range(1, len(clu_main_concepts) + 1):
        print('{}번 카테고리 주요개념 ({}개)\n\t'.format(i, len(clu_main_concepts[i])), clu_main_concepts[i])
