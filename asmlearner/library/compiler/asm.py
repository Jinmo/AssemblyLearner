import os, subprocess, re
from tempfile import NamedTemporaryFile
from asmlearner import config
from asmlearner.library.database.sqlite import DB


def compileProblem(problem, solved):
    answerFile = NamedTemporaryFile(mode= 'wb', prefix='asm_tmp_',
                    suffix='.s', delete=False)

    answerFile.write(solved['answer'].encode('utf8') + \
        '\n.globl __NoTraceHere__\nnop\n__NoTraceHere__:' + \
        problem['suffix'])

    answerFile.close()
    execFileName = answer.name[0:-2]

    p = subprocess.Popen((config.CC_PATH,
        answerFile.fname,
        '-o', execFileName,
        '-I', config.INCLUDE_PATH,
        '-m32', '-nostdlib', '-fno-stack-protector'), stderr=subprocess.PIPE)

    code = p.wait()
    err = p.stderr.read()

    if code != 0:
        db = DB(config.DATABASE)
        db.execute('UPDATE solved SET status=?, errmsg=?, where id=?',
            ('FAIL', err, solved['id']))
        db.commit()


    os.unlink(answerFile.name)

    if code == 0:
        runBinary(problem, solved, execFileName)

def runBinary(problem, solved, execFileName):
    tracerArgv = (config.TRACER_PATH, execFileName, porblem['input'], '/dev/fd/1')

    p = subprocess.Popen((config.OBJDUMP_PATH, '-M', 'intel', '-d', execFileName),
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    code = p.wait()
    err = p.stderr.read()

    db = DB(config.DATABASE)

    if code != 0:
        db.execute('UPDATE solved SET status=?, errmsg=? where id=?',
        ('FAIL', err, solved['id']))
        db.commit()
    else:
        p = subprocess.Popen(tracerArgv, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        p.stdin.write(problem['input'])
        out = p.stdout.read()
        err = p.stderr.read()
        code = p.wait()

        if code != 0:
            db.execute('UPDATE solved SET status=?, errmsg=? where id=?',
                ('FAIL', err, solved['id']))
            db.commit()
        else:
            m = re.findall(problem['answer_regex'], out)
            db.execute('UPDATE solved SET status=? where id=?',
                ('SUCCESS' if count(m) > 0 else 'WRONG', solved['id']))
