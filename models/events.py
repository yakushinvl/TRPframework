class Event:
    def __init__(self, id, name, max_duration):
        self.id = id
        self.name = name
        self.max_duration = max_duration

    def __str__(self):
        return f"[{self.id}] {self.name} (лимит: {self.max_duration} мин)"

def add_event(events, name, max_duration):
    event = Event(len(events) + 1, name, max_duration)
    events.append(event)
    return event

def find_event_by_id(events, event_id):
    for e in events:
        if e.id == event_id:
            return e
    return None

def sort_events(events):
    return sorted(events, key=lambda e: e.name)
