import json

class MakeGraph:
    def py2json(self, conceptRelation):
        return json.dump(conceptRelation)
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
        ],
        "edges": [
            {
                "source": 0,
                "target": 1
            }
        ]
    }
            '''