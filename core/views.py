from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import response, decorators, permissions, status
from core.serializers import SongSerializer,PlaylistSerializer,AlbumSerializer
from django.core.files.storage import FileSystemStorage
from django.contrib.sites.shortcuts import get_current_site
from core.models import Playlist,Song, Album
from core.helper import recommendations
import uuid

# Retrieves all playlist or creates a playlist
class PlaylistView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request,format='json'):
        
        playlist = request.user.playlists.all()
        playlistSerial = PlaylistSerializer(playlist,many=True)
        
        return Response(playlistSerial.data,status=status.HTTP_200_OK)
    def post(self,request,format='json'):
        context = {'request':request}
        playlist = PlaylistSerializer(data=request.data,context = context)
        if playlist.is_valid():
            playlist.save()
            return Response(playlist.data,status=status.HTTP_201_CREATED)
        return Response(playlist.errors,status=status.HTTP_400_BAD_REQUEST)
    
# Retrives a single playlist or deletes the playlist
class PlaylistDetail(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request,pk,format='json'):
        playlist = Playlist.objects.get(pk=pk)
        playlistSerial = PlaylistSerializer(playlist)
        return Response(playlistSerial.data,status=status.HTTP_200_OK)
 
    
    def delete(self,request,pk,format=None):
        playlist = Playlist.objects.get(pk)
        playlist.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Adds song(s) to a give Playlist
class PlaylistSong(APIView):
    def post(self,request):
        song_pk = request.data["song_pk"]
        playlist_pk = request.data["playlist_pk"]
        try:
            playlist = Playlist.objects.get(pk= playlist_pk)
        except Playlist.DoesNotExist:
            return Response("Playlist Does not exist",status=status.HTTP_404_NOT_FOUND)
        if isinstance(song_pk,list):
            song = Song.objects.get(pk__in=song_pk)
            playlist.song.set(song)
        else:
            song = Song.objects.get(pk=song_pk)
            playlist.song.add(song)


        return Response(status=status.HTTP_201_CREATED)
   
    def delete(self,request):
        song_pk = request.data["song_pk"]
        playlist_pk = request.data["playlist_pk"]
        song = Song.objects.get(pk=song_pk)
        playlist = Playlist.objects.get(pk= playlist_pk)
        playlist.song.remove(song)
        return Response(status=status.HTTP_204_NO_CONTENT)

# Allows an artist to add a song or for a user(Artist/Consumer) to retrieve all songs 
class SongView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request,format="json"):
        if request.user.accountType != 'A':
            return Response({"Response":"Not Allowed"},status=status.HTTP_403_FORBIDDEN)
        if request.FILES['song']:
            song = request.FILES['song']
            
            fs = FileSystemStorage()
            filename = fs.save('./static/'+song.name,song)
            song_url = 'http://'+str(get_current_site(request))+fs.url(filename)
            data = {
                "title":request.data["title"],
                "url": song_url,
                "genre":request.data["genre"],
                "release_date":request.data["release_date"]
            }
            context = {'request':request}
            song = SongSerializer(data=data,context=context)
            if song.is_valid():
                song.save()

                return Response(song.data,status=status.HTTP_200_OK)
            return Response(song.errors,status=status.HTTP_400_BAD_REQUEST)
            
        return Response({"eror":"No song provided"},status=status.HTTP_400_BAD_REQUEST)

    def get(self,request):
        song_pk = request.GET.get("song_pk","")
        songs = Song.objects.all()

        if song_pk:
            songs = Song.objects.get(pk=pk)
        songSerializer = SongSerializer(songs,many=True)

        return Response(songSerializer.data,status=status.HTTP_200_OK)

# Allows an artist to create an album
class AlbumCreate(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request):
        if request.user.accountType != 'A':
            return Response({"Response":"Not Allowed"},status=status.HTTP_403_FORBIDDEN)
        
        context = {"request":request}

        album = AlbumSerializer(data=request.data,context=context)
        if album.is_valid():
            album.save()
            return Response(album.data,status=status.HTTP_200_OK)
        return Response(album.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def get(self,request):
        album_pk = request.GET.get("album_pk","")
        if not album_pk:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        album = Album.objects.get(pk=album_pk)
        return Response(AlbumSerializer(album).data,status=status.HTTP_200_OK)

# Allows an artist to add songs to an album
class AlbumSong(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request):
        if request.user.accountType != 'A':
            return Response({"Response":"Not Allowed"},status=status.HTTP_403_FORBIDDEN)
        song_pks = request.data["song_pks"]
        album_pk = request.data["album_pk"]
        songs = Song.objects.filter(pk__in=song_pks)
        album = Album.objects.get(pk=album_pk)

        album.songs.set(songs)

        return Response(status=status.HTTP_201_CREATED)

# Recommends new songs or curates a playlist
class RecommendationSystem(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request):
        category = request.data.get("category","")
        length = request.data.get("length",10)
        name = request.data.get("name",uuid.uuid4().hex[:6].upper())
        curated_playlist = recommendations(name,length,True,category,request)
       
        songs = SongSerializer(curated_playlist,many=True)
        return Response(songs.data,status=status.HTTP_202_ACCEPTED)
    def post(self,request):
        category = request.data.get("category","")
        length = request.data.get("length",10)
        name = request.data.get("name",uuid.uuid4().hex[:6].upper())
        curated_playlist = recommendations(name,length,False,category,request)
       
        
        playlist = Playlist.objects.create(name = name,user=request.user)
        playlist.song.set(curated_playlist)
        playlist = PlaylistSerializer(playlist)
        return Response(playlist.data,status=status.HTTP_201_CREATED)
        
            