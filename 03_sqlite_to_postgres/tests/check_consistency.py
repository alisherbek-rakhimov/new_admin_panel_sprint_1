import contextlib
import os
import sqlite3
from dataclasses import astuple
import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor
from dotenv import load_dotenv

from ..my_dataclasses import Filmwork, Person, Genre, GenreFilmwork, PersonFilmwork, dataclass_factory

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

