from core.models import Playlist,Song, Album
from authentication.models import User
from django.db.models import Count
from fuzzywuzzy import fuzz
from queue import PriorityQueue
from collections import defaultdict
def recommendations(name,length,auto_suggest,category,request):
    curated_playlist = []
    songs = Song.objects.all()
    userSongs = None
    for idx, playlist in enumerate(request.user.playlists.all()):
        if idx == 0:
            userSongs = playlist.song.all()
        else:
            userSongs = userSongs | playlist.song.all()
        
    playlist = None
    if userSongs:
        song_pk = [song.id for song in userSongs.all()]
        # Basic logic : Match songs in db to users playlists songs using genre/artist/album or all
        # If length of those songs is less than required length add songs from the users playlists
        # Every match is given a score using fuzzywuzzy library higher the score higher the similarity
        # between two songs
        if category == "genre":
            genre_list = [song.genre for song in userSongs.all()]
            genre_list = sorted(genre_list,key= genre_list.count,reverse=True)
            genre_dict = defaultdict(int)
            for genre in genre_list:
                genre_dict[genre] += 1
            completed_genres = []
            for genre in genre_list:
                if genre not in completed_genres:
                    genre_songs = Song.objects.exclude(pk__in=song_pk).filter(genre=genre).all()
                    curated_playlist += genre_songs[:round(genre_dict[genre]/len(genre_list)*length)]
                    completed_genres.append(genre)
                

            if len(curated_playlist) < length:
                curated_playlist.extend(userSongs.all()[:length-len(curated_playlist)])
            
        elif category == "album":
            album_list = []
            curated_playlist = Song.objects.none()
            for song in userSongs:
                if song.album:
                    album_list.append(song.album.id)
            album_list = sorted(album_list,key= album_list.count,reverse=True)
            album_dict = defaultdict(int)
            for album in album_list:
                album_dict[album] += 1
            completed_albums = []
            for album in album_list:
                if album not in completed_albums:
                    album_songs = Album.objects.get(pk=album).songs.exclude(pk__in=song_pk)
                    curated_playlist = curated_playlist | album_songs[:round(album_dict[album]/len(album_list)*length)]
                    completed_albums.append(album)
            if len(curated_playlist) < length:
                curated_playlist = curated_playlist | Song.objects.filter(pk__in=song_pk).all()[:length-len(curated_playlist)]
            
        elif category == "artist":
            artist_list = []
            curated_playlist = Song.objects.none()
            for song in userSongs:
                if song.artist.user.username:
                    artist_list.append(song.artist.user.username)
            
            artist_list = sorted(artist_list,key=artist_list.count,reverse=True)
            artist_dict = defaultdict(int)
            for artist in artist_list:
                artist_dict[artist] += 1
            completed_artist = []
            for artist in artist_list:
                if artist not in completed_artist:
                    artist_songs = User.objects.get(username=artist).artist_account.songs_artist.exclude(pk__in=song_pk)
                    curated_playlist = curated_playlist | artist_songs[:round(artist_dict[artist]/len(artist_list)*length)]
                    completed_artist.append(artist)
            
            if len(curated_playlist) < length:
                curated_playlist = curated_playlist | Song.objects.filter(pk__in=song_pk).all()[:length-len(curated_playlist)]
            
        else:
            user_song_list = [(song.id, ''.join([song.title,song.genre,song.artist.user.username,song.album.title if song.album else ""])) for song in userSongs]
            s = Song.objects.exclude(pk__in=song_pk)
            
            possible_playlist_songs = [(song.id, ''.join([song.title,song.genre,song.artist.user.username,song.album.title if song.album else ""])) for song in s]
            q = PriorityQueue()
            for possible_playlist_song in possible_playlist_songs:
                song_score = 0
                for user_song in user_song_list:
                    song_score += fuzz.WRatio(user_song[1],possible_playlist_song[1])
                
                q.put((-song_score,possible_playlist_song[0]))
            
            while not q.empty():
                next_item = q.get()
                curated_playlist.append(next_item[1])
            if len(curated_playlist) < length:
                curated_playlist.extend(song_pk[:length-len(curated_playlist)])
            songs = Song.objects.filter(pk__in=curated_playlist)
            curated_playlist = songs
    else:
        curated_playlist = Song.objects.all()[:length]
    return curated_playlist