# Generated by Django 4.2 on 2023-04-20 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_alter_user_tg_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
