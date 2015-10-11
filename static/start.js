'use strict';

var sourceEditor;
var $output = $('#output');

var whitelist = {
  '\n': 1,
  '\r': 1,
  '\t': 1
}

function escapeForJS(string) {
  return string.split('').map(function(x) {
    if(!whitelist[x] && x.charCodeAt(0) < 0x1f || x.charCodeAt(0) > 0x7e) {
      var s = x.charCodeAt(0).toString(16);
      if(s.length == 1) s = '0' + s;
      return '\\x' + s;
    } else {
      return x;
    }
  }).join('');
}

function ace_editor(self) {
	var editor = ace.edit(self);
	editor.session.setMode("ace/mode/assembly_x86");

	editor.commands.addCommand({
		name: 'run',
		bindKey: {win: 'Ctrl-Enter', mac: 'Command-Enter'},
		exec: runProgram
	});

	editor.getSession().setTabSize(2);
	editor.getSession().setUseSoftTabs(true);

	return editor;
}

function compiler_error() {
	return;
}

function solve() {
	alert('풀렸습니다!');
	return;
}

function showAnswer() {
	return;
}

function runProgram() {
	var source = sourceEditor.getValue();

	if(lecture == null) {
		alert("강의 내용이 안 불러와져요. (js문제)");
		return;
	}

	$.post('/run', {
		level:  lecture.level,
		source: source
	}, function(data) {
		data = JSON.parse(data);

		$output.text(escapeForJS(atob(data.output)));
		$output.scrollTop(0);

		if(data.code == -1) {
			compiler_error();
		}

		if(data.success == 1) solve();
	})
}

sourceEditor = ace_editor('source');
