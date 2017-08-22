// dataset만들기   js 를 나누기 적용이 아직 안됨 ..
// 노드가 들어있는 데이터셋
var nodes = new vis.DataSet();
// 엣지가 들어있는 데이터셋
var edges = new vis.DataSet();

$.getJSON('{% static "" %}play/data/{{video}}.json', function(json) {
  // add nodes
  console.log({{video}})
  for(var i = 0; i < json.nodes.length; i++){
    nodes.add({
      id: json.nodes[i].id,
      label: json.nodes[i].label,
      shape: 'box'
    });
  }
  // add edges
  for(var i = 0; i < json.edges.length; i++){
    edges.add({
      from: json.edges[i].from,
      to: json.edges[i].to,
      arrows:'to'
    });
  }
});
// id가 conceptmap인 엘리먼트 선택
var container = document.getElementById('conceptmap');

// data에 노드와 엣지 저장
var data = {
    nodes: nodes,
    edges: edges
};
var options = {
    layout: {
    randomSeed: undefined,
    improvedLayout:true,
    hierarchical: {
      enabled:true,
      levelSeparation: 80,
      nodeSpacing: 100,
      treeSpacing: 200,
      blockShifting: false,
      edgeMinimization: false,
      parentCentralization: false,
      direction: 'UD',        // UD, DU, LR, RL
      sortMethod: 'hubsize'   // hubsize, directed
    }
  }
};
// data와 option을 이용하여 container에 그래프 초기화
var network = new vis.Network(container, data, options);

network.setOptions(options);

console.log("end");