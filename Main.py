#import ExtractConcept as EX
from ConceptExtraction import _conceptExtraction_ as CE
from ConceptExtraction import _conceptMapping_ as CM

import DefineDistanceByConcept as DD
import GetWikiFeature as GF
import wikiRocation as WR
import MakeGraph as MG
import os


def main():
    ##################Concept Extraction##################
    originURL = "PL8dPuuaLjXtN0ge7yDk_UA0ldZJdhwkoV"#playlist로 감  #:로마 역사  # "ZM8ECpBuQYE / PL8dPuuaLjXtN0ge7yDk_UA0ldZJdhwkoV" :물리학
    playlistURL = 'https://www.youtube.com/playlist?list=' + originURL
    submitCode = "1503382656%7Ce5c72339e330f6814ae2fe97aa5c6301"
    defineConcept = DD.DefineDistance(submitCode)
    makeGraph = MG.MakeGraph()

    num_concept = 6
    playlist_url = 'https://www.youtube.com/playlist?list=PL8dPuuaLjXtN0ge7yDk_UA0ldZJdhwkoV'
    Con = CE.ConceptExtraction(playlist_url)
    Result = Con.get_Kconcept(num_concept)
    print(Result)

    """NOTE 08-24 15:20 가중치를 정해서 컨셉추출할 때 사용합니다.
    일괄적으로 강의별 k개 씩 컨셉추출을 하면 가중치가 낮은 의미 없을 수 있는 단어까지 주요 개념으로 추출
    -> but 가중치를 정해서 추출하면 정말 중요한 단어만 추출할 수 있습니다.
    
    parameter: max_concept 최대 컨셉 수, max_weight 가중치 커트라인
    
    #####여기부터#####
    playlist_url = 'https://www.youtube.com/playlist?list=PL8dPuuaLjXtN0ge7yDk_UA0ldZJdhwkoV'
    Con = CE.ConceptExtraction(playlist_url)
    max_concept, max_weight = 5, 0.08  
    Result = Con.get_only_concepts(max_concept, max_weight)
    print(Result) #가중치 적용 결과 (밑에 결과 적어놨어요)
    """

    #######################################################
    """NOTE 위의 결과 비교 <일괄적 K개 컨셉추출 vs 가중치적용하여 컨셉추출>
    1. K=5 결과(기존)
        ['acceleration', 'velocity', 'displacement', 'motion', 'light']
        ['derivative', 'velocity', 'calculus', 'acceleration', 'power']
        ['integral', 'derivative', 'acceleration', 'velocity', 'displacement']
        ['vector', 'machine', 'velocity', 'dimension', 'motion']
        ['force', 'gravity', 'acceleration', 'mass', 'inertia']
        ['force', 'gravity', 'acceleration', 'trigonometry', 'sound']
        ['circle', 'acceleration', 'motion', 'speed', 'velocity']
        ['acceleration', 'gravity', 'mass', 'force', 'ground']
        ['energy', 'pendulum', 'work', 'force', 'distance']
        ['momentum', 'mass', 'pendulum', 'velocity', 'energy']
        ['velocity', 'motion', 'circle', 'acceleration', 'frequency']
        ['inertia', 'torque', 'mass', 'energy', 'momentum']
        ['stress', 'torque', 'force', 'statics', 'length']
        ['pressure', 'fluid', 'density', 'volume', 'force']
        ['fluid', 'density', 'pressure', 'viscosity', 'volume']
        ['amplitude', 'motion', 'energy', 'frequency', 'velocity']
        ['wave', 'pulse', 'amplitude', 'crest', 'sound']
        ['sound', 'wave', 'watt', 'pressure', 'decibel']
        ['wave', 'wavelength', 'frequency', 'sound', 'length']
        ['temperature', 'volume', 'pressure', 'kelvin', 'length']
        ['temperature', 'liquid', 'pressure', 'kelvin', 'speed']
        ['heat', 'temperature', 'convection', 'phase', 'radiation']
        ['entropy', 'heat', 'thermodynamics', 'volume', 'temperature']
        ['engine', 'heat', 'temperature', 'work', 'volume']
        ['coulomb', 'electron', 'atom', 'force', 'ground']
        ['coulomb', 'force', 'density', 'point', 'electromagnetism']
        ['capacitor', 'capacitance', 'voltage', 'energy', 'dielectric']
        ['voltage', 'ohm', 'battery', 'power', 'light']
        ['voltage', 'battery', 'ohm', 'resistor', 'light']
        ['resistor', 'ohm', 'voltage', 'voltmeter', 'ammeter']
        ['voltage', 'capacitor', 'capacitance', 'battery', 'resistor']
        ['force', 'radiation', 'vector', 'magnetism', 'tesla']
        ['circle', 'integral', 'ampere', 'torque', 'force']
        ['flux', 'electromagnet', 'length', 'drag', 'magnetism']
        ['voltage', 'transformer', 'electricity', 'inductance', 'flux']
        ['voltage', 'inductor', 'inductance', 'flux', 'battery']
        ['flux', 'wave', 'permittivity', 'density', 'energy']
        ['refraction', 'light', 'reflection', 'length', 'distance']
        ['wave', 'light', 'diffraction', 'interference', 'wavelength']
        ['light', 'interference', 'wave', 'diffraction', 'phase']
        ['light', 'focus', 'diffraction', 'wave', 'length']
        ['light', 'speed', 'length', 'spacetime', 'distance']
        ['light', 'photon', 'wave', 'energy', 'frequency']
        ['electron', 'quantum', 'probability', 'momentum', 'wavelength']
        ['mass', 'atom', 'energy', 'proton', 'electron']
        ['universe', 'radiation', 'light', 'redshift', 'plasma']
    
    2. 가중치 적용 (w=0.08)
        1번 강의의 컨셉(3개) :  ['acceleration', 'velocity', 'displacement']
        2번 강의의 컨셉(4개) :  ['derivative', 'velocity', 'calculus', 'acceleration']
        3번 강의의 컨셉(4개) :  ['integral', 'derivative', 'acceleration', 'velocity']
        4번 강의의 컨셉(4개) :  ['vector', 'machine', 'velocity', 'dimension']
        5번 강의의 컨셉(5개) :  ['force', 'gravity', 'acceleration', 'mass', 'inertia']
        6번 강의의 컨셉(3개) :  ['force', 'gravity', 'acceleration']
        7번 강의의 컨셉(2개) :  ['circle', 'acceleration']
        8번 강의의 컨셉(4개) :  ['acceleration', 'gravity', 'mass', 'force']
        9번 강의의 컨셉(2개) :  ['energy', 'pendulum']
        10번 강의의 컨셉(3개) :  ['momentum', 'mass', 'pendulum']
        11번 강의의 컨셉(4개) :  ['velocity', 'motion', 'circle', 'acceleration']
        12번 강의의 컨셉(5개) :  ['inertia', 'torque', 'mass', 'energy', 'momentum']
        13번 강의의 컨셉(5개) :  ['stress', 'torque', 'force', 'statics', 'length']
        14번 강의의 컨셉(5개) :  ['pressure', 'fluid', 'density', 'volume', 'force']
        15번 강의의 컨셉(5개) :  ['fluid', 'density', 'pressure', 'viscosity', 'volume']
        16번 강의의 컨셉(4개) :  ['amplitude', 'motion', 'energy', 'frequency']
        17번 강의의 컨셉(5개) :  ['wave', 'pulse', 'amplitude', 'crest', 'sound']
        18번 강의의 컨셉(5개) :  ['sound', 'wave', 'watt', 'pressure', 'decibel']
        19번 강의의 컨셉(4개) :  ['wave', 'wavelength', 'frequency', 'sound']
        20번 강의의 컨셉(5개) :  ['temperature', 'volume', 'pressure', 'kelvin', 'length']
        21번 강의의 컨셉(4개) :  ['temperature', 'liquid', 'pressure', 'kelvin']
        22번 강의의 컨셉(5개) :  ['heat', 'temperature', 'convection', 'phase', 'radiation']
        23번 강의의 컨셉(5개) :  ['entropy', 'heat', 'thermodynamics', 'volume', 'temperature']
        24번 강의의 컨셉(3개) :  ['engine', 'heat', 'temperature']
        25번 강의의 컨셉(5개) :  ['coulomb', 'electron', 'atom', 'force', 'ground']
        26번 강의의 컨셉(2개) :  ['coulomb', 'force']
        27번 강의의 컨셉(5개) :  ['capacitor', 'capacitance', 'voltage', 'energy', 'dielectric']
        28번 강의의 컨셉(5개) :  ['voltage', 'ohm', 'battery', 'power', 'light']
        29번 강의의 컨셉(5개) :  ['voltage', 'battery', 'ohm', 'resistor', 'light']
        30번 강의의 컨셉(4개) :  ['resistor', 'ohm', 'voltage', 'voltmeter']
        31번 강의의 컨셉(5개) :  ['voltage', 'capacitor', 'capacitance', 'battery', 'resistor']
        32번 강의의 컨셉(5개) :  ['force', 'radiation', 'vector', 'magnetism', 'tesla']
        33번 강의의 컨셉(3개) :  ['circle', 'integral', 'ampere']
        34번 강의의 컨셉(1개) :  ['flux']
        35번 강의의 컨셉(5개) :  ['voltage', 'transformer', 'electricity', 'inductance', 'flux']
        36번 강의의 컨셉(4개) :  ['voltage', 'inductor', 'inductance', 'flux']
        37번 강의의 컨셉(5개) :  ['flux', 'wave', 'permittivity', 'density', 'energy']
        38번 강의의 컨셉(4개) :  ['refraction', 'light', 'reflection', 'length']
        39번 강의의 컨셉(5개) :  ['wave', 'light', 'diffraction', 'interference', 'wavelength']
        40번 강의의 컨셉(5개) :  ['light', 'interference', 'wave', 'diffraction', 'phase']
        41번 강의의 컨셉(3개) :  ['light', 'focus', 'diffraction']
        42번 강의의 컨셉(3개) :  ['light', 'speed', 'length']
        43번 강의의 컨셉(5개) :  ['light', 'photon', 'wave', 'energy', 'frequency']
        44번 강의의 컨셉(5개) :  ['electron', 'quantum', 'probability', 'momentum', 'wavelength']
        45번 강의의 컨셉(5개) :  ['mass', 'atom', 'energy', 'proton', 'electron']
        46번 강의의 컨셉(5개) :  ['universe', 'radiation', 'light', 'redshift', 'plasma']
        """

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
    ##TEST##
    print('[첫 번째 문서(강의)에 대한 컨셉-위키피디아 URL 매핑 결과]')
    for concept in Result[0]:
        URL = Cmap.maping_Concept2Wiki(concept)
        print('\t{}의 위키피디아 URL> '.format(concept), URL)

    ##URL의 고유 path name(e.g. "Motion_(physics)")을 알고 싶을 경우##
    for concept in Result[0]:
        URL = Cmap.maping_Concept2Wiki(concept)
        idx = URL.find('/wiki/') + 6
        print('\t{}의 위키피디아 URL> '.format(URL[idx:]), URL)
    ##################################################
    '''

    #### NOTE ####
    #### 임시로 밑에 getConceptRelation2 파라미터-> Result[1]으로 해놓았습니다.
    #### Result[doc_num]   0 <= doc_num < 47
    #print(Result)
    #관계부분 시작
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

    #관계 두번째 알고리즘
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