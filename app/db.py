import sqlite3
import random
import string


def init_database():
    connection = sqlite3.connect('database.db')


    with open('schema.sql') as f:
        connection.executescript(f.read())

    cur = connection.cursor()

    cur.execute('drop table if exists flags;')
    cur.execute('''create table flags (
      id integer primary key autoincrement,
      level_name TEXT unique not null,
      flag TEXT unique not null,
      solved integer
    );''')

    def get_random_string(length):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))

    flags = []
    for i in range(1, 10):
        flag = get_random_string(10)
        if flag not in flags:
            flags.append(flag)
        else:
            continue

    for i, flag in enumerate(flags):
        cur.execute("insert into flags (level_name, flag, solved) values (?, ?, ?)",
                        ('Zadanie {}'.format(i), flag, 0)
                        )

    connection.commit()
    connection.close()