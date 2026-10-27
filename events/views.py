from django.http import HttpResponse
from homepage.views import page
from models.events import find_event_by_id
from storage import load_events

EVENTS_FILE = "data/events.json"


def event_list(request):
    events = load_events(EVENTS_FILE)
    items = ""
    for ev in events:
        items += f"""
        <li class="list-group-item d-flex justify-content-between align-items-center">
            <a href="/events/{ev.id}/" class="text-decoration-none fw-bold">{ev.name}</a>
            <span class="badge bg-primary rounded-pill">регламент: {ev.max_duration} мин</span>
        </li>
        """
    content = f"""
    <h2>список мероприятий</h2>
    <ul class="list-group shadow-sm mt-3">{items}</ul>
    <a href="/" class="btn btn-outline-secondary mt-3">← на главную</a>
    """
    return HttpResponse(page("мероприятия", content))


def event_detail(request, event_id):
    events = load_events(EVENTS_FILE)
    event = find_event_by_id(events, event_id)
    if event is None:
        content = """
        <div class="alert alert-danger mt-3">
            <h4>мероприятие не найдено</h4>
            <a href="/events/" class="btn btn-outline-secondary mt-2">← к списку мероприятий</a>
        </div>
        """
        return HttpResponse(page("не найдено", content), status=404)

    content = f"""
    <div class="card shadow-sm mt-3">
        <div class="card-body">
            <h4 class="card-title">{event.name}</h4>
            <p class="card-text"><strong>id:</strong> {event.id}</p>
            <p class="card-text"><strong>лимит выступления:</strong> {event.max_duration} мин</p>
            <a href="/events/" class="btn btn-outline-secondary">← к списку мероприятий</a>
        </div>
    </div>
    """
    return HttpResponse(page(event.name, content))
