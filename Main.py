import ExtractConcept
import DefineDistanceByConcept

def main():
    video_id = "bxe2T-V8XRs"
    video_list_id = "PLiaHhY2iBX9hdHaRr6b7XevZtgZRa1PoU"
    getConcept = ExtractConcept.ExtractConcept()
    defineConcept = DefineDistanceByConcept.DefineDistance()


    concept = getConcept.Extract_Concept(getConcept.getConcept(video_list_id))
    print(concept)
    conceptRelation = defineConcept.getConceptRelation(concept)
    print(conceptRelation)

    #MakeGraph
if __name__ == "__main__":
    main()