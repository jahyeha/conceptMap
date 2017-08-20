from ConceptExtraction import _conceptExtraction_ as CE
import operator
import numpy as np

from sklearn.metrics.pairwise import cosine_similarity
from scipy.cluster.hierarchy import ward, dendrogram, fcluster
import matplotlib.pyplot as plt


class Clustering():
    def __init__(self):
        self.playlistURL = 'https://www.youtube.com/playlist?list=PL8dPuuaLjXtN0ge7yDk_UA0ldZJdhwkoV'
        self.Pre = CE.Preprocessor(self.playlistURL)      #module1
        self.all_urls = self.Pre.get_all_URLs()
        self.video_titles = self.Pre.get_videoTitle(self.all_urls)
        self.Con = CE.ConceptExtraction(self.playlistURL) #module2
        self.dict_set = self.Con.create_dictSet()

    def get_cosMatrix(self):
        tfidf_dicSet = self.get_tfidf_result()
        cosine = self.cosine_similarity(tfidf_dicSet)
        return cosine
        ##########################################################################

    def get_tfidf_result(self):
        ##Importing ConceptExtraction module from CE to get TF-IDF(concept extraction) result
        num_concept = 5
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

    def Hclustering(self, cos):
        dist = 1 - cos
        #linkage_matrix = hier.linkage(dist, method='single')  #single-linkage
        linkage_matrix = ward(dist)
        num_cluster = 4
        cluster_id = fcluster(linkage_matrix, num_cluster, criterion='maxclust')
        #print(cluster_id)

        ### Plotting ###
        title_name = self.video_titles
        titles = ['{}: {}'.format(i+1, title_name[i]) for i in range(len(title_name))]

        dflt_col = "#808080"
        assign_col = {1: "#1b9e77", 2: "#FFD041", 3: "#6E9ECF", 4: "#6A60A9"}
        D_leaf_colors = {}

        for i in range(len(titles)):
            D_leaf_colors[titles[i]] = assign_col[cluster_id[i]]

        link_cols = {}
        for i, i12 in enumerate(linkage_matrix[:, :2].astype(int)):
            c1, c2 = (link_cols[x] if x > len(linkage_matrix) else D_leaf_colors["{}: ".format(x+1)+title_name[x]] for x in i12)
            link_cols[i + 1 + len(linkage_matrix)] = c1 if c1 == c2 else dflt_col

        ax = dendrogram(Z=linkage_matrix,
                        orientation="left",
                        labels=titles,
                        link_color_func=lambda x: link_cols[x],
                        leaf_font_size=9.,
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
    c = Clustering()
    cos = c.get_cosMatrix()
    c.Hclustering(cos)