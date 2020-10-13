from django.contrib import admin
from core.models import Song,Playlist,Album
# Register your models here.

admin.site.register(Song)
admin.site.register(Playlist)
admin.site.register(Album)