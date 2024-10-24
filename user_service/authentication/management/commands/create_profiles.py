# create_profiles.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from authentication.models import UserProfile

class Command(BaseCommand):
    help = 'Create missing UserProfile for existing users'

    def handle(self, *args, **kwargs):
        users_without_profile = User.objects.filter(userprofile__isnull=True)
        for user in users_without_profile:
            UserProfile.objects.create(user=user)
            self.stdout.write(self.style.SUCCESS(f'Created profile for {user.username}'))
