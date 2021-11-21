from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.db.models import Q
from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .forms import ClientUpdateForm
from .models import Client, License, LicenseItem, LicensePayment, Location, Year


class YearListView(LoginRequiredMixin, ListView):
    model = Year


class ClientListView(LoginRequiredMixin, ListView):
    model = Client

    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get("q")
        if query:
            clients = Client.objects.filter(
                Q(client_name__icontains=query)
                | Q(client_id__icontains=query)
                | Q(phone__icontains=query)
                | Q(nic__icontains=query)
            ).distinct()
            context["object_list"] = clients
        else:
            context["object_list"] = Client.objects.all()
        return context


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientUpdateForm
    template_name_suffix = "_update_form"
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["licenses"] = License.objects.filter(client=self.object)
    #     return context


class LicenseListView(LoginRequiredMixin, ListView):
    model = License


class LocationListView(LoginRequiredMixin, ListView):
    model = Location


class LicensePaymentListView(LoginRequiredMixin, ListView):
    model = LicensePayment
