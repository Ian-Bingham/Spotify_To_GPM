from django.urls import path
from . import views

app_name = 'spotify_to_gpm_app'  # for namespacing
urlpatterns = [
    path('', views.index, name='index'),
    path('auth/login/spotify/', views.spotify_login, name='spotify_login'),
    path('spotify_logout/', views.spotify_logout, name='spotify_logout'),
    path('gpm_login/', views.gpm_login, name='gpm_login'),
    path('gpm_logout/', views.gpm_logout, name='gpm_logout'),
    path('import_songs_to_db/', views.import_songs_to_db, name='import_songs_to_db'),
    path('gpm_to_spotify/', views.gpm_to_spotify, name='gpm_to_spotify'),
    path('spotify_to_gpm/', views.spotify_to_gpm, name='spotify_to_gpm'),
]
