import json
import os
from db.database import DB_PATH, get_connection, init_db

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_json(filename):
    path = os.path.join(BASE_DIR, "data", filename)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def import_all(db_path=DB_PATH):
    init_db(db_path)
    events = load_json("events.json")
    students = load_json("students.json")
    presentations = load_json("presentations.json")

    with get_connection(db_path) as conn:
        conn.execute("DELETE FROM presentations")
        conn.execute("DELETE FROM students")
        conn.execute("DELETE FROM events")

        conn.executemany(
            "INSERT INTO events (id, name, max_duration) VALUES (?, ?, ?)",
            [(e["id"], e["name"], e["max_duration"]) for e in events],
        )
        conn.executemany(
            "INSERT INTO students (id, name, group_name) VALUES (?, ?, ?)",
            [(s["id"], s["name"], s["group"]) for s in students],
        )
        conn.executemany(
            "INSERT INTO presentations (id, event_id, student_id, title, duration, score_1, score_2) VALUES (?, ?, ?, ?, ?, ?, ?)",
            [
                (
                    p["id"],
                    p["event_id"],
                    p["student_id"],
                    p["title"],
                    p["duration"],
                    p["score_1"],
                    p["score_2"],
                )
                for p in presentations
            ],
        )


if __name__ == "__main__":
    import_all()
    print("данные успешно импортированы в базу")
