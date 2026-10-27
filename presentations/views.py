from django.http import HttpResponse
from homepage.views import page
from models.presentations import find_presentation_by_id
from storage import load_events, load_presentations, load_students

STUDENTS_FILE = "data/students.json"
EVENTS_FILE = "data/events.json"
PRESENTATIONS_FILE = "data/presentations.json"


def presentation_list(request):
    events = load_events(EVENTS_FILE)
    students = load_students(STUDENTS_FILE)
    presentations = load_presentations(PRESENTATIONS_FILE, events, students)

    items = ""
    for p in presentations:
        status = p.check_duration()
        badge_timing = "bg-success" if status == "в регламенте" else "bg-danger"
        badge_result = "bg-primary" if "место" in p.result else "bg-secondary"

        items += f"""
        <li class="list-group-item d-flex justify-content-between align-items-center">
            <div>
                <a href="/presentations/{p.id}/" class="fw-bold text-decoration-none">
                    {p.student.name} ({p.student.group})
                </a>
                <div class="text-muted small">тема: «{p.title}» | мероприятие: {p.event.name}</div>
            </div>
            <div>
                <span class="badge {badge_timing} me-2">{status} ({p.duration} мин)</span>
                <span class="badge {badge_result}">{p.result} ({p.total_score} б)</span>
            </div>
        </li>
        """

    content = f"""
    <h2>список выступлений</h2>
    <ul class="list-group shadow-sm mt-3">{items}</ul>
    <a href="/" class="btn btn-outline-secondary mt-3">← на главную</a>
    """
    return HttpResponse(page("выступления", content))


def presentation_detail(request, presentation_id):
    events = load_events(EVENTS_FILE)
    students = load_students(STUDENTS_FILE)
    presentations = load_presentations(PRESENTATIONS_FILE, events, students)

    p = find_presentation_by_id(presentations, presentation_id)
    if p is None:
        content = """
        <div class="alert alert-danger mt-3">
            <h4>выступление не найдено</h4>
            <a href="/presentations/" class="btn btn-outline-secondary mt-2">← к списку выступлений</a>
        </div>
        """
        return HttpResponse(page("не найдено", content), status=404)

    status = p.check_duration()
    badge_timing = "bg-success" if status == "в регламенте" else "bg-danger"
    badge_result = "bg-primary" if "место" in p.result else "bg-secondary"

    content = f"""
    <div class="card shadow-sm mt-3">
        <div class="card-body">
            <h4 class="card-title">выступление №{p.id}: «{p.title}»</h4>
            <hr>
            <p><strong>студент:</strong> {p.student.name} (группа: {p.student.group})</p>
            <p><strong>мероприятие:</strong> {p.event.name} (лимит: {p.event.max_duration} мин)</p>
            <p><strong>время доклада:</strong> {p.duration} мин <span class="badge {badge_timing}">{status}</span></p>
            <p><strong>баллы жюри:</strong> {p.score_1} (доклад) + {p.score_2} (ответы) = <strong>{p.total_score}</strong></p>
            <p><strong>итог:</strong> <span class="badge {badge_result} fs-6">{p.result}</span></p>
            <a href="/presentations/" class="btn btn-outline-secondary mt-2">← к списку выступлений</a>
        </div>
    </div>
    """
    return HttpResponse(page(f"выступление: {p.title}", content))
