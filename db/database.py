import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "tracker.sqlite")
SCHEMA_PATH = os.path.join(BASE_DIR, "sql", "schema.sql")


def get_connection(db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(db_path=DB_PATH, schema_path=SCHEMA_PATH):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = f.read()
    with get_connection(db_path) as conn:
        conn.executescript(schema)
