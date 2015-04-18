$(function() {
	//Calls the tocify method on your HTML div.
	$("#toc").toc({
		'container': '#notebook-content'
	});

	var myCodeMirror = CodeMirror.fromTextArea(document.getElementById("notebook-editor"), {
		smartIndent:true,
		lineNumbers: true,
		autofocus:true
	});
});