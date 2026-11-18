import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tracker.settings")
django.setup()

from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.db.models import Avg, Count, F, Max, Min, Q
from django.test import Client, RequestFactory
from events.context_processors import events_context
from events.models import Event
from presentations.models import Presentation
from students.models import Student


def test_models_creation():
    event, _ = Event.objects.get_or_create(name="Тестовое мероприятие", defaults={"max_duration": 12})
    student, _ = Student.objects.get_or_create(name="Тестовый Студент", defaults={"group": "ЭФБО-16-24"})
    presentation, _ = Presentation.objects.get_or_create(
        event=event,
        student=student,
        title="Тестовый доклад",
        defaults={"duration": 10, "score_1": 4.5, "score_2": 4.7},
    )
    assert event.pk is not None
    assert student.pk is not None
    assert presentation.pk is not None
    assert "Тестовое мероприятие" in str(event)
    assert "Тестовый Студент" in str(student)
    assert "Тестовый доклад" in str(presentation)
    assert presentation.total_score == 9.2
    assert presentation.result == "1 место"
    assert presentation.check_duration() == "в регламенте"


def test_orm_relationships_and_reverse():
    event, _ = Event.objects.get_or_create(name="Хакатон", defaults={"max_duration": 10})
    student, _ = Student.objects.get_or_create(name="Иванов И.", defaults={"group": "ЭФБО-16-24"})
    p1, _ = Presentation.objects.get_or_create(
        event=event,
        student=student,
        title="Проект 1",
        defaults={"duration": 8, "score_1": 4.0, "score_2": 4.0},
    )
    p2, _ = Presentation.objects.get_or_create(
        event=event,
        student=student,
        title="Проект 2",
        defaults={"duration": 12, "score_1": 4.5, "score_2": 4.5},
    )
    assert event.presentations.count() >= 2
    assert student.presentations.count() >= 2
    assert p1.event == event
    assert p2.student == student


def test_orm_filter_exclude_search_sorting():
    event, _ = Event.objects.get_or_create(name="Секция 1", defaults={"max_duration": 10})
    student, _ = Student.objects.get_or_create(name="Сидоров С.", defaults={"group": "ЭФБО-16-24"})
    Presentation.objects.get_or_create(
        event=event,
        student=student,
        title="Алгоритмы",
        defaults={"duration": 7, "score_1": 4.5, "score_2": 4.5},
    )
    Presentation.objects.get_or_create(
        event=event,
        student=student,
        title="Архитектура",
        defaults={"duration": 12, "score_1": 4.0, "score_2": 4.0},
    )

    # filter
    short = Presentation.objects.filter(duration__lte=10)
    assert short.exists()

    # filter by related field
    by_group = Presentation.objects.filter(student__group="ЭФБО-16-24")
    assert by_group.exists()

    # exclude
    excluded = Presentation.objects.exclude(duration__gt=10)
    assert excluded.exists()

    # search
    search_res = Presentation.objects.filter(Q(title__contains="Алгоритм"))
    assert search_res.exists()

    # sorting
    sorted_res = Presentation.objects.order_by("-duration")
    assert sorted_res.first().duration >= 12


def test_orm_aggregation_and_annotation():
    summary = Presentation.objects.aggregate(
        total=Count("id"),
        avg_dur=Avg("duration"),
        min_dur=Min("duration"),
        max_dur=Max("duration"),
    )
    assert summary["total"] >= 1
    assert summary["avg_dur"] > 0
    assert summary["min_dur"] > 0

    events = Event.objects.annotate(
        count=Count("presentations"),
        avg_dur=Avg("presentations__duration"),
    )
    assert events.exists()


def test_paginator():
    qs = Presentation.objects.all()
    paginator = Paginator(qs, 5)
    page1 = paginator.get_page(1)
    assert len(page1) > 0


def test_views_endpoints():
    client = Client()
    assert client.get("/").status_code == 200
    assert client.get("/events/").status_code == 200
    assert client.get("/events/1/").status_code == 200
    assert client.get("/events/9999/").status_code == 404
    assert client.get("/presentations/").status_code == 200
    assert client.get("/presentations/?event=1").status_code == 200
    assert client.get("/presentations/?q=веб").status_code == 200
    assert client.get("/presentations/?sort=duration").status_code == 200
    assert client.get("/presentations/?regulation=1").status_code == 200
    assert client.get("/presentations/1/").status_code == 200
    assert client.get("/presentations/9999/").status_code == 404
    assert client.get("/presentations/statistics/").status_code == 200


def test_slug_and_generated_field():
    ev, _ = Event.objects.get_or_create(
        name="Большая конференция 2026",
        defaults={"max_duration": 20},
    )
    assert ev.slug is not None
    assert "bolshaia-konferentsiia-2026" in ev.slug
    assert ev.is_long is True
    assert ev.get_absolute_url() == f"/events/{ev.slug}/"

    client = Client()
    resp = client.get(ev.get_absolute_url())
    assert resp.status_code == 200


def test_presentation_statuses_and_manager():
    event, _ = Event.objects.get_or_create(name="Тест Статусов", defaults={"max_duration": 15})
    student, _ = Student.objects.get_or_create(name="Тест Студент", defaults={"group": "ЭФБО-16-24"})

    p_active, _ = Presentation.objects.get_or_create(
        event=event,
        student=student,
        title="Активный доклад",
        defaults={"duration": 10, "score_1": 4.0, "score_2": 4.0, "status": Presentation.Status.ACTIVE},
    )
    p_cancelled, _ = Presentation.objects.get_or_create(
        event=event,
        student=student,
        title="Отмененный доклад",
        defaults={"duration": 5, "score_1": 0.0, "score_2": 0.0, "status": Presentation.Status.CANCELLED},
    )

    assert Presentation.objects.active().filter(pk=p_active.pk).exists()
    assert Presentation.objects.cancelled().filter(pk=p_cancelled.pk).exists()
    assert not Presentation.objects.completed().filter(pk=p_cancelled.pk).exists()


def test_context_processor():
    rf = RequestFactory()
    req = rf.get("/")
    ctx = events_context(req)
    assert "site_name" in ctx
    assert "events_count" in ctx
    assert ctx["events_count"] == Event.objects.count()


def test_admin_panel():
    User = get_user_model()
    admin_user, _ = User.objects.get_or_create(
        username="admin",
        defaults={"is_superuser": True, "is_staff": True},
    )
    admin_user.set_password("admin")
    admin_user.is_superuser = True
    admin_user.is_staff = True
    admin_user.save()

    client = Client()
    client.login(username="admin", password="admin")

    assert client.get("/admin/").status_code == 200
    assert client.get("/admin/events/event/").status_code == 200
    assert client.get("/admin/students/student/").status_code == 200
    assert client.get("/admin/presentations/presentation/").status_code == 200
