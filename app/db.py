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
    cur.execute('drop table if exists users;')
    cur.execute('drop table if exists userFlags;')
    cur.execute('drop table if exists data_prisoners;')
    cur.execute('drop table if exists data_guards;')
    cur.execute('''create table users(
    id integer primary key autoincrement,
    username TEXT unique not null,
    hash TEXT unique not null
    );''')
    cur.execute('''create table userFlags(
    id integer primary key autoincrement,
    user_id integer,
    level_id integer,
    timestamp timestamp
    );''')
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
            flags.append('PRctf{'+flag+'}')
        else:
            continue
    hidden = 0
    for i, flag in enumerate(flags):
        if (i + 1) >= 8:
            hidden = 1
        cur.execute("insert into flags (level_name, flag, hidden, solved) values (?, ?, ?, ?)",
                        ('Zadanie {}'.format(i + 1), flag, hidden, 0)
                        )

    #cur.execute("update flags set flag ='PR{Dr0pp3r_MC_SteeringDoor_50252541965624420956295H' WHERE id = 4 ")

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
                (3, 'Drużyna AAA', 'Porada', '''Nigdy nie zapominaj o zabraniu na wyprawę koca termicznego - w kryzysowej sytuacji może posłużyć on do budowy prowizorycznego schronienia.''', 0)
                )

    cur.execute("insert into posts (id, author, title, content, hidden) values (?, ?, ?, ?, ?)",
                (27, 'Administrator', 'Flaga', flags[3], 1)
                )
    
    cur.execute('''create table data_prisoners (
      key integer primary key autoincrement,
      id TEXT,
      name TEXT,
      b_date TEXT,
      r_date TEXT,
      blok TEXT,
      cellnumber TEXT,
      diet TEXT,
      sentence TEXT,
      job TEXT
    );''')

    cur.execute('''create table data_guards (
      key integer primary key autoincrement,
      id TEXT,
      name TEXT,
      b_date TEXT,
      start_date TEXT,
      rank TEXT,
      salary TEXT,
      blok TEXT,
      phone TEXT
    );''')
