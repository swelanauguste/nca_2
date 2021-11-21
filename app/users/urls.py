from django.urls import path

from . import views

app_name = "users"


urlpatterns = [
    path(
        "detail/<slug:slug>", views.ProfileDetailView.as_view(), name="profile-detail"
    ),
    path("edit/<slug:slug>", views.ProfileUpdateView.as_view(), name="profile-update"),
]
