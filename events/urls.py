from django.urls import path
from . import views

app_name = "events"

urlpatterns = [
    path("", views.event_list, name="list"),
    path("<int:event_id>/", views.event_detail, name="detail"),
    path("<slug:slug>/", views.event_detail_by_slug, name="detail_by_slug"),
]
