# Generated by Django 4.2 on 2023-05-18 15:31

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_visitor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visitor',
            name='timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
