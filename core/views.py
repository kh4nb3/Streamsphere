from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.db.models import Q, Avg, Count
from .models import Movie, Genre, Mood, UserRating, Watchlist, WatchHistory
import json
import random


def home(request):
    """Home page with featured and new release movies"""
    # Get featured movies for trending section
    featured_movies = Movie.objects.filter(is_featured=True)[:8]
    
    # Get new releases
    new_releases = Movie.objects.filter(is_new_release=True)[:8]
    
    # If no featured movies, show most viewed
    if not featured_movies.exists():
        featured_movies = Movie.objects.all().order_by('-view_count')[:8]
    
    # If no new releases, show most recent
    if not new_releases.exists():
        new_releases = Movie.objects.all().order_by('-created_at')[:8]
    
    context = {
        'featured_movies': featured_movies,
        'new_releases': new_releases,
    }
    return render(request, 'home.html', context)


def movies_list(request):
    """List all movies with filtering and pagination"""
    movies = Movie.objects.all()
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        movies = movies.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Genre filtering
    genre_id = request.GET.get('genre')
    if genre_id:
        movies = movies.filter(genres__id=genre_id)
    
    # Year filtering
    year = request.GET.get('year')
    if year:
        movies = movies.filter(year=year)
    
    # Subscription filtering
    subscription = request.GET.get('subscription')
    if subscription:
        movies = movies.filter(subscription_required=subscription)
    
    # Sorting
    sort_by = request.GET.get('sort', '-created_at')
    valid_sorts = ['-created_at', 'title', '-year', '-view_count', '-user_ratings__rating']
    if sort_by in valid_sorts:
        if sort_by == '-user_ratings__rating':
            movies = movies.annotate(avg_rating=Avg('user_ratings__rating')).order_by('-avg_rating')
        else:
            movies = movies.order_by(sort_by)
    
    # Pagination
    paginator = Paginator(movies, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get all genres for filter dropdown
    genres = Genre.objects.all()
    
    # Get available years
    years = Movie.objects.values_list('year', flat=True).distinct().order_by('-year')
    
    context = {
        'page_obj': page_obj,
        'genres': genres,
        'years': years,
        'search_query': search_query,
        'selected_genre': genre_id,
        'selected_year': year,
        'selected_subscription': subscription,
        'sort_by': sort_by,
    }
    return render(request, 'movies_list.html', context)


def movie_detail(request, movie_id):
    """Movie detail page with rating and watchlist functionality"""
    movie = get_object_or_404(Movie, id=movie_id)
    
    # Get user's rating if logged in
    user_rating = None
    in_watchlist = False
    if request.user.is_authenticated:
        user_rating = UserRating.objects.filter(user=request.user, movie=movie).first()
        in_watchlist = Watchlist.objects.filter(user=request.user, movie=movie).exists()
    
    # Get related movies (same genres)
    related_movies = Movie.objects.filter(
        genres__in=movie.genres.all()
    ).exclude(id=movie.id).distinct()[:6]
    
    # Get recent reviews
    recent_reviews = UserRating.objects.filter(
        movie=movie,
        review__isnull=False
    ).exclude(review='').order_by('-created_at')[:5]
    
    context = {
        'movie': movie,
        'user_rating': user_rating,
        'in_watchlist': in_watchlist,
        'related_movies': related_movies,
        'recent_reviews': recent_reviews,
    }
    return render(request, 'movie_detail.html', context)


def login_view(request):
    """User login view"""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'login.html')


def signup_view(request):
    """User registration view"""
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        
        # Basic validation
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            return redirect('home')
    
    return render(request, 'signup.html')


def logout_view(request):
    """User logout view"""
    logout(request)
    return redirect('home')


def subscription(request):
    """Subscription management page"""
    return render(request, 'subscription.html')


@login_required
@require_POST
@csrf_exempt
def rate_movie(request):
    """AJAX endpoint for rating movies"""
    try:
        data = json.loads(request.body)
        movie_id = data.get('movie_id')
        rating = int(data.get('rating'))
        review = data.get('review', '')
        
        movie = get_object_or_404(Movie, id=movie_id)
        
        # Create or update rating
        user_rating, created = UserRating.objects.get_or_create(
            user=request.user,
            movie=movie,
            defaults={'rating': rating, 'review': review}
        )
        
        if not created:
            user_rating.rating = rating
            user_rating.review = review
            user_rating.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Rating saved successfully',
            'average_rating': movie.average_rating
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        })


