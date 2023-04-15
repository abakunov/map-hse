from django.db.models import fields
from rest_framework import serializers
from rest_framework.fields import Field
from rest_framework.serializers import Serializer

import datetime

from core.models import *

class LocationSerializer(serializers.ModelSerializer):
    floor = serializers.Field()

    class Meta:
        model = Location
        fields = ('x', 'y', 'floor')

    @property
    def floor(self):
        return self.floor.number


class UserSerializer(serializers.ModelSerializer):
    views_all_time = serializers.Field()
    views_today = serializers.Field()
    # location = LocationSerializer()

    class Meta:
        model = User
        fields = ('id', 'tg_id', 'tg_username', 'name', 'age', 'bio', 'department', 'photo', 'song', 'interests', 'views_all_time', 'views_today', 'last_time_set_location')
        depth = 3

    @property
    def in_coworking(self):
        return self.last_time_set_location > datetime.datetime.now() - datetime.timedelta(hours=1)

    @property
    def views_all_time(self):
        return ProfileView.objects.filter(target_user=self).count()
    
    @property
    def views_today(self):
        return ProfileView.objects.filter(target_user=self, time__date=datetime.date.today()).count()


class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = '__all__'


class FloorSerializer(serializers.ModelSerializer):
    map_height = serializers.Field()
    map_width = serializers.Field()
    
    class Meta:
        model = Floor
        fields = ('map_image', 'number', 'map_height', 'map_width')

    @property
    def map_height(self):
        return self.map_image.height
    
    @property
    def map_width(self):
        return self.map_image.width


class MapSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'photo', 'location')
        depth = 1
