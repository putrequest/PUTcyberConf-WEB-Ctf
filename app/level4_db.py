import sqlite3
import random
import string


def init_database():
    connection = sqlite3.connect('database_level4.db')


    # with open('schema.sql') as f:
    #     connection.executescript(f.read())

    cur = connection.cursor()

    cur.execute('drop table if exists doors;')
    cur.execute('drop table if exists doors_eng;')
    cur.execute('drop table if exists posts;')

    cur.execute('''create table doors (
          key integer primary key autoincrement,
          id integer,
          author TEXT,
          title TEXT not null,
          content TEXT,
          hidden int
        );''')
    cur.execute("insert into doors (id, author, title, content, hidden) values (?, ?, ?, ?, ?)",
                (1, 'Administrator', 'Kod do Spacerniaka', "Kod: 9326", 0)
                )

    cur.execute("insert into doors (id, author, title, content, hidden) values (?, ?, ?, ?, ?)",
                (2, 'Adam', 'Kod do Stołówki', "Kod: 7503", 0)
                )
    cur.execute("insert into doors (id, author, title, content, hidden) values (?, ?, ?, ?, ?)",
                (3, 'Drużyna AAA', 'Kod do Składziku', "Kod: 0572", 0)
                )
    cur.execute("insert into doors (id, author, title, content, hidden) values (?, ?, ?, ?, ?)",
                (4, 'Administrator', 'Kod do Warsztatu', "Kod: 9326", 0)
                )

    cur.execute("insert into doors (id, author, title, content, hidden) values (?, ?, ?, ?, ?)",
                (5, 'Adam', 'Kod do Piwnicy', "Kod: 7503", 0)
                )
    cur.execute("insert into doors (id, author, title, content, hidden) values (?, ?, ?, ?, ?)",
                (6, 'Drużyna AAA', 'Kod do Gabinetu', "Kod: 0572", 1)
                )
    cur.execute("insert into doors (id, author, title, content, hidden) values (?, ?, ?, ?, ?)",
                (7, 'Administrator', 'Kod do Łazienek', "Kod: 9326", 0)
                )

    cur.execute("insert into doors (id, author, title, content, hidden) values (?, ?, ?, ?, ?)",
                (8, 'Adam', 'Kod do Kaplicy', "Kod: 7503", 0)
                )
    cur.execute("insert into doors (id, author, title, content, hidden) values (?, ?, ?, ?, ?)",
                (9, 'Drużyna AAA', 'Kod do Izolatki', "Kod: 0572", 0)
                )

    cur.execute("insert into doors (id, author, title, content, hidden) values (?, ?, ?, ?, ?)",
                (133, 'Administrator', 'Kod do Sterowni', "Kod: 3341", 1)
                )
    cur.execute('''create table doors_eng (
          key integer primary key autoincrement,
          id integer,
          author TEXT,
          title TEXT not null,
          content TEXT,
          hidden int
        );''')
    cur.execute("insert into doors_eng (id, author, title, content, hidden) values (?, ?, ?, ?, ?)",
                (1, 'Administrator', 'Code to The Yard', "Code: 9326", 0)
                )

    cur.execute("insert into doors_eng (id, author, title, content, hidden) values (?, ?, ?, ?, ?)",
                (2, 'Adam', 'Code to Canteen', "Code: 7503", 0)
                )
    cur.execute("insert into doors_eng (id, author, title, content, hidden) values (?, ?, ?, ?, ?)",
                (3, 'Team AAA', 'Code to Storeroom', "Code: 0572", 0)
                )
    cur.execute("insert into doors_eng (id, author, title, content, hidden) values (?, ?, ?, ?, ?)",
                (4, 'Administrator', 'Code to Workshop', "Code: 9326", 0)
                )

    cur.execute("insert into doors_eng (id, author, title, content, hidden) values (?, ?, ?, ?, ?)",
                (5, 'Adam', 'Code to Cellar', "Code: 7503", 0)
                )
    cur.execute("insert into doors_eng (id, author, title, content, hidden) values (?, ?, ?, ?, ?)",
                (6, 'Team AAA', 'Code to The Office', "Code: 93 million miles", 1)
                )
    cur.execute("insert into doors_eng (id, author, title, content, hidden) values (?, ?, ?, ?, ?)",
                (7, 'Administrator', 'Code to Bathroom', "Code: 9326", 0)
                )

    cur.execute("insert into doors_eng (id, author, title, content, hidden) values (?, ?, ?, ?, ?)",
                (8, 'Adam', 'Code to Chapel', "Code: 7503", 0)
                )
    cur.execute("insert into doors_eng (id, author, title, content, hidden) values (?, ?, ?, ?, ?)",
                (9, 'Drużyna AAA', 'Code to The Isolation ward', "Code: 0572", 0)
                )

    cur.execute("insert into doors_eng (id, author, title, content, hidden) values (?, ?, ?, ?, ?)",
                (133, 'Administrator', 'Code to The Control room', "Code: 3341", 1)
                )
    connection.commit()
    connection.close()