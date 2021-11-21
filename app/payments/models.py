from django.db import models
from django.contrib import admin
from django.utils.text import slugify
from django.urls import reverse


class Location(models.Model):
    location = models.CharField(max_length=255)

    class Meta:
        ordering = ("location",)

    def __str__(self):
        return f"{self.location}"


class License(models.Model):
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    license = models.CharField(max_length=255)
    annual_fee = models.DecimalField(max_digits=10, decimal_places=2, default=500.00)

    class Meta:
        ordering = ("license",)
        unique_together = ("location", "license")

    def __str__(self):
        return f"{self.license}, ({self.location.location} - XCD${self.annual_fee})"


GENDER_LIST = (
    ("M", "M"),
    ("F", "F"),
)


class Client(models.Model):
    client_id = models.CharField(max_length=10, unique=True)
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)
    client_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_LIST, default="M")
    dob = models.DateField("DOB", blank=True, null=True)
    nic = models.CharField("NIC", max_length=10, unique=True, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ("client_name",)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.client_id + " - " + self.client_name)
        super(Client, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("client-detail", kwargs={"slug": self.slug})

    def get_absolute_update_url(self):
        return reverse("client-update", kwargs={"slug": self.slug})

    def __str__(self):
        return f"{self.client_name}({self.client_id})"


class LicenseItem(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    license = models.ForeignKey(License, on_delete=models.CASCADE)
    year = models.ForeignKey("Year", on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"({self.year.year}){self.client.name} - {self.license.license}"


class LicensePayment(models.Model):
    """
    Model representing a payment.
    """

    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)
    year = models.ForeignKey("Year", on_delete=models.SET_DEFAULT, default=1)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def get_license_cost(self):
        return self.client.licenses.all().aggregate(models.Sum("annual_fee"))[
            "annual_fee__sum"
        ]

    @admin.display(description="get client licenses")
    def get_client_licenses(self):
        return self.client.licenses.all()

    @admin.display(description="client total licenses cost")
    def get_client_total_licenses_cost(self):
        return self.get_client_licenses().aggregate(models.Sum("annual_fee"))[
            "annual_fee__sum"
        ]

    @admin.display(description="client total payments")
    def get_client_total_payments(self):
        client_total_payments = LicensePayment.objects.filter(
            client=self.client
        ).aggregate(models.Sum("amount"))["amount__sum"]
        return client_total_payments

    @admin.display(description="client balance")
    def get_client_balance(self):
        clients_balance = (
            self.get_client_total_licenses_cost() - self.get_client_total_payments()
        )
        return clients_balance

    def __str__(self):
        return f"{self.client.name} - XCD${self.amount}"


class Year(models.Model):
    year = models.IntegerField(unique=True)

    @admin.display(description="get_payment_year")
    def get_payment_year(self):
        return LicensePayment.objects.filter(year__year=self.year).aggregate(
            models.Sum("amount")
        )["amount__sum"]

    # @admin.display(description="get_licenses_year")
    # def get_licenses_year(self):
    #     return Payment.objects.filter(client__licenses__license__annual_fee=self.year)

    def __str__(self):
        return f"{self.year}"
