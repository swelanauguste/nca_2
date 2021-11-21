from django.shortcuts import render
from django.views.generic import UpdateView, DetailView, ListView
from .models import Profile
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = "__all__"
    template_name_suffix = '_update_form'
    


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
