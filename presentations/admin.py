from django.contrib import admin
from presentations.models import Presentation


@admin.register(Presentation)
class PresentationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "event",
        "student",
        "student_group",
        "title",
        "duration",
        "status",
        "total_score",
        "result",
    )
    list_display_links = ("id", "title")
    list_filter = ("event", "status")
    search_fields = ("title", "student__name", "event__name")
    autocomplete_fields = ("event", "student")
    list_select_related = ("event", "student")
    readonly_fields = ("id", "total_score", "result")
    ordering = ("-id",)
    list_per_page = 20
    actions = ["mark_completed", "mark_active", "mark_cancelled"]

    @admin.display(description="группа")
    def student_group(self, obj):
        return obj.student.group

    @admin.action(description="отметить как завершённые")
    def mark_completed(self, request, queryset):
        queryset.update(status=Presentation.Status.COMPLETED)

    @admin.action(description="отметить как активные")
    def mark_active(self, request, queryset):
        queryset.update(status=Presentation.Status.ACTIVE)

    @admin.action(description="отметить как отменённые")
    def mark_cancelled(self, request, queryset):
        queryset.update(status=Presentation.Status.CANCELLED)
