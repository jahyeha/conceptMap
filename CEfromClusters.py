from ConceptExtraction import _conceptExtraction_ as CE
import Clustering as Clu

"""NOTE 2017-08-21 01:15  :-)
Concept Extraction from k개 Clusters
"""

playlistURL = 'https://www.youtube.com/playlist?list=PL8dPuuaLjXtN0ge7yDk_UA0ldZJdhwkoV'

C = Clu.Clustering(playlistURL)
Pre = CE.Preprocessor(playlistURL)
Con = CE.ConceptExtraction(playlistURL)

cos = C.get_cosMatrix()
Z, labels = C.Hclustering(cos)
titles = Pre.get_videoID_titles()[1]
#titles = ['{}: {}'.format(i+1, titles[i]) for i in range(len(titles))]

"""
#labels
[4 4 4 4 4 4 4 4 4 4 
 4 4 4 3 3 4 2 2 2 3 
 3 3 3 3 4 4 1 1 ..]

#titles
['Motion in a Straight Line', 'Derivatives', 'Integrals', 
 'Vectors and 2D Motion', "Newton's Laws", 'Friction', 
 'Uniform Circular Motion', 'Newtonian Gravity', 'Work, Energy, and Power',
 'Collisions', 'Rotational Motion', 'Torque', 'Statics',..]
"""

#### Get a dictionary which contains video titles that each cluster has ####
cluster_videos = {}
for i in range(len(titles)):
    if labels[i] not in cluster_videos:
        cluster_videos[labels[i]] = [(i+1, titles[i])]
    else:
        cluster_videos[labels[i]].append((i+1, titles[i]))
#print(cluster_concepts)

"""
#cluster_videos 
{1: [(27, 'Voltage, Electric Energy, and Capacitors'), (28, 'Electric Current'), 
     (29, 'DC Resistors & Batteries'), (30, 'Circuit Analysis'), ...]
 2: [(17, 'Traveling Waves'), (18, 'Sound'), (19, 'The Physics of Music'),..], ...}
"""

#### Extract "Concepts" from each cluster ####
num_concepts = 1
concepts = Con.get_Concepts(num_concepts)
#len(concepts) = 46 (the num. of video lectures)
cluster_concepts = {}

for i in range(1, len(cluster_videos)+1): # i= each cluster, 1 ~ 4
    #Video lectures of (i)th cluster
    video_list = cluster_videos[i]
    #video_list = [(27, 'Voltage, Electric Energy, and Capacitors',
    #               28, 'Electric Current',... ]
    temp = []
    for j in range(len(video_list)): #j= each video lecture in cluster(i)
        conceptList= concepts[video_list[j][0] - 1]
        temp += conceptList
    cluster_concepts[i] = set(temp) ###
print(cluster_concepts)

"""NOTE 클러스터에 속한 각 강의들로부터 (concept 추출 개수(k)에 따라) 컨셉들을 extract, =>set한 결과
#cluster_concepts 

    **num concept=3**
1: {'transformer', 'ohm', 'voltage', 'inductance', 'resistor', 'battery', 
    'electricity', 'capacitance', 'inductor', 'capacitor'}, #10

2: {'probability', 'watt', 'reflection', 'radiation', 'amplitude', 'electromagnet', 
    'quantum', 'flux', 'speed', 'diffraction', 'wavelength', 'frequency', 'pulse', 
    'wave', 'light', 'permittivity', 'interference', 'electron', 'universe', 
    'photon', 'length', 'focus', 'refraction', 'sound'}, #24

3: {'temperature', 'liquid', 'engine', 'density', 'heat', 'convection', 'pressure',
    'entropy', 'volume', 'fluid', 'thermodynamics'}, #11
    
4: {'machine', 'density', 'derivative', 'radiation', 'acceleration', 'amplitude', 
    'vector', 'circle', 'velocity', 'displacement', 'integral','momentum', 'gravity', 
    'coulomb', 'work', 'motion', 'pendulum', 'stress', 'force', 'atom', 'electron',
    'ampere', 'torque', 'energy', 'inertia', 'calculus', 'mass'} #27
####################################################################################
    **num concept=2**
1: {'voltage', 'ohm', 'capacitance', 'transformer', 'resistor', 'capacitor', 'battery', 'inductor'} #8
, 
2: {'light', 'focus', 'wavelength', 'sound', 'quantum', 'refraction', 'radiation', 'interference', 
    'universe', 'wave', 'flux', 'pulse', 'speed', 'electromagnet', 'photon', 'electron'}, #16
    
3: {'volume', 'pressure', 'density', 'liquid', 'heat', 'engine', 'fluid', 'temperature', 'entropy'},#9 

4: {'integral', 'amplitude', 'velocity', 'radiation', 'mass', 'torque', 'gravity', 'force', 'atom',
    'energy', 'electron', 'momentum', 'circle', 'motion', 'inertia', 'coulomb', 'acceleration', 
    'derivative', 'pendulum', 'machine', 'vector', 'stress'}#22
####################################################################################
    **num concept=1**
1: {'resistor', 'voltage', 'capacitor'},  #3
2: {'refraction', 'light', 'wave', 'flux', 'electron', 'sound', 'universe'}, #7
3: {'engine', 'entropy', 'pressure', 'temperature', 'heat', 'fluid'}, #6
4: {'amplitude', 'acceleration', 'energy', 'mass', 'inertia', 'coulomb', 
    'velocity', 'force', 'circle', 'momentum', 'derivative', 'integral', 'stress', 'vector'} #14

1: 20 -> 8 -> 3
2: 24 -> 16 -> 7
3: 11 -> 9 -> 6
4: 27 -> 22 -> 14
"""
#클러스터를 5개로? ## 확인하기.


"""

Updating..

"""