@login_required
@require_POST
@csrf_exempt
def toggle_watchlist(request):
    """AJAX endpoint for adding/removing movies from watchlist"""
    try:
        data = json.loads(request.body)
        movie_id = data.get('movie_id')
        
        movie = get_object_or_404(Movie, id=movie_id)
        
        watchlist_item, created = Watchlist.objects.get_or_create(
            user=request.user,
            movie=movie
        )
        
        if not created:
            # Remove from watchlist
            watchlist_item.delete()
            in_watchlist = False
            message = 'Removed from watchlist'
        else:
            # Added to watchlist
            in_watchlist = True
            message = 'Added to watchlist'
        
        return JsonResponse({
            'success': True,
            'in_watchlist': in_watchlist,
            'message': message
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        })


@login_required
def watchlist_view(request):
    """User's watchlist page"""
    watchlist_items = Watchlist.objects.filter(user=request.user).order_by('-added_at')
    
    # Pagination
    paginator = Paginator(watchlist_items, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'watchlist.html', {'page_obj': page_obj})


@login_required
def watch_history(request):
    """User's watch history page"""
    history = WatchHistory.objects.filter(user=request.user).order_by('-watched_at')
    
    # Pagination
    paginator = Paginator(history, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'watch_history.html', {'page_obj': page_obj})


@login_required
@require_POST
@csrf_exempt
def record_watch(request):
    """Record when user watches a movie"""
    try:
        data = json.loads(request.body)
        movie_id = data.get('movie_id')
        duration = data.get('duration_minutes', 0)
        completed = data.get('completed', False)
        
        movie = get_object_or_404(Movie, id=movie_id)
        
        # Create watch record
        WatchHistory.objects.create(
            user=request.user,
            movie=movie,
            watch_duration_minutes=duration,
            completed=completed
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Watch recorded successfully'
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        })


def genres_list(request):
    """List all genres"""
    genres = Genre.objects.all()
    return render(request, 'genres.html', {'genres': genres})


def genre_movies(request, genre_id):
    """Movies by genre"""
    genre = get_object_or_404(Genre, id=genre_id)
    movies = Movie.objects.filter(genres=genre)
    
    # Sort options
    sort_by = request.GET.get('sort', '-created_at')
    if sort_by in ['-created_at', 'title', '-year', '-average_rating']:
        movies = movies.order_by(sort_by)
    
    # Pagination
    paginator = Paginator(movies, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get all genres for sidebar
    all_genres = Genre.objects.annotate(movies_count=Count('movies')).order_by('name')
    
    return render(request, 'genre_movies.html', {
        'genre': genre,
        'page_obj': page_obj,
        'all_genres': all_genres,
    })


def mood_recommendations(request):
    """Mood-based movie recommendations"""
    moods = Mood.objects.all()
    return render(request, 'mood_recommendations.html', {'moods': moods})


def movies_by_mood(request, mood_id):
    """Get all movies by mood"""
    mood = get_object_or_404(Mood, id=mood_id)
    movies = Movie.objects.filter(moods=mood).order_by('title')  # Show all movies, ordered by title
    
    context = {
        'mood': mood,
        'movies': movies,
    }
    return render(request, 'movies_by_mood.html', context)


@csrf_exempt
def get_random_movie_by_mood(request):
    """AJAX endpoint to get a random movie by mood"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            mood_id = data.get('mood_id')
            
            mood = get_object_or_404(Mood, id=mood_id)
            movies = list(Movie.objects.filter(moods=mood))
            
            if movies:
                movie = random.choice(movies)
                return JsonResponse({
                    'success': True,
                    'mood': {
                        'id': mood.id,
                        'name': mood.name,
                        'icon': mood.icon,
                        'color': mood.color,
                    },
                    'movie': {
                        'id': movie.id,
                        'title': movie.title,
                        'year': movie.year,
                        'description': movie.description,
                        'poster': movie.poster,
                        'average_rating': movie.average_rating,
                        'genres': [genre.name for genre in movie.genres.all()],
                    }
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': f'No movies found for {mood.name} mood'
                })
        
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})


def get_random_movie(request):
    """API endpoint to get a random movie"""
    try:
        movies = list(Movie.objects.all())
        if movies:
            random_movie = random.choice(movies)
            return JsonResponse({
                'success': True,
                'movie_id': random_movie.id
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'No movies available'
            })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'Error getting random movie'
        })



