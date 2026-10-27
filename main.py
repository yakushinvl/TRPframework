from models.events import add_event, find_event_by_id
from models.presentations import (
    create_presentation,
    find_presbystud,
    sort_presbyscore,
)
from models.students import add_student, find_student_by_id
from storage import (
    load_events,
    load_presentations,
    load_students,
    save_events,
    save_presentations,
    save_students,
)
from utils import input_float, input_int

STUDENTS_FILE = "data/students.json"
EVENTS_FILE = "data/events.json"
PRESENTATIONS_FILE = "data/presentations.json"


def show_events(events):
    if not events:
        print("список мероприятий пуст")
        return
    print("\n--- мероприятия ---")
    for event in events:
        print(event)


def show_students(students):
    if not students:
        print("список студентов пуст")
        return
    print("\n--- студенты ---")
    for s in students:
        print(s)


def show_presentations(presentations):
    if not presentations:
        print("список выступлений пуст")
        return
    print("\n--- выступления ---")
    for p in presentations:
        print(p)


def main():
    events = load_events(EVENTS_FILE)
    students = load_students(STUDENTS_FILE)
    presentations = load_presentations(PRESENTATIONS_FILE, events, students)

    while True:
        print("\n=== меню ===")
        print("1. показать мероприятия")
        print("2. добавить мероприятие")
        print("3. показать студентов")
        print("4. добавить студента")
        print("5. показать выступления")
        print("6. добавить выступление")
        print("7. поиск выступлений по студенту")
        print("8. сортировка выступлений по баллам")
        print("0. выход")

        choice = input("выбери действие: ").strip()

        if choice == "1":
            show_events(events)
        elif choice == "2":
            name = input("название мероприятия: ").strip()
            max_duration = input_int("максимальная длительность (мин): ")
            add_event(events, name, max_duration)
            save_events(EVENTS_FILE, events)
            print("мероприятие добавлено")
        elif choice == "3":
            show_students(students)
        elif choice == "4":
            name = input("фио студента: ").strip()
            group = input("группа: ").strip()
            add_student(students, name, group)
            save_students(STUDENTS_FILE, students)
            print("студент добавлен")
        elif choice == "5":
            show_presentations(presentations)
        elif choice == "6":
            if not events or not students:
                print("сначала добавь мероприятие и студента")
                continue
            show_events(events)
            ev_id = input_int("id мероприятия: ")
            event = find_event_by_id(events, ev_id)
            if not event:
                print("мероприятие не найдено")
                continue

            show_students(students)
            st_id = input_int("id студента: ")
            student = find_student_by_id(students, st_id)
            if not student:
                print("студент не найден")
                continue

            title = input("тема выступления: ").strip()
            duration = input_int("длительность (мин): ")
            s1 = input_float("балл за выступление: ")
            s2 = input_float("балл за ответы: ")

            create_presentation(
                presentations, event, student, title, duration, s1, s2
            )
            save_presentations(PRESENTATIONS_FILE, presentations)
            print("выступление сохранено")
        elif choice == "7":
            query = input("введи имя студента: ").strip()
            found = find_presbystud(presentations, query)
            show_presentations(found)
        elif choice == "8":
            sorted_p = sort_presbyscore(presentations)
            show_presentations(sorted_p)
        elif choice == "0":
            print("выход из программы")
            break
        else:
            print("неверный ввод, повтори попытку")


if __name__ == "__main__":
    main()
