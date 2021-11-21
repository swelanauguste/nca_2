from django.contrib import admin

from .models import Client, Location, License, LicensePayment, Year, LicenseItem

admin.site.register(Client)
admin.site.register(Location)
admin.site.register(License)
admin.site.register(LicenseItem)


@admin.register(LicensePayment)
class LicensePaymentAdmin(admin.ModelAdmin):
    list_display = (
        "client",
        "amount",
        "get_client_total_licenses_cost",
        "get_client_total_payments",
        "get_client_balance"
    )

@admin.register(Year)
class LicensePaymentAdmin(admin.ModelAdmin):
    list_display = (
        "year",
        "get_payment_year",
        # "get_licenses_year"
    )
