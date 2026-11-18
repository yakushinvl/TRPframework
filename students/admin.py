from django.contrib import admin
from presentations.models import Presentation
from students.models import Student


class PresentationInline(admin.TabularInline):
    model = Presentation
    extra = 0
    fields = ("event", "title", "duration", "status")
    autocomplete_fields = ("event",)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "group", "presentations_count")
    list_display_links = ("name",)
    search_fields = ("name", "group")
    list_filter = ("group",)
    ordering = ("name",)
    list_per_page = 20
    readonly_fields = ("id",)
    inlines = [PresentationInline]

    @admin.display(description="выступлений")
    def presentations_count(self, obj):
        return obj.presentations.count()
