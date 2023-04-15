# Generated by Django 4.2 on 2023-04-15 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_user_last_time_set_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='blacklist',
            field=models.ManyToManyField(blank=True, related_name='blacklist_users', to='core.user'),
        ),
    ]
