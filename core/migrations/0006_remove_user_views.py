# Generated by Django 4.2 on 2023-04-14 00:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_remove_profileview_user_profileview_from_user_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='views',
        ),
    ]