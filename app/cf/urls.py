from django.contrib import admin
from django.urls import path, include

# from assets.assets import DashboardView

urlpatterns = [
    # path("", DashboardView.as_view(), name="dashboard"),
    path("admin/", admin.site.urls),
    path("profile/", include("users.urls", namespace="users")),
    path("", include("payments.urls")),
    path("accounts/", include("allauth.urls")),
]
