from django.contrib import admin
from events.models import Event
from presentations.models import Presentation


class PresentationInline(admin.TabularInline):
    model = Presentation
    extra = 0
    fields = ("student", "title", "duration", "status")
    autocomplete_fields = ("student",)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug", "max_duration", "is_long", "presentations_count")
    list_display_links = ("name",)
    list_editable = ("max_duration",)
    search_fields = ("name", "slug")
    ordering = ("name",)
    list_per_page = 20
    readonly_fields = ("id", "is_long")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [PresentationInline]
    view_on_site = True

    @admin.display(description="выступлений")
    def presentations_count(self, obj):
        return obj.presentations.count()
