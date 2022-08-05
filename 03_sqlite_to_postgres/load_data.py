import contextlib
import os
import sqlite3
from dataclasses import astuple
import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor
from dotenv import load_dotenv

from my_dataclasses import Filmwork, Person, Genre, GenreFilmwork, PersonFilmwork, dataclass_factory

env_ready = load_dotenv()


class SQLiteLoader:
    def __init__(self, sqlite_conn: sqlite3.Connection):
        self.conn = sqlite_conn

    def load_movies(self):
        self.conn.row_factory = dataclass_factory(Genre)
        curs = self.conn.cursor()
        curs.execute("SELECT * FROM genre;")
        genre = curs.fetchall()

        self.conn.row_factory = dataclass_factory(Filmwork)
        curs = self.conn.cursor()
        curs.execute("SELECT * FROM film_work;")
        film_work = curs.fetchall()

        self.conn.row_factory = dataclass_factory(Person)
        curs = self.conn.cursor()
        curs.execute("SELECT * FROM person;")
        person = curs.fetchall()

        self.conn.row_factory = dataclass_factory(PersonFilmwork)
        curs = self.conn.cursor()
        curs.execute("SELECT * FROM person_film_work;")
        person_film_work = curs.fetchall()

        self.conn.row_factory = dataclass_factory(GenreFilmwork)
        curs = self.conn.cursor()
        curs.execute("SELECT * FROM genre_film_work;")
        genre_film_work = curs.fetchall()

        res = {Filmwork: film_work, Genre: genre, Person: person, GenreFilmwork: genre_film_work,
               PersonFilmwork: person_film_work}

        return res


class PostgresSaver:
    def __init__(self, pg_conn: _connection):
        self.conn = pg_conn

    def save_all_data(self, d_class, rows):
        curs = self.conn.cursor()
        query = f'''
                INSERT INTO content.{d_class.table()} ({d_class.attrs()})
                VALUES ({d_class.attr_placeholders()}) ON CONFLICT (id) DO NOTHING;
            '''

        tuple_generator = (astuple(row) for row in rows)

        curs.executemany(query, tuple_generator)

        pg_conn.commit()


def load_from_sqlite(sqlite_conn: sqlite3.Connection, pg_conn: _connection):
    sqlite_loader = SQLiteLoader(sqlite_conn)
    postgres_saver = PostgresSaver(pg_conn)

    data = sqlite_loader.load_movies()
    for d_class, rows in data.items():
        postgres_saver.save_all_data(d_class, rows)


if __name__ == '__main__':
    dsn = {
        'dbname': os.environ.get('PG_DB_NAME'),
        'user': os.environ.get('PG_DB_USER'),
        'password': os.environ.get('PG_DB_PASSWORD'),
        'host': os.environ.get('PG_HOST'),
        'port': int(os.environ.get('PG_DB_PORT')),
        'options': f'-c search_path={os.environ.get("PG_DB_SEARCH_PATH")}',
    }
    db_path = os.environ.get('DB_PATH')
    with contextlib.closing(sqlite3.connect(db_path)) as sqlite_conn, contextlib.closing(
            psycopg2.connect(**dsn, cursor_factory=DictCursor)
    ) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
