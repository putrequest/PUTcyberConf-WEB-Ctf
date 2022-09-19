from flask import *
import os
import db
import sqlite3
import base64

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/favicon.ico")
def main_css():
	return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico',mimetype='image/vnd.microsof.icon')

@app.route("/main.css")
def favicon():
	return send_from_directory(os.path.join(app.root_path, 'static'),'main.css')

@app.route("/")
def index():
    conn = get_db_connection()
    names = conn.execute('select level_name from flags where hidden = 0').fetchall()
    conn.close()
    return render_template('index.html', data=names)

@app.route("/level1")
def level_01():
    conn = get_db_connection()
    flag = conn.execute('select flag from flags where level_name = "Zadanie 1"').fetchall()[0][0]
    conn.close()
    return render_template('level01.html', flag='{'+flag+'}')

@app.route('/level2', methods=['GET', 'POST'])
def level_02():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'putrequest' or request.form['password'] != 'ce7664fdd1b2863dc28c718c15b911ed':
            error = 'Niepoprawne dane logowania.'
        else:
            return redirect(url_for('level_02_flag'))
    return render_template('level02.html', error=error)

@app.route("/level2flag")
def level_02_flag():
    conn = get_db_connection()
    flag = conn.execute('select flag from flags where level_name = "Zadanie 2"').fetchall()[0][0]
    conn.close()
    return render_template('level02_flag.html', flag='{'+flag+'}')

@app.route("/level3")
def level_03():
    conn = get_db_connection()
    flag = conn.execute('select flag from flags where level_name = "Zadanie 3"').fetchall()[0][0]
    conn.close()
    f = 'putrequest{'+flag+'}'
    return render_template('level03.html', flag=base64.b64encode(f.encode('ascii')).decode("ascii"))

@app.route("/level4")
def level_04():
    conn = get_db_connection()
    p = conn.execute('select * from posts where hidden = 0').fetchall()
    conn.close()
    print(p)
    return render_template('level04.html', posts=p)

@app.route("/level4/post/<id>")
def level_04_post(id):
    try:
        conn = get_db_connection()
        query = """select * from posts where id = ?"""
        p = conn.execute(query, (id)).fetchall()[0]
        conn.close()
        return render_template('level04_post.html', object=p)
    except:
        return render_template('404.html')

@app.route('/level5')
def hello():
    return redirect("/level5/test.txt", code=302)


@app.route('/level5/<filename>')
def level_05(filename):
    with open('static\\files\\{}'.format(filename), 'r') as file:
        return file.read()

@app.route('/level6', methods=['GET', 'POST'])
def level_06():
    error = None
    if request.cookies.get('admin'):
        if request.cookies.get('admin') == "1":
            conn = get_db_connection()
            flag = conn.execute('select flag from flags where level_name = "Zadanie 6"').fetchall()[0][0]
            conn.close()
            resp = make_response(render_template('level06_flag.html', flag = 'putrequest{' + flag + '}'))
            resp.set_cookie('admin', '1')
            return resp
    if request.method == 'POST':
        if request.form['username'] != 'putrequest' or request.form['password'] != 'ce7664fdd1b2863dc28c718c15b911ed':
            error = 'Niepoprawne dane logowania.'
        else:
            resp = make_response(render_template('level06_page.html'))
            resp.set_cookie('admin', '0')
            return resp

    return render_template('level06_login.html', error=error)

@app.route('/level7')
def level_07():
    return render_template('level07.html', data={})

if __name__ == '__main__':
    db.init_database()
    app.run(host='127.0.0.1', port=8000, debug=True)