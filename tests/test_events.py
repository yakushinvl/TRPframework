from events import add_event, find_event, sort_events


def test_add_event():
    events = []
    add_event(events, "Конференция", 10)
    assert len(events) == 1
    assert events[0]["name"] == "Конференция"


def test_find_event():
    events = [{"id": 1, "name": "Семинар"}]
    assert find_event(events, 1) is not None
    assert find_event(events, 2) is None


def test_sort_events():
    events = [
        {"id": 1, "name": "Форум"},
        {"id": 2, "name": "Ассамблея"}
    ]
    sorted_ev = sort_events(events)
    assert sorted_ev[0]["name"] == "Ассамблея"
