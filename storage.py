import json
from models import Student, Event, Presentation
from models.events import find_event
from models.students import find_student

def load_students(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [Student(d["id"], d["name"], d["group"]) for d in data]
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_students(filename, students):
    with open(filename, "w", encoding="utf-8") as f:
        data = [{"id": s.id, "name": s.name, "group": s.group} for s in students]
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_events(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [Event(d["id"], d["name"], d["max_duration"]) for d in data]
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_events(filename, events):
    with open(filename, "w", encoding="utf-8") as f:
        data = [{"id": e.id, "name": e.name, "max_duration": e.max_duration} for e in events]
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_presentations(filename, events, students):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            presentations = []
            for d in data:
                event = find_event(events, d["event_id"])
                student = find_student(students, d["student_id"])
                if event and student:
                    p = Presentation(
                        d["id"], event, student, d["title"],
                        d["duration"], d["score_1"], d["score_2"]
                    )
                    presentations.append(p)
            return presentations
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_presentations(filename, presentations):
    with open(filename, "w", encoding="utf-8") as f:
        data = [
            {
                "id": p.id,
                "event_id": p.event.id,
                "student_id": p.student.id,
                "title": p.title,
                "duration": p.duration,
                "score_1": p.score_1,
                "score_2": p.score_2
            }
            for p in presentations
        ]
        json.dump(data, f, ensure_ascii=False, indent=2)
