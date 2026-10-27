from django.urls import path
from . import views

urlpatterns = [
    path("", views.presentation_list, name="presentation_list"),
    path("<int:presentation_id>/", views.presentation_detail, name="presentation_detail"),
]
