import json

class MakeGraph:
    def py2json(self, concept,conceptRelation):
        out = dict()
        nodes = list()
        edges = list()
        resistDistnace = 3

        for i, ci in enumerate(concept):
            node = dict()
            node['id'] = i
            node['label'] = ci
            nodes.append(node)
            for j in range(i+1,len(concept)):
                # print("i:",i,"j:", j)
                # print("conceptRelation[i]:",conceptRelation[i])
                # print("conceptRelation[j]",conceptRelation[j])
                if (conceptRelation[i] == conceptRelation[j]):
                    #if(conceptRelation[i]==1):
                    edge = dict()
                    edge['to'] = i
                    edge['from'] = j
                    edge['middle'] = 'none'
                    edges.append(edge)
                    continue
                elif(conceptRelation[i][j] > conceptRelation[j][i]):
                    if(conceptRelation[i][j] < resistDistnace):
                        if(conceptRelation[j][i] < 2):
                            source = i
                            target = j
                        else:
                            continue
                    else:
                        continue
                else:
                    if (conceptRelation[j][i] < resistDistnace):
                        if(conceptRelation[i][j] < 2):
                            source = j
                            target = i
                        else:
                            continue
                    else:
                        continue

                edge = dict()
                edge['to'] = target
                edge['from'] = source
                edge['middle'] = 'yes'
                edges.append(edge)

        out['nodes'] = nodes
        out['edges'] = edges
        #print("dic")
        #print(out)
        source = json.dumps(out,indent=4)
        #print(source)
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