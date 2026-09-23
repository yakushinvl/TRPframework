def check_duration(duration, limit):
    if duration <= limit:
        return "В регламенте"
    return "Превышен"

def calculate_total_score(s1, s2):
    return round(s1 + s2, 2)

def get_result(score):
    if score >= 9.0:
        return "1 место"
    elif score >= 8.0:
        return "2 место"
    elif score >= 7.0:
        return "3 место"
    else:
        return "Участник"

def add_presentation(presentations, event_id, student, group, title, duration, score_1, score_2):
    total = calculate_total_score(score_1, score_2)
    presentation = {
        "id": len(presentations) + 1,
        "event_id": event_id,
        "student": student,
        "group": group,
        "title": title,
        "duration": duration,
        "score_1": score_1,
        "score_2": score_2,
        "total_score": total,
        "result": get_result(total)
    }
    presentations.append(presentation)
    return presentation

def find_presentations_by_student(presentations, query):
    query_lower = query.lower()
    return [p for p in presentations if query_lower in p.get("student", "").lower()]

def sort_presentations_by_score(presentations):
    return sorted(presentations, key=lambda p: p.get("total_score", 0.0), reverse=True)
