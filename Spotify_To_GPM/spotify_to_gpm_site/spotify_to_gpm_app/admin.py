from django.contrib import admin
from .models import SpotifyPlaylist, SpotifyTrack, SpotifyLibrary, GPMUser, GPMTrack, GPMLibrary, GPMPlaylist


class SpotifyTrackAdmin(admin.ModelAdmin):
    list_filter = ["library"]

    class Meta:
        model = SpotifyTrack


class GPMTrackAdmin(admin.ModelAdmin):
    list_filter = ["library"]

    class Meta:
        model = GPMTrack


admin.site.register(SpotifyPlaylist)
admin.site.register(SpotifyTrack, SpotifyTrackAdmin)
admin.site.register(SpotifyLibrary)
admin.site.register(GPMUser)
admin.site.register(GPMTrack, GPMTrackAdmin)
admin.site.register(GPMLibrary)
admin.site.register(GPMPlaylist)
