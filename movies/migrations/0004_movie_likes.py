# Generated by Django 3.2.10 on 2022-02-05 19:19

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('movies', '0003_alter_movie_favorite'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='likes', to=settings.AUTH_USER_MODEL),
        ),
    ]