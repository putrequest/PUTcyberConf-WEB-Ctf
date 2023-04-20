import datetime

from flask import *
import os

from werkzeug.utils import secure_filename
import db
import level4_db
import sqlite3
import base64
from flask import make_response, session
from flask_session import Session
import jwt
import math

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def checkLevel(request, conn, reqLevel):
    cursor = conn.cursor()
    cursor.execute('select id from users where hash ="{}"'.format(request.cookies.get('session_id')))
    user_id = cursor.fetchone()

    if user_id is None:
        response = redirect(url_for('login'))
        response.set_cookie('user_id', 'resetting', expires=0)
        response.set_cookie('session_id', 'resetting', expires=0)
        return response

    cursor = conn.cursor()
    cursor.execute('SELECT MAX(level_id) FROM userFlags WHERE user_id = ?', (user_id[0],))
    row = cursor.fetchone()

    if row is None:
        response = redirect(url_for('login'))
        response.set_cookie('user_id', 'resetting', expires=0)
        response.set_cookie('session_id', 'resetting', expires=0)
        return response

    current_level = row[0] or 0
    if not reqLevel == current_level + 1:
        return redirect(url_for('level_0' + str(current_level + 1)))
    return None

def getDiff(user_id, level_id):
    conn = get_db_connection()
    c = conn.cursor()
    print(user_id)
    if level_id == 1:
        # For level 1, use the timestamp from userFlags table where level_id = 1 minus the timestamp from users table
        last_timestamp = c.execute('select timestamp from userFlags where user_id=? and level_id=?', (user_id, 1)).fetchall()[0][0]
        last_timestamp_user = c.execute('select timestamp from users where id=?', (user_id,)).fetchall()[0][0]
        return (datetime.datetime.strptime(last_timestamp, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(last_timestamp_user, '%Y-%m-%d %H:%M:%S.%f')).total_seconds()
    elif level_id == 0:
        return 1
    else:
        # For the other levels, use the timestamp from userFlags table where level_id = current level_id minus the timestamp from userFlags table where level_id = current level_id - 1
        last_timestamp = c.execute('select timestamp from userFlags where user_id=? and level_id=?', (user_id, level_id)).fetchall()[0][0]
        last_timestamp_prev = c.execute('select timestamp from userFlags where user_id=? and level_id=?', (user_id, level_id - 1)).fetchall()[0][0]
        return (datetime.datetime.strptime(last_timestamp, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(last_timestamp_prev, '%Y-%m-%d %H:%M:%S.%f')).total_seconds()

def checkFlag(request, flag, conn, level):
    user_id = \
        conn.execute('select id from users where hash ="{}"'.format(request.cookies.get('session_id'))).fetchall()[0][0]

    # print(request.cookies.get('session_id'));
    row = conn.execute('select * from flags where flag = "{}"'.format(flag)).fetchall()

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
        minutes_elapsed = math.floor(getDiff(user_id, level)/60)
        points_to_add = max(50, 500 - minutes_elapsed * 50)
        conn.execute("update userFlags set points =? where user_id=? AND level_id=?", (points_to_add, user_id, level))
        conn.execute("update users set points = points+? where id=?", (points_to_add, user_id))
        conn.commit()
        conn.close()
        return render_template('flag.html',
                               congrats='Gratuluję! {} zostało rozwiązane.'.format(row[0]['level_name']),
                               page='Zgłoś flagę')

#def checkPoints(level_id):
#    # Get the user ID from the users table by hash
#    conn = get_db_connection()
#    c = conn.cursor()
#    user_id = c.execute('select id from users where hash ="{}"'.format(request.cookies.get('session_id'))).fetchall()[0][0]
#
#    # Calculate the time elapsed since the last attempt
#    # Calculate the points based on the time elapsed and a constant for the level
#    match(level_id):
#        case 0:
#            return 0
#        case 1:
#            level_constant = 10000
#        case 2:
#            level_constant = 20000
#        case 3:
#            level_constant = 30
#
#    points = int(level_constant / time_elapsed)
#
#    # Check if points for this level have already been calculated
#    current_points = c.execute('select points from userFlags where user_id=? and level_id=?', (user_id, level_id)).fetchall()
#    if current_points != 0:
#        points = int(current_points[0][0])
#    else:
#        # Update the userFlags table with the new points
#        c.execute('insert or replace into userFlags (user_id, level_id, timestamp, points) values (user_id, level_id, current_timestamp, ?)', (points))
#        conn.commit()
#
#        # Update the points in the users table
#        current_points = c.execute('select points from users where id=?', (user_id,)).fetchall()[0][0]
#        c.execute('update users set points=? where id=?', (current_points + points, user_id))
#        conn.commit()
#
#    # Return the current points
#    return points

def getPoints():
    conn = get_db_connection()
    c = conn.cursor()
    user_id = c.execute('select username from users where hash ="{}"'.format(request.cookies.get('session_id'))).fetchall()[0][0]
    points = c.execute('select points from users where username=?', (user_id,)).fetchall()[0][0]
    conn.close()
    return [user_id, points]

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
            query = """insert into users (username, hash, timestamp, points) values(?, ?, ?, ?) RETURNING *"""
            # added timestamp to users table and points
            result = conn.execute(query, (user_name, user_hash, datetime.datetime.now(), 0)).fetchall()[0][1]
            conn.commit()
        except sqlite3.IntegrityError as e:
            return render_template('login.html', error='db error ' + e.args[0])
        s = Session()
        s.user_id = user_hash
        s.ip = request.remote_addr
        response = make_response(redirect('/level1'))
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
    redirect_resp = checkLevel(request, conn, 1)
    
    if redirect_resp is not None:
        return redirect_resp

    user_id, points = getPoints()
    flag = conn.execute('select flag from flags where level_name = "Zadanie 1"').fetchall()[0][0]
    if (request.method == 'POST'):
        user_flag = request.form['flag']
        if user_flag == flag:
            checkFlag(request, user_flag, conn, 1)
            # print(checkPoints(1))
            return redirect(url_for('level_02'))
        elif user_flag == '':
            error = 'Nie podano klucza.'
            return render_template('level01.html', error=error, flag=flag, page='Zadanie 1')
        else:
            error = 'Niepoprawny klucz.'
            return render_template('level01.html', error=error, flag=flag, page='Zadanie 1')

    return render_template('level01.html', flag=flag, page='Zadanie 1', username=user_id, points=points)


# @app.route("/level2", methods=['GET', 'POST'])
# def level_02():
#    conn = get_db_connection()
#    flag = conn.execute('select flag from flags where level_name = "Zadanie 2"').fetchall()[0][0]
#    if (request.method == 'POST'):
#        user_flag = request.form['flag']
#        return checkFlag(request, user_flag, conn, 2)
#
#    return render_template('level02.html', flag=flag, page='Zadanie 2')

@app.route("/level2", methods=['GET', 'POST'])
def level_02():
    conn = get_db_connection()
    redirect_resp = checkLevel(request, conn, 2)
    if redirect_resp is not None:
        return redirect_resp
    user_id, points = getPoints()
    return render_template('level02.html', page='Zadanie 2',username=user_id, points=points)

@app.route("/robots.txt", methods=['GET', 'POST'])
def robots():
    conn = get_db_connection()
    redirect_resp = checkLevel(request, conn, 2)
    if redirect_resp is not None:
        return redirect_resp
    
    robots = open("static/files/robots.txt", 'r').read()
    return render_template('level02_robots.html', robots=robots)


@app.route('/blok-D/cela-6132/Mopsik', methods=['GET', 'POST'])
def level_02_Mops():
    conn = get_db_connection()
    redirect_resp = checkLevel(request, conn, 2)
    if redirect_resp is not None:
        return redirect_resp
    user_id, points = getPoints()

    if request.method == 'POST':
        if request.form.get('Idziemy dalej!') == 'Idziemy dalej!':
            conn = get_db_connection()
            flag = conn.execute('select flag from flags where level_name = "Zadanie 2"').fetchall()[0][0]
            checkFlag(request, flag, conn, 2)
            conn.close()
            return redirect(url_for('level_03'))
    conn = get_db_connection()
    checkLevel(request, conn, 2)

    return render_template('level02_flag.html', page='Zadanie 2',username=user_id, points=points)


@app.route('/level3', methods=['GET', 'POST'])
def level_03():
    error = None

    conn = get_db_connection()
    redirect_resp = checkLevel(request, conn, 3)
    if redirect_resp is not None:
        return redirect_resp
    user_id, points = getPoints()

    if request.method == 'POST':
        if request.form.get('Idziemy dalej!') == 'Idziemy dalej!':
            conn = get_db_connection()
            flag = conn.execute('select flag from flags where level_name = "Zadanie 3"').fetchall()[0][0]
            checkFlag(request, flag, conn, 3)
            conn.close()
            return redirect(url_for('level_04'))

    if request.cookies.get('admin'):
        if request.cookies.get('admin') == "true":
            resp = make_response(render_template('level03_flag.html', page='Zadanie 3'))
            return resp

    if request.method == 'POST':
        if request.form['username'] == 'putrequest' and request.form['password'] == 'bardzotrudnehaslo':
            resp = make_response(render_template('level03_page.html', page='Zadanie 3'))
            resp.set_cookie('admin', "false")
            return resp
        else:
            error = 'Niepoprawne dane logowania.'
            return render_template('level03_login.html', error=error, page='Zadanie 3')
    return render_template('level03_login.html', page='Zadanie 3',username=user_id, points=points)


@app.route("/level4", methods=['GET', 'POST'])
def level_04():
    conn = get_db_connection()
    redirect_resp = checkLevel(request, conn, 4)
    if redirect_resp is not None:
        return redirect_resp
    user_id, points = getPoints()

    if request.method == 'POST':
        if request.form['key']:

            key = request.form['key']

            conn = get_level4_db_connection()
            query = "select * from doors where title = '%s' AND hidden = 0" % (key)
            p = conn.execute(query).fetchall()
            conn.close()
            # 'OR 1=1--
            if p:
                print(p[0])
                return render_template('level04.html', posts=p, page='Zadanie 4')
            else:
                return render_template('level04.html', error="Brak odpowiedzi na zapytanie", page='Zadanie 4')
        else:
            conn = get_level4_db_connection()
            p = conn.execute("select * from doors where hidden = 0").fetchall()
            conn.close()
            return render_template('level04.html', posts=p, page='Zadanie 4',username=user_id, points=points)

    else:
        conn = get_level4_db_connection()
        p = conn.execute("select * from doors where hidden = 0").fetchall()
        conn.close()
        return render_template('level04.html', posts=p, page='Zadanie 4',username=user_id, points=points)


@app.route("/level4/post/<id>", methods=['GET', 'POST'])
def level_04_post(id):
    conn = get_db_connection()
    redirect_resp = checkLevel(request, conn, 4)
    if redirect_resp is not None:
        return redirect_resp


    if request.method == 'POST':
        if request.form.get('btn-succes') == 'Następne zadanie!':
            conn = get_db_connection()
            flag = conn.execute('select flag from flags where level_name = "Zadanie 3"').fetchall()[0][0]
            checkFlag(request, flag, conn, 4)
            conn.close()
            return redirect(url_for('level_05'))

    user_id, points = getPoints()


    try:
        conn = get_level4_db_connection()
        query = """select * from doors where id = ?"""
        p = conn.execute(query, (id,)).fetchall()[0]
        conn.close()
        return render_template('level04_page.html', object=p, page='Zadanie 4',username=user_id, points=points)
    except Exception as e:
        return render_template('404.html')


def get_level4_db_connection():
    conn = sqlite3.connect('database_level4.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/level5', methods=['GET', 'POST'])
def level_05():
    conn = get_db_connection()
    redirect_resp = checkLevel(request, conn, 5)
    if redirect_resp is not None:
        return redirect_resp
    user_id, points = getPoints()

    rec = url_for('static', filename='files/camera_video.gif')
    allowed_extensions = {'.png', '.jpg', '.jpeg'}
    if request.method == 'POST':

        if request.form.get('Idziemy dalej!') == 'Idziemy dalej!':
            conn = get_db_connection()
            flag = conn.execute('select flag from flags where level_name = "Zadanie 5"').fetchall()[0][0]
            checkFlag(request, flag, conn, 5)
            conn.close()
            return redirect(url_for('level_06'))


        # POST payload could be empty or the file could be missing a filename
        if 'file' not in request.files or not request.files['file'].filename:
            error = 'Nie wybrano pliku'
            return render_template('level05_upload.html', page='Zadanie 5', error=error, rec=rec,username=user_id, points=points)

        # Sanitize the filename
        # https://flask.palletsprojects.com/en/2.2.x/patterns/fileuploads/
        fileName = secure_filename(request.files['file'].filename)
        fileExt = os.path.splitext(fileName)[1]

        if fileExt == '.php5':
            rec = url_for('static', filename='files/Never.gif')
            return render_template('level05_upload.html', page='Zadanie 5', rec=rec, done=True,username=user_id, points=points)
        elif fileExt not in allowed_extensions:
            error = 'Zabronione rozszerzenie pliku'
            return render_template('level05_upload.html', page='Zadanie 5', error=error, rec=rec,username=user_id, points=points)
        else:
            print('Załadowano plik')
            success = 'Plik został załadowany pomyślnie'
            return render_template('level05_upload.html', page='Zadanie 5', rec=rec, success=success,username=user_id, points=points)

    return render_template('level05_upload.html', page='Zadanie 5', rec=rec, username=user_id, points=points)


@app.route('/level6', methods=['GET', 'POST'])
# JWT dla Makłowicza eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbWnEmSI6IlJvYmVydCBXaXRvbGQgTWFrxYJvd2ljeiIsImRhdGFfdXJvZHplbmlhIjoiMTIuMDcuMTk2MyIsInJvbGEiOiJ3acSZemllxYQiLCJFRUVFRUVFIjoxMDQsIkRlbGZpbnkiOiJhaGFoaGFoYWhhaGFoYWhhaGEifQ.deyO8lu_qgRY6y_AFHRIc8C0ChpG_bdsgFwSggn9E20
def level_06():
    conn = get_db_connection()
    redirect_resp = checkLevel(request, conn, 6)
    if redirect_resp is not None:
        return redirect_resp
    user_id, points = getPoints()

    # def_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbWnEmSI6IlJvYmVydCBXaXRvbGQgTWFrxYJvd2ljeiIsImRhdGFfdXJvZHplbmlhIjoiMTIuMDcuMTk2MyIsInJvbGEiOiJ3acSZemllxYQiLCJFRUVFRUVFIjoxMDQsIkRlbGZpbnkiOiJhaGFoaGFoYWhhaGFoYWhhaGEifQ.deyO8lu_qgRY6y_AFHRIc8C0ChpG_bdsgFwSggn9E20'
    error = None
    JWTsecret = "832p13c2ny_k1uc2"
    def_token = jwt.encode({'imie': "Robert Witold Makłowicz",
                            'data_ur': "12.07.1963",
                            'rola': "więzień",
                            'EEEEEE': 104,
                            'delfiny': "ahahahahahahahah"},
                           JWTsecret, algorithm='HS256')

    resp = make_response(render_template('level06_page.html', page='Zadanie 6',username=user_id, points=points))
    set_token = request.cookies.get('token')

    if request.method == 'POST':
        if request.form.get('Idziemy dalej!') == 'Idziemy dalej!':
            return redirect('/level7/dane/21')

    if set_token is None:
        resp.set_cookie('token', def_token)
        return resp

    key = ""
    try:
        key = jwt.decode(set_token, JWTsecret, algorithms=['HS256'])['rola']
    except (jwt.DecodeError, TypeError):
        resp.set_cookie('token', def_token)
        return resp

    if key == "strażnik":
        conn = get_db_connection()
        flag = conn.execute('select flag from flags where level_name = "Zadanie 6"').fetchall()[0][0]
        checkFlag(request, flag, conn, 6)
        conn.close()
        resp = make_response(render_template('level06_flag.html', flag=flag, page='Zadanie 6',username=user_id, points=points))
        return resp

    return resp


@app.route("/level7/dane/<id>", methods=['GET', 'POST'])
# id Makłowicza 21 trzeba zmienić na 3
def level_07_dane(id):
    conn = get_db_connection()
    redirect_resp = checkLevel(request, conn, 7)
    if redirect_resp is not None:
        return redirect_resp

    user_id, points = getPoints()

    if request.method == 'POST':
        if request.form.get('next') == 'Ustaw Profil':
            conn = get_db_connection()
            query = """select * from data_guards where id = ?"""
            p = conn.execute(query, (id,)).fetchall()[0]
            conn.close()
            if id == '3':
                conn = get_db_connection()
                flag = conn.execute('select flag from flags where level_name = "Zadanie 7"').fetchall()[0][0]
                checkFlag(request, flag, conn, 7)
                conn.close()
                success = 'Gratulacje! Ustawiono profil.'
                return render_template('level07_guard.html', success=success, page='Zadanie 7', object=p,username=user_id, points=points)
                # return redirect("/")
            else:
                error = 'Nie udało się ustawić profilu. Osoba nie jest podobna do Makłowicza.'
                return render_template('level07_guard.html', error=error, page='Zadanie 7', object=p,username=user_id, points=points)
    try:
        if int(id) >= 10:
            conn = get_db_connection()
            query = """select * from data_prisoners where id = ?"""
            p = conn.execute(query, (id,)).fetchall()[0]
            conn.close()
            return render_template('level07_prisoner.html', object=p, page='Zadanie 7',username=user_id, points=points)
        else:
            conn = get_db_connection()
            query = """select * from data_guards where id = ?"""
            p = conn.execute(query, (id,)).fetchall()[0]
            conn.close()

            return render_template('level07_guard.html', object=p, page='Zadanie 7',username=user_id, points=points)
    except Exception as e:
        return render_template('404.html')


@app.route('/level8', methods=['FLAG'])
def level_08():
    user_id, points = getPoints()
    if request.method == 'FLAG':
        if request.form.get('Klknij mnie!') == 'Klknij mnie!':
            conn = get_db_connection()
            flag = conn.execute('select flag from flags where level_name = "Zadanie 8"').fetchall()[0][0]
            checkFlag(request, flag, conn, 8)
            conn.close()
            return render_template('Main_opis.html', page='Zadanie 8', data="Dziękujemy że byliście z nami! To już definitywny koniec:)")

        return render_template('level08.html', page='Zadanie 8')

    else:
        return render_template('level08.html', info="JUST GET THE FLAG :)", page='Zadanie 8',username=user_id, points=points)


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
    level4_db.init_database()
    app.run(host='127.0.0.1', port=8000, debug=False)
