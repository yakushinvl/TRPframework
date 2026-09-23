def add_event(events, name, max_duration):
    event = {
        "id": len(events) + 1,
        "name": name,
        "max_duration": max_duration
    }
    events.append(event)
    return event

def find_event(events, event_id):
    for event in events:
        if event.get("id") == event_id:
            return event
    return None

def sort_events(events):
    return sorted(events, key=lambda e: e.get("name", ""))
