from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class User(AbstractUser):
    """Custom user model with additional fields for streaming platform"""
    email = models.EmailField(unique=True)
    subscription_type = models.CharField(
        max_length=20,
        choices=[
            ('free', 'Free'),
            ('basic', 'Basic'),
            ('premium', 'Premium'),
        ],
        default='free'
    )
    subscription_start_date = models.DateTimeField(null=True, blank=True)
    subscription_end_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

    @property
    def has_active_subscription(self):
        if self.subscription_type == 'free':
            return True
        if self.subscription_end_date:
            return timezone.now() <= self.subscription_end_date
        return False


class Genre(models.Model):
    """Movie genres"""
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Mood(models.Model):
    """Movie moods for recommendation system"""
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    icon = models.CharField(
        max_length=50,
        help_text="FontAwesome icon class (e.g., 'fas fa-heart')"
    )
    color = models.CharField(
        max_length=7,
        default='#3b82f6',
        help_text="Hex color code for the mood"
    )
    
    def __str__(self):
        return self.name


class Movie(models.Model):
    """Main movie model storing all movie information"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    poster_url = models.URLField(
        help_text="URL to the movie poster image"
    )
    poster_image = models.ImageField(
        upload_to='movie_posters/',
        null=True,
        blank=True,
        help_text="Upload poster image file (optional if poster_url is provided)"
    )
    
    # Movie details
    year = models.PositiveIntegerField()
    duration_minutes = models.PositiveIntegerField(
        help_text="Duration in minutes"
    )
    rating = models.CharField(
        max_length=10,
        choices=[
            ('G', 'General Audiences'),
            ('PG', 'Parental Guidance'),
            ('PG-13', 'Parents Strongly Cautioned'),
            ('R', 'Restricted'),
            ('NC-17', 'Adults Only'),
        ],
        default='PG-13'
    )
    
    # Relationships
    genres = models.ManyToManyField(Genre, related_name='movies')
    moods = models.ManyToManyField(Mood, related_name='movies', blank=True)
    
    # Metadata
    is_featured = models.BooleanField(
        default=False,
        help_text="Show in featured/trending section"
    )
    is_new_release = models.BooleanField(
        default=False,
        help_text="Show in new releases section"
    )
    
    # Subscription requirements
    subscription_required = models.CharField(
        max_length=20,
        choices=[
            ('free', 'Free'),
            ('basic', 'Basic'),
            ('premium', 'Premium'),
        ],
        default='free',
        help_text="Minimum subscription level required to watch"
    )
    
    # View tracking with random initial values
    view_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.title} ({self.year})"

    @property
    def poster(self):
        """Return poster image URL, preferring uploaded file over URL"""
        if self.poster_image:
            return self.poster_image.url
        return self.poster_url

    @property
    def backdrop(self):
        """Return backdrop image URL"""
        return None

    @property
    def average_rating(self):
        """Calculate average user rating"""
        ratings = self.user_ratings.all()
        if ratings.exists():
            return round(ratings.aggregate(models.Avg('rating'))['rating__avg'], 1)
        return 0

    @property
    def formatted_duration(self):
        """Format duration as hours and minutes"""
        hours = self.duration_minutes // 60
        minutes = self.duration_minutes % 60
        if hours > 0:
            return f"{hours}h {minutes}m"
        return f"{minutes}m"

    @property
    def trailer_url(self):
        """Return fixed trailer URL for all movies"""
        return "https://www.youtube.com/watch?v=ScMzIvxBSi4"

    @property
    def video_url(self):
        """Return fixed video URL for all movies"""
        return "https://www.youtube.com/watch?v=ScMzIvxBSi4"

    class Meta:
        ordering = ['title']
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['year']),
            models.Index(fields=['is_featured']),
            models.Index(fields=['is_new_release']),
        ]


class UserRating(models.Model):
    """User ratings for movies"""
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='ratings')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='user_ratings')
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating from 1 to 5 stars"
    )
    review = models.TextField(blank=True)
    year = models.PositiveIntegerField(default=2024)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.movie.title}: {self.rating}/5"

    class Meta:
        unique_together = ['user', 'movie']
        ordering = ['-year']


class Watchlist(models.Model):
    """User's watchlist/favorites"""
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='watchlist')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='in_watchlists')
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"

    class Meta:
        unique_together = ['user', 'movie']
        ordering = ['-added_at']


class WatchHistory(models.Model):
    """Track user's viewing history"""
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='watch_history')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='watch_records')
    watched_at = models.DateTimeField(auto_now_add=True)
    watch_duration_minutes = models.PositiveIntegerField(
        default=0,
        help_text="How long the user watched in minutes"
    )
    completed = models.BooleanField(
        default=False,
        help_text="Whether the user finished watching the movie"
    )

    def __str__(self):
        return f"{self.user.username} watched {self.movie.title}"

    class Meta:
        ordering = ['-watched_at']
        indexes = [
            models.Index(fields=['user', '-watched_at']),
        ]
