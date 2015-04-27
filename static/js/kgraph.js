var nodes = [];
var edges = [];
var network;

function getGraphJSON(data) {
	//console.log(data);
	nodes = data['nodes'];
	edges = data['edges'];

	var data= {
		nodes: nodes,
		edges: edges,
	};

	var options = {
	    width: '100%',
	    height: '100%',
	    hover: true,
	    hideEdgesOnDrag: true,
	    stabilize: false,
	    clustering: false,
	    keyboard: false,
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
	network = new vis.Network(container, data, options);	
	
	network.on('select', function (properties) {
		//alert('selected nodes: ' + properties.nodes);
		if (properties.nodes.length > 0) {
			
			var animation_options = {
				easingFunction:'easeInOutCubic'
			};

			var zoom_options = {
				scale:1.3,
				animation: animation_options,
				locked: true
			};

			network.focusOnNode(properties.nodes, zoom_options);

			console.log(network.getConnectedNodes(properties.nodes));
		}
	});

	network.on('doubleClick', function (properties) {
		console.log('Node Clicked!')
		if (properties.nodes.length > 0) {
			window.location.href = properties.nodes;
		}
	});

	network.on('stabilized', function (properties) {
		console.log('stabilized!');
		//network.zoomExtent();
	});

	Mousetrap.bind('esc', function() { 
		var animation_options = {
			easingFunction:'easeInOutCubic'
		};

		network.zoomExtent(animation_options);
	});

	NProgress.done();

	$("#search-box-input").focus();

/*
	setInterval(function() { 
		var node = nodes[getRandomInt(0, 41)]["id"];
		console.log(node);
		network.focusOnNode(node);
	}, 100);
*/
}

NProgress.start();
$.getJSON("/api/graph", getGraphJSON);

var notebooks = new Bloodhound({
  //datumTokenizer: Bloodhound.tokenizers.whitespace,
  datumTokenizer: Bloodhound.tokenizers.obj.whitespace('name'),
  queryTokenizer: Bloodhound.tokenizers.whitespace,
  prefetch: '/api/notebookList'
});

notebooks.initialize();

$(function() {
	$('#search-box .typeahead').typeahead({
	  hint: false,
	  highlight: true,
	  minLength: 1
	},
	{
	  name: 'notebooks',
	  source: notebooks
	});

	$('.typeahead').bind('typeahead:select', function(ev, suggestion) {
  		window.location.href = getNodeID(suggestion);
	});

	$('.typeahead').bind('typeahead:cursorchange', function(ev, suggestion) {
		var zoom_options = {
			scale:1.3,
			animation: {
				easingFunction:'easeInOutCubic'
			},
			duration:2000
		};

  		//var node = nodes[getRandomInt(0, 41)]["id"];
  		var node = getNodeID(suggestion);

  		//network.zoomExtent({duration:2000});
  		//network.freezeSimulation(true);
  		//network.focusOnNode(getNodeID(suggestion), zoom_options);
  		network.focusOnNode(node, zoom_options);
	});
});

function getNodeID(nodeName) {
	for (var i = 0; i < nodes.length; i++) {
		//console.log(nodes[i]['label']);
		if (nodes[i]['label'] === nodeName) {
			console.log(nodes[i]['id']);
			return String(nodes[i]['id']);
		}
	}
}

function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}