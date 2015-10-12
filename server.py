import sqlite3
import os
import time
import subprocess
import json
from hashlib import sha1
from collections import OrderedDict
from os.path import join

from flask import Flask, session, redirect, render_template, g, request
import eventlet
from utils import make_dirs

eventlet.monkey_patch()

CURPATH = os.path.dirname(os.path.realpath(__file__))

DATABASE = join(CURPATH, 'db.db')
INIT_SQL = join(CURPATH, 'init.sql')

PROBLEM_PATH = join(CURPATH, 'problem')
OUTPUT_PATH   = join(CURPATH, 'output')
INCLUDE_PATH  = join(CURPATH, 'include')

TRACER_PATH = join(CURPATH, 'tool/tracer')
CC_PATH     = '/usr/bin/gcc'

OBJDUMP_PATH = '/usr/bin/objdump'

problems   = OrderedDict()
categories = OrderedDict()

def connect_to_database():
    return sqlite3.connect(DATABASE)

def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_to_database()
        db.row_factory = make_dicts
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def commit_db(query, args):
    cur = get_db().execute(query, args)
    cur.close()

    get_db().commit()

app = Flask(__name__)
app.secret_key = 'lolthisissecretkeyforthisapp'

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    if 'user' in session:
        return redirect('/list')
    return redirect('/login')

@app.route('/login')
def login():
    if 'user' in session:
        return redirect('/list')
    return render_template('login.html', action='/check', title='AL Login', type='login')

@app.route('/logout')
def logout():
    if 'user' in session:
        del session['user']
    return redirect('/login')

@app.route('/problem/<category>/<problem>')
def start(category, problem):
    global problems
    if 'user' not in session:
        return redirect('/login')
    if category in problems:
        sub_problems = problems[category]['problems']
        if problem in sub_problems:
            problem = sub_problems[problem]
            return render_template('start.html', problem=problem)
        else:
            return ''
    else:
        return ''

@app.route('/list')
def _list():
    if 'user' not in session:
        return redirect('/login')
    return render_template('list.html', problems=problems)

@app.route('/check', methods=['POST'])
def checkuser():
    id_ = request.form['id']
    password_ = request.form['password']
    hashobj = sha1(password_ * 10)
    password_hash = hashobj.hexdigest()
    info = query_db('SELECT * FROM user WHERE id=? AND password=?', (id_, password_hash), True)
    if info is None:
        return '''<script>
        alert("ID or PW is incorrect");
        history.back(-1);
        </script>'''
    else:
        session['user'] = user = dict(info)
        user_parse_solved(user)
        return redirect('/list')

def user_parse_solved(user):
    try:
        user['solved'] = dict(map(lambda x: x.split(' ', 1)[::-1], user['solved'].strip().split('\n')))
    except:
        user['solved'] = {}
    print user['solved']

@app.route('/createuser')
def createuser():
    return render_template('login.html', action='/check_createuser', title='AL Create User', type='createuser')

@app.route('/check_createuser', methods=['POST'])
def check_createuser():
    id_ = request.form['id']
    password_ = request.form['password']
    hashobj = sha1(password_ * 10)
    password_hash = hashobj.hexdigest()
    info = query_db('SELECT 1 FROM user WHERE id=?', (id_, ), True)
    if info is None:
        commit_db('INSERT INTO user VALUES(?, ?, \'\')', (id_, password_hash))
        return '''<script>
        alert('Successfully created user!');
        location.href = '/login';
        </script>'''
    else:
        return '''<script>
        alert('User already exists!');
        history.back(-1);
        </script>'''

def issolved(problem):
    if 'user' in session:
        return problem['directory_name'] in session['user']['solved']
    return False

def load_problem():
    print ' - Trying to load category informations'
    rows = query_db("SELECT * FROM category ORDER by order_no ASC")
    for row in rows:
        name = row['name']
        categories[name] = row['title']

    print ' -  ' + str(len(categories)) + ' categories loaded'

    print ' - Trying to load problems'
    probs = os.listdir(PROBLEM_PATH)
    for row in probs:
        name = row
        if '_' in name:
            category, name = name.split('_', 1)
        else:
            category, name = '', name
        
        if category in categories:
            category_title = categories[category]
        else:
            category_title = category

        if category not in problems:
            problems[category] = {
                'title': category_title,
                'problems': {}
            }
        problem_info_file = open(os.path.join(PROBLEM_PATH, row, 'info.txt'), 'r')
        problem_info = tuple(problem_info_file.read().decode('utf8').split('\n'))
        problem_info_file.close()
        problems[category]['problems'][name] = dict(zip(('directory_name', 'name', 'category', 'title', 'order', ), (row, name, category) + problem_info))

    for category in problems:
        problems[category]['problems'] = OrderedDict(sorted(problems[category]['problems'].items(), key=lambda prob: prob[0], reverse=False))

    print ' -  ' + str(len(probs)) + ' problems loaded'

@app.route('/_load_problem')
def _load_problem():
    load_problem()
    return '<script>alert("Success!"); history.back(-1);</script>'

