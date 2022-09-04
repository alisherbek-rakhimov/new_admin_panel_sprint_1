import contextlib
import os
import sqlite3
from dataclasses import astuple
from datetime import datetime
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
import pytest
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

from load_data import SQLiteLoader, PostgresLoader
from my_dataclasses import Filmwork, Person, Genre, GenreFilmwork, PersonFilmwork, dataclass_factory, TheBaseDataclass

env_ready = load_dotenv()


def test_film_work(loaders):
    sqlite_loader, postgres_loader = loaders

    sqlite_data = sqlite_loader.load_one_table(Filmwork, as_dataclass=False)
    pg_data = postgres_loader.load_one_table(Filmwork)

    sqlite_loader.close_conn()
    postgres_loader.close_conn()

    assert sqlite_data == pg_data


def test_genre(loaders):
    sqlite_loader, postgres_loader = loaders

    sqlite_data = sqlite_loader.load_one_table(Genre, as_dataclass=False)
    pg_data = postgres_loader.load_one_table(Genre)

    sqlite_loader.close_conn()
    postgres_loader.close_conn()

    assert sqlite_data == pg_data


def test_person(loaders):
    sqlite_loader, postgres_loader = loaders

    sqlite_data = sqlite_loader.load_one_table(Person, as_dataclass=False)
    pg_data = postgres_loader.load_one_table(Person)

    sqlite_loader.close_conn()
    postgres_loader.close_conn()

    assert sqlite_data == pg_data



def test_genre_film_work(loaders):
    sqlite_loader, postgres_loader = loaders

    sqlite_data = sqlite_loader.load_one_table(GenreFilmwork, as_dataclass=False)
    pg_data = postgres_loader.load_one_table(GenreFilmwork)

    sqlite_loader.close_conn()
    postgres_loader.close_conn()

    assert sqlite_data == pg_data


def test_person_film_work(loaders):
    sqlite_loader, postgres_loader = loaders

    sqlite_data = sqlite_loader.load_one_table(PersonFilmwork, as_dataclass=False)
    pg_data = postgres_loader.load_one_table(PersonFilmwork)

    sqlite_loader.close_conn()
    postgres_loader.close_conn()

    assert sqlite_data == pg_data
