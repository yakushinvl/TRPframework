from django.shortcuts import render
from db.database import get_connection
from models.events import Event
from models.presentations import Presentation
from models.students import Student

SELECT_PRESENTATION = """
SELECT
    p.id, p.title, p.duration, p.score_1, p.score_2,
    s.id AS student_id, s.name AS student_name, s.group_name,
    e.id AS event_id, e.name AS event_name, e.max_duration
FROM presentations p
JOIN students s ON p.student_id = s.id
JOIN events e ON p.event_id = e.id
"""


def row_to_presentation(row):
    student = Student(row["student_id"], row["student_name"], row["group_name"])
    event = Event(row["event_id"], row["event_name"], row["max_duration"])
    return Presentation(
        row["id"],
        event,
        student,
        row["title"],
        row["duration"],
        row["score_1"],
        row["score_2"],
    )


def presentation_list(request):
    q = request.GET.get("q", "").strip()
    sql = SELECT_PRESENTATION
    params = []
    if q:
        sql += " WHERE s.name LIKE ? OR p.title LIKE ?"
        params = [f"%{q}%", f"%{q}%"]
    sql += " ORDER BY p.id"

    with get_connection() as conn:
        rows = conn.execute(sql, params).fetchall()
        presentations = [row_to_presentation(r) for r in rows]

    return render(
        request,
        "presentations/presentation_list.html",
        {"presentations": presentations, "q": q},
    )


def presentation_detail(request, presentation_id):
    sql = SELECT_PRESENTATION + " WHERE p.id = ?"
    with get_connection() as conn:
        row = conn.execute(sql, (presentation_id,)).fetchone()
    p = row_to_presentation(row) if row else None
    return render(
        request,
        "presentations/presentation_detail.html",
        {"p": p},
        status=404 if p is None else 200,
    )


def statistics(request):
    with get_connection() as conn:
        events_stats = conn.execute(
            """
            SELECT
                e.id,
                e.name,
                COUNT(p.id) AS count,
                COALESCE(AVG(p.duration), 0) AS avg_duration,
                COALESCE(AVG(p.score_1 + p.score_2), 0) AS avg_score
            FROM events e
            LEFT JOIN presentations p ON e.id = p.event_id
            GROUP BY e.id, e.name
            ORDER BY e.id
            """
        ).fetchall()
        summary = conn.execute(
            """
            SELECT
                COUNT(id) AS total_count,
                COALESCE(AVG(duration), 0) AS avg_duration,
                COALESCE(MIN(duration), 0) AS min_duration,
                COALESCE(MAX(duration), 0) AS max_duration,
                COALESCE(AVG(score_1 + score_2), 0) AS avg_score
            FROM presentations
            """
        ).fetchone()

    return render(
        request,
        "presentations/statistics.html",
        {"events_stats": events_stats, "summary": summary},
    )