def load_instruction(problem):
    path = os.path.join(PROBLEM_PATH, problem['directory_name'], 'instruction.txt')
    instruction_file = open(path, 'r')
    instruction_data = instruction_file.read().decode('utf8')
    instruction_file.close() 
    return instruction_data

def load_example(problem):
    path = os.path.join(PROBLEM_PATH, problem['directory_name'], 'example.txt')
    example_file = open(path, 'r')
    example_data = example_file.read().decode('utf8')
    example_file.close()
    return example_data

def solved(problem):
    if 'user' not in session:
        return
    commit_db('UPDATE user SET solved=ifnull(solved, \'\') || ? WHERE INSTR(solved, ?) = 0 AND id = ?', ('\n%f %s' % (time.time(), problem), problem, session['user']['id']))
    session['user'] = query_db('SELECT * FROM user WHERE id=?', (session['user']['id'], ), True)
    user_parse_solved(session['user'])

def load_code(problem, code):
    problem_path = os.path.join(PROBLEM_PATH, problem)
    input_path = os.path.join(problem_path, 'input.txt')
    if not os.path.isfile(input_path):
        input_path = '/dev/null'
    suffix_path = os.path.join(problem_path, 'suffix.txt')
    if os.path.isfile(suffix_path):
        suffix_file = open(suffix_path, 'rb')
        suffix = suffix_file.read()
        suffix_file.close()
    else:
        suffix = ''
    answer_path = os.path.join(problem_path, 'answer.txt')
    if os.path.isfile(answer_path):
        answer_file = open(answer_path, 'rb')
        answer = answer_file.read().strip()
        answer_file.close()
    else:
        answer = 'My answer is here!'
    identifier = '%s_%f' % (problem, time.time())
    code_directory = os.path.join(OUTPUT_PATH, problem)
    if not os.path.isdir(code_directory):
        os.mkdir(code_directory)
    code_path = os.path.join(code_directory, identifier + '.s')
    code_file = open(code_path, 'wb')
    code_file.write(code.encode('utf8') + '\n.globl __NoTraceHere__\nnop\n__NoTraceHere__:' + suffix)
    code_file.close()
    exec_path = os.path.join(OUTPUT_PATH, problem, identifier + '.out')
    output_path = os.path.join(OUTPUT_PATH, problem, identifier + '.stdout')
    def read_process():
        global proc
        print ' -  Running compiler..'
        p = subprocess.Popen((CC_PATH, code_path, '-o', exec_path, '-I', INCLUDE_PATH, '-m32', '-nostdlib', '-fno-stack-protector'), stderr=subprocess.PIPE)
        code = p.wait()
        line = p.stderr.read()

        print ' -  [program] ', line
        if code != 0:
            return json.dumps({'code': -1, 'output': line.encode('base64'), 'success': 0})

        print ' -  Compiler stopped'

        os.unlink(code_path)
        if os.path.isfile(exec_path):
            print ' -  Compile ok'
            tracer_argv = (TRACER_PATH, exec_path, input_path, '/dev/fd/1')
            print ' -  argv: ' + ' '.join(tracer_argv)
            input_file = open(input_path, 'rb')
            p = subprocess.Popen((OBJDUMP_PATH, '-M', 'intel', '-d', exec_path, ), stdout=subprocess.PIPE)
            line = p.stdout.read()
            result = '--- Here are disassembly for this program (without hidden code)'

            for oneLine in line.split('\n')[3:]:
                if 'NoTraceHere' in oneLine: break
                print oneLine
                result += '\n' + oneLine

            p = subprocess.Popen(tracer_argv, stdout=subprocess.PIPE, stdin=input_file, stderr=subprocess.PIPE)
            line = p.stdout.read() + '\n' + result
            code = p.wait()

            if answer in line:
                print 'it was correct!'
                solved(problem)
                line = line.replace(answer, 'correct!')
                success = True
            else:
                success = False

            print ' -  [program] ', line
#            os.unlink(exec_path)
            return json.dumps({'code': code, 'output': line.encode('base64'), 'success': success})
        else:
            return

    return read_process()

@app.route('/run', methods=['POST'])
def _run():
    if 'user' not in session:
        return redirect('/login')
    source = request.form['source']
    problem = request.form['level']
    if '_' not in problem:
        return ''
    category, name = problem.split('_', 1)
    if category in problems and name in problems[category]['problems']:
        return load_code(problem, source)
    else:
        return ''

if __name__ == '__main__':
    print ' - Loading init.sql'
    init_sql_file = open(INIT_SQL, 'rb')
    init_sql_data = init_sql_file.read()
    init_sql_file.close()

    make_dirs(OUTPUT_PATH)

    with app.app_context():
        print ' -  Executing init.sql'
        get_db().executescript(init_sql_data)
        get_db().commit()
        print ' -  Execution success: init.sql'
        load_problem() # load problem

    app.jinja_env.globals.update(issolved=issolved)
    app.jinja_env.globals.update(load_instruction=load_instruction)
    app.jinja_env.globals.update(load_example=load_example)

    app.debug = True
    app.run(host='0.0.0.0', port=3333)
