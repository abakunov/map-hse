from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Song)
admin.site.register(Interest)
admin.site.register(Floor)
admin.site.register(Location)
admin.site.register(ProfileView)

@admin.register(Visitor)
class Visitor(admin.ModelAdmin):
    list_display = ('tg_id', 'tg_username', 'who_invited', 'timestamp')
    list_filter = ('who_invited', 'timestamp')
    search_fields = ('tg_id', 'tg_username')
    ordering = ('-timestamp',)