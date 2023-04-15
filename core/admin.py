from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Song)
admin.site.register(Interest)
admin.site.register(Floor)
admin.site.register(Location)
admin.site.register(ProfileView)
