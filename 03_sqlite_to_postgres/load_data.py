import contextlib
import os
import sqlite3
from dataclasses import astuple
from datetime import datetime
from sqlite3 import DatabaseError

import psycopg2
from dateutil.parser import parse
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor
from dotenv import load_dotenv
import contextlib
import os
import random
import sqlite3
import time
import uuid
from typing import Iterator, Dict, Any, Generator, Iterable, Tuple, List
from psycopg2 import sql
from collections import namedtuple
from dataclasses import astuple

import dateutil
from dotenv import load_dotenv
from typing import Type
from dataclasses import fields
import dataclasses
from dateutil.parser import parse

from datetime import datetime, date
from dataclasses import dataclass
from dataclasses import field
import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor, RealDictCursor
from psycopg2.extras import execute_batch, execute_values

from my_dataclasses import Filmwork, Person, Genre, GenreFilmwork, PersonFilmwork, dataclass_factory, TheBaseDataclass

env_ready = load_dotenv()

sqlite3.register_converter("timestamp", lambda b: parse(b.decode('utf-8')))
# person table has incorrect naming for timestamp
sqlite3.register_converter("timestam", lambda b: parse(b.decode('utf-8')))


class SQLiteLoader:
    def __init__(self, sqlite_conn: sqlite3.Connection):
        self.conn = sqlite_conn

    def load_one_table(self, d_class, as_dataclass=True):
        if as_dataclass:
            self.conn.row_factory = dataclass_factory(d_class)

        curs = self.conn.cursor()

        query = f'''SELECT {d_class.sqlite_attrs()} from {d_class.table_name()} order by id desc;'''

        curs.execute(query)

        return curs.fetchall()

    def load_movies(self, d_classes: List[Type[TheBaseDataclass]]) -> Dict[Type[TheBaseDataclass], list[Any]]:
        res = {}

        for d_class in d_classes:
            res[d_class] = self.load_one_table(d_class)

        return res

    def close_conn(self):
        self.conn.close()


class PostgresSaver:
    def __init__(self, pg_conn: _connection):
        self.conn = pg_conn

    def save_all_data(self, d_class: Type[TheBaseDataclass], rows):
        curs = self.conn.cursor()

        columns = sql.SQL(', ').join(map(sql.Identifier, d_class.pg_attrs()))

        insert_sql = sql.SQL(
            "INSERT INTO {table_name} ({columns}) VALUES %s ON CONFLICT (id) DO NOTHING;"
        ).format(columns=columns, table_name=sql.Identifier(d_class.table_name()))

        row_tuples: Iterable[Tuple[Any]] = (astuple(row) for row in rows)

        execute_values(curs, insert_sql, row_tuples, page_size=1000)

        pg_conn.commit()

    def truncate_tables(self, d_classes: Iterable[Type[TheBaseDataclass]]):
        curs = self.conn.cursor()
        table_names = (d_class.table_name() for d_class in d_classes)

        table_names = sql.SQL(', ').join(map(sql.Identifier, table_names))

        query = sql.SQL("TRUNCATE TABLE {table_names};").format(table_names=table_names)
        curs.execute(query.as_string(pg_conn))
        pg_conn.commit()


class PostgresLoader:
    def __init__(self, pg_conn: _connection):
        self.conn = pg_conn

    def load_one_table(self, d_class: Type[TheBaseDataclass]):
        curs = self.conn.cursor()

        columns = sql.SQL(', ').join(map(sql.Identifier, d_class.pg_attrs()))

        query = sql.SQL(
            '''SELECT {columns} from {table_name} order by id desc'''
        ).format(columns=columns, table_name=sql.Identifier(d_class.table_name()))

        curs.execute(query)

        return curs.fetchall()

    def close_conn(self):
        self.conn.close()


def load_from_sqlite(sqlite_conn: sqlite3.Connection, pg_conn: _connection):
    sqlite_loader = SQLiteLoader(sqlite_conn)
    postgres_saver = PostgresSaver(pg_conn)

    d_classes = [Filmwork, Person, Genre, GenreFilmwork, PersonFilmwork]

    data = sqlite_loader.load_movies(d_classes)

    postgres_saver.truncate_tables(d_classes)

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

    db_path = os.path.join(os.getcwd(), os.environ.get('DB_PATH'))

    try:
        with contextlib.closing(
                sqlite3.connect(f'file:{db_path}?mode=ro', detect_types=sqlite3.PARSE_DECLTYPES, uri=True)
        ) as sqlite_conn, contextlib.closing(psycopg2.connect(**dsn, cursor_factory=DictCursor)) as pg_conn:
            load_from_sqlite(sqlite_conn, pg_conn)
    except DatabaseError as e:
        print(e)
    except psycopg2.OperationalError as e:
        print(e)
