import os
import sqlite3
import sys
from pathlib import Path
import django
from django.db import transaction

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
SOURCE_DB = BASE_DIR / "data" / "tracker.sqlite"

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tracker.settings")
django.setup()

from events.models import Event
from presentations.models import Presentation
from students.models import Student


def main():
    if not SOURCE_DB.exists():
        raise FileNotFoundError(f"исходная база не найдена: {SOURCE_DB}")

    with sqlite3.connect(SOURCE_DB) as connection:
        connection.row_factory = sqlite3.Row
        events = connection.execute("SELECT id, name, max_duration FROM events ORDER BY id").fetchall()
        students = connection.execute("SELECT id, name, group_name FROM students ORDER BY id").fetchall()
        presentations = connection.execute(
            "SELECT id, event_id, student_id, title, duration, score_1, score_2 FROM presentations ORDER BY id"
        ).fetchall()

    with transaction.atomic():
        for row in events:
            Event.objects.update_or_create(
                pk=row["id"],
                defaults={
                    "name": row["name"],
                    "max_duration": row["max_duration"],
                },
            )

        for row in students:
            Student.objects.update_or_create(
                pk=row["id"],
                defaults={
                    "name": row["name"],
                    "group": row["group_name"],
                },
            )

        for row in presentations:
            Presentation.objects.update_or_create(
                pk=row["id"],
                defaults={
                    "event_id": row["event_id"],
                    "student_id": row["student_id"],
                    "title": row["title"],
                    "duration": row["duration"],
                    "score_1": row["score_1"],
                    "score_2": row["score_2"],
                },
            )

    print("перенос данных завершён")
    print(f"мероприятий: {Event.objects.count()}")
    print(f"студентов: {Student.objects.count()}")
    print(f"выступлений: {Presentation.objects.count()}")


if __name__ == "__main__":
    main()
