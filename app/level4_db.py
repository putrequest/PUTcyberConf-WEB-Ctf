import sqlite3
import random
import string


def init_database():
    connection = sqlite3.connect('database_level4.db')


    # with open('schema.sql') as f:
    #     connection.executescript(f.read())

    cur = connection.cursor()

    cur.execute('drop table if exists doors;')
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
                (1, 'Administrator', 'Kod do Spacerniaka', "Kod do klucza: 9326", 0)
                )

    cur.execute("insert into doors (id, author, title, content, hidden) values (?, ?, ?, ?, ?)",
                (2, 'Adam', 'Kod do Stołówki', "Kod do klucza: 7503", 0)
                )
    cur.execute("insert into doors (id, author, title, content, hidden) values (?, ?, ?, ?, ?)",
                (3, 'Drużyna AAA', 'Kod do Składziku', "Kod do klucza: 0572", 0)
                )
    cur.execute("insert into doors (id, author, title, content, hidden) values (?, ?, ?, ?, ?)",
                (4, 'Administrator', 'Kod do Warsztatu', "Kod do klucza: 9326", 0)
                )

    cur.execute("insert into doors (id, author, title, content, hidden) values (?, ?, ?, ?, ?)",
                (5, 'Adam', 'Kod do Piwnicy', "Kod do klucza: 7503", 0)
                )
    cur.execute("insert into doors (id, author, title, content, hidden) values (?, ?, ?, ?, ?)",
                (6, 'Drużyna AAA', 'Kod do Gabinetu', "Kod do klucza: 0572", 0)
                )
    cur.execute("insert into doors (id, author, title, content, hidden) values (?, ?, ?, ?, ?)",
                (7, 'Administrator', 'Kod do Łazienek', "Kod do klucza: 9326", 0)
                )

    cur.execute("insert into doors (id, author, title, content, hidden) values (?, ?, ?, ?, ?)",
                (8, 'Adam', 'Kod do Kaplicy', "Kod do klucza: 7503", 0)
                )
    cur.execute("insert into doors (id, author, title, content, hidden) values (?, ?, ?, ?, ?)",
                (9, 'Drużyna AAA', 'Kod do Izolatki', "Kod do klucza: 0572", 0)
                )

    cur.execute("insert into doors (id, author, title, content, hidden) values (?, ?, ?, ?, ?)",
                (133, 'Administrator', 'Kod do Sterowni', "Kod do klucza: 3341", 1)
                )
    connection.commit()
    connection.close()