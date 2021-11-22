from django.urls import path

from . import views


urlpatterns = [
    path("", views.YearListView.as_view(), name="year-list"),
    path("clients", views.ClientListView.as_view(), name="client-list"),
    path(
        "client/search", views.ClientSearchListView.as_view(), name="client-search-list"
    ),
    path(
        "client-detail-<slug:slug>",
        views.ClientDetailView.as_view(),
        name="client-detail",
    ),
    path(
        "client-update-<slug:slug>",
        views.ClientUpdateView.as_view(),
        name="client-update",
    ),
    path("licenses", views.LicenseListView.as_view(), name="license-list"),
    path("locations", views.LocationListView.as_view(), name="location-list"),
    path(
        "license-payments",
        views.LicensePaymentListView.as_view(),
        name="license-payment-list",
    ),
    path(
        "license-payment-detail-<slug:slug>",
        views.LicensePaymentDetailView.as_view(),
        name="license-payment-detail",
    ),
    path(
        "license-payment-update-<slug:slug>",
        views.LicensePaymentUpdateView.as_view(),
        name="license-payment-update",
    ),
]
