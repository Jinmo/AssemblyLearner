import os
import re
import subprocess
from tempfile import NamedTemporaryFile

from .config import app
from ..config import config
from ..library.snippets import save_snippet


@app.task
def compiler(id):
    from ..db.models import History
    print id
    history = History.get(id)
    code = history.code
    challenge = history.chal

    suffix = challenge.suffix

    code_path = save_snippet(history.owner, '__' + str(challenge.id) + '.s', code)

    suffix_path = NamedTemporaryFile(suffix='.s')
    suffix_path.write(suffix)
    suffix_path.flush()

    exec_path = code_path.name[0:-2]

    argv = (config.CC_PATH,
            code_path.name,
            suffix_path.name,
            '-o', exec_path,
            '-I', config.INCLUDE_PATH,
            '-I', os.path.join(config.SNIPPET_PATH),
            '-m32', '-nostdlib', '-fno-stack-protector')
    p = subprocess.Popen(argv, stderr=subprocess.PIPE)

    code = p.wait()
    err = p.stderr.read()

    if code != 0:
        print(err)
        history.status = 'FAIL'
        history.errmsg = err
        history.update(True)

    os.unlink(code_path.name)
    suffix_path.close()

    if code == 0:
        runBinary(challenge, history, exec_path)


def runBinary(problem, solved, execFileName):
    inputFile = NamedTemporaryFile(mode='w', prefix='asm_input_tmp_', delete=False)
    inputFile.write(problem.input)
    inputFile.close()
    inputFilePath = inputFile.name
    print(open(inputFilePath, 'rb').read())
    tracerArgv = (config.TRACER_PATH, execFileName, inputFilePath, '/dev/fd/1')
    p = subprocess.Popen((config.OBJDUMP_PATH, '-M', 'intel', '-d', execFileName),
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    code = p.wait()
    dump_out = p.stdout.read()

    if code != 0:
        solved.update(True,
                      status='FAIL', errmsg=dump_out)
    else:
        inputFileRead = open(inputFilePath, 'rb')

        p = subprocess.Popen(tracerArgv, stdout=subprocess.PIPE, stdin=inputFileRead, stderr=subprocess.PIPE)
        err = out = p.stdout.read()
        code = p.wait()

        if code != 0:
            solved.update(True, status='WRONG', errmsg=err)
        else:
            out = out + b'\n\n$ objdump -d [binary_file]\n' + dump_out
            m = re.findall(problem.answer_regex, out)
            solved.update(True, status='CORRECT' if len(m) > 0 else 'WRONG', errmsg=out)
    os.unlink(execFileName)
    os.unlink(inputFilePath)


if __name__ == '__main__':
    p = {"suffix": "____suffix____"}

    s = {"answer": "answer"}
    print(s['answer'])
    compiler(p, s)
