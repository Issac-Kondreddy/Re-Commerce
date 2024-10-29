# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    # Check if the profile exists, create it if missing
    if created:
        UserProfile.objects.create(user=instance)
    else:
        # This ensures the profile is created if somehow it's missing on an existing user
        UserProfile.objects.get_or_create(user=instance)
    instance.userprofile.save()  # Save profile to handle any changes

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
