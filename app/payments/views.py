from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Sum, fields
from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .forms import ClientUpdateForm
from .models import Client, License, IssuedLicense, LicensePayment, Location, Year


class YearListView(LoginRequiredMixin, ListView):
    model = Year


class ClientSearchListView(LoginRequiredMixin, ListView):
    model = Client
    paginate_by = 25

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


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    paginate_by = 10


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
    paginate_by = 10


class LicenseSearchListView(LoginRequiredMixin, ListView):
    model = License
    paginate_by = 25

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get("q")
        if query:
            clients = Client.objects.filter(
                Q(license__icontains=query) | Q(annual_fee__icontains=query)
            ).distinct()
            context["object_list"] = License
        else:
            context["object_list"] = License.objects.all()
        return context


class LocationListView(LoginRequiredMixin, ListView):
    model = Location


class LicensePaymentListView(LoginRequiredMixin, ListView):
    model = LicensePayment
    paginate_by = 10


class LicensePaymentDetailView(LoginRequiredMixin, DetailView):
    model = LicensePayment


class LicensePaymentUpdateView(LoginRequiredMixin, UpdateView):
    model = LicensePayment
    fields = "__all__"
    template_name_suffix = "_update_form"
    
