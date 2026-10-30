from django.shortcuts import render
from models.events import find_event_by_id
from storage import load_events

EVENTS_FILE = "data/events.json"


def event_list(request):
    events = load_events(EVENTS_FILE)
    return render(request, "events/event_list.html", {"events": events})


def event_detail(request, event_id):
    events = load_events(EVENTS_FILE)
    event = find_event_by_id(events, event_id)
    return render(
        request,
        "events/event_detail.html",
        {"event": event},
        status=404 if event is None else 200,
    )
