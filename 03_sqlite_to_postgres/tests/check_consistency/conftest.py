import os
import sqlite3
from sqlite3 import DatabaseError
import logging
import psycopg2
import pytest
from dotenv import load_dotenv

from load_data import PostgresLoader, SQLiteLoader
from settings import dsn, db_path

env_ready = load_dotenv()


@pytest.fixture(autouse=True)
def loaders():
    try:
        sqlite_conn = sqlite3.connect(f'file:{db_path}?mode=ro', detect_types=sqlite3.PARSE_DECLTYPES, uri=True)
        pg_conn = psycopg2.connect(**dsn)

        sqlite_loader = SQLiteLoader(sqlite_conn)
        postgres_loader = PostgresLoader(pg_conn)

        return sqlite_loader, postgres_loader

    except DatabaseError as e:
        logging.error(e)
    except psycopg2.OperationalError as e:
        logging.error(e)
