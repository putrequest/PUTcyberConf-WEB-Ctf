from flask import *
import os
import db
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/favicon.ico")
def favicon():
	return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico',mimetype='image/vnd.microsof.icon')

@app.route("/")
def hello_world():
    conn = get_db_connection()
    names = conn.execute('select level_name from flags').fetchall()
    conn.close()
    print(names)
    return render_template('index.html', data=names)

if __name__ == '__main__':
    db.init_database()
    app.run(host='127.0.0.1', port=8000, debug=True)