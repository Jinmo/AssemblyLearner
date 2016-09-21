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

var _wrongMessages = ["컴파일은 잘 되었지만, 틀렸대요.",
//  "너틀림ㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋ",
  "아이고.. 틀렸어요..",
//  "진용휘님이 이 코드를 싫어합니다.",
  "틀렸어요",
  // "프로그래밍에 정답은 없습니다. 하지만 오답은 있단다. (퍽퍽)",
  // "틀렸고요~ 인정? 어 인정. 앙 어셈띠!",
  // "오답 각 인정? 앙 기모띠",
  "아, 없네요~ 답이 없네요~"];

var $codeArea = $('#codeArea'),
    $allCodeAreas,
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
    tabSize: 2,
    scrollbarStyle: "simple"
});

$allCodeAreas = $('#codeArea, .CodeMirror');

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
        .fadeIn('fast')
        .children('#content')
        .html('정답입니다!');
    }
};

function showError(type, message) {
    $errorArea
    .stop()
    .hide()
    .attr('class', 'ui ' + type + ' message')
    .fadeIn('fast')
    .children('#content')
    .html(message);
};

function hideError() {
    $errorArea.hide();
}

closeError = hideError;

function fail(status) {
    _wrongMessage = _wrongMessages[Math.floor(Math.random() * _wrongMessages.length)];
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
                   doneLoading();
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
               doneLoading();
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
            if (response.status == 'CORRECT') {
                solvedModal(); clearInterval(timerVar);
            } else if (response.status == 'WRONG' || response.status == 'FAIL')  {
                fail(response.status); clearInterval(timerVar);
            }
            else { return; }
            $outputContent.text(response.errmsg);
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

function resetCode() {
    editor.setValue(problem.example);
}

editor.setOption('extraKeys', {
    'Ctrl-Enter': compileCode,
    'Command-Enter': compileCode
});

// outputArea draggable

function resizer(target, options) {
    var options = options || {};
    var resizer = document.createElement('div');

    target.className = target.className + ' resizable';
    resizer.className = 'resizer';
    resizer.style.cssText = 'width: 100%; height: 5px; background: #555; border: 0px solid #222; border-width: 1px 0 1px 0; position:absolute; left: 0; top: -4px; cursor: s-resize; box-sizing: border-box;';
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
        var newHeight = (startHeight - e.clientY + startY);
        target.style.height = newHeight + 'px';

        if(options.resize) {
            options.resize(newHeight);
        }
    }

    function stopDrag(e) {
        document.documentElement.removeEventListener('mousemove', doDrag, false);    document.documentElement.removeEventListener('mouseup', stopDrag, false);
    }

    function doSelectStart(e) {
        e.preventDefault();
        return false;
    }
}

resizer($outputArea[0], {
    resize: function(newHeight) {
        $allCodeAreas.css('bottom', newHeight);
    }
});

var commands = {};

commands['history'] = function loadHistory(id) {
    var id = parseInt(id).toString();
    $.get('/api/history/' + id, function(data) {
        editor.getDoc().setValue(data.answer);
    });
}

function runCommand(cmd, params) {
    console.log(cmd, params);
    if(commands.hasOwnProperty(cmd))
        commands[cmd].apply(this, params);
}

function removeUrlHash () {
    var scrollV, scrollH, loc = window.location;
    if ("pushState" in history)
        history.pushState("", document.title, loc.pathname + loc.search);
    else {
        // Prevent scrolling by storing the page's current scroll offset
        scrollV = document.body.scrollTop;
        scrollH = document.body.scrollLeft;

        loc.hash = "";

        // Restore the scroll offset, should be flicker free
        document.body.scrollTop = scrollV;
        document.body.scrollLeft = scrollH;
    }
}

var urlHash = location.hash[0] == '#' ? location.hash.substr(1) : location.hash;
if(urlHash != '') {
    var params = urlHash.split('/');
    if(params.shift(0) == '!') {
        var cmd = params.shift(0);

        runCommand(cmd, params);
//        removeUrlHash();
    }
}
