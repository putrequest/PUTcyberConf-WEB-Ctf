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
        file.write('putrequest{' + flags[4] + '}')

    cur.execute('''create table posts (
      id integer primary key,
      author TEXT,
      title TEXT not null,
      content TEXT,
      hidden int
    );''')
    cur.execute("insert into posts (id, author, title, content, hidden) values (?, ?, ?, ?, ?)",
                (1, 'a', 'Test', '''Content Content Content Content Content Content Content Content Content Content 
                Content Content Content Content Content Content Content Content Content Content Content Content Content 
                Content Content Content Content Content Content Content Content ''', 0)
                )

    cur.execute("insert into posts (id, author, title, content, hidden) values (?, ?, ?, ?, ?)",
                (2, 'b', 'Test1', '''Content1 Content Content Content Content Content Content Content Content Content 
                Content Content Content Content Content Content Content Content Content Content Content Content Content 
                Content Content Content Content Content Content Content Content ''', 1)
                )
    cur.execute("insert into posts (id, author, title, content, hidden) values (?, ?, ?, ?, ?)",
                (3, 'c', 'Test1', '''Content1 Content Content Content Content Content Content Content Content Content 
                Content Content Content Content Content Content Content Content Content Content Content Content Content 
                Content Content Content Content Content Content Content Content ''', 0)
                )

    connection.commit()
    connection.close()