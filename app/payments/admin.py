from django.contrib import admin

from .models import Client, Location, License, LicensePayment, Year, IssuedLicense

admin.site.register(Client)
admin.site.register(Location)
admin.site.register(License)


@admin.register(IssuedLicense)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "client",
        "license",
        "location",
        "year",
        "is_active",
        "get_total_fees_by_year",
    )


@admin.register(LicensePayment)
class LicensePaymentAdmin(admin.ModelAdmin):
    list_display = (
        "issued_license",
        "amount",
        # "get_client_total_payments",
        # "get_client_balance"
    )


@admin.register(Year)
class LicensePaymentAdmin(admin.ModelAdmin):
    list_display = (
        "year",
        "get_issued_licenses_due_per_year",
        "get_issued_licenses_paid_per_year"
    )
