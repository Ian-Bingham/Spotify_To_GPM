from django.contrib import admin
from .models import SpotifyPlaylist, SpotifyTrack, SpotifyLibrary, GPMUser, GPMTrack, GPMLibrary, GPMPlaylist

admin.site.register(SpotifyPlaylist)
admin.site.register(SpotifyTrack)
admin.site.register(SpotifyLibrary)
admin.site.register(GPMUser)
admin.site.register(GPMTrack)
admin.site.register(GPMLibrary)
admin.site.register(GPMPlaylist)