#przykładowe dane do tabeli data_prisoners
##########################################################################################################################################
    cur.execute("insert into data_prisoners (id, name, b_date, r_date, blok, cellnumber, diet, sentence, job) values (?, ?, ?, ?, ?, ?, ?, ?, ?)", ('10', 'Robert Witold Makłowicz', '12.08.1963', '21.07.2037', 'D', 'D-2138', 'Mięsna', 'Kradziez z włamaniem', 'Kucharz')
                    )
    cur.execute("insert into data_prisoners (id, name, b_date, r_date, blok, cellnumber, diet, sentence, job) values (?, ?, ?, ?, ?, ?, ?, ?, ?)", ('11', 'Adam Kowalski', '01.01.1980', '15.01.2030', 'A', 'A-123', 'Bezmięsna', 'Kradzież', 'Elektryk')
                    )
    cur.execute("insert into data_prisoners (id, name, b_date, r_date, blok, cellnumber, diet, sentence, job) values (?, ?, ?, ?, ?, ?, ?, ?, ?)", ('12', 'Karol Nowak', '15.03.1992', '25.03.2034', 'B', 'B-231', 'Wegetariańska', 'Napad', 'Stolarz')
                    )
    cur.execute("insert into data_prisoners (id, name, b_date, r_date, blok, cellnumber, diet, sentence, job) values (?, ?, ?, ?, ?, ?, ?, ?, ?)", ('13', 'Alicja Nowakowska', '05.05.1985', '05.05.2030', 'C', 'C-012', 'Halal', 'Oszustwo', 'Nauczycielka')
                    )
    cur.execute("insert into data_prisoners (id, name, b_date, r_date, blok, cellnumber, diet, sentence, job) values (?, ?, ?, ?, ?, ?, ?, ?, ?)", ('14', 'Piotr Jankowski', '20.07.1976', '20.07.2031', 'A', 'A-456', 'Bezmięsna', 'Napad z bronią', 'Kierowca')
                    )
    cur.execute("insert into data_prisoners (id, name, b_date, r_date, blok, cellnumber, diet, sentence, job) values (?, ?, ?, ?, ?, ?, ?, ?, ?)", ('15', 'Monika Nowacka', '10.10.1990', '10.10.2035', 'D', 'D-789', 'Wegetariańska', 'Przemoc w rodzinie', 'Fryzjerka')
                    )
    cur.execute("insert into data_prisoners (id, name, b_date, r_date, blok, cellnumber, diet, sentence, job) values (?, ?, ?, ?, ?, ?, ?, ?, ?)", ('16', 'Tomasz Kozłowski', '22.12.1982', '22.12.2030', 'B', 'B-567', 'Halal', 'Posiadanie narkotyków', 'Sprzątacz')
                    )
    cur.execute("insert into data_prisoners (id, name, b_date, r_date, blok, cellnumber, diet, sentence, job) values (?, ?, ?, ?, ?, ?, ?, ?, ?)", ('17', 'Katarzyna Wiśniewska', '30.05.1988', '30.05.2033', 'C', 'C-456', 'Bezglutenowa', 'Kradzież', 'Księgowa')
                    )
    cur.execute("insert into data_prisoners (id, name, b_date, r_date, blok, cellnumber, diet, sentence, job) values (?, ?, ?, ?, ?, ?, ?, ?, ?)", ('18', 'Krzysztof Kowalczyk', '01.01.1980', '15.01.2030', 'A', 'A-123', 'Bezmięsna', 'Kradzież', 'Elektryk')
                    )
    cur.execute("insert into data_prisoners (id, name, b_date, r_date, blok, cellnumber, diet, sentence, job) values (?, ?, ?, ?, ?, ?, ?, ?, ?)", ('19', 'Janusz Nowicki', '18.09.1975', '18.09.2030', 'A', 'A-789', 'Halal', 'Przemoc domowa', 'Kucharz')
                    )
    cur.execute("insert into data_prisoners (id, name, b_date, r_date, blok, cellnumber, diet, sentence, job) values (?, ?, ?, ?, ?, ?, ?, ?, ?)", ('20', 'Katarzyna Kowalska', '01.01.1980', '15.01.2030', 'A', 'A-123', 'Bezmięsna', 'Kradzież', 'Elektryk')
                    )
    cur.execute("insert into data_prisoners (id, name, b_date, r_date, blok, cellnumber, diet, sentence, job) values (?, ?, ?, ?, ?, ?, ?, ?, ?)", ('21', 'Kamila Kowalczyk', '02.04.1993', '02.04.2033', 'D', 'D-234', 'Wegetariańska', 'Kradzież z włamaniem', 'Fotograf')
                    )
    cur.execute("insert into data_prisoners (id, name, b_date, r_date, blok, cellnumber, diet, sentence, job) values (?, ?, ?, ?, ?, ?, ?, ?, ?)", ('22', 'Marek Szymański', '28.07.1987', '28.07.2032', 'C', 'C-678', 'Bezmięsna', 'Napad na bank', 'Programista')
                    )
    cur.execute("insert into data_prisoners (id, name, b_date, r_date, blok, cellnumber, diet, sentence, job) values (?, ?, ?, ?, ?, ?, ?, ?, ?)", ('23', 'Anna Żółkiewska', '15.02.1995', '15.02.2035', 'B', 'B-123', 'Halal', 'Oszustwo podatkowe', 'Księgowa')
                    )
    cur.execute("insert into data_prisoners (id, name, b_date, r_date, blok, cellnumber, diet, sentence, job) values (?, ?, ?, ?, ?, ?, ?, ?, ?)", ('24', 'Tadeusz Wójcik', '10.11.1983', '10.11.2033', 'A', 'A-567', 'Wegetariańska', 'Posiadanie broni', 'Mechanik')
                    )
    cur.execute("insert into data_prisoners (id, name, b_date, r_date, blok, cellnumber, diet, sentence, job) values (?, ?, ?, ?, ?, ?, ?, ?, ?)", ('25', 'Karolina Kaczmarek', '23.06.1991', '23.06.2031', 'C', 'C-012', 'Bezmięsna', 'Napad na sklep', 'Sprzedawca')
                    )
    cur.execute("insert into data_prisoners (id, name, b_date, r_date, blok, cellnumber, diet, sentence, job) values (?, ?, ?, ?, ?, ?, ?, ?, ?)", ('26', 'Karolina Kaczmarek', '23.06.1991', '23.06.2031', 'C', 'C-012', 'Bezmięsna', 'Napad na sklep', 'Sprzedawca'))
    cur.execute("insert into data_prisoners (id, name, b_date, r_date, blok, cellnumber, diet, sentence, job) values (?, ?, ?, ?, ?, ?, ?, ?, ?)", ('27', 'Paweł Górski', '09.03.1986', '09.03.2036', 'D', 'D-345', 'Wegetariańska', 'Kradzież z podstępem', 'Grafik')
                    )
    cur.execute("insert into data_prisoners (id, name, b_date, r_date, blok, cellnumber, diet, sentence, job) values (?, ?, ?, ?, ?, ?, ?, ?, ?)", ('28', 'Katarzyna Kowalska', '07.12.1989', '07.12.2034', 'B', 'B-456', 'Bezmięsna', 'Nieumyślne spowodowanie śmierci', 'Pielęgniarka')
                    )
    cur.execute("insert into data_prisoners (id, name, b_date, r_date, blok, cellnumber, diet, sentence, job) values (?, ?, ?, ?, ?, ?, ?, ?, ?)", ('29', 'Michał Nowak', '28.09.1996', '28.09.2036', 'A', 'A-123', 'Halal', 'Napaść na funkcjonariusza publicznego', 'Student')
                    )
    cur.execute("insert into data_prisoners (id, name, b_date, r_date, blok, cellnumber, diet, sentence, job) values (?, ?, ?, ?, ?, ?, ?, ?, ?)", ('30', 'Joanna Tomczyk', '14.05.1980', '14.05.2035', 'C', 'C-901', 'Wegetariańska', 'Oszustwo', 'Prawnik')
                    )
    cur.execute("insert into data_prisoners (id, name, b_date, r_date, blok, cellnumber, diet, sentence, job) values (?, ?, ?, ?, ?, ?, ?, ?, ?)", ('31', 'Wojciech Kowalewski', '03.08.1977', '03.08.2037', 'D', 'D-567', 'Bezmięsna', 'Napad z bronią', 'Mechanik')
                    )
    cur.execute("insert into data_prisoners (id, name, b_date, r_date, blok, cellnumber, diet, sentence, job) values (?, ?, ?, ?, ?, ?, ?, ?, ?)", ('32', 'Magdalena Szymańska', '30.12.1992', '30.12.2037', 'B', 'B-789', 'Halal', 'Nieumyślne spowodowanie ciężkiego uszczerbku na zdrowiu', 'Asystentka')
                    )
    cur.execute("insert into data_prisoners (id, name, b_date, r_date, blok, cellnumber, diet, sentence, job) values (?, ?, ?, ?, ?, ?, ?, ?, ?)", ('33', 'Kamil Woźniak', '17.01.1988', '17.01.2038', 'A', 'A-234', 'Wegetariańska', 'Przemoc w rodzinie', 'Informatyk')
                    )
    cur.execute("insert into data_prisoners (id, name, b_date, r_date, blok, cellnumber, diet, sentence, job) values (?, ?, ?, ?, ?, ?, ?, ?, ?)", ('34', 'Monika Kozłowska', '28.07.1994', '28.07.2034', 'C', 'C-345', 'Bezmięsna', 'Kradzież z włamaniem', 'Grafik')
                    )
    
    #przykładowe dane dla tabeli data_guards ######################################################################################################################################
    cur.execute("insert into data_guards (id, name, b_date, start_date, rank, salary, blok, phone) values (?, ?, ?, ?, ?, ?, ?, ?)",
                    ('1', 'Jan Kowalski', '12.08.1963', '21.07.2010', 'Starszy Strażnik', '5000', 'A i B', '123 456 789')
                    )
    cur.execute("insert into data_guards (id, name, b_date, start_date, rank, salary, blok, phone) values (?, ?, ?, ?, ?, ?, ?, ?)", ('2', 'Kazimierz Gulski', '12.08.1963', '21.07.2010', 'Starszy Strażnik', '5000', 'A i B', '183 436 769')
                    )
    cur.execute("insert into data_guards (id, name, b_date, start_date, rank, salary, blok, phone) values (?, ?, ?, ?, ?, ?, ?, ?)", ('3', 'Adam Nowak', '24.05.1985', '01.02.2012', 'Strażnik', '3500', 'C i D', '987 654 321')
                    )
    cur.execute("insert into data_guards (id, name, b_date, start_date, rank, salary, blok, phone) values (?, ?, ?, ?, ?, ?, ?, ?)", ('4', 'Katarzyna Szymańska', '09.11.1990', '15.09.2015', 'Strażnik', '3500', 'A i C', '543 210 987')
                    )
    cur.execute("insert into data_guards (id, name, b_date, start_date, rank, salary, blok, phone) values (?, ?, ?, ?, ?, ?, ?, ?)", ('5', 'Marek Wojciechowski', '01.02.1982', '03.05.2013', 'Strażnik', '3500', 'B i D', '777 888 999')
                    )
    cur.execute("insert into data_guards (id, name, b_date, start_date, rank, salary, blok, phone) values (?, ?, ?, ?, ?, ?, ?, ?)", ('6', 'Anna Wiśniewska', '05.09.1978', '12.03.2011', 'Strażnik', '3500', 'A i B', '111 222 333')
                    )
    cur.execute("insert into data_guards (id, name, b_date, start_date, rank, salary, blok, phone) values (?, ?, ?, ?, ?, ?, ?, ?)", ('7', 'Paweł Kaczmarek', '21.06.1992', '02.08.2017', 'Strażnik', '3500', 'C i D', '444 555 666')
                    )
    cur.execute("insert into data_guards (id, name, b_date, start_date, rank, salary, blok, phone) values (?, ?, ?, ?, ?, ?, ?, ?)", ('8', 'Dariusz Lewandowski', '15.01.1987', '11.10.2014', 'Strażnik', '3500', 'B i C', '777 999 222')
                    )
    cur.execute("insert into data_guards (id, name, b_date, start_date, rank, salary, blok, phone) values (?, ?, ?, ?, ?, ?, ?, ?)", ('9', 'Małgorzata Jankowska', '18.12.1980', '25.01.2009', 'Starszy Strażnik', '5000', 'A i D', '333 444 555')
                    )
    
    
    
    
    connection.commit()
    connection.close()