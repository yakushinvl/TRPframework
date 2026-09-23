from models import Student, Event, Presentation
from models.presentations import (
    create_presentation,
    find_presentations_by_student,
    sort_presentations_by_score,
)

def test_presentation_creation_and_methods():
    event = Event(1, "Конференция", 10)
    student = Student(1, "Якушин Владимир", "ЭФБО-16-24")
    p = Presentation(1, event, student, "Тема", 8, 4.8, 4.5)

    assert p.id == 1
    assert p.event is event
    assert p.student is student
    assert p.check_duration() == "В регламенте"
    assert p.total_score == 9.3
    assert p.result == "1 место"
    assert "В регламенте" in str(p)

def test_presentation_duration_limit():
    event = Event(1, "Конференция", 10)
    student = Student(1, "Студент", "Группа")
    p = Presentation(1, event, student, "Тема", 12, 4.0, 4.0)
    assert p.check_duration() == "Превышен"

def test_create_presentation():
    presentations = []
    event = Event(1, "Конференция", 10)
    student = Student(1, "Студент", "Группа")
    create_presentation(presentations, event, student, "Тема", 8, 4.0, 4.0)
    assert len(presentations) == 1
    assert presentations[0].total_score == 8.0
    assert presentations[0].result == "2 место"

def test_find_and_sort_presentations():
    event = Event(1, "Конференция", 10)
    s1 = Student(1, "Иванов", "Группа")
    s2 = Student(2, "Петров", "Группа")
    p1 = Presentation(1, event, s1, "Тема 1", 8, 3.5, 3.5)
    p2 = Presentation(2, event, s2, "Тема 2", 8, 4.8, 4.8)
    presentations = [p1, p2]

    found = find_presentations_by_student(presentations, "иван")
    assert len(found) == 1
    assert found[0].student.name == "Иванов"

    sorted_p = sort_presentations_by_score(presentations)
    assert sorted_p[0].total_score == 9.6
