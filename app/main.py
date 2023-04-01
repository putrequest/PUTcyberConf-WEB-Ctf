import datetime

import requests
from flask import *
import os
import db
import sqlite3
import base64
from flask import make_response, session
from flask_session import Session

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def checkFlag(request, conn, level):
    user_id = \
        conn.execute('select id from users where hash ="{}"'.format(request.cookies.get('session_id'))).fetchall()[0][0]

    # print(request.cookies.get('session_id'));
    row = conn.execute('select * from flags where flag = "{}"'.format(request.form['flag'])).fetchall()

    conn.close()
    if len(row) == 1:
        conn = get_db_connection()
        q2 = """insert into userFlags(user_id, level_id, timestamp) values (?, ?, ?)"""
        conn.execute(q2, (user_id, level, datetime.datetime.now()))
        q = """update flags set solved = 1 where id = {}""".format(row[0]['id'])
        # print(q)
        e = conn.execute(q)
        # print(e)
        conn.commit()
        conn.close()
        return render_template('flag.html',
                               congrats='Gratuluję! {} zostało rozwiązane.'.format(row[0]['level_name']),
                               page='Zgłoś flagę')


@app.route("/favicon.ico")
def main_css():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsof.icon')


@app.route("/login.css")
def styles():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'login.css')


@app.route("/main.css")
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'main.css')


@app.route("/login", methods=['GET', 'POST'])
def login():
    conn = get_db_connection()
    render_template("login.html")
    if request.method == 'POST':
        user_name = request.form['username']
        if len(user_name) < 4:
            error = "username should be at least 4 symbols lenght"
            return render_template('login.html', error=error, page='login')
        try:
            user_hash = str(hash(user_name))
            query = """insert into users (username, hash) values(?, ?) RETURNING *"""
            result = conn.execute(query, (user_name, user_hash,)).fetchall()[0][1]
            conn.commit()
        except sqlite3.IntegrityError as e:
            return render_template('login.html', error='db error ' + e.args[0])
        s = Session()
        s.user_id = user_hash
        s.ip = request.remote_addr
        response = make_response(redirect('/'))
        response.set_cookie('user_id', result)
        response.set_cookie('session_id', s.user_id)
        return response
        # return redirect(url_for('index'))
    else:
        return render_template('login.html')


@app.before_request
def before_request():
    if not request.cookies.get('session_id') and request.endpoint != 'login':
        return redirect(url_for('login'))

@app.route("/")
def index():
    conn = get_db_connection()

    names = conn.execute('select id, level_name, solved from flags where hidden = 0').fetchall()
    conn.close()
    return render_template('index.html', data=names)


@app.route("/level1", methods=['GET', 'POST'])
def level_01():
    conn = get_db_connection()

    flag = conn.execute('select flag from flags where level_name = "Zadanie 1"').fetchall()[0][0]
    if (request.method == 'POST'):
        return checkFlag(request, conn, 1)

    return render_template('level01.html', flag=flag, page='Zadanie 1')


@app.route('/level2', methods=['GET', 'POST'])
def level_02():
    error = None
    if request.cookies.get('admin'):
        if request.cookies.get('admin') == "true":
            conn = get_db_connection()
            flag = conn.execute('select flag from flags where level_name = "Zadanie 2"').fetchall()[0][0]
            conn.close()
            resp = make_response(render_template('level02_flag.html', flag=flag, page='Zadanie 2'))
            return resp
    if request.method == 'POST':
        if request.form['username'] == 'putrequest' and request.form['password'] == 'bardzotrudnehaslo':
            resp = make_response(render_template('level02_page.html', page='Zadanie 2'))
            return resp
        else:
            error = 'Niepoprawne dane logowania.'
            return render_template('level02_login.html', error=error, page='Zadanie 2')
    return render_template('level02_login.html', page='Zadanie 2')


@app.route("/level2flag", methods=['GET', 'POST'])
def level_02_flag():
    if request.cookies.get('admin'):
        if request.cookies.get('admin') == "true":

            conn = get_db_connection()
            flag = conn.execute('select flag from flags where level_name = "Zadanie 2"').fetchall()[0][0]
            if request.method == 'POST':

                return checkFlag(request, conn, 2)
            conn.close()
        else:
            return render_template('404.html')
    else:
        return render_template('404.html')
    return render_template('level02_flag.html', flag=flag, page='Zadanie 2')


@app.route("/level3")
def level_03():
    conn = get_db_connection()
    flag = conn.execute('select flag from flags where level_name = "Zadanie 3"').fetchall()[0][0]
    conn.close()
    return render_template('level03.html', flag=base64.b64encode(flag.encode('ascii')).decode("ascii"),
                           page='Zadanie 3')


