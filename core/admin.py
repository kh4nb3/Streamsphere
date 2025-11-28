from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Movie, Genre, Mood, UserRating, Watchlist, WatchHistory


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'subscription_type', 'has_active_subscription', 'date_joined']
    list_filter = ['subscription_type', 'is_active', 'date_joined']
    search_fields = ['username', 'email']
    fieldsets = UserAdmin.fieldsets + (
        ('Subscription Info', {
            'fields': ('subscription_type', 'subscription_start_date', 'subscription_end_date')
        }),
    )


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']
    prepopulated_fields = {'description': ('name',)}


@admin.register(Mood)
class MoodAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'color']
    search_fields = ['name']


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'year', 'subscription_required', 'is_featured', 'is_new_release', 'view_count', 'average_rating']
    list_filter = ['subscription_required', 'is_featured', 'is_new_release', 'year', 'genres', 'moods', 'rating']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['genres', 'moods']
    readonly_fields = ['average_rating']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'description', 'year', 'duration_minutes', 'rating', 'genres', 'moods')
        }),
        ('Media', {
            'fields': ('poster_url', 'poster_image')
        }),
        ('Display Options', {
            'fields': ('is_featured', 'is_new_release', 'subscription_required')
        }),
    )


@admin.register(UserRating)
class UserRatingAdmin(admin.ModelAdmin):
    list_display = ['user', 'movie', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['user__username', 'movie__title']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Watchlist)
class WatchlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'movie', 'added_at']
    list_filter = ['added_at']
    search_fields = ['user__username', 'movie__title']
    readonly_fields = ['added_at']


@admin.register(WatchHistory)
class WatchHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'movie', 'watched_at', 'watch_duration_minutes', 'completed']
    list_filter = ['completed', 'watched_at']
    search_fields = ['user__username', 'movie__title']
    readonly_fields = ['watched_at']
