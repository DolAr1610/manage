from django.urls import path
from .views import *

urlpatterns = [
    path('song/', SongView.as_view(), name='song'),
    path('song/<int:pk>/', SongView.as_view(), name='song-id'),

    path('playlist/', PlaylistView.as_view(), name='playlist'),
    path('playlist/<int:pk>/', PlaylistView.as_view(), name='playlist-id'),
]
