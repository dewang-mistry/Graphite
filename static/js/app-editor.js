$(function() {

	var myCodeMirror = CodeMirror.fromTextArea(document.getElementById("notebook-editor"), {
		smartIndent:true,
		lineNumbers: true,
		autofocus:true,
		disableSpellcheck:false
	});

});