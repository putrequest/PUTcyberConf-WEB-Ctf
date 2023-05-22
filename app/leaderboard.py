from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def update_leaderboard():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    leaderboard_data = c.execute('SELECT username, points FROM users ORDER BY points DESC').fetchall()
    conn.close()

    return leaderboard_data

@app.route('/')
def leaderboard():
    leaderboard_data = update_leaderboard()

    return render_template('leaderboard.html', leaderboard_data=leaderboard_data)

@app.route('/update_board')
def update():
    leaderboard_data = update_leaderboard()

    return render_template('update_board.html', leaderboard_data=leaderboard_data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
