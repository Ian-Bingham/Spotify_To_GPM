from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.views import logout as auth_logout
from .models import SpotifyPlaylist, SpotifyTrack, SpotifyLibrary, GPMUser, GPMTrack, GPMLibrary
from social_django.utils import load_strategy
from .forms import GPMLoginForm
import spotipy
from gmusicapi import Mobileclient

gpm = None


def index(request):
    if not request.user.is_authenticated:
        return render(request, 'spotify_to_gpm_app/spotify_login.html')
    else:
        return render(request, 'spotify_to_gpm_app/gpm_login.html')


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


def spotify_login(request):
    """Home view, displays login mechanism"""
    return redirect('social:begin', 'spotify')


def spotify_logout(request):
    if SpotifyLibrary.objects.filter(spotify_user=request.user).exists():
        spot_lib = SpotifyLibrary.objects.get(spotify_user=request.user)
        spot_lib.delete()
    auth_logout(request)
    return redirect('/capstone/')


def gpm_logout(request):
    if GPMLibrary.objects.filter(gpm_user=request.user.GPMUser).exists():
        gpm_lib = GPMLibrary.objects.get(gpm_user=request.user.GPMUser)
        gpm_lib.delete()
    global gpm
    gpm.logout()
    return redirect('/capstone/gpm_login')


def logout_both(request):
    spot_lib = get_object_or_404(SpotifyLibrary, spotify_user=request.user)
    spot_lib.delete()
    gpm_lib = get_object_or_404(GPMLibrary, gpm_user=request.user.GPMUser)
    gpm_lib.delete()
    global gpm
    gpm.logout()
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
                # new_name = ''.join(e for e in item['track']['name'] if e.isalnum())
                new_track = SpotifyTrack(track_name=item['track']['name'],
                                         artist_name=item['track']['album']['artists'][0]['name'],
                                         album_name=item['track']['album']['name'],
                                         track_id=item['track']['id'])
                new_track.save()

            spotify_track = get_object_or_404(SpotifyTrack, track_id=item['track']['id'])

            if spotify_track not in library.spotifytrack_set.all():
                library.spotifytrack_set.add(spotify_track)

        myoffset += 50
        if not library_json['next']:
            break

    return render(request, 'spotify_to_gpm_app/homepage.html')


def gpm_lib_to_db(request):
    if not GPMLibrary.objects.filter(gpm_user=request.user.GPMUser).exists():
        mylibrary = GPMLibrary(library_name=request.user.GPMUser.email, gpm_user=request.user.GPMUser)
        mylibrary.save()
    library = get_object_or_404(GPMLibrary, gpm_user=request.user.GPMUser)

    global gpm
    gpm_tracks = gpm.get_all_songs()
    for track in gpm_tracks:
        if not GPMTrack.objects.filter(store_id=track['storeId']).exists():
            # new_name = ''.join(e for e in track['title'] if e.isalnum())
            new_gpm_track = GPMTrack(track_name=track['title'],
                                     artist_name=track['artist'],
                                     album_name=track['album'],
                                     store_id=track['storeId'])
            new_gpm_track.save()

        gpm_track = get_object_or_404(GPMTrack, store_id=track['storeId'])

        if gpm_track not in library.gpmtrack_set.all():
            library.gpmtrack_set.add(gpm_track)

    return render(request, 'spotify_to_gpm_app/homepage.html')


def gpm_to_spotify(request):
    sp = get_spotify_user(request)
    gpm_lib = get_object_or_404(GPMLibrary, gpm_user=request.user.GPMUser)
    gpm_tracks = GPMTrack.objects.filter(library=gpm_lib)
    spotify_tracks_added = []
    spotify_tracks_not_added = []

    # go through all of the GPM tracks
    for track in gpm_tracks[:100]:
        song_found = False
        # search Spotify for the GPM track
        q = f"{track.track_name} artist:{track.artist_name} album:{track.album_name}"
        search_results = sp.search(q, limit=20)['tracks']['items']
        cleaned_gpm_track_name = ''.join(e for e in track.track_name if e.isalnum())
        for item in search_results:
            cleaned_searched_name = ''.join(e for e in item['name'] if e.isalnum())
            # check the search results track names against the GPM track name (excluding special chars)
            # if the names match, then we found the song we want to add
            if cleaned_gpm_track_name.lower() in cleaned_searched_name.lower() or \
                cleaned_searched_name.lower() in cleaned_gpm_track_name.lower():
                song_found = True
                # check if the GPM track already exists in the Spotify Library
                # if not, add it
                if not SpotifyTrack.objects.filter(track_id=item['id']).exists():
                    sp.current_user_saved_tracks_add([item['id']])
                    spotify_tracks_added.append(track)
                    break

            if not song_found and (search_results.index(item) == len(search_results) - 1):
                spotify_tracks_not_added.append(track)

    return render(request, 'spotify_to_gpm_app/homepage.html', {'spotify_tracks_added': spotify_tracks_added,
                                                                'spotify_tracks_not_added': spotify_tracks_not_added,})

