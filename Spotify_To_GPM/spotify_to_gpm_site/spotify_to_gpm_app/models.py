from django.db import models
from django.contrib.auth.models import User


class GPMUser(models.Model):
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    spotify_user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="GPMUser")

    def __str__(self):
        return self.email


class GPMLibrary(models.Model):
    library_name = models.CharField(max_length=100)
    gpm_user = models.OneToOneField(GPMUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.library_name


class GPMPlaylist(models.Model):
    playlist_name = models.CharField(max_length=100)
    playlist_id = models.CharField(max_length=100)
    gpm_user = models.ForeignKey(GPMUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.playlist_name


class GPMTrack(models.Model):
    track_name = models.CharField(max_length=100)
    artist_name = models.CharField(max_length=100)
    album_name = models.CharField(max_length=100)
    store_id = models.CharField(max_length=100)
    playlist = models.ForeignKey(GPMPlaylist, on_delete=models.CASCADE, null=True, blank=True)
    library = models.ForeignKey(GPMLibrary, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.track_name


class SpotifyLibrary(models.Model):
    library_name = models.CharField(max_length=100)
    spotify_user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.library_name


class SpotifyPlaylist(models.Model):
    playlist_name = models.CharField(max_length=100)
    playlist_id = models.CharField(max_length=100)
    spotify_user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.playlist_name


class SpotifyTrack(models.Model):
    track_name = models.CharField(max_length=100)
    artist_name = models.CharField(max_length=100)
    album_name = models.CharField(max_length=100)
    track_id = models.CharField(max_length=100)
    playlist = models.ForeignKey(SpotifyPlaylist, on_delete=models.CASCADE, null=True, blank=True)
    library = models.ForeignKey(SpotifyLibrary, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.track_name
