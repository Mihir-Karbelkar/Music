from rest_framework import serializers
from core.models import Song,Playlist,Album
from authentication.serializers import ArtistSerializer

class AlbumSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    artwork = serializers.URLField(required=False)
    release_date = serializers.DateField(required=False)
    
class SongSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    genre = serializers.CharField()
    url = serializers.URLField()
    release_date = serializers.DateField()
    album = AlbumSerializer(read_only=True)
    artist = ArtistSerializer(read_only=True)
    class Meta:
        model = Song
        fields = ['__all__','songs_artist']
    def create(self,validated_data):
        print(self.context['request'].user.accountType)
        song = Song.objects.create(artist=self.context['request'].user.artist_account,**validated_data)
        return song


class PlaylistSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    description = serializers.CharField()
    artwork = serializers.URLField()
    song = SongSerializer(read_only=True,many=True)
    class Meta:
        model = Playlist
        fields = ('id','name','description','artwork','song')
    
    def create(self,validated_data):
        print(validated_data)
        playlist = Playlist.objects.create(user=self.context['request'].user,**validated_data)
        print(playlist.artwork)
        return playlist

class AlbumSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    artwork = serializers.URLField(required=False)
    release_date = serializers.DateField(required=False)
    songs = SongSerializer(read_only=True,many=True)
    class Meta:
        model = Album
        fields = ('id','name','description','artwork','songs')
    
    def create(self,validated_data):
        album = Album.objects.create(artist=self.context['request'].user.artist_account,**validated_data)

        return album
        