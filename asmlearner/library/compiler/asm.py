import os, subprocess, re
from tempfile import NamedTemporaryFile
from asmlearner import config
from asmlearner.library.database.sqlite import DB
from asmlearner.library.snippets import save_snippet
import io
import binascii

def compileProblem(problem, solved):
    db = DB(config.DATABASE)
    db.execute('UPDATE solved SET status=? where id=?', ('COMPILING', solved['id']))
    db.commit()

    snippet_dir = os.path.join( 'data/snippets', binascii.hexlify( bytes(solved['owner'], 'utf-8') ).decode('utf-8') )

    code = solved['answer']

    suffix = problem['suffix']
    suffix = bytes(suffix.encode('utf-8'))

    answerFile = save_snippet(solved['owner'], '_' + str(problem['id']) + '.s', code)

    suffixFile = open(os.path.join( 'data/suffixes', '_' + str(solved['problem']) + '.s'), 'wb')
    suffixFile.write(suffix)

    suffixFile.close()
    execFileName = answerFile.name[0:-2]

    p = subprocess.Popen((config.CC_PATH,
        answerFile.name,
        suffixFile.name,
        '-o', execFileName,
        '-I', config.INCLUDE_PATH,
        '-I', snippet_dir,
        '-m32', '-nostdlib', '-fno-stack-protector'), stderr=subprocess.PIPE)

    code = p.wait()
    err = p.stderr.read()

    if code != 0:
        print(err)
        db.execute('UPDATE solved SET status=?, errmsg=? where id=?',
            ('FAIL', err, solved['id']))
        db.commit()


    if code == 0:
        runBinary(problem, solved, execFileName)

def runBinary(problem, solved, execFileName):
    inputFile = NamedTemporaryFile(mode='w', prefix='asm_input_tmp_', delete=False)
    inputFile.write(problem['input'])
    inputFile.close()
    inputFilePath = inputFile.name
    print(open(inputFilePath, 'rb').read())
    tracerArgv = (config.TRACER_PATH, execFileName, inputFilePath, '/dev/fd/1')
    p = subprocess.Popen((config.OBJDUMP_PATH, '-M', 'intel', '-d', execFileName),
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print(tracerArgv)
    code = p.wait()
    dump_out = p.stdout.read()

    db = DB(config.DATABASE)
    if code != 0:
        db.execute('UPDATE solved SET status=?, errmsg=? where id=?',
        ('FAIL', dump_out, solved['id']))
        db.commit()
    else:
        inputFileRead = open(inputFilePath, 'rb')

        p = subprocess.Popen(tracerArgv, stdout=subprocess.PIPE, stdin=inputFileRead, stderr=subprocess.PIPE)
        err = out = p.stdout.read()
        code = p.wait()

        if code != 0:
            db.execute('UPDATE solved SET status=?, errmsg=? where id=?',
                ('WRONG', err, solved['id']))
        else:
            out = out + b'\n\n$ objdump -d [binary_file]\n' + dump_out
            print(out)
            m = re.findall(problem['answer_regex'].encode(), out)
            print(len(m))
            db.execute('UPDATE solved SET status=?, errmsg=? where id=?',
                ('CORRECT' if len(m) > 0 else 'WRONG', out, solved['id']))
    db.commit()
    os.unlink(execFileName)
    os.unlink(inputFilePath)
