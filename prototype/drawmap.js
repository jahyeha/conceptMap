
var config = {
  dataSource: 'data/contrib.json',
  directedEdges: true,
  forceLocked: true,
//  nodeCaption: 'caption',
//  nodeMouseOver: 'caption',
  graphHeight: function(){ return 400; },
  graphWidth: function(){ return 400; },      
  linkDistance: function(){ return 40; },
//  nodeTypes: {"node_type":[ "Maintainer",
//                            "Contributor"]},
  nodeStyle: {
    "all": {
      "color": "#4286f4",
      "captionColor": "#FFFFFF"
    }
  },
  edgeStyle: {
    "all": {
      "color": "#ffffff"
    }
  },
//};
  nodeCaption: function(node){ 
    return node.caption;}
  };

alchemy = new Alchemy(config)
//alchemy.begin(config)
