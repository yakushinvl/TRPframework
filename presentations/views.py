from django.core.paginator import Paginator
from django.db.models import Avg, Count, F, Max, Min, Q
from django.shortcuts import get_object_or_404, render
from events.models import Event
from presentations.models import Presentation
from students.models import Student


def presentation_list(request):
    q = request.GET.get("q", "").strip()
    event_id = request.GET.get("event", "").strip()
    student_id = request.GET.get("student", "").strip()
    sort = request.GET.get("sort", "id").strip()
    regulation_only = request.GET.get("regulation", "").strip()

    qs = Presentation.objects.select_related("event", "student")

    if q:
        qs = qs.filter(Q(title__icontains=q) | Q(student__name__icontains=q))

    if event_id.isdigit():
        qs = qs.filter(event_id=int(event_id))

    if student_id.isdigit():
        qs = qs.filter(student_id=int(student_id))

    if regulation_only == "1":
        qs = qs.exclude(duration__gt=F("event__max_duration"))

    sort_fields = {
        "id": "id",
        "title": "title",
        "duration": "duration",
        "-duration": "-duration",
        "student": "student__name",
        "event": "event__name",
    }
    sort_field = sort_fields.get(sort, "id")
    qs = qs.order_by(sort_field, "id")

    paginator = Paginator(qs, 5)
    page_obj = paginator.get_page(request.GET.get("page"))

    context = {
        "presentations": page_obj,
        "page_obj": page_obj,
        "events": Event.objects.order_by("name"),
        "students": Student.objects.order_by("name"),
        "q": q,
        "selected_event": event_id,
        "selected_student": student_id,
        "selected_sort": sort,
        "regulation_only": regulation_only,
    }
    return render(request, "presentations/presentation_list.html", context)


def presentation_detail(request, presentation_id):
    p = get_object_or_404(
        Presentation.objects.select_related("event", "student"),
        pk=presentation_id,
    )
    return render(request, "presentations/presentation_detail.html", {"p": p})


def statistics(request):
    events_stats = Event.objects.annotate(
        count=Count("presentations"),
        avg_duration=Avg("presentations__duration"),
        avg_score=Avg(F("presentations__score_1") + F("presentations__score_2")),
    ).order_by("-count", "name")

    summary = Presentation.objects.aggregate(
        total_count=Count("id"),
        avg_duration=Avg("duration"),
        min_duration=Min("duration"),
        max_duration=Max("duration"),
        avg_score=Avg(F("score_1") + F("score_2")),
    )
    return render(
        request,
        "presentations/statistics.html",
        {"events_stats": events_stats, "summary": summary},
    )
