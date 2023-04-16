import sqlite3
import random
import string


def init_database():
    connection = sqlite3.connect('database_level4.db')


    # with open('schema.sql') as f:
    #     connection.executescript(f.read())

    cur = connection.cursor()

    cur.execute('drop table if exists users;')

    cur.execute('''create table users(
    id integer primary key autoincrement,
    username TEXT unique not null,
    password TEXT not null
    );''')

    cur.execute("insert into users (id, username, password) values (?, ?, ?)",
                (1, 'Administrator', 'Cześć')
                )
    cur.execute("insert into users (id, username, password) values (?, ?, ?)",
                (2, 'PHPPrzemo', 'ArkaGdynia...')
                )
    cur.execute("insert into users (id, username, password) values (?, ?, ?)",
                (3, 'GordonRam', 'UżyjDropa')
                )
    cur.execute("insert into users (id, username, password) values (?, ?, ?)",
                (4, 'ZnanyAgentKwadrat', 'PR{Dr0pp3r_MC_SteeringDoor_50252541965624420956295H')
                )
    cur.execute("insert into users (id, username, password) values (?, ?, ?)",
                (5, 'test', 'test')
                )

    connection.commit()
    connection.close()