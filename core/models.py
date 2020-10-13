from django.db import models
from authentication.models import User,Artist

class Album(models.Model):
    title = models.CharField(max_length=20)
    artwork = models.URLField(null=True)
    release_date = models.DateField(null=True)
    artist = models.ForeignKey(Artist,on_delete=models.CASCADE,related_name='albums')

class Song(models.Model):
    title = models.CharField(max_length=20)
    url = models.URLField(max_length=2048)
    genre = models.CharField(max_length=20)
    artist = models.ForeignKey(Artist,on_delete=models.CASCADE,related_name='songs_artist')
    release_date = models.DateField(null=True)
    album  = models.ForeignKey(Album,on_delete=models.CASCADE,null=True,related_name='songs')
    listenCount = models.IntegerField(default=0)

class Playlist(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=50)
    artwork = models.URLField(max_length=2048)
    song = models.ManyToManyField(Song)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='playlists')




