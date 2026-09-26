from models.events import add_event, find_event
from models.presentations import create_presentation, find_presbystud, sort_presbyscore
from models.students import add_student, find_student
from storage import load_events, load_presentations, load_students, save_events, save_presentations, save_students
from utils import input_float, input_int

STUDENTS = "data/students.json"
EVENTS = "data/events.json"
PRESENTATIONS = "data/presentations.json"

def show_events(events):
    if not events:
        print("Список мероприятий пуст")
        return
    print("\nМероприятия")
    for event in events:
        print(event)

def show_students(students):
    if not students:
        print("Список студентов пуст")
        return
    print("\nСтуденты")
    for s in students:
        print(s)

def show_presentations(presentations):
    if not presentations:
        print("Список выступлений пуст")
        return
    print("\nВыступления")
    for p in presentations:
        print(p)

events = load_events(EVENTS)
students = load_students(STUDENTS)
presentations = load_presentations(PRESENTATIONS, events, students)

while True:
    print("\nМеню")
    print("1. Показать мероприятия")
    print("2. Добавить мероприятие")
    print("3. Показать студентов")
    print("4. Добавить студента")
    print("5. Показать выступления")
    print("6. Добавить выступление")
    print("7. Поиск выступлений по студенту")
    print("8. Сортировка выступлений по баллам")
    print("0. Выход")

    choice = input("Выбери действие: ").strip()

    if choice == "1":
        show_events(events)
    elif choice == "2":
        name = input("Название: ").strip()
        max_duration = input_int("Макс. длительность: ")
        add_event(events, name, max_duration)
        save_events(EVENTS, events)
        print("Мероприятие добавлено")
    elif choice == "3":
        show_students(students)
    elif choice == "4":
        name = input("ФИО студента: ").strip()
        group = input("Группа: ").strip()
        add_student(students, name, group)
        save_students(STUDENTS, students)
        print("Студент добавлен")
    elif choice == "5":
        show_presentations(presentations)
    elif choice == "6":
        if not events or not students:
            print("Сначала добавь мероприятие и студента")
            continue
        show_events(events)
        ev_id = input_int("ID мероприятия: ")
        event = find_event(events, ev_id)
        if not event:
            print("Мероприятие не найдено")
            continue

        show_students(students)
        st_id = input_int("ID студента: ")
        student = find_student(students, st_id)
        if not student:
            print("Студент не найден")
            continue

        title = input("Тема выступления: ").strip()
        duration = input_int("Длительность: ")
        s1 = input_float("Балл за выступление: ")
        s2 = input_float("Балл за ответы: ")

        create_presentation(presentations, event, student, title, duration, s1, s2)
        save_presentations(PRESENTATIONS, presentations)
        print("Выступление сохранено")
    elif choice == "7":
        query = input("Имя студента: ").strip()
        found = find_presbystud(presentations, query)
        show_presentations(found)
    elif choice == "8":
        sorted_p = sort_presbyscore(presentations)
        show_presentations(sorted_p)
    elif choice == "0":
        break
    else:
        print("Неверный ввод")
