from django.shortcuts import render
from db.database import get_connection
from models.events import Event


def event_list(request):
    with get_connection() as conn:
        rows = conn.execute("SELECT id, name, max_duration FROM events ORDER BY id").fetchall()
        events = [Event(row["id"], row["name"], row["max_duration"]) for row in rows]
    return render(request, "events/event_list.html", {"events": events})


def event_detail(request, event_id):
    with get_connection() as conn:
        row = conn.execute(
            "SELECT id, name, max_duration FROM events WHERE id = ?",
            (event_id,),
        ).fetchone()
    event = Event(row["id"], row["name"], row["max_duration"]) if row else None
    return render(
        request,
        "events/event_detail.html",
        {"event": event},
        status=404 if event is None else 200,
    )
