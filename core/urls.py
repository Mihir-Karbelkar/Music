from django.urls import path
from core.views import PlaylistView,SongView,PlaylistDetail, PlaylistSong, AlbumCreate,AlbumSong,RecommendationSystem

urlpatterns = [
    path('playlist/',PlaylistView.as_view()),
    path('playlist/<int:pk>/',PlaylistDetail.as_view()),
    path('song',SongView.as_view()),
    path('addSong',PlaylistSong.as_view()),
    path('album',AlbumCreate.as_view()),
    path('addAlbumSong',AlbumSong.as_view()),
    path('recommendation',RecommendationSystem.as_view()),
]