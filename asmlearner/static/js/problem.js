jQuery(window).ready(function() {
    var $codeArea = $('#codeArea');
    var editor = CodeMirror.fromTextArea($codeArea[0], {
        lineNumbers: true,
        mode: {
            name: 'gas',
            architecture: 'x86'
        }
    });
});
