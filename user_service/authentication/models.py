from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)  # ImageField for profile picture
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    dob = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True)
    gender = models.CharField(max_length=10, blank=True)
    phone_number = PhoneNumberField(blank=True, null=True)  # Allowing null and blank

    def __str__(self):
            return f"{self.user.username}'s Profile"