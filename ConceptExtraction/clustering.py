"""
@author: Jahye Ha
"""
import operator
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from scipy.cluster.hierarchy import ward, dendrogram, fcluster
import matplotlib.pyplot as plt

from ConceptExtraction import conceptExtraction as CE


class HClustering:

    def __init__(self, playlistURL):
        self.playlist_url = playlistURL
        self.Pre = CE.Preprocessor(self.playlist_url)      #module1
        self.video_titles = self.Pre._get_videotitles()
        self.Con = CE.ConceptExtraction(self.playlist_url) #module2
        self.bowSet = self.Pre._getResult()
        self.dict_set = self.Con._createDictSet(self.bowSet)

    def _Hclustering(self, cos, num_cluster):
        dist = 1 - cos
        #linkage_matrix = hier.linkage(dist, method='single')  #singleprint(Z, labels)-linkage
        linkage_matrix = ward(dist)
        cluster_id = fcluster(linkage_matrix, num_cluster, criterion='maxclust')
        return linkage_matrix, cluster_id

    def _getCosMatrix(self):
        num_concept = 5
        tfidf_dicSet = self._getTfidfResult(num_concept, self.bowSet)
        cosine = self._cosineSimilarity(tfidf_dicSet)
        return cosine
        ##########################################################################

    def _getTfidfResult(self, num_concept, bowSet):
        sorted_dictSet = [sorted(dic.items(), key=operator.itemgetter(1), reverse=True) for dic in self.dict_set]
        BOW_result = [dic[:num_concept] for dic in sorted_dictSet]
        Tfidf_dicSet = self.Con._runTfIdf(bowSet)
        return Tfidf_dicSet

    def _cosineSimilarity(self,Tfidf_dicSet):
        tfidf_weights = np.array([list(dict.values()) for dict in Tfidf_dicSet])
        return cosine_similarity(tfidf_weights)

    def _plotClusters(self, Z, labels):
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