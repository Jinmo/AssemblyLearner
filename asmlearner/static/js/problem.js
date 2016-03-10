/*
 * problem.js for problem editor
 *
 * requires:
 * var problem = {
 *  id: <problem id>
 * };
 */

var _wrongMessage = "컴파일은 잘 되었지만, 틀렸대요.",
    _failMessage = "컴파일이 잘 안됬대요. 코드에 오류가 없는지 잘 보세요. 에러 메세지를 드렸어요.",
    _unknownErrorMessage = "사이트에 뭔가 문제가 있나봐요. 관리자에게 문의해보세요!\n만약 관리자분이시라면 <a href=\"http://github.com/Jinmo/AssemblyLearner\">http://github.com/Jinmo/AssemblyLearner</a> 에 이슈를 넣어주세요!";

var $codeArea = $('#codeArea'),
    $errorArea = $('#errorArea'),
    $codeButtonLoader = $('#codeButtonLoader'),
    $codeButton = $('#codeButton'),
    $outputArea = $('#outputArea'),
    $outputContent = $('#outputContent');

var editor = CodeMirror.fromTextArea($codeArea[0], {
    lineNumbers: true,
    mode: {
        name: 'gas',
        architecture: 'x86'
    },
    theme: 'dracula',
    tabSize: 2
});

var usingSolvedModal = false;

function solvedModal() {
    if(usingSolvedModal) {
        $('#solvedModal')
        .modal('show');
    } else {
        $errorArea
            .stop()
            .hide()
            .attr('class', 'ui positive message')
            .text('정답입니다!')
            .fadeIn('fast');
    }
};

function showError(type, message) {
    $errorArea
    .stop()
    .hide()
    .attr('class', 'ui ' + type + ' message')
    .fadeIn('fast')
    .children('#content')
    .html(message)
};

function hideError() {
    $errorArea.hide();
}

closeError = hideError;

function fail(status) {
    var message = _unknownErrorMessage;
    if(status == 'FAIL')
        message = _failMessage;
    else if(status == 'WRONG')
        message = _wrongMessage;
    showError('error', message);
};

function compileError(response) {
    var error = response.error;
    showError('warning', error);
};

function unknownError() {
    showError('warning', _unknownErrorMessage);
};


var timerVar;
var isLoading = false;

function compileCode() {
    if (isLoading == true) return;

    var code = editor.getValue();

    $codeButtonLoader.addClass('active');
    isLoading = true;
    $codeButton.addClass('disabled');

    $.post('/problem/' + encodeURIComponent(problem.id) + '/submit',
           {
               code: code
           })
           .done(function(response) {
               //                $codeButtonLoader.removeClass('active');

               try {
                   if (typeof response == 'string')
                       response = JSON.parse(response);
               } catch(e) {
                   unknownError();
               }
               console.log(response);
               if (response.status == 'success') {
                   timerVar = setInterval(checkStatus(response.sid), 1000);
               }
               else
                   fail();

           })
           .fail(function() {
               unknownError();
               $codeButtonLoader.removeClass('active');
           });
}

function checkStatus(id, callback) {
    return function() {
        $.post('/answer/' + encodeURIComponent(id) + '/status')
        .done(function(response) {
            try {
                if (typeof response == 'string')
                    response = JSON.parse(response);
            } catch(e) {
                doneLoading();
                unknownError();
                clearInterval(timerVar);
            }
            console.log(response);
            $outputContent.text(response.errmsg);
            if (response.status == 'CORRECT') {
                solvedModal(); clearInterval(timerVar);
            } else if (response.status == 'WRONG' || response.status == 'FAIL')  {
                fail(response.status); clearInterval(timerVar);
            } 
            else { return; }
            doneLoading();

        })
        .fail(function() {
            doneLoading();
            unknownError();
            clearInterval(timerVar);
        });
    }
}

function doneLoading() {
    isLoading = false;
    $codeButtonLoader.removeClass('active');
    $codeButton.removeClass('disabled');
}

editor.setOption('extraKeys', {
    'Ctrl-Enter': compileCode,
    'Command-Enter': compileCode
});

// outputArea draggable

function resizer(target) {
    target.className = target.className + ' resizable';
    var resizer = document.createElement('div');
    resizer.className = 'resizer';
    resizer.style.cssText = 'width: 100%; height: 3px; background: #555; border: 0px solid #222; border-width: 1px 0 1px 0; position:absolute; left: 0; top: -2px; cursor: s-resize; box-sizing: border-box;';
    target.appendChild(resizer);
    resizer.addEventListener('mousedown', initDrag, false);
    resizer.addEventListener('selectstart', doSelectStart, false);

    var startY, startHeight;

    function initDrag(e) {
        startY = e.clientY;
        startHeight = parseInt(document.defaultView.getComputedStyle(target).height, 10);
        document.documentElement.addEventListener('mousemove', doDrag, false);
        document.documentElement.addEventListener('mouseup', stopDrag, false);
        e.preventDefault();
    }

    function doDrag(e) {
        target.style.height = (startHeight - e.clientY + startY) + 'px';
    }

    function stopDrag(e) {
        document.documentElement.removeEventListener('mousemove', doDrag, false);    document.documentElement.removeEventListener('mouseup', stopDrag, false);
    }

    function doSelectStart(e) {
        e.preventDefault();
        return false;
    }
}

resizer($outputArea[0]);
