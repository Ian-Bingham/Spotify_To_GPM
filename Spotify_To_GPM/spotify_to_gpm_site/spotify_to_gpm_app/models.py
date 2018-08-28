from django.db import models


# Create your models here.
class SpotifyPlaylist(models.Model):
    playlist_name = models.CharField(max_length=100)
    playlist_id = models.CharField(max_length=100)
    user_id = models.CharField(max_length=100)

    def __str__(self):
        return self.playlist_name


class SpotifyLibrary(models.Model):
    library_name = models.CharField(max_length=100)
    user_id = models.CharField(max_length=100)

    def __str__(self):
        return self.library_name


class SpotifyTrack(models.Model):
    track_name = models.CharField(max_length=100)
    artist_name = models.CharField(max_length=100)
    album_name = models.CharField(max_length=100)
    track_id = models.CharField(max_length=100)
    playlist = models.ForeignKey(SpotifyPlaylist, on_delete=models.CASCADE, null=True, blank=True)
    library = models.ForeignKey(SpotifyLibrary, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.track_name
