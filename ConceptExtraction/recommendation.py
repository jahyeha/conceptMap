"""
@author: Jahye Ha
"""
from clustering import HClustering
from ConceptExtraction import conceptExtraction as CE

""" NOTE
    Step 1. Extract concepts from each cluster    
    Step 2. Recommend lectures based on weights """
class Recommendation:
    def __init__(self):
        self.url = 'https://www.youtube.com/playlist?list=PL8dPuuaLjXtN0ge7yDk_UA0ldZJdhwkoV'
        self.Pre = CE.Preprocessor(self.url)
        self.Con = CE.ConceptExtraction(self.url)
        self.Clu = HClustering(self.url)
        self.titles = self.Pre._get_videoID_titles()[1]

    def _recommendLec(self, max_concept, max_weight, concept_name):
        Concept2Lec = self._linkWord2Lec(max_concept, max_weight)
        #print(Concept2Lec)

        """ Concept2Lec (e.g.)
        {'universe': [(0.30756, '46: Astrophysics and Cosmology')], 
         'vector': [(0.58311, '4: Vectors and 2D Motion'), (0.10636, '32: Magnetism')], 
         'interference': [(0.15056, '39: Light Is Waves'), (0.24237, '40: Spectra Interference')],..
        """
        return sorted(Concept2Lec[concept_name], reverse=True)


    def _linkWord2Lec(self, max_concept, max_weight):
        playlistURL = "https://www.youtube.com/playlist?list=PL8dPuuaLjXtN0ge7yDk_UA0ldZJdhwkoV"
        Con = CE.ConceptExtraction(playlistURL)
        Pre = CE.Preprocessor(playlistURL)
        final_concept_weight = Con._get_conceptWeight(max_concept, max_weight)
        titles = Pre._get_videoID_titles()[1]

        lec_title = {}
        # e.g. {1:'Motion in a Straight Line', 2: 'Derivatives', 3: 'Integrals',..}
        for i in range(len(titles)):
            lec_title[i+1] = titles[i]

        ConceptToLec = {}
        for i in range(len(final_concept_weight)):
            for word, val in final_concept_weight[i]:
                if word in ConceptToLec:
                    ConceptToLec[word].append((val, '{}: {}'.format(i+1, lec_title[i+1]))) #강의번호는 +1 해줘야함
                else:
                    ConceptToLec[word] = [(val, '{}: {}'.format(i+1, lec_title[i+1]))]
        return ConceptToLec

    def _getCluVideos(self):
        cluster_videos = {}
        cos = self.Clu._getCosMatrix()
        titles = self.titles
        Z, labels = HClustering._Hclustering(cos, num_cluster=5)

        for i in range(len(titles)):
            if labels[i] not in cluster_videos:
                cluster_videos[labels[i]] = [(i+1, titles[i])]
            else:
                cluster_videos[labels[i]].append((i+1, titles[i]))
        return cluster_videos
    """cluster_videos (e.g.)
        {1: [(27, 'Voltage, Electric Energy, and Capacitors'), (28, 'Electric Current'), 
             (29, 'DC Resistors & Batteries'), (30, 'Circuit Analysis'), ...], 2: [..], ..}"""

    def _cluMainConcepts(self, max_concept, max_weight):
        # NOTE 카테고리(클러스터)별 주요 개념 추출
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

    """ Main concepts from each cluster (total 5 clusters, max concept(of each cluster): 5, max weight: 0.1)
    {1: ['battery', 'transformer', 'flux', 'voltmeter', 'voltage', 'resistor', 'energy', 'electricity', 'inductor', 'capacitor', 'capacitance', 'ohm', 'inductance'], 
     2: ['pressure', 'flux', 'probability', 'frequency', 'momentum', 'wave', 'watt', 'interference', 'universe', 'plasma', 'permittivity', 'wavelength', 'crest', 'radiation', 'density', 'pulse', 'reflection', 'speed', 'redshift', 'photon', 'diffraction', 'electron', 'refraction', 'focus', 'light', 'energy', 'sound', 'quantum', 'amplitude'], 
     3: ['pressure', 'density', 'entropy', 'thermodynamics', 'heat', 'fluid', 'liquid', 'volume', 'kelvin', 'viscosity', 'convection', 'engine', 'temperature'], 
     4: ['circle', 'velocity', 'calculus', 'derivative', 'integral', 'motion', 'acceleration', 'displacement'], 
     5: ['amplitude', 'radiation', 'vector', 'velocity', 'inertia', 'magnetism', 'atom', 'torque', 'electron', 'machine', 'mass', 'force', 'proton', 'energy', 'motion', 'stress', 'momentum', 'acceleration', 'coulomb', 'gravity']}
    """

    def _lecMainConcepts(self, max_concept, max_weight):
        # NOTE 강의(lecture)별 주요 개념 추출, 총 46개 강의
        only_concepts = self.Con._get_onlyConcepts(max_concept, max_weight)
        """only_concepts
        [['acceleration', 'velocity', 'displacement'],          #1st lecture's Concepts
        ['derivative', 'velocity', 'calculus', 'acceleration'], #2nd
        ['integral', 'derivative', 'acceleration', 'velocity'], #3rd ..
        """
        lec_conceptDic = {}
        for i in range(len(self.titles)):
            lec_conceptDic[i+1] = only_concepts[i]
        """lec_conceptDic
        {1 : ['acceleration', 'velocity', 'displacement'], 
         2 : ['derivative', 'velocity', 'calculus', 'acceleration'],..}
        """
        return lec_conceptDic



if __name__ == "__main__":
    max_concept = 5
    max_weight = 0.1
    concept_name = 'torque'
    #print(recommendLec(max_concept, max_weight, concept_name))
    RE = Recommendation()
    #################TEST#################
    #print(RE._cluMainConcepts(max_concept, max_weight))
    #print(RE._lecMainConcepts(max_concept, max_weight))
    #print(RE._getCluVideos())
    print(RE._recommendLec(max_concept, max_weight, concept_name))

