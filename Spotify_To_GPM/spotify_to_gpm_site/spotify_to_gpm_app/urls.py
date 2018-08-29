from django.urls import path
from . import views

app_name = 'spotify_to_gpm_app'  # for namespacing
urlpatterns = [
    path('', views.index, name='index'),
    path('gpm_login/', views.gpm_login, name='gpm_login'),
    path('gpm_logout/', views.gpm_logout, name='gpm_logout'),
    path('auth/login/spotify/', views.spotify_login, name='spotify_login'),
    path('spotify_logout/', views.spotify_logout, name='spotify_logout'),
    path('logout_both/', views.logout_both, name='logout_both'),
    path('spotify_lib_to_db/', views.spotify_lib_to_db, name='spotify_lib_to_db'),
    path('gpm_lib_to_db/', views.gpm_lib_to_db, name='gpm_lib_to_db'),
    path('spotify_to_gpm/', views.spotify_to_gpm, name='spotify_to_gpm'),
    # path('disp_pl_tracks/<str:pl_id>', views.disp_pl_tracks, name='disp_pl_tracks'),
]