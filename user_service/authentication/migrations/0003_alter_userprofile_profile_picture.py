# Generated by Django 5.0.3 on 2024-10-24 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "authentication",
            "0002_remove_userprofile_city_remove_userprofile_country_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="userprofile",
            name="profile_picture",
            field=models.ImageField(blank=True, null=True, upload_to="profile_pics/"),
        ),
    ]