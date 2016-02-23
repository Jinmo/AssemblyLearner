/*
 * problem.js for problem editor
 *
 * requires:
 * var problem = {
 *  id: <problem id>
 * };
 */

var _failMessage = "컴파일은 잘 되었지만, 틀렸대요.",
    _unknownErrorMessage = "사이트에 뭔가 문제가 있나봐요. 관리자에게 문의해보세요!\n만약 관리자분이시라면 http://github.com/Jinmo/AssemblyLearner에 이슈를 넣어주세요!";

var $codeArea = $('#codeArea'),
    $errorArea = $('#errorArea'),
    $codeButtonLoader = $('#codeButtonLoader');
var editor = CodeMirror.fromTextArea($codeArea[0], {
    lineNumbers: true,
    mode: {
        name: 'gas',
        architecture: 'x86'
    },
    theme: 'dracula'
});

function solvedModal() {
};

function showError(type, message) {
    $errorArea
    .stop()
    .hide()
    .attr('class', 'ui ' + type + ' message')
    .text(message)
    .fadeIn('fast');
};

function fail() {
    showError('error', _failMessage);
};

function compileError(response) {
    var error = response.error;
    showError('warning', error);
};

function unknownError() {
    showError('warning', _unknownErrorMessage);
};

function compileCode() {
    var code = editor.getValue();

    $codeButtonLoader.addClass('active');
    $.post('/problem/' + encodeURIComponent(problem.id) + '/submit',
            {
                code: code
            })
            .done(function(response) {
                $codeButtonLoader.removeClass('active');

                try {   
                    response = JSON.parse(response);
                } catch(e) {
                    unknownError();
                }
                if (response.status == 'success')
                    solvedModal();
                else
                    fail();

            });
}
//function compileCode() {
//    var code = editor.getValue();
//
//    $codeButtonLoader.addClass('active');
//    $.post('/problem/' + encodeURIComponent(problem.id) + '/run',
//           {
//               code: code
//           })
//           .done(function(response) {
//               $codeButtonLoader.removeClass('active');
//               try {
//                   response = JSON.parse(response);
//               } catch(e) {
//                   unknownError();
//               }
//               if(response.status == 'solved') {
//                   solvedModal();
//               } else if(response.status == 'fail') {
//                   fail();
//               } else if(response.status == 'compileError') {
//                   compileError(response);
//               } else {
//                   unknownError();
//               }
//           }
//          )
//          .fail(function() {
//              unknownError();
//              $codeButtonLoader.removeClass('active');
//          });
//}

editor.setOption('extraKeys', {
    'Ctrl-Enter': compileCode,
    'Command-Enter': compileCode
});
