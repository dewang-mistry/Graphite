$(function() {
	//Calls the tocify method on your HTML div.
	$("#toc").toc({
		'container': '#notebook-content'
	});

	$("#side-bar").sticky({topSpacing:10});

	$(".flashcard").flip();
});
