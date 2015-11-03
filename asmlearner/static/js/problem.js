/*
 * problem.js for problem editor
 *
 * requires:
 * var problem = {
 *  id: <problem id>
 * };
 */

jQuery(window).ready(function() {
    var $codeArea = $('#codeArea');
    var editor = CodeMirror.fromTextArea($codeArea[0], {
        lineNumbers: true,
        mode: {
            name: 'gas',
            architecture: 'x86'
        },
        theme: 'dracula'
    });

    function compileCode(editor) {
        var code = editor.getValue();
        $.post('/problem/' + encodeURIComponent(problem.id) + '/run',
               {
                   code: code
               },
               function(response) {
                   response = JSON.parse(response);
                   if(response.status == 'solved') {
                       solvedModal();
                   } else if(response.status == 'fail') {
                       fail();
                   } else if(response.status == 'compileError') {
                       compileError(response);
                   } else {
                       unknownError();
                   }
               }
              );
    }

    editor.setOption('extraKeys', {
        'Ctrl-Enter': compileCode,
        'Command-Enter': compileCode
    });
});
