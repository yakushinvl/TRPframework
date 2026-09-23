from datetime import date

student = "Якушин Владимир"
group = "ЭФБО-16-24"
event = "Конференция"
event_date = date(2026, 10, 15)
max_duration = 10
presentation = "Веб-сервисы"
duration = 8
score_1 = 4.8
score_2 = 4.5


def check_duration(duration, limit):
    if duration <= limit:
        return "В регламенте"
    return "Превышен"


def calculate_total_score(s1, s2):
    return s1 + s2


def get_result(score):
    if score >= 9.0:
        return "1 место"
    elif score >= 8.0:
        return "2 место"
    elif score >= 7.0:
        return "3 место"
    else:
        return "Участник"


status = check_duration(duration, max_duration)
total = calculate_total_score(score_1, score_2)
result = get_result(total)

print(f"Студент: {student}")
print(f"Группа: {group}")
print(f"Мероприятие: {event}")
print(f"Дата: {event_date}")
print(f"Выступление: {presentation}")
print(f"Время: {duration} мин ({status})")
print(f"Балл: {total}")
print(f"Результат: {result}")
