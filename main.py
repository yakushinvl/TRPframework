from events import add_event, find_event
from presentations import add_presentation, check_duration, find_presentations_by_student, sort_presentations_by_score
from storage import load_data, save_data
from utils import input_float, input_int

EVENTS_FILE = "data/events.json"
PRESENTATIONS_FILE = "data/presentations.json"

def show_events(events):
    if not events:
        print("Список мероприятий пуст.")
        return
    print("\n--- Мероприятия ---")
    for event in events:
        print(f"[{event['id']}] {event['name']} (лимит: {event['max_duration']} мин)")

def show_presentations(presentations, events):
    if not presentations:
        print("Список выступлений пуст.")
        return
    print("\n--- Выступления ---")
    for p in presentations:
        event = find_event(events, p["event_id"])
        ev_name = event["name"] if event else "Неизвестно"
        ev_limit = event["max_duration"] if event else 0
        status = check_duration(p["duration"], ev_limit)
        print(
            f"[{p['id']}] {p['student']} ({p['group']}) | "
            f"Мероприятие: {ev_name} | "
            f"Тема: {p['title']} | "
            f"Время: {p['duration']} мин ({status}) | "
            f"Балл: {p['total_score']} | "
            f"Результат: {p['result']}"
        )

events = load_data(EVENTS_FILE)
presentations = load_data(PRESENTATIONS_FILE)

while True:
    print("\n=== Меню ===")
    print("1. Показать мероприятия")
    print("2. Добавить мероприятие")
    print("3. Показать выступления")
    print("4. Добавить выступление")
    print("5. Поиск выступлений по студенту")
    print("6. Сортировка выступлений по баллам")
    print("0. Выход")

    choice = input("Выбери действие: ").strip()

    if choice == "1":
        show_events(events)
    elif choice == "2":
        name = input("Название мероприятия: ").strip()
        max_duration = input_int("Максимальная длительность (мин): ")
        add_event(events, name, max_duration)
        save_data(EVENTS_FILE, events)
        print("Мероприятие добавлено.")
    elif choice == "3":
        show_presentations(presentations, events)
    elif choice == "4":
        if not events:
            print("Сначала добавьте мероприятие.")
            continue
        show_events(events)
        ev_id = input_int("ID мероприятия: ")
        student = input("ФИО студента: ").strip()
        group = input("Группа: ").strip()
        title = input("Тема выступления: ").strip()
        duration = input_int("Длительность (мин): ")
        s1 = input_float("Балл за выступление: ")
        s2 = input_float("Балл за ответы: ")

        add_presentation(presentations, ev_id, student, group, title, duration, s1, s2)
        save_data(PRESENTATIONS_FILE, presentations)
        print("Выступление сохранено.")
    elif choice == "5":
        query = input("Введи имя студента: ").strip()
        found = find_presentations_by_student(presentations, query)
        show_presentations(found, events)
    elif choice == "6":
        sorted_p = sort_presentations_by_score(presentations)
        show_presentations(sorted_p, events)
    elif choice == "0":
        print("Выход.")
        break
    else:
        print("Неверный ввод.")