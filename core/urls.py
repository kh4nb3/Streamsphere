from django.urls import path
from . import views

urlpatterns = [
    # Main pages
    path('', views.home, name='home'),
    path('movies/', views.movies_list, name='movies_list'),
    path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    
    # Authentication
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    
    # User features
    path('watchlist/', views.watchlist_view, name='watchlist'),
    path('history/', views.watch_history, name='watch_history'),
    path('subscription/', views.subscription, name='subscription'),
    
    # AJAX endpoints
    path('api/rate/', views.rate_movie, name='rate_movie'),
    path('api/watchlist/toggle/', views.toggle_watchlist, name='toggle_watchlist'),
    path('api/watch/record/', views.record_watch, name='record_watch'),
    
    # Genres
    path('genres/', views.genres_list, name='genres_list'),
    path('genre/<int:genre_id>/', views.genre_movies, name='genre_movies'),
    
    # Mood recommendations
    path('recommendations/', views.mood_recommendations, name='mood_recommendations'),
    path('mood/<int:mood_id>/', views.movies_by_mood, name='movies_by_mood'),
    path('api/random-movie-by-mood/', views.get_random_movie_by_mood, name='random_movie_by_mood'),
    path('api/random-movie/', views.get_random_movie, name='random_movie'),
]