@app.route("/level4")
def level_04():
    conn = get_db_connection()
    p = conn.execute('select * from posts where hidden = 0').fetchall()
    conn.close()
    return render_template('level04.html', posts=p, page='Zadanie 4')

##def level_04():
##    conn = get_db_connection()
##    p = conn.execute('select * from posts where hidden = 0').fetchall()
##    conn.close()
##    return render_template('level04.html', posts=p, page='Zadanie 4')


@app.route("/level4/post/<id>")
def level_04_post(id):
    try:
        conn = get_db_connection()
        query = """select * from posts where id = ?"""
        p = conn.execute(query, (id,)).fetchall()[0]
        conn.close()
        return render_template('level04_post.html', object=p, page='Zadanie 4')
    except Exception as e:
        return render_template('404.html')


@app.route('/level5')
def level_05():
    filename = request.args.get('filename', default='test.txt', type=str)
    path = 'static\\files\\{}'.format(filename)
    if os.path.isdir(path):
        return '''Zawartość folderu {}:\n{}'''.format(path, '\n'.join(os.listdir(path)))
    elif os.path.isfile(path):
        with open(path, 'r') as file:
            return file.read()
    else:
        return "Nierozpoznane."


@app.route('/level6', methods=['GET', 'POST'])
def level_06():
    error = None
    if request.cookies.get('admin'):
        if request.cookies.get('admin') == "1":
            conn = get_db_connection()
            flag = conn.execute('select flag from flags where level_name = "Zadanie 6"').fetchall()[0][0]
            conn.close()
            resp = make_response(render_template('level06_flag.html', flag=flag, page='Zadanie 6'))
            resp.set_cookie('admin', '1')
            return resp
    if request.method == 'POST':
        if request.form['username'] == 'putrequest' and request.form['password'] == 'bardzotrudnehaslo':
            resp = make_response(render_template('level06_page.html', page='Zadanie 6'))
            resp.set_cookie('admin', '0')
            return resp
        else:
            error = 'Niepoprawne dane logowania.'
            return render_template('level06_login.html', error=error, page='Zadanie 6')
    return render_template('level06_login.html', page='Zadanie 6')


@app.route('/level7', methods=['GET', 'POST'])
def level_07():
    if request.method == 'POST':
        if request.form['query'].lower().strip() == 'flag':
            conn = get_db_connection()
            flag = conn.execute('select flag from flags where level_name = "Zadanie 7"').fetchall()[0][0]
            conn.close()
            return render_template('level07_flag.html', data=flag, page='Zadanie 7')
        else:
            return render_template('level07_flag.html', data=request.form['query'].lower().strip(), page='Zadanie 7')
    return render_template('level07.html', data={}, page='Zadanie 7')


@app.route('/hidden9182', methods=['GET', 'POST'])
def level_08():
    if request.method == 'POST':
        if 'alert(\'flag\')' in request.form['query'].lower().strip():
            conn = get_db_connection()
            flag = conn.execute('select flag from flags where level_name = "Zadanie 8"').fetchall()[0][0]
            conn.close()
            return render_template('level08_flag.html', data='<script>alert(\"' + flag + '\")</script>',
                                   page='Zadanie 8')
        else:
            return render_template('level08_flag.html', data=request.form['query'].lower().strip(), page='Zadanie 8')
    return render_template('level08.html', data={}, page='Zadanie 8')


@app.route('/help')
def help():
    return render_template('help.html', page='Podręcznik')


@app.route('/flag', methods=['GET', 'POST'])
def flag():
    if request.method == 'POST':
        if request.form['flag']:
            conn = get_db_connection()
            row = conn.execute('select * from flags where flag = "{}"'.format(request.form['flag'])).fetchall()
            conn.close()
            if len(row) == 1:
                conn = get_db_connection()
                q = """update flags set solved = 1 where id = {}""".format(row[0]['id'])
                # print(q)

                e = conn.execute(q)
                # print(e)
                conn.commit()
                conn.close()
                return render_template('flag.html',
                                       congrats='Gratuluję! {} zostało rozwiązane.'.format(row[0]['level_name']),
                                       page='Zgłoś flagę')
            else:
                return render_template('flag.html', congrats='Nieprawidowa flaga.', page='Zgłoś flagę')
        else:
            return redirect(url_for('flag'))
    return render_template('flag.html', page='Złoś flagę')


if __name__ == '__main__':
    db.init_database()
    app.run(host='127.0.0.1', port=8000, debug=True)
