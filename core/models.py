from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime


class User(models.Model):
    tg_id = models.PositiveIntegerField(unique=True)
    tg_username = models.CharField(max_length=1000, unique=True)
    name = models.CharField(max_length=1000)
    department = models.CharField(max_length=1000)
    bio = models.TextField(blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    interests = models.ManyToManyField('Interest', related_name='interests', blank=True)
    photo = models.ImageField(blank=True, null=True)
    song = models.ForeignKey('Song', on_delete=models.SET_NULL, blank=True, null=True)
    location = models.ForeignKey('Location', on_delete=models.SET_NULL, blank=True, null=True)

    last_time_set_location = models.DateTimeField(default=datetime.datetime(2001, 1, 1))

    blacklist = models.ManyToManyField('User', related_name='blacklist_users', blank=True)

    # переделать счетчик просмотров
    @property
    def views_all_time(self):
        return ProfileView.objects.filter(target_user=self).count()

    @property
    def views_today(self):
        return ProfileView.objects.filter(target_user=self, time__date=datetime.date.today()).count()

    @property
    def in_coworking(self):
        return self.last_time_set_location > datetime.datetime.now() - datetime.timedelta(hours=1)

    def __str__(self):
        return str(self.tg_id)


class ProfileView(models.Model):
    from_user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='from_user', blank=True, null=True)
    target_user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='target_user', blank=True, null=True)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.from_user) + ' ' + str(self.target_user)


class Interest(models.Model):
    name = models.CharField(max_length=1000)

    def __str__(self):
        return self.name


class Floor(models.Model):
    map_image = models.ImageField()
    number = models.PositiveIntegerField(unique=True)
    
    @property
    def map_height(self):
        return self.map_image.height
    
    @property
    def map_width(self):
        return self.map_image.width

    def __str__(self):
        return str(self.number)


class Location(models.Model):
    floor = models.ForeignKey('Floor', on_delete=models.CASCADE)
    x = models.PositiveIntegerField()
    y = models.PositiveIntegerField()

    def __str__(self):
        return str(self.floor) + ' ' + str(self.x) + ' ' + str(self.y)


class Song(models.Model):
    name = models.CharField(max_length=1000)
    artist = models.CharField(max_length=1000)
    cover = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.name + ' ' + self.artist