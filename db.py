from __future__ import annotations

import mysql.connector
from mysql.connector.connection import MySQLConnection
from contextlib import contextmanager
from typing import Iterator

from config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME


@contextmanager
def conectar(database: str | None = DB_NAME) -> Iterator[MySQLConnection]:
    conn = mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=database,
        autocommit=False,
    )
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def fetchall_dict(cur):
    cols = [c[0] for c in cur.description]
    return [dict(zip(cols, row)) for row in cur.fetchall()]


def fetchone_dict(cur):
    row = cur.fetchone()
    if not row:
        return None
    cols = [c[0] for c in cur.description]
    return dict(zip(cols, row))