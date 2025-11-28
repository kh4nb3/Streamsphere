import random
from django.core.management.base import BaseCommand
from core.models import Movie


class Command(BaseCommand):
    help = 'Update all movies with random view counts'

    def handle(self, *args, **options):
        """Update all movies with random view counts between 100 and 10,000"""
        movies = Movie.objects.all()
        
        for movie in movies:
            # Generate random view count between 100 and 10,000
            movie.view_count = random.randint(100, 10000)
            movie.save()
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Updated "{movie.title}" with {movie.view_count} views'
                )
            )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully updated {movies.count()} movies with random view counts'
            )
        )