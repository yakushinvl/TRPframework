from models import Event
from models.events import add_event, find_event_by_id, sort_events

def test_event_creation():
    e = Event(1, "Конференция", 10)
    assert e.id == 1
    assert e.name == "Конференция"
    assert e.max_duration == 10
    assert "Конференция" in str(e)

def test_add_event():
    events = []
    add_event(events, "Семинар", 15)
    assert len(events) == 1
    assert events[0].max_duration == 15

def test_find_event_by_id():
    events = [Event(1, "Форум", 20)]
    assert find_event_by_id(events, 1) is not None
    assert find_event_by_id(events, 2) is None

def test_sort_events():
    events = [Event(1, "Форум", 10), Event(2, "Ассамблея", 10)]
    sorted_ev = sort_events(events)
    assert sorted_ev[0].name == "Ассамблея"
