var states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California',
  'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii',
  'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana',
  'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota',
  'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire',
  'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota',
  'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island',
  'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont',
  'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming'
];

var states = new Bloodhound({
  datumTokenizer: Bloodhound.tokenizers.whitespace,
  queryTokenizer: Bloodhound.tokenizers.whitespace,
  // `states` is an array of state names defined in "The Basics"
  //local: states
  prefetch: '/api/notebookList'
});


function getGraphJSON(data) {
	//console.log(data);
	var nodes = data['nodes'];
	var edges = data['edges']

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
	var network = new vis.Network(container, data, options);	
	
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
		$("#search-box-input").focus();
	});

	NProgress.done();

	$("#search-box-input").focus();
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
NProgress.start();
$.getJSON("/api/graph", getGraphJSON);

$(function() {
	$('#search-box .typeahead').typeahead({
	  hint: true,
	  highlight: true,
	  minLength: 1
	},
	{
	  name: 'states',
	  source: states
	});
});