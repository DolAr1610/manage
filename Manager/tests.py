from django.test import TestCase
from django.contrib.auth.models import User
from .models import Song, Playlist
from rest_framework.test import APIClient
from rest_framework import status


class SongTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.song1 = Song.objects.create(title="Song1", artist="Artist1", release_year=2020)
        self.song2 = Song.objects.create(title="Song2", artist="Artist2", release_year=2021)
        self.song_data = {'title': 'Updated Song', 'artist': 'Updated Artist', 'release_year': 2023}

    def test_song_creation(self):
        song1 = Song.objects.get(title="Song1")
        self.assertEqual(song1.artist, "Artist1")

    def test_get_single_song(self):
        response = self.client.get(f'/song/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_songs(self):
        response = self.client.get('/song/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 2)

    def test_delete_song(self):
        response = self.client.delete(f'/song/{self.song1.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_patch_song(self):
        response = self.client.patch(f'/song/{self.song1.id}/', self.song_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_song = Song.objects.get(id=self.song1.id)
        self.assertEqual(updated_song.title, 'Updated Song')

    def test_post_song_with_invalid_data(self):
        invalid_data = {'title': '', 'artist': '', 'release_year': ''}
        response = self.client.post('/song/', invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.force_authenticate(user=self.user)
        self.song_data = {'title': 'New Song', 'artist': 'New Artist', 'release_year': 2022}
        self.playlist_data = {'title': 'New Playlist', 'created_by': self.user.id, 'is_public': False}

    def test_api_can_create_a_song(self):
        response = self.client.post('/song/', self.song_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_api_can_create_a_playlist(self):
        response = self.client.post('/playlists/', self.playlist_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_single_playlist(self):
        response = self.client.get(f'/playlists/{self.playlist.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Playlist')

    def test_get_all_playlists(self):
        response = self.client.get('/playlists/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)

    def test_delete_playlist(self):
        response = self.client.delete(f'/playlists/{self.playlist.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_patch_playlist(self):
        response = self.client.patch(f'/playlists/{self.playlist.id}/', self.playlist_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Playlist')
