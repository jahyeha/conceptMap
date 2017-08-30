#import ExtractConcept as EX
from ConceptExtraction import conceptExtraction as CE
from ConceptExtraction import conceptMapping as CM

import DefineDistanceByConcept as DD
import GetWikiFeature as GF
import wikiRocation as WR
import MakeGraph as MG
import os


def main():
    ##################Concept Extraction##################
    originURL = "PL8dPuuaLjXtN0ge7yDk_UA0ldZJdhwkoV"
    playlistURL = 'https://www.youtube.com/playlist?list=' + originURL
    submitCode = "1503382656%7Ce5c72339e330f6814ae2fe97aa5c6301"
    defineConcept = DD.DefineDistance(submitCode)
    makeGraph = MG.MakeGraph()

    num_concept = 6
    playlist_url = 'https://www.youtube.com/playlist?list=PL8dPuuaLjXtN0ge7yDk_UA0ldZJdhwkoV'
    Con = CE.ConceptExtraction(playlist_url)
    max_concept, max_weight = 5, 0.08  
    Result = Con._get_onlyConcepts(max_concept, max_weight)
    print(Result) #가중치 적용 결과
    origins = Con.Pre.get_all_URLs()
    print(Con.Pre.get_all_URLs())

    ##################Concept Mapping##################
    """
    NOTE (e.g.)
    Input(concept) : 'inertia'
    Output(URL) : https://en.wikipedia.org/wiki/Inertia
    """
    Cmap = CM.Mapping()

    '''
    ###TEST###
    print('[첫 번째 문서(강의)에 대한 컨셉-위키피디아 URL 매핑 결과]')
    for concept in Result[0]:
        URL = Cmap.maping_Concept2Wiki(concept)
        print('\t{}의 위키피디아 URL> '.format(concept), URL)

    ##URL의 고유 path name(e.g. "Motion_(physics)")을 알고 싶을 경우##
    for concept in Result[0]:
        URL = Cmap.maping_Concept2Wiki(concept)
        idx = URL.find('/wiki/') + 6
        print('\t{}의 위키피디아 URL> '.format(URL[idx:]), URL)
    '''

    ##################Relation Extraction##################
    print(len(origins))
    print(len(Result))
    for index in range(len(origins)):

        sourceName = origins[index].split("v=")[1].split("&")[0] + ".json"
        print(Result[index])
        print(sourceName)
        conceptRelation, All_degree = defineConcept.getConceptRelation(Result[index])
        print(conceptRelation)

        #그래프 시작
        graphSource = makeGraph.py2json(Result[index], conceptRelation)
        #sourceName = str(originURL)+"_index"+str(index)+".json"
        sourceLoc = os.path.join("./Web/conceptproto/play/static/play/data/" +sourceName)
        print(sourceLoc)
        with open(sourceLoc, "w") as f:
            f.write(graphSource)

    # 관계 두번째 알고리즘
    # Rocation_Algo2 = WR.WikiRotion(All_degree)
    # Rocation_Algo2.get_rocation()
    # testFeature(Result[index])


def testFeature(concept):
    for c in concept:
        c = c.replace("/wiki/", "")
        #print(c)
        feature = GF.GetWikiFeature(c)

        Indegree = feature.getIndegree()
        Outdegree = feature.getOutdegree()
        LanguageNum = feature.getLanguageNum()
        Categoriesdegree = feature.getCategoriesdegree()

        print("Indegree 수 : ",Indegree)
        print("Outdegree 수 : ", Outdegree)
        print("LanguageNum 수 : ", LanguageNum)
        print("Categoriesdegree 수 : ", Categoriesdegree)

