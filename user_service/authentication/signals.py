from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    # This ensures the profile is created if missing, or retrieved if already exists
    user_profile, _ = UserProfile.objects.get_or_create(user=instance)
    # Now you can perform additional actions here if needed, for instance:
    # user_profile.some_field = 'some_value'
    user_profile.save()  # Save any changes to the profile
