class Student:
    def __init__(self, id, name, group):
        self.id = id
        self.name = name
        self.group = group

    def __str__(self):
        return f"[{self.id}] {self.name} ({self.group})"

def add_student(students, name, group):
    student = Student(len(students) + 1, name, group)
    students.append(student)
    return student

def find_student_by_id(students, student_id):
    for s in students:
        if s.id == student_id:
            return s
    return None
