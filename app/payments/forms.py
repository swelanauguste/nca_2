from django import forms
from django.forms import widgets

from .models import Client, License, Location, LicensePayment


class ClientUpdateForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = "__all__"
        widgets = {
            "dob": widgets.TextInput(attrs={"type": "date"}),
        }


class LicensePaymentCreateForm(forms.ModelForm):
    class Meta:
        model = LicensePayment
        fields = "__all__"
        exclude = ["slug"]
