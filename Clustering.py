from ConceptExtraction import _conceptExtraction_ as CE
import operator
import numpy as np

from sklearn.metrics.pairwise import cosine_similarity
from scipy.cluster.hierarchy import ward, dendrogram
import matplotlib.pyplot as plt

"""
Updating..
"""

class Clustering():
    def __init__(self):
        self.playlistURL = 'https://www.youtube.com/playlist?list=PL8dPuuaLjXtN0ge7yDk_UA0ldZJdhwkoV'
        self.Pre = CE.Preprocessor(self.playlistURL)
        self.all_urls = self.Pre.get_all_URLs()
        self.video_titles = self.Pre.get_videoTitle(self.all_urls)

    def test(self):
        tfidf_dicSet = self.get_data()
        cosine = self.cosine_similarity(tfidf_dicSet)
        Hcluster = self.clustering(cosine)
        return Hcluster
        ##########################################################################

    def get_data(self):
        #Importing ConceptExtraction module from CE to get TF-IDF(concept extraction) result
        num_concept = 5
        Con = CE.ConceptExtraction(self.playlistURL)
        dict_set = Con.create_dictSet()
        sorted_dictSet = [sorted(dic.items(), key=operator.itemgetter(1), reverse=True) for dic in dict_set]
        BOW_result = [dic[:num_concept] for dic in sorted_dictSet]
        # BOW_result = [[('acceleration',30), ('velocity',28),..],['pressure',41),..],..]
        Tfidf_dicSet = Con.run_TfIdf()
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

    def clustering(self, cos):
        ##### Updating.. #####
        dist = 1 - cos ## 0에 가까울 수록 similarity UP
        linkage_matrix = ward(dist)

        ## Plotting.. ##
        vt = self.video_titles
        titles = ['{}: {}'.format(i+1, vt[i]) for i in range(len(vt))]

        fig, ax = plt.subplots()
        ax = dendrogram(linkage_matrix, orientation="left", labels=titles)

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
    c.test()