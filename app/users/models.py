from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django.urls import reverse


class User(AbstractUser):
    # is_customer = models.BooleanField(default=True)
    # is_dispatcher = models.BooleanField(default=False)
    # is_team_lead = models.BooleanField(default=False)
    # is_driver = models.BooleanField(default=False)
    pass


class Profile(models.Model):
    """
    User Profile model
    """

    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    dob = models.DateField("date of birth", blank=True, null=True)
    gender = models.CharField(max_length=1)
    contact = models.CharField(max_length=15)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.username)
        super(Profile, self).save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse("users:profile-detail", kwargs={"slug": self.slug})
    

    def get_email(self):
        return self.user.email

    def __str__(self):
        if self.first_name and self.last_name:
            return self.first_name + " " + self.last_name
        return self.user.username
