from events.models import Event


def events_context(request):
    return {
        "site_name": "учёт выступлений",
        "events_count": Event.objects.count(),
    }
