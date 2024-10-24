# Generated migration file
from django.db import migrations

def create_profiles(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    UserProfile = apps.get_model('authentication', 'UserProfile')
    
    for user in User.objects.all():
        if not hasattr(user, 'userprofile'):
            UserProfile.objects.create(user=user)

class Migration(migrations.Migration):

    dependencies = [
       (
            "authentication",
            "0002_remove_userprofile_city_remove_userprofile_country_and_more",
        ),
    ]

    operations = [
        migrations.RunPython(create_profiles),
    ]