def testGraph():
    originURL = "PLmhKTejvqnoOrQOcTY-pxN00BOZTGSWc3"#"PL8dPuuaLjXtN0ge7yDk_UA0ldZJdhwkoV" :물리학
    playlistURL = 'https://www.youtube.com/playlist?list=' + originURL
    #c_extraction = CE.ConceptExtraction(playlistURL)
    #defineConcept = DD.DefineDistance()

    makeGraph = MG.MakeGraph()
    Result = [['acceleration', 'velocity', 'displacement', 'motion', 'light', 'universe'], ['derivative', 'velocity', 'calculus', 'acceleration', 'power', 'mathematics'], ['integral', 'derivative', 'acceleration', 'velocity', 'displacement', 'calculus'], ['vector', 'machine', 'velocity', 'dimension', 'motion', 'ground'], ['force', 'gravity', 'acceleration', 'mass', 'inertia', 'ground'], ['force', 'gravity', 'acceleration', 'trigonometry', 'sound', 'heat'], ['circle', 'acceleration', 'motion', 'speed', 'velocity', 'spin'], ['acceleration', 'gravity', 'mass', 'force', 'ground', 'focus'], ['energy', 'pendulum', 'work', 'force', 'distance', 'ground'], ['momentum', 'mass', 'pendulum', 'velocity', 'energy', 'sound'], ['velocity', 'motion', 'circle', 'acceleration', 'frequency', 'ground'], ['inertia', 'torque', 'mass', 'energy', 'momentum', 'motion'], ['stress', 'torque', 'force', 'statics', 'length', 'pressure'], ['pressure', 'fluid', 'density', 'volume', 'force', 'gravity'], ['fluid', 'density', 'pressure', 'viscosity', 'volume', 'energy'], ['amplitude', 'motion', 'energy', 'frequency', 'velocity', 'wave'], ['wave', 'pulse', 'amplitude', 'crest', 'sound', 'interference'], ['sound', 'wave', 'watt', 'pressure', 'decibel', 'plane'], ['wave', 'wavelength', 'frequency', 'sound', 'length', 'wind'], ['temperature', 'volume', 'pressure', 'kelvin', 'length', 'stress'], ['temperature', 'liquid', 'pressure', 'kelvin', 'speed', 'phase'], ['heat', 'temperature', 'convection', 'phase', 'radiation', 'energy'], ['entropy', 'heat', 'thermodynamics', 'volume', 'temperature', 'pressure'], ['engine', 'heat', 'temperature', 'work', 'volume', 'pressure'], ['coulomb', 'electron', 'atom', 'force', 'electricity', 'ground'], ['coulomb', 'force', 'density', 'point', 'capacitor', 'electromagnetism'], ['capacitor', 'capacitance', 'voltage', 'energy', 'dielectric', 'battery'], ['voltage', 'ohm', 'battery', 'power', 'light', 'electricity'], ['voltage', 'battery', 'ohm', 'resistor', 'light', 'energy'], ['resistor', 'ohm', 'voltage', 'voltmeter', 'ammeter', 'battery'], ['voltage', 'capacitor', 'capacitance', 'battery', 'resistor', 'ohm'], ['force', 'radiation', 'vector', 'magnetism', 'tesla', 'length'], ['circle', 'integral', 'ampere', 'torque', 'force', 'point'], ['flux', 'electromagnet', 'length', 'drag', 'magnetism', 'mean'], ['voltage', 'transformer', 'electricity', 'inductance', 'flux', 'power'], ['voltage', 'inductor', 'inductance', 'flux', 'battery', 'resistor'], ['flux', 'wave', 'permittivity', 'density', 'energy', 'speed'], ['refraction', 'light', 'reflection', 'length', 'distance', 'optics'], ['wave', 'light', 'diffraction', 'interference', 'wavelength', 'amplitude'], ['light', 'interference', 'wave', 'diffraction', 'phase', 'wavelength'], ['light', 'focus', 'diffraction', 'wave', 'length', 'distance'], ['light', 'speed', 'length', 'spacetime', 'distance', 'vacuum'], ['light', 'photon', 'wave', 'energy', 'frequency', 'electron'], ['electron', 'quantum', 'probability', 'momentum', 'wavelength', 'wave'], ['mass', 'atom', 'energy', 'proton', 'electron', 'neutrino'], ['universe', 'radiation', 'light', 'redshift', 'plasma', 'matter']]
    origins = ['https://www.youtube.com/watch?v=ZM8ECpBuQYE&amp;list=PL8dPuuaLjXtN0ge7yDk_UA0ldZJdhwkoV&amp;index=1', 'https://www.youtube.com/watch?v=ObHJJYvu3RE&amp;list=PL8dPuuaLjXtN0ge7yDk_UA0ldZJdhwkoV&amp;index=2', 'https://www.youtube.com/watch?v=jLJLXka2wEM&amp;list=PL8dPuuaLjXtN0ge7yDk_UA0ldZJdhwkoV&amp;index=3', 'https://www.youtube.com/watch?v=w3BhzYI6zXU&amp;list=PL8dPuuaLjXtN0ge7yDk_UA0ldZJdhwkoV&amp;index=4', 'https://www.youtube.com/watch?v=kKKM8Y-u7ds&amp;list=PL8dPuuaLjXtN0ge7yDk_UA0ldZJdhwkoV&amp;index=5', 'https://www.youtube.com/watch?v=fo_pmp5rtzo&amp;list=PL8dPuuaLjXtN0ge7yDk_UA0ldZJdhwkoV&amp;index=6', 'https://www.youtube.com/watch?v=bpFK2VCRHUs&amp;list=PL8dPuuaLjXtN0ge7yDk_UA0ldZJdhwkoV&amp;index=7', 'https://www.youtube.com/watch?v=7gf6YpdvtE0&amp;list=PL8dPuuaLjXtN0ge7yDk_UA0ldZJdhwkoV&amp;index=8', 'https://www.youtube.com/watch?v=w4QFJb9a8vo&amp;list=PL8dPuuaLjXtN0ge7yDk_UA0ldZJdhwkoV&amp;index=9', 'https://www.youtube.com/watch?v=Y-QOfc2XqOk&amp;list=PL8dPuuaLjXtN0ge7yDk_UA0ldZJdhwkoV&amp;index=10', 'https://www.youtube.com/watch?v=fmXFWi-WfyU&amp;list=PL8dPuuaLjXtN0ge7yDk_UA0ldZJdhwkoV&amp;index=11', 'https://www.youtube.com/watch?v=b-HZ1SZPaQw&amp;list=PL8dPuuaLjXtN0ge7yDk_UA0ldZJdhwkoV&amp;index=12', 'https://www.youtube.com/watch?v=9cbF9A6eQNA&amp;list=PL8dPuuaLjXtN0ge7yDk_UA0ldZJdhwkoV&amp;index=13', 'https://www.youtube.com/watch?v=b5SqYuWT4-4&amp;list=PL8dPuuaLjXtN0ge7yDk_UA0ldZJdhwkoV&amp;index=14', 'https://www.youtube.com/watch?v=fJefjG3xhW0&amp;list=PL8dPuuaLjXtN0ge7yDk_UA0ldZJdhwkoV&amp;index=15', 'https://www.youtube.com/watch?v=jxstE6A_CYQ&amp;list=PL8dPuuaLjXtN0ge7yDk_UA0ldZJdhwkoV&amp;index=16', 'https://www.youtube.com/watch?v=TfYCnOvNnFU&amp;list=PL8dPuuaLjXtN0ge7yDk_UA0ldZJdhwkoV&amp;index=17', 'https://www.youtube.com/watch?v=qV4lR9EWGlY&amp;list=PL8dPuuaLjXtN0ge7yDk_UA0ldZJdhwkoV&amp;index=18', 'https://www.youtube.com/watch?v=XDsk6tZX55g&amp;list=PL8dPuuaLjXtN0ge7yDk_UA0ldZJdhwkoV&amp;index=19', 'https://www.youtube.com/watch?v=6BHbJ_gBOk0&amp;list=PL8dPuuaLjXtN0ge7yDk_UA0ldZJdhwkoV&amp;index=20', 'https://www.youtube.com/watch?v=WOEvvHbc240&amp;list=PL8dPuuaLjXtN0ge7yDk_UA0ldZJdhwkoV&amp;index=21', 'https://www.youtube.com/watch?v=tuSC0ObB-qY&amp;list=PL8dPuuaLjXtN0ge7yDk_UA0ldZJdhwkoV&amp;index=22', 'https://www.youtube.com/watch?v=4i1MUWJoI0U&amp;list=PL8dPuuaLjXtN0ge7yDk_UA0ldZJdhwkoV&amp;index=23', 'https://www.youtube.com/watch?v=p1woKh2mdVQ&amp;list=PL8dPuuaLjXtN0ge7yDk_UA0ldZJdhwkoV&amp;index=24', 'https://www.youtube.com/watch?v=TFlVWf8JX4A&amp;list=PL8dPuuaLjXtN0ge7yDk_UA0ldZJdhwkoV&amp;index=25', 'https://www.youtube.com/watch?v=mdulzEfQXDE&amp;list=PL8dPuuaLjXtN0ge7yDk_UA0ldZJdhwkoV&amp;index=26', 'https://www.youtube.com/watch?v=ZrMltpK6iAw&amp;list=PL8dPuuaLjXtN0ge7yDk_UA0ldZJdhwkoV&amp;index=27', 'https://www.youtube.com/watch?v=HXOok3mfMLM&amp;list=PL8dPuuaLjXtN0ge7yDk_UA0ldZJdhwkoV&amp;index=28', 'https://www.youtube.com/watch?v=g-wjP1otQWI&amp;list=PL8dPuuaLjXtN0ge7yDk_UA0ldZJdhwkoV&amp;index=29', 'https://www.youtube.com/watch?v=-w-VTw0tQlE&amp;list=PL8dPuuaLjXtN0ge7yDk_UA0ldZJdhwkoV&amp;index=30', 'https://www.youtube.com/watch?v=vuCJP_5KOlI&amp;list=PL8dPuuaLjXtN0ge7yDk_UA0ldZJdhwkoV&amp;index=31', 'https://www.youtube.com/watch?v=s94suB5uLWw&amp;list=PL8dPuuaLjXtN0ge7yDk_UA0ldZJdhwkoV&amp;index=32', 'https://www.youtube.com/watch?v=5fqwJyt4Lus&amp;list=PL8dPuuaLjXtN0ge7yDk_UA0ldZJdhwkoV&amp;index=33', 'https://www.youtube.com/watch?v=pQp6bmJPU_0&amp;list=PL8dPuuaLjXtN0ge7yDk_UA0ldZJdhwkoV&amp;index=34', 'https://www.youtube.com/watch?v=9kgzA0Vd8S8&amp;list=PL8dPuuaLjXtN0ge7yDk_UA0ldZJdhwkoV&amp;index=35', 'https://www.youtube.com/watch?v=Jveer7vhjGo&amp;list=PL8dPuuaLjXtN0ge7yDk_UA0ldZJdhwkoV&amp;index=36', 'https://www.youtube.com/watch?v=K40lNL3KsJ4&amp;list=PL8dPuuaLjXtN0ge7yDk_UA0ldZJdhwkoV&amp;index=37', 'https://www.youtube.com/watch?v=Oh4m8Ees-3Q&amp;list=PL8dPuuaLjXtN0ge7yDk_UA0ldZJdhwkoV&amp;index=38', 'https://www.youtube.com/watch?v=IRBfpBPELmE&amp;list=PL8dPuuaLjXtN0ge7yDk_UA0ldZJdhwkoV&amp;index=39', 'https://www.youtube.com/watch?v=-ob7foUzXaY&amp;list=PL8dPuuaLjXtN0ge7yDk_UA0ldZJdhwkoV&amp;index=40', 'https://www.youtube.com/watch?v=SddBPTcmqOk&amp;list=PL8dPuuaLjXtN0ge7yDk_UA0ldZJdhwkoV&amp;index=41', 'https://www.youtube.com/watch?v=AInCqm5nCzw&amp;list=PL8dPuuaLjXtN0ge7yDk_UA0ldZJdhwkoV&amp;index=42', 'https://www.youtube.com/watch?v=7kb1VT0J3DE&amp;list=PL8dPuuaLjXtN0ge7yDk_UA0ldZJdhwkoV&amp;index=43', 'https://www.youtube.com/watch?v=qO_W70VegbQ&amp;list=PL8dPuuaLjXtN0ge7yDk_UA0ldZJdhwkoV&amp;index=44', 'https://www.youtube.com/watch?v=lUhJL7o6_cA&amp;list=PL8dPuuaLjXtN0ge7yDk_UA0ldZJdhwkoV&amp;index=45', 'https://www.youtube.com/watch?v=VYxYuaDvdM0&amp;list=PL8dPuuaLjXtN0ge7yDk_UA0ldZJdhwkoV&amp;index=46']

    conceptRelation = [[0, 1, 1, 1, 2],
                       [2, 0, 2, 1, 2],
                       [1, 1, 0, 1, 2],
                       [1, 1, 1, 0, 1],
                       [2, 2, 2, 2, 0]]

    graphSource = makeGraph.py2json(Result, conceptRelation)
    for index in range(len(origins)):

        sourceName = origins[index].split("v=")[1].split("&")[0] + ".json"
        print(Result[index])
        print(sourceName)
        submitCode = "1503382656%7Ce5c72339e330f6814ae2fe97aa5c6301"
        defineConcept = DD.DefineDistance(submitCode)

        conceptRelation, All_degree = defineConcept.getConceptRelation(Result[index])
        print(conceptRelation)

        #그래프 시작
        graphSource = makeGraph.py2json(Result[index], conceptRelation)
        #sourceName = str(originURL)+"_index"+str(index)+".json"
        sourceLoc = os.path.join("./Web/conceptproto/play/static/play/data/" +sourceName)
        print(sourceLoc)
        with open(sourceLoc, "w") as f:
            f.write(graphSource)

if __name__ == "__main__":
    main()
    #testGraph()