from rest_framework import serializers

from User.models import User
from .models import Song, Playlist


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ['id', 'title', 'artist', 'album', 'release_year']


class PlaylistSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Playlist
        fields = ['id', 'title', 'created_by', 'is_public', 'songs']
