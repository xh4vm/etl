import os
from typing import Any
import psycopg2

from psycopg2.extras import DictCursor, register_uuid
from contextlib import contextmanager
import logging
from dotenv import load_dotenv

from .extractor import Extractor
from .transformer import Transformer


@contextmanager
def pg_conn_context(postgresql_dsl: dict[str, Any]):
    conn = psycopg2.connect(**postgresql_dsl, cursor_factory=DictCursor)

    yield conn

    conn.close()


def get_postgresql_dsl() -> dict[str, Any]:
    return {
        'dbname': os.environ.get('DB_NAME'),
        'user': os.environ.get('DB_USER'),
        'password': os.environ.get('DB_PASSWORD'),
        'host': os.environ.get('DB_HOST', '127.0.0.1'),
        'port': os.environ.get('DB_PORT', 5432),
    }


if __name__ == '__main__':
    logging.root.setLevel(logging.NOTSET)
    logging.basicConfig(level=logging.NOTSET)
    
    load_dotenv()

    postgresql_dsl = get_postgresql_dsl()

    with pg_conn_context(postgresql_dsl) as pg_conn, pg_conn.cursor() as pg_cursor:

        register_uuid()
