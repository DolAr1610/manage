from django.db import models
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated

from djangoProject import settings


class Song(models.Model):
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    album = models.CharField(max_length=200, blank=True)
    release_year = models.IntegerField()

    class Meta:
        db_table = 'Song'


class Playlist(models.Model):
    title = models.CharField(max_length=200)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='playlists')
    is_public = models.BooleanField(default=False)
    songs = models.ManyToManyField(Song)

    class Meta:
        db_table = 'Playlist'
