import sqlite3
import random
import string


def init_database():
    connection = sqlite3.connect('database.db')


    # with open('schema.sql') as f:
    #     connection.executescript(f.read())

    cur = connection.cursor()

    cur.execute('drop table if exists flags;')
    cur.execute('drop table if exists posts;')
    cur.execute('''create table flags (
      id integer primary key autoincrement,
      level_name TEXT unique not null,
      flag TEXT unique not null,
      hidden integer,
      solved integer
    );''')

    def get_random_string(length):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))

    flags = []
    for i in range(1, 10):
        flag = get_random_string(10)
        if flag not in flags:
            flags.append('putrequest{'+flag+'}')
        else:
            continue
    hidden = 0
    for i, flag in enumerate(flags):
        if (i + 1) >= 8:
            hidden = 1
        cur.execute("insert into flags (level_name, flag, hidden, solved) values (?, ?, ?, ?)",
                        ('Zadanie {}'.format(i + 1), flag, hidden, 0)
                        )

    with open('static\\files\\flag.txt', 'w') as file:
        file.write(flags[4])

    cur.execute('''create table posts (
      key integer primary key autoincrement,
      id integer,
      author TEXT,
      title TEXT not null,
      content TEXT,
      hidden int
    );''')
    cur.execute("insert into posts (id, author, title, content, hidden) values (?, ?, ?, ?, ?)",
                (1, 'Administrator', 'Cześć', '''Miło mi że wszedłeś na naszego bloga. Wraz ze znajomymi będziemy umieszczać tu relacje z naszego życia. Do zobaczenia w następnych postach.''', 0)
                )

    cur.execute("insert into posts (id, author, title, content, hidden) values (?, ?, ?, ?, ?)",
                (2, 'Adam', 'Przedstawienie', '''Pora abyście poznali naszę ekipę. Jesteśmy grupą trzech osób pozytywnie zakręconych na punkcie pieszych wycieczek i aktywnego spędzania czasu wolnego. W następnych postach będziemy dzieli się informacjami jak sprawinie i bezpiecznie podróżować. Do zobaczenia na szlaku: Adam, Artur, Andrzej! ''', 0)
                )
    cur.execute("insert into posts (id, author, title, content, hidden) values (?, ?, ?, ?, ?)",
                (3, 'Drużyna AAA', 'Porada', '''Nigdy nie zapominaj o zabraniu na wyprawę koca termicznego - w kryzysowej sytuacji może posłużyć on do budoty prowizorycznego schronienia.''', 0)
                )

    cur.execute("insert into posts (id, author, title, content, hidden) values (?, ?, ?, ?, ?)",
                (27, 'Administrator', 'Flaga', flags[3], 1)
                )
    connection.commit()
    connection.close()