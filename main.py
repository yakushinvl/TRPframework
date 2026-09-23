from models.events import add_event, find_event_by_id
from models.presentations import create_presentation, find_presentations_by_student, sort_presentations_by_score
from models.students import add_student, find_student_by_id
from storage import load_events, load_presentations, load_students, save_events, save_presentations, save_students
from utils import input_float, input_int

STUDENTS_FILE = "data/students.json"
EVENTS_FILE = "data/events.json"
PRESENTATIONS_FILE = "data/presentations.json"

def show_events(events):
    if not events:
        print("Список мероприятий пуст.")
        return
    print("\n--- Мероприятия ---")
    for event in events:
        print(event)

def show_students(students):
    if not students:
        print("Список студентов пуст.")
        return
    print("\n--- Студенты ---")
    for s in students:
        print(s)

def show_presentations(presentations):
    if not presentations:
        print("Список выступлений пуст.")
        return
    print("\n--- Выступления ---")
    for p in presentations:
        print(p)

events = load_events(EVENTS_FILE)
students = load_students(STUDENTS_FILE)
presentations = load_presentations(PRESENTATIONS_FILE, events, students)

while True:
    print("\n=== Меню ===")
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
        name = input("Название мероприятия: ").strip()
        max_duration = input_int("Максимальная длительность (мин): ")
        add_event(events, name, max_duration)
        save_events(EVENTS_FILE, events)
        print("Мероприятие добавлено.")
    elif choice == "3":
        show_students(students)
    elif choice == "4":
        name = input("ФИО студента: ").strip()
        group = input("Группа: ").strip()
        add_student(students, name, group)
        save_students(STUDENTS_FILE, students)
        print("Студент добавлен.")
    elif choice == "5":
        show_presentations(presentations)
    elif choice == "6":
        if not events or not students:
            print("Сначала добавь мероприятие и студента.")
            continue
        show_events(events)
        ev_id = input_int("ID мероприятия: ")
        event = find_event_by_id(events, ev_id)
        if not event:
            print("Мероприятие не найдено.")
            continue

        show_students(students)
        st_id = input_int("ID студента: ")
        student = find_student_by_id(students, st_id)
        if not student:
            print("Студент не найден.")
            continue

        title = input("Тема выступления: ").strip()
        duration = input_int("Длительность (мин): ")
        s1 = input_float("Балл за выступление: ")
        s2 = input_float("Балл за ответы: ")

        create_presentation(
            presentations, event, student, title, duration, s1, s2
        )
        save_presentations(PRESENTATIONS_FILE, presentations)
        print("Выступление сохранено.")
    elif choice == "7":
        query = input("Введи имя студента: ").strip()
        found = find_presentations_by_student(presentations, query)
        show_presentations(found)
    elif choice == "8":
        sorted_p = sort_presentations_by_score(presentations)
        show_presentations(sorted_p)
    elif choice == "0":
        print("Выход.")
        break
    else:
        print("Неверный ввод.")
