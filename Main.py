import ExtractConcept as EX
import DefineDistanceByConcept as DD
import GetWikiFeature as GF


def main():
    #input
    video_id = "bxe2T-V8XRs"
    video_list_id = "PLiaHhY2iBX9hdHaRr6b7XevZtgZRa1PoU"

    #instance
    extractConcept = EX.ExtractConcept()
    defineConcept = DD.DefineDistance()

    #concept = extractConcept.getConcept(video_list_id)
    #print(concept)

    #tmpt concept
    concept = [
    'Machine_learning',
    'Supervised_learning',
    'Linear_regression',
    'Classification',
    # 'Statistical_classification',
    # 'Artificial_neural_network',
    # 'Neuron',
    # 'Layered_hidden_Markov_model',
    # 'Deep_learning',
    # 'Synapse',
    # 'Activation_function',
    # 'Sigmoid_function'
    ]

    conceptRelation = defineConcept.getConceptRelation2(concept)
    print(conceptRelation)


    def testFeature(concept):
        for c in concept:
            c = c.replace("/wiki/", "")
            print(c)
            feature = GF.GetWikiFeature(c)

            feature.getCategoriesdegree()
            feature.getIndegree()
            feature.getOutdegree()
            feature.getLanguageNum()


if __name__ == "__main__":
    main()