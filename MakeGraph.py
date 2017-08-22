import json


class MakeGraph:
    def __init__(self):
        self.parisent = []
    def py2json(self, concept, conceptRelation):
        out = dict()
        nodes = list()
        edges = list()
        resistDistnace = 3
        # print(concept, conceptRelation)

        for i, ci in enumerate(concept):
            node = dict()
            node['id'] = i
            node['label'] = ci
            nodes.append(node)
            for j in range(i + 1, len(concept)):
                # print("i:", i, "j:", j)
                # print("conceptRelation[i]:", conceptRelation[i])
                # print("conceptRelation[j]", conceptRelation[j])
                if (conceptRelation[i][j] == conceptRelation[j][i]):
                    # 다른 feature로 정의
                    # print(i, j)
                    edge = dict()
                    edge['to'] = i
                    edge['from'] = j
                    edge['option'] = 'none'
                    edge['value'] = conceptRelation[i][j]
                    edges.append(edge)
                    #print("\n")
                    continue
                elif (conceptRelation[i][j] > conceptRelation[j][i]):
                    if(conceptRelation[i][j] < resistDistnace):
                        source = i
                        target = j
                        v = conceptRelation[j][i]
                    else:
                        continue
                else:
                    if (conceptRelation[j][i] < resistDistnace):
                        source = j
                        target = i
                        v = conceptRelation[i][j]
                    else:
                        continue
                edge = dict()
                edge['to'] = target
                edge['from'] = source
                edge['option'] = 'direct'
                edge['value'] = v
                edges.append(edge)
        #tree
        sorted_edge = sorted(edges, key = lambda k:k['value'],reverse=True)
        print(sorted_edge)
        node_size = len(nodes)
        edge_size = len(sorted_edge)-1
        self.parent = [-1 for _ in range(node_size)]

        treeEdges = list()
        while(node_size - 1 != 0):
            a = sorted_edge[edge_size]['to']
            b = sorted_edge[edge_size]['from']
            #print(a,b)
            if(self.is_cycle(a, b)):
                print("cycle!")
            else:
                print(a, b)
                treeEdges.append(sorted_edge[edge_size])
                edge_size-=1
                if(node_size == 0):
                    break
            node_size -= 1

        out['nodes'] = nodes
        out['edges'] = treeEdges
        #print("dic")
        #print(out)

        source = json.dumps(out, indent=4)
        #print(source)
        # file write  : ./con
        return source

    def find(self,i):
        if (self.parent[i] == -1):
            return i
            pass
        return self.find(self.parent[i])

    def union(self, x, y):
        xx = self.find(x)
        yy = self.find(y)
        if(xx==yy): #사이클 존재할 수 있음
            return False
        else:
            self.parent[xx] = yy
            return True

    def is_cycle(self,a,b):
        return self.union(a, b)


    def find(self,i):
        if (self.parent[i] == -1):
            return i
            pass
        return self.find(self.parent[i])

    def union(self, x, y):
        xx = self.find(x)
        yy = self.find(y)
        if(xx == yy): #사이클 존재할 수 있음
            return True
        else:
            self.parent[xx] = yy
            return False

    def is_cycle(self, x, y):
        return self.union(x, y)


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