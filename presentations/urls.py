from django.urls import path
from . import views

app_name = "presentations"

urlpatterns = [
    path("", views.presentation_list, name="list"),
    path("statistics/", views.statistics, name="statistics"),
    path("<int:presentation_id>/", views.presentation_detail, name="detail"),
]
