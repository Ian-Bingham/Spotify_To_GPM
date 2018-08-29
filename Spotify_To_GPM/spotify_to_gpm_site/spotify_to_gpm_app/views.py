from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.views import logout as auth_logout
from .models import SpotifyPlaylist, SpotifyTrack, SpotifyLibrary, GPMUser
from django.contrib.auth.models import User
from social_django.utils import load_strategy
from .forms import GPMLoginForm
import spotipy
from gmusicapi import Mobileclient
from django.http import HttpResponse


# def index(request):
#     context = {}
#     if request.user.is_authenticated:
#         social = request.user.social_auth.get(provider='spotify')
#         token = social.extra_data['access_token']
#         if token:
#             sp = spotipy.Spotify(auth=token)
#             curr_user = sp.current_user()
#             playlists_json = sp.user_playlists(curr_user['id'])
#             for playlist in playlists_json['items']:
#                 playlist = Playlist(playlist_name=playlist['name'],
#                                     spotify_playlist_id=playlist['id'])
#                 if not Playlist.objects.filter(spotify_playlist_id=playlist.spotify_playlist_id).exists():
#                     playlist.save()
#                 else:
#                     continue
#                 tracks = sp.user_playlist_tracks(curr_user['id'], playlist.spotify_playlist_id)
#                 for track in tracks['items']:
#                     new_track = Track(track_name=track['track']['name'],
#                                       artist_name=track['track']['album']['artists'][0]['name'],
#                                       album_name=track['track']['album']['name'],
#                                       spotify_track_id=track['track']['id'],
#                                       playlist=playlist)
#                     new_track.save()
#         else:
#             context = {'invalid': "Can't get token"}
#     return render(request, 'spotify_to_gpm_app/index.html', context)

gpm = None


def gpm_login(request):
    if request.method == 'POST':
        form = GPMLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            global gpm
            gpm = Mobileclient()
            gpm_loggedIn = gpm.login(email, password, Mobileclient.FROM_MAC_ADDRESS)
            if gpm_loggedIn:
                if not GPMUser.objects.filter(spotify_user=request.user).exists():
                    new_gpm_user = GPMUser(spotify_user=request.user, email=email, password=password)
                    new_gpm_user.save()
                return render(request, 'spotify_to_gpm_app/homepage.html')
            else:
                form = GPMLoginForm()
                return render(request, 'spotify_to_gpm_app/gpm_login.html', {'failed': 'GPM Login Failed. Try again.', 'form': form})
        # if the form is invalid, we just send it back to the template
    else:
        form = GPMLoginForm()
    return render(request, 'spotify_to_gpm_app/gpm_login.html', {'form': form})


def gpm_logout():
    global gpm
    gpm.logout()


def spotify_login(request):
    """Home view, displays login mechanism"""
    return redirect('social:begin', 'spotify')


def spotify_logout(request):
    auth_logout(request)
    return redirect('/capstone/')


def logout_both(request):
    gpm_logout()
    auth_logout(request)
    return redirect('/capstone/')


# get the Spotify user after OAuth has been completed
def get_spotify_user(request):
    social = request.user.social_auth.get(provider='spotify')
    social.refresh_token(load_strategy())
    token = social.extra_data['access_token']
    sp = spotipy.Spotify(auth=token)
    return sp


def spotify_lib_to_db(request):
    sp = get_spotify_user(request)
    if not SpotifyLibrary.objects.filter(spotify_user=request.user).exists():
        mylibrary = SpotifyLibrary(library_name=request.user.username, spotify_user=request.user)
        mylibrary.save()
    library = get_object_or_404(SpotifyLibrary, spotify_user=request.user)

    myoffset = 0
    while True:
        library_json = sp.current_user_saved_tracks(limit=50, offset=myoffset)
        for item in library_json['items']:
            if not SpotifyTrack.objects.filter(track_id=item['track']['id']).exists():
                new_track = SpotifyTrack(track_name=item['track']['name'],
                                         artist_name=item['track']['album']['artists'][0]['name'],
                                         album_name=item['track']['album']['name'],
                                         track_id=item['track']['id'])
                new_track.save()

            track = get_object_or_404(SpotifyTrack, track_id=item['track']['id'])

            if track not in library.spotifytrack_set.all():
                library.spotifytrack_set.add(track)

        myoffset += 50
        if not library_json['next']:
            break


def spotify_lib_to_gpm(request):
    spotify_lib_to_db(request)
    


def index(request):
    if not request.user.is_authenticated:
        return render(request, 'spotify_to_gpm_app/spotify_login.html')
    else:
        return render(request, 'spotify_to_gpm_app/gpm_login.html')


def homepage(request):
    pass
    # sp, curr_spotify_user = get_spotify_user(request)
    # if sp and curr_spotify_user:
    #     # import_spotify_pl(sp, curr_spotify_user)
    #     # import_spotify_pl_tracks(sp, curr_spotify_user)
    #     # context['spotify_playlists'] = Playlist.objects.filter(user_id=curr_spotify_user['id'])
    #     # context['spotify_library'] = SpotifyLibrary.objects.filter(
    #     #     user_id=curr_spotify_user['id'])
    #     import_spotify_library(sp, curr_spotify_user)
    # else:
    #     context['invalid'] = 'Could not get OAuth token'


# # store the current user's Spotify playlist info into the database
# def import_spotify_pl(sp, curr_user):
#     playlists_json = sp.user_playlists(curr_user['id'])
#     for playlist in playlists_json['items']:
#         playlist = SpotifyPlaylist(playlist_name=playlist['name'],
#                             playlist_id=playlist['id'],
#                             user_id=curr_user['id'])
#         if not SpotifyPlaylist.objects.filter(playlist_id=playlist.playlist_id).exists():
#             playlist.save()
#
#
# # store info about each playlist' tracks into the database
# def import_spotify_pl_tracks(sp, curr_user):
#     playlists = SpotifyPlaylist.objects.filter(user_id=curr_user['id'])
#     for playlist in playlists:
#         tracks = sp.user_playlist_tracks(curr_user['id'], playlist.playlist_id)
#         for item in tracks['items']:
#             new_track = SpotifyTrack(track_name=item['track']['name'],
#                               artist_name=item['track']['album']['artists'][0]['name'],
#                               album_name=item['track']['album']['name'],
#                               track_id=item['track']['id'],
#                               playlist=playlist)
#             if not SpotifyTrack.objects.filter(track_id=new_track.track_id).exists():
#                 new_track.save()
#
#
# def disp_pl_tracks(request, pl_id):
#     context = {}
#     playlist = get_object_or_404(SpotifyPlaylist, playlist_id=pl_id)
#     context['tracks'] = playlist.spotifytrack_set.all()
#     return render(request, 'spotify_to_gpm_app/disp_pl_tracks.html', context)
