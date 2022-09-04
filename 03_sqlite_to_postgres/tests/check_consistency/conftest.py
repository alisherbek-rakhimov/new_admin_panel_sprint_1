import contextlib
import os
import sqlite3
from dataclasses import astuple
from datetime import datetime
from sqlite3 import DatabaseError

import psycopg2
import pytest
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

from load_data import SQLiteLoader, PostgresLoader
from my_dataclasses import Filmwork, Person, Genre, GenreFilmwork, PersonFilmwork, dataclass_factory, TheBaseDataclass

env_ready = load_dotenv()


@pytest.fixture(autouse=True)
def loaders():
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
        sqlite_conn = sqlite3.connect(f'file:{db_path}?mode=ro', detect_types=sqlite3.PARSE_DECLTYPES, uri=True)
        pg_conn = psycopg2.connect(**dsn)

        sqlite_loader = SQLiteLoader(sqlite_conn)
        postgres_loader = PostgresLoader(pg_conn)

        return sqlite_loader, postgres_loader

    except DatabaseError as e:
        print(e)
    except psycopg2.OperationalError as e:
        print(e)