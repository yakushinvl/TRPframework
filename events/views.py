from django.shortcuts import get_object_or_404, render
from events.models import Event


def event_list(request):
    events = Event.objects.order_by("name")
    return render(request, "events/event_list.html", {"events": events})


def event_detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    return render(request, "events/event_detail.html", {"event": event})


def event_detail_by_slug(request, slug):
    event = get_object_or_404(Event, slug=slug)
    return render(request, "events/event_detail.html", {"event": event})
