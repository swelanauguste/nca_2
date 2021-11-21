from django import forms
from django.forms import widgets

from .models import Client, License, Location


class ClientUpdateForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = "__all__"
        widgets = {
            "dob": widgets.TextInput(attrs={"type": "date"}),
        }
