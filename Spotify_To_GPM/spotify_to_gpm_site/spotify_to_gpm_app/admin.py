from django.contrib import admin
from .models import SpotifyPlaylist, SpotifyTrack, SpotifyLibrary, GPMUser

admin.site.register(SpotifyPlaylist)
admin.site.register(SpotifyTrack)
admin.site.register(SpotifyLibrary)
admin.site.register(GPMUser)
