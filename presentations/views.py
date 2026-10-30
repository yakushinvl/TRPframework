from django.shortcuts import render
from models.presentations import find_presentation_by_id
from storage import load_events, load_presentations, load_students

STUDENTS_FILE = "data/students.json"
EVENTS_FILE = "data/events.json"
PRESENTATIONS_FILE = "data/presentations.json"


def presentation_list(request):
    events = load_events(EVENTS_FILE)
    students = load_students(STUDENTS_FILE)
    presentations = load_presentations(PRESENTATIONS_FILE, events, students)
    return render(
        request,
        "presentations/presentation_list.html",
        {"presentations": presentations},
    )


def presentation_detail(request, presentation_id):
    events = load_events(EVENTS_FILE)
    students = load_students(STUDENTS_FILE)
    presentations = load_presentations(PRESENTATIONS_FILE, events, students)
    p = find_presentation_by_id(presentations, presentation_id)
    return render(
        request,
        "presentations/presentation_detail.html",
        {"p": p},
        status=404 if p is None else 200,
    )