# ###### NOT WORKING ERROR 502 ######
# def gpm_to_spotify(request):
#     sp = get_spotify_user(request)
#     gpm_lib = get_object_or_404(GPMLibrary, gpm_user=request.user.GPMUser)
#     gpm_tracks = GPMTrack.objects.filter(library=gpm_lib)
#     spotify_tracks_added = []
#     spotify_tracks_not_added = []
#
#     # go through all of the GPM tracks
#     for track in gpm_tracks[5:9]:
#         # search Spotify for the GPM track
#         q = f"{track.track_name} artist:{track.artist_name} album:{track.album_name}"
#         search_result = sp.search(q, limit=5)['tracks']['items']
#         print(search_result)
#         # only keep letters and numbers
#         # if search_result:
#         #     cleaned_gpm_name = ''.join(e for e in track.track_name if e.isalnum())
#         #     cleaned_searched_name = ''.join(e for e in search_result[0]['name'] if e.isalnum())
#         #     if cleaned_gpm_name.lower() == cleaned_searched_name.lower():
#         #         # check if the song already exists in the Spotify Library, if not add it
#         #         if not SpotifyTrack.objects.filter(track_id=search_result[0]['id']).exists():
#         #             sp.current_user_saved_tracks_add([search_result[0]['id']])
#         #             spotify_tracks_added.append(track)
#         #     else:
#         #         spotify_tracks_not_added.append(track)
#         # else:
#         #     spotify_tracks_not_added.append(track)
#
#     return render(request, 'spotify_to_gpm_app/homepage.html', {'spotify_tracks_added': spotify_tracks_added,
#                                                                 'spotify_tracks_not_added': spotify_tracks_not_added,})


def spotify_to_gpm(request):
    return HttpResponse('ok')
#     spotify_lib = get_object_or_404(SpotifyLibrary, spotify_user=request.user)
#     spotify_tracks = SpotifyTrack.objects.filter(library=spotify_lib)
#     gpm_tracks_not_added_count = 0
#     gpm_tracks_not_found = []
#
#     # for track in spotify_tracks[:3]:
#     #     q = f"{track.track_name} {track.artist_name} {track.album_name}"
#     #     global gpm
#     #     searched_list = gpm.search(q, max_results=1)
#     #     cleaned_spotify_name = ''.join(e for e in track.track_name if e.isalnum())
#     #     cleaned_searched_name = ''.join(e for e in searched_list['song_hits']['track']['title'] if e.isalnum())
#     #     if cleaned_spotify_name.lower() == cleaned_searched_name.lower():
#     #         if not GPMTrack.objects.filter(store_id=searched_list['song_hits']['track']['storeId']).exists():
#     #             gpm.add_store_track(searched_list['song_hits']['track']['storeId'])
#     #     else:
#     #         gpm_tracks_not_found.append(track)
#     #         gpm_tracks_not_added_count += 1
#
#     return render(request, 'spotify_to_gpm_app/homepage.html', {'gpm_tracks_not_found': gpm_tracks_not_found,
#                                                                 'gpm_tracks_not_added_count': gpm_tracks_not_added_count,})


# def spotify_to_gpm(request):
#     sp = get_spotify_user(request)
#     myoffset = 0
#     while True:
#         library_json = sp.current_user_saved_tracks(limit=50, offset=myoffset)
#         for item in library_json['items']:
#             track_name = item['track']['name']
#             artist_name = item['track']['album']['artists'][0]['name']
#             album_name = item['track']['album']['name']
#             track_id = item['track']['id']
#
#             search_gpm(track_name, artist_name, album_name)
#
#         myoffset += 50
#         if not library_json['next']:
#             break
#
#     return render(request, 'spotify_to_gpm_app/homepage.html')


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
