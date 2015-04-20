$(function() {
	//Calls the tocify method on your HTML div.
	$("#toc").toc({
		'container': '#notebook-content'
	});

	$("#toc").sticky({topSpacing:10});

});