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
    # location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)
    license = models.CharField(max_length=255)
    annual_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.license + " - " + str(self.annual_fee)[:3])
        super(License, self).save(*args, **kwargs)

    class Meta:
        ordering = ("license",)

    def __str__(self):
        return f"{self.license} - XCD${self.annual_fee}"


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
        return f"{self.client_name}({self.client_id.upper()})"


class IssuedLicense(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    license = models.ForeignKey(
        License, related_name="issued_licenses", on_delete=models.CASCADE
    )
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    year = models.ForeignKey(
        "Year", related_name="issued_license_years", on_delete=models.CASCADE
    )
    is_active = models.BooleanField(default=True)
    
    def get_absolute_url(self):
        return reverse("issued-license-detail", kwargs={"pk": self.pk})

    @admin.display(description="get_total_fees_by_year")
    def get_total_fees_by_year(self):
        return IssuedLicense.objects.filter(year=self.year).aggregate(
            total_fees=models.Sum("license__annual_fee")
        )["total_fees"]

    def __str__(self):
        return f"{self.client.client_name} - {self.license.license} ({self.year.year})"


class LicensePayment(models.Model):
    """
    Model representing a payment.
    """

    issued_license = models.ForeignKey(
        IssuedLicense, on_delete=models.SET_NULL, null=True
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)

    class Meta:
        ordering = ("issued_license__year",)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.issued_license)
        super(LicensePayment, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("license-payment-detail", kwargs={"slug": self.slug})

    def get_absolute_update_url(self):
        return reverse("license-payment-update", kwargs={"slug": self.slug})

    def get_license_cost(self):
        return self.client.licenses.all().aggregate(models.Sum("annual_fee"))[
            "annual_fee__sum"
        ]

    #     @admin.display(description="get client licenses")
    #     def get_client_licenses(self):
    #         return self.client.licenses.all()

    #     @admin.display(description="client total licenses cost")
    #     def get_client_total_licenses_cost(self):
    #         return self.get_client_licenses().aggregate(models.Sum("annual_fee"))[
    #             "annual_fee__sum"
    #         ]

    #     @admin.display(description="client total payments")
    #     def get_client_total_payments(self):
    #         client_total_payments = LicensePayment.objects.filter(
    #             client=self.client
    #         ).aggregate(models.Sum("amount"))["amount__sum"]
    #         return client_total_payments

    #     @admin.display(description="client balance")
    #     def get_client_balance(self):
    #         clients_balance = (
    #             self.get_client_total_licenses_cost() - self.get_client_total_payments()
    #         )
    #         return clients_balance

    def __str__(self):
        return f"{self.issued_license} - XCD${self.amount}"


class Year(models.Model):
    year = models.IntegerField(unique=True)

    @admin.display(description="get_issued_licenses_due_per_year")
    def get_issued_licenses_due_per_year(self):
        return IssuedLicense.objects.filter(year__year=self.year).aggregate(
            models.Sum("license__annual_fee")
        )["license__annual_fee__sum"]

    @admin.display(description="get_issued_licenses_paid_per_year")
    def get_issued_licenses_paid_per_year(self):
        get_issued_licenses_paid_per_year = LicensePayment.objects.filter(
            issued_license__year__year=self.year
        ).aggregate(models.Sum("amount"))["amount__sum"]
        return get_issued_licenses_paid_per_year

    def __str__(self):
        return f"{self.year}"
