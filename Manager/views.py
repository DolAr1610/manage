from rest_framework import generics, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import *
from django.http import HttpResponseForbidden


class SongView(APIView):

    def get(self, request, pk=None):
        if pk:
            # Вивести конкретну пісню за її ID
            song = Song.objects.filter(pk=pk).first()
            if song:
                serializer = SongSerializer(song)
                return Response(serializer.data)
            else:
                return Response({"message": "Song not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            # Вивести всі пісні
            songs = Song.objects.all()
            serializer = SongSerializer(songs, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = SongSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            song = Song.objects.get(pk=pk)
            song.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Song.DoesNotExist:
            return Response({"message": "Song not found"}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, pk):
        try:
            song = Song.objects.get(pk=pk)
        except Song.DoesNotExist:
            return Response({"message": "Song not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = SongSerializer(song, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            # Логування або відладка
            print(serializer.errors)  # Для відладки
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PlaylistView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk=None):
        if pk:
            # Get a specific playlist by ID
            playlist = Playlist.objects.filter(pk=pk).first()
            if playlist:
                # Check if the playlist is public or if the current user is the creator
                if playlist.is_public or request.user == playlist.created_by:
                    serializer = PlaylistSerializer(playlist)
                    return Response(serializer.data)
                else:
                    return HttpResponseForbidden("You do not have permission to view this playlist.")
            return Response({"message": "Playlist not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            # Get all playlists visible to the current user
            playlists = Playlist.objects.filter(is_public=True) | Playlist.objects.filter(created_by=request.user)
            serializer = PlaylistSerializer(playlists, many=True)
            return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        # Перевірте, чи користувач аутентифікований
        if not request.user.is_authenticated:
            # Якщо користувач не аутентифікований, поверніть заборонену відповідь
            return HttpResponseForbidden("You must be logged in to create a playlist.")

        serializer = PlaylistSerializer(data=request.data)
        if serializer.is_valid():
            # Призначте поточного користувача (request.user) полю created_by
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            playlist = Playlist.objects.get(pk=pk)
            playlist.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Playlist.DoesNotExist:
            return Response({"message": "Playlist not found"}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, pk):
        try:
            playlist = Playlist.objects.get(pk=pk)
            # Check if the playlist is public or if the current user is the creator
            if playlist.is_public or request.user == playlist.created_by:
                serializer = PlaylistSerializer(playlist, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return HttpResponseForbidden("You do not have permission to edit this playlist.")
        except Playlist.DoesNotExist:
            return Response({"message": "Playlist not found"}, status=status.HTTP_404_NOT_FOUND)