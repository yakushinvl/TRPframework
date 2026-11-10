import sqlite3
from db.database import get_connection, init_db
from db.import_json import import_all


def test_init_db(tmp_path):
    db_file = tmp_path / "test.sqlite"
    init_db(str(db_file))
    conn = get_connection(str(db_file))
    cursor = conn.cursor()
    tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    table_names = [t["name"] for t in tables]
    assert "students" in table_names
    assert "events" in table_names
    assert "presentations" in table_names
    conn.close()


def test_import_data(tmp_path):
    db_file = tmp_path / "test.sqlite"
    import_all(str(db_file))
    conn = get_connection(str(db_file))
    students_count = conn.execute("SELECT COUNT(*) FROM students").fetchone()[0]
    events_count = conn.execute("SELECT COUNT(*) FROM events").fetchone()[0]
    pres_count = conn.execute("SELECT COUNT(*) FROM presentations").fetchone()[0]
    assert students_count >= 1
    assert events_count >= 1
    assert pres_count >= 1
    conn.close()


def test_foreign_keys_enabled(tmp_path):
    db_file = tmp_path / "test.sqlite"
    conn = get_connection(str(db_file))
    fk = conn.execute("PRAGMA foreign_keys").fetchone()[0]
    assert fk == 1
    conn.close()
