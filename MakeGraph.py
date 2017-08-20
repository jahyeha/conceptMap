import json

class MakeGraph:
    def py2json(self, concept,conceptRelation):
        out = dict()
        nodes = list()
        edges = list()
        resistDistnace = len(concept)/2 - 1
        print("py")
        print(concept, conceptRelation)

        for i, ci in enumerate(concept):
            node = dict()
            node['id'] = i
            node['label'] = ci
            nodes.append(node)
            for j in range(i+1,len(concept)):
                #print(i, j)
                if (conceptRelation[i] == conceptRelation[j]):
                    # 다른 feature로 정의
                    print(i, j)
                    edge = dict()
                    edge['to'] = i
                    edge['from'] = j
                    edges.append(edge)

                    edge['to'] = j
                    edge['from'] = i
                    edges.append(edge)

                    print("\n")
                    continue
                elif(conceptRelation[i][j] > conceptRelation[j][i]):
                    if(conceptRelation[i][j] < resistDistnace):
                        source = i
                        target = j
                    else:
                        continue
                else:
                    if (conceptRelation[j][i] < resistDistnace):
                        source = j
                        target = i
                    else:
                        continue

                edge = dict()
                edge['to'] = target
                edge['from'] = source
                edges.append(edge)

        out['nodes'] = nodes
        out['edges'] = edges
        print("dic")
        print(out)
        source = json.dumps(out,indent=4)
        print(source)
        # file write  : ./con
        return source

    '''
    example
        #conceptRelation -> dict()
    
    
    conceptRelation = {
        'nodes' : [{'id' :0, 'caption':'asdf'}, ...]
        'edges' : [{'source' : 0, 'target':1]}
    }
    
    ->
    {
        "comment": "test",
        "nodes": [
            {
                "id": 0,
                "caption": "Synapse"
            },
            {
            }
        ],
        "edges": [
            {
                "source": 0,
                "target": 1
            }
        ]
    }
            '''