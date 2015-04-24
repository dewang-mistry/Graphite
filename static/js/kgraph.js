function getGraphJSON(data) {
	//console.log(data);
	var nodes = data['nodes'];
	var edges = data['edges']

	console.log(nodes);
	console.log(edges);

	var data= {
		nodes: nodes,
		edges: edges,
	};

	var options = {
	    width: '100%',
	    height: '100%',
	    hover: true,
	    hideEdgesOnDrag: true,
	    stabilize: true,
	    clustering: true,
	    nodes: {
		    color: {
		      background: 'white',
		      border: 'red',
		      highlight: {
		        background: 'pink',
		        border: 'red'
		      }
		    },
		    shape: 'dot',
		    radius: 10
		}
	};

	var container = document.getElementById('graphvis');
	var network = new vis.Network(container, data, options);	
	
	network.on('select', function (properties) {
		//alert('selected nodes: ' + properties.nodes);
		if (properties.nodes.length > 0) {
			window.location.href = properties.nodes;
		}
	});
}

/*
var nodes = new vis.DataSet();
var edges = new vis.DataSet();
nodes.add([
    {id: '1', label: 'Node 1'},
    {id: '2', label: 'Node 2'},
    {id: '3', label: 'Node 3'},
    {id: '4', label: 'Node 4'},
]);

edges.add([
    {from: '1', to: '2'},
    {from: '1', to: '3'},
    {from: '2', to: '4'},
    {from: '2', to: '5'},
]);
*/

$.getJSON("/api/graph", getGraphJSON);