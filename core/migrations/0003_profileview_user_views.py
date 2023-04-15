# Generated by Django 4.2 on 2023-04-13 23:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_delete_song_rename_image_floor_map_image_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfileView',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.user')),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='views',
            field=models.ManyToManyField(blank=True, related_name='views', to='core.profileview'),
        ),
    ]