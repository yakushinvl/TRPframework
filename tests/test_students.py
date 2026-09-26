from models import Student
from models.students import add_student, find_student

def test_studentcreate():
    s = Student(1, "Якушин Владимир", "ЭФБО-16-24")
    assert s.id == 1
    assert s.name == "Якушин Владимир"
    assert s.group == "ЭФБО-16-24"
    assert "Якушин" in str(s)

def test_addstudent():
    students = []
    add_student(students, "Петров Иван", "ЭФБО-16-24")
    assert len(students) == 1
    assert students[0].name == "Петров Иван"

def test_findstudent():
    students = [Student(1, "Иванов", "Группа")]
    assert find_student(students, 1) is not None
    assert find_student(students, 99) is None
