from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from core.models import Movie, Genre, Mood, UserRating
import random


class Command(BaseCommand):
    help = 'Load sample movie data into the database'

    def handle(self, *args, **options):
        self.stdout.write('Loading sample data...')
        
        User = get_user_model()
        
        # Create genres
        genres_data = [
            {'name': 'Action', 'description': 'Action-packed adventures and thrills'},
            {'name': 'Sci-Fi', 'description': 'Science fiction and futuristic stories'},
            {'name': 'Drama', 'description': 'Character-driven dramatic stories'},
            {'name': 'Thriller', 'description': 'Suspenseful and tension-filled movies'},
            {'name': 'Crime', 'description': 'Crime and criminal underworld stories'},
            {'name': 'Adventure', 'description': 'Epic adventures and journeys'},
            {'name': 'Fantasy', 'description': 'Magical and fantastical worlds'},
        ]
        
        # Create moods
        moods_data = [
            {'name': 'Happy', 'description': 'Feel-good movies to brighten your day', 'icon': 'fas fa-smile', 'color': '#fbbf24'},
            {'name': 'Sad', 'description': 'Emotional dramas for when you need a good cry', 'icon': 'fas fa-sad-tear', 'color': '#60a5fa'},
            {'name': 'Excited', 'description': 'High-energy action and adventure films', 'icon': 'fas fa-bolt', 'color': '#f59e0b'},
            {'name': 'Romantic', 'description': 'Love stories to warm your heart', 'icon': 'fas fa-heart', 'color': '#f43f5e'},
            {'name': 'Scared', 'description': 'Thrilling horrors and suspenseful movies', 'icon': 'fas fa-ghost', 'color': '#8b5cf6'},
            {'name': 'Thoughtful', 'description': 'Mind-bending and philosophical films', 'icon': 'fas fa-brain', 'color': '#06b6d4'},
            {'name': 'Nostalgic', 'description': 'Classic films that take you back in time', 'icon': 'fas fa-clock', 'color': '#d97706'},
            {'name': 'Adventurous', 'description': 'Epic journeys and exploration movies', 'icon': 'fas fa-compass', 'color': '#10b981'},
        ]
        
        created_genres = {}
        for genre_data in genres_data:
            genre, created = Genre.objects.get_or_create(
                name=genre_data['name'],
                defaults={'description': genre_data['description']}
            )
            created_genres[genre.name] = genre
            if created:
                self.stdout.write(f'Created genre: {genre.name}')
        
        # Create moods
        created_moods = {}
        for mood_data in moods_data:
            mood, created = Mood.objects.get_or_create(
                name=mood_data['name'],
                defaults={
                    'description': mood_data['description'],
                    'icon': mood_data['icon'],
                    'color': mood_data['color']
                }
            )
            created_moods[mood.name] = mood
            if created:
                self.stdout.write(f'Created mood: {mood.name}')
        
        # Create movies with the original mock data
        movies_data = [
            {
                'title': 'Inception',
                'poster_url': 'https://images.unsplash.com/photo-1626814026160-2237a95fc5a0?q=80&w=2070&auto=format&fit=crop',
                'year': 2010,
                'description': 'A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.',
                'duration_minutes': 148,
                'genres': ['Sci-Fi', 'Action', 'Thriller'],
                'moods': ['Thoughtful', 'Excited'],
                'is_featured': True,
                'subscription_required': 'basic'
            },
            {
                'title': 'Interstellar',
                'poster_url': 'https://images.unsplash.com/photo-1419242902214-272b3f66ee7a?q=80&w=2013&auto=format&fit=crop',
                'year': 2014,
                'description': 'A team of explorers travel through a wormhole in space in an attempt to ensure humanity\'s survival.',
                'duration_minutes': 169,
                'genres': ['Sci-Fi', 'Drama', 'Adventure'],
                'moods': ['Thoughtful', 'Adventurous', 'Sad'],
                'is_featured': True,
                'subscription_required': 'premium'
            },
            {
                'title': 'The Dark Knight',
                'poster_url': 'https://images.unsplash.com/photo-1559583985-b81d2100a93f?q=80&w=2070&auto=format&fit=crop',
                'year': 2008,
                'description': 'When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests.',
                'duration_minutes': 152,
                'genres': ['Action', 'Crime', 'Drama'],
                'moods': ['Excited', 'Scared', 'Thoughtful'],
                'is_featured': True,
                'subscription_required': 'basic'
            },
            {
                'title': 'Avatar',
                'poster_url': 'https://images.unsplash.com/photo-1518709268805-4e9042af9f23?q=80&w=1968&auto=format&fit=crop',
                'year': 2009,
                'description': 'A paraplegic Marine dispatched to the moon Pandora on a unique mission becomes torn between following orders and protecting an alien civilization.',
                'duration_minutes': 162,
                'genres': ['Action', 'Adventure', 'Fantasy'],
                'moods': ['Adventurous', 'Excited', 'Happy'],
                'is_new_release': True,
                'subscription_required': 'premium'
            },
            {
                'title': 'Dune',
                'poster_url': 'https://images.unsplash.com/photo-1541963463532-d68292c34b19?q=80&w=1976&auto=format&fit=crop',
                'year': 2021,
                'description': 'Feature adaptation of Frank Herbert\'s science fiction novel about the son of a noble family entrusted with the protection of the most valuable asset.',
                'duration_minutes': 155,
                'genres': ['Sci-Fi', 'Adventure', 'Drama'],
                'moods': ['Thoughtful', 'Adventurous', 'Excited'],
                'is_new_release': True,
                'subscription_required': 'premium'
            },
            {
                'title': 'Blade Runner 2049',
                'poster_url': 'https://images.unsplash.com/photo-1534447677768-be436bb09401?q=80&w=2094&auto=format&fit=crop',
                'year': 2017,
                'description': 'A young blade runner\'s discovery of a long-buried secret leads him to track down former blade runner Rick Deckard.',
                'duration_minutes': 164,
                'genres': ['Sci-Fi', 'Drama', 'Thriller'],
                'moods': ['Thoughtful', 'Sad', 'Nostalgic'],
                'is_new_release': True,
                'subscription_required': 'basic'
            },
            {
                'title': 'The Matrix',
                'poster_url': 'https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?q=80&w=2070&auto=format&fit=crop',
                'year': 1999,
                'description': 'A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.',
                'duration_minutes': 136,
                'genres': ['Action', 'Sci-Fi'],
                'moods': ['Thoughtful', 'Excited', 'Nostalgic'],
                'is_featured': True,
                'subscription_required': 'free'
            },
            {
                'title': 'Pulp Fiction',
                'poster_url': 'https://images.unsplash.com/photo-1594909122845-11baa439b7bf?q=80&w=2070&auto=format&fit=crop',
                'year': 1994,
                'description': 'The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption.',
                'duration_minutes': 154,
                'genres': ['Crime', 'Drama'],
                'moods': ['Nostalgic', 'Thoughtful', 'Excited'],
                'is_featured': True,
                'subscription_required': 'basic'
            },
            {
                'title': 'Fight Club',
                'poster_url': 'https://images.unsplash.com/photo-1599058945522-28d584b6f0ff?q=80&w=2069&auto=format&fit=crop',
                'year': 1999,
                'description': 'An insomniac office worker and a devil-may-care soapmaker form an underground fight club that evolves into much more.',
                'duration_minutes': 139,
                'genres': ['Drama', 'Thriller'],
                'moods': ['Thoughtful', 'Excited', 'Sad'],
                'is_new_release': True,
                'subscription_required': 'basic'
            },
            {
                'title': 'Mad Max: Fury Road',
                'poster_url': 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?q=80&w=2070&auto=format&fit=crop',
                'year': 2015,
                'description': 'In a post-apocalyptic wasteland, a woman rebels against a tyrannical ruler in search for her homeland with the aid of a group of female prisoners.',
                'duration_minutes': 120,
                'genres': ['Action', 'Adventure', 'Thriller'],
                'moods': ['Excited', 'Adventurous'],
                'is_featured': True,
                'subscription_required': 'basic'
            },
            {
                'title': 'The Shawshank Redemption',
                'poster_url': 'https://images.unsplash.com/photo-1549989476-69a92fa57c36?q=80&w=2070&auto=format&fit=crop',
                'year': 1994,
                'description': 'Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.',
                'duration_minutes': 142,
                'genres': ['Drama'],
                'moods': ['Sad', 'Happy', 'Thoughtful'],
                'is_featured': True,
                'subscription_required': 'free'
            },
            {
                'title': 'The Godfather',
                'poster_url': 'https://images.unsplash.com/photo-1478720568477-b0a8c5e2ec9e?q=80&w=2070&auto=format&fit=crop',
                'year': 1972,
                'description': 'The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.',
                'duration_minutes': 175,
                'genres': ['Crime', 'Drama'],
                'moods': ['Thoughtful', 'Nostalgic'],
                'is_featured': True,
                'subscription_required': 'free'
            },
            {
                'title': 'Forrest Gump',
                'poster_url': 'https://images.unsplash.com/photo-1551698618-1dfe5d97d256?q=80&w=2070&auto=format&fit=crop',
                'year': 1994,
                'description': 'The presidencies of Kennedy and Johnson through the eyes of an Alabama man with an IQ of 75.',
                'duration_minutes': 142,
                'genres': ['Drama'],
                'moods': ['Happy', 'Sad', 'Nostalgic'],
                'is_featured': True,
                'subscription_required': 'free'
            },
            {
                'title': 'Spider-Man: Into the Spider-Verse',
                'poster_url': 'https://images.unsplash.com/photo-1549989476-69a92fa57c36?q=80&w=2070&auto=format&fit=crop',
                'year': 2018,
                'description': 'Teen Miles Morales becomes Spider-Man and must save the multiverse from collapse.',
                'duration_minutes': 117,
                'genres': ['Action', 'Adventure', 'Fantasy'],
                'moods': ['Happy', 'Excited', 'Adventurous'],
                'is_new_release': True,
                'subscription_required': 'basic'
            },
            {
                'title': 'Parasite',
                'poster_url': 'https://images.unsplash.com/photo-1440404653325-ab127d49abc1?q=80&w=2070&auto=format&fit=crop',
                'year': 2019,
                'description': 'A poor family schemes to become employed by a wealthy family by infiltrating their household.',
                'duration_minutes': 132,
                'genres': ['Drama', 'Thriller'],
                'moods': ['Thoughtful', 'Scared', 'Excited'],
                'is_new_release': True,
                'subscription_required': 'premium'
            },
            {
                'title': 'The Lion King',
                'poster_url': 'https://images.unsplash.com/photo-1574870111867-089730e5a72b?q=80&w=2070&auto=format&fit=crop',
                'year': 1994,
                'description': 'A young lion prince flees his kingdom only to learn the true meaning of responsibility and bravery.',
                'duration_minutes': 88,
                'genres': ['Adventure', 'Drama', 'Fantasy'],
                'moods': ['Happy', 'Sad', 'Adventurous', 'Nostalgic'],
                'is_featured': True,
                'subscription_required': 'free'
            },
            {
                'title': 'John Wick',
                'poster_url': 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?q=80&w=2070&auto=format&fit=crop',
                'year': 2014,
                'description': 'An ex-hitman comes out of retirement to track down the gangsters that took everything from him.',
                'duration_minutes': 101,
                'genres': ['Action', 'Crime', 'Thriller'],
                'moods': ['Excited', 'Sad'],
                'is_featured': True,
                'subscription_required': 'basic'
            },
            {
                'title': 'Spirited Away',
                'poster_url': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?q=80&w=2070&auto=format&fit=crop',
                'year': 2001,
                'description': 'During her family\'s move to the suburbs, a girl wanders into a world ruled by gods and spirits.',
                'duration_minutes': 125,
                'genres': ['Adventure', 'Fantasy'],
                'moods': ['Happy', 'Adventurous', 'Thoughtful'],
                'is_featured': True,
                'subscription_required': 'basic'
            },
            {
                'title': 'Avengers: Endgame',
                'poster_url': 'https://images.unsplash.com/photo-1635805737707-575885ab0820?q=80&w=2070&auto=format&fit=crop',
                'year': 2019,
                'description': 'The Avengers assemble once more to reverse Thanos\' actions and restore balance to the universe.',
                'duration_minutes': 181,
                'genres': ['Action', 'Adventure', 'Sci-Fi'],
                'moods': ['Excited', 'Sad', 'Happy', 'Adventurous'],
                'is_new_release': True,
                'subscription_required': 'premium'
            },
            {
                'title': 'La La Land',
                'poster_url': 'https://images.unsplash.com/photo-1514306191717-452ec28c7814?q=80&w=2069&auto=format&fit=crop',
                'year': 2016,
                'description': 'A jazz musician and an aspiring actress meet and fall in love in Los Angeles.',
                'duration_minutes': 128,
                'genres': ['Drama'],
                'moods': ['Romantic', 'Happy', 'Sad'],
                'is_featured': True,
                'subscription_required': 'basic'
            },
            {
                'title': 'Get Out',
                'poster_url': 'https://images.unsplash.com/photo-1507924538820-ede94a04019d?q=80&w=2070&auto=format&fit=crop',
                'year': 2017,
                'description': 'A young African-American visits his white girlfriend\'s parents for the weekend, where his simmering uneasiness becomes a nightmare.',
                'duration_minutes': 104,
                'genres': ['Thriller'],
                'moods': ['Scared', 'Thoughtful'],
                'is_new_release': True,
                'subscription_required': 'premium'
            },
            {
                'title': 'The Grand Budapest Hotel',
                'poster_url': 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?q=80&w=2070&auto=format&fit=crop',
                'year': 2014,
                'description': 'The adventures of Gustave H, a legendary concierge at a famous European hotel.',
                'duration_minutes': 99,
                'genres': ['Adventure', 'Drama'],
                'moods': ['Happy', 'Nostalgic', 'Adventurous'],
                'is_featured': True,
                'subscription_required': 'basic'
            },
            {
                'title': 'Black Panther',
                'poster_url': 'https://images.unsplash.com/photo-1635805737707-575885ab0820?q=80&w=2070&auto=format&fit=crop',
                'year': 2018,
                'description': 'T\'Challa, heir to the hidden but advanced kingdom of Wakanda, must step forward to lead his people.',
                'duration_minutes': 134,
                'genres': ['Action', 'Adventure', 'Sci-Fi'],
                'moods': ['Excited', 'Adventurous', 'Thoughtful'],
                'is_new_release': True,
                'subscription_required': 'premium'
            }
        ]
        
        for movie_data in movies_data:
            # Create slug from title
            slug = slugify(movie_data['title'])
            
            movie, created = Movie.objects.get_or_create(
                title=movie_data['title'],
                defaults={
                    'slug': slug,
                    'poster_url': movie_data['poster_url'],
                    'year': movie_data['year'],
                    'description': movie_data['description'],
                    'duration_minutes': movie_data['duration_minutes'],
                    'is_featured': movie_data.get('is_featured', False),
                    'is_new_release': movie_data.get('is_new_release', False),
                    'subscription_required': movie_data.get('subscription_required', 'free'),
                    'rating': 'PG-13',
                }
            )
            
            if created:
                # Add genres
                for genre_name in movie_data['genres']:
                    if genre_name in created_genres:
                        movie.genres.add(created_genres[genre_name])
                
                # Add moods
                for mood_name in movie_data.get('moods', []):
                    if mood_name in created_moods:
                        movie.moods.add(created_moods[mood_name])
                
                self.stdout.write(f'Created movie: {movie.title}')
            else:
                # Update existing movie with moods if they don't have any
                if not movie.moods.exists():
                    for mood_name in movie_data.get('moods', []):
                        if mood_name in created_moods:
                            movie.moods.add(created_moods[mood_name])
                
                self.stdout.write(f'Movie already exists: {movie.title}')
        
        # Create dummy users and reviews
        self.create_dummy_reviews()
        
        self.stdout.write(
            self.style.SUCCESS('Sample data loaded successfully!')
        )
    
    def create_dummy_reviews(self):
        """Create dummy users and reviews for movies"""
        User = get_user_model()
        
        # Create dummy users
        dummy_users = [
            {'username': 'moviebuff87', 'email': 'moviebuff87@example.com'},
            {'username': 'cinemafan', 'email': 'cinemafan@example.com'},
            {'username': 'filmcritic', 'email': 'filmcritic@example.com'},
            {'username': 'actionlover', 'email': 'actionlover@example.com'},
            {'username': 'dramaaddict', 'email': 'dramaaddict@example.com'},
            {'username': 'scifigeek', 'email': 'scifigeek@example.com'},
        ]
        
        created_users = []
        for user_data in dummy_users:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'password': 'dummypass123'
                }
            )
            created_users.append(user)
            if created:
                self.stdout.write(f'Created user: {user.username}')
        
        # Sample reviews for each movie
        reviews_data = {
            'Inception': [
                {'user': 'moviebuff87', 'rating': 5, 'review': 'Mind-bending masterpiece! Christopher Nolan outdid himself with this one. The layers of dreams within dreams kept me guessing until the very end.'},
                {'user': 'cinemafan', 'rating': 4, 'review': 'Visually stunning and conceptually brilliant. Some parts were a bit confusing but overall an amazing experience.'},
                {'user': 'scifigeek', 'rating': 5, 'review': 'This is what science fiction should be - intelligent, thought-provoking, and visually spectacular. A modern classic!'}
            ],
            'Interstellar': [
                {'user': 'dramaaddict', 'rating': 5, 'review': 'Made me cry multiple times. The relationship between Cooper and Murph was beautifully portrayed. Space scenes were breathtaking.'},
                {'user': 'scifigeek', 'rating': 4, 'review': 'Great hard sci-fi concepts mixed with emotional storytelling. The black hole visuals were incredible.'},
                {'user': 'filmcritic', 'rating': 4, 'review': 'Nolan delivers another complex narrative. Some pacing issues in the middle but the ending is satisfying.'}
            ],
            'The Dark Knight': [
                {'user': 'actionlover', 'rating': 5, 'review': 'Heath Ledger\'s Joker is legendary! Best superhero movie ever made. Perfect blend of action and psychological thriller.'},
                {'user': 'moviebuff87', 'rating': 5, 'review': 'Dark, gritty, and absolutely phenomenal. This transcends the superhero genre and becomes pure cinema.'},
                {'user': 'cinemafan', 'rating': 4, 'review': 'Incredible performances all around. The action sequences are expertly choreographed.'}
            ],
            'Avatar': [
                {'user': 'scifigeek', 'rating': 4, 'review': 'Revolutionary visual effects that still hold up today. The world-building of Pandora is incredible.'},
                {'user': 'actionlover', 'rating': 4, 'review': 'Epic adventure with stunning visuals. The final battle sequence is spectacular.'},
                {'user': 'dramaaddict', 'rating': 3, 'review': 'Beautiful to look at but the story is pretty predictable. Still worth watching for the visuals.'}
            ],
            'Dune': [
                {'user': 'scifigeek', 'rating': 5, 'review': 'Finally, a proper adaptation of Herbert\'s masterpiece! Denis Villeneuve nailed the atmosphere and scope.'},
                {'user': 'filmcritic', 'rating': 4, 'review': 'Visually stunning and faithfully adapted. Looking forward to part two!'},
                {'user': 'moviebuff87', 'rating': 4, 'review': 'Epic in scale and vision. The desert planet feels real and lived-in.'}
            ],
            'Blade Runner 2049': [
                {'user': 'scifigeek', 'rating': 5, 'review': 'A worthy sequel that honors the original while telling its own story. Visually magnificent.'},
                {'user': 'cinemafan', 'rating': 4, 'review': 'Slow burn but incredibly rewarding. The cinematography is absolutely gorgeous.'},
                {'user': 'dramaaddict', 'rating': 4, 'review': 'Emotional and thoughtful sci-fi. Ryan Gosling delivers a great performance.'}
            ],
            'The Matrix': [
                {'user': 'actionlover', 'rating': 5, 'review': 'Revolutionary action sequences and mind-bending concept. Changed cinema forever!'},
                {'user': 'scifigeek', 'rating': 5, 'review': 'Groundbreaking in every way. The philosophy mixed with amazing action is perfect.'},
                {'user': 'moviebuff87', 'rating': 4, 'review': 'Iconic movie that defined a generation. The bullet-time effects were incredible for 1999.'}
            ],
            'Pulp Fiction': [
                {'user': 'filmcritic', 'rating': 5, 'review': 'Tarantino\'s masterpiece. Non-linear storytelling at its finest with unforgettable dialogue.'},
                {'user': 'cinemafan', 'rating': 5, 'review': 'Every scene is quotable. Samuel L. Jackson and John Travolta have amazing chemistry.'},
                {'user': 'dramaaddict', 'rating': 4, 'review': 'Dark, funny, and brilliantly written. Not for everyone but definitely a classic.'}
            ],
            'Fight Club': [
                {'user': 'moviebuff87', 'rating': 5, 'review': 'Subversive and thought-provoking. The twist ending still gives me chills. Brad Pitt is phenomenal.'},
                {'user': 'filmcritic', 'rating': 4, 'review': 'Dark satire of consumer culture. Fincher\'s direction is flawless as always.'},
                {'user': 'dramaaddict', 'rating': 4, 'review': 'Disturbing but compelling. The commentary on masculinity and society is brilliant.'}
            ]
        }
        
        # Create reviews for movies
        for movie_title, movie_reviews in reviews_data.items():
            try:
                movie = Movie.objects.get(title=movie_title)
                for review_data in movie_reviews:
                    user = User.objects.get(username=review_data['user'])
                    review, created = UserRating.objects.get_or_create(
                        user=user,
                        movie=movie,
                        defaults={
                            'rating': review_data['rating'],
                            'review': review_data['review']
                        }
                    )
                    if created:
                        self.stdout.write(f'Created review for {movie_title} by {user.username}')
            except Movie.DoesNotExist:
                self.stdout.write(f'Movie {movie_title} not found, skipping reviews')
            except User.DoesNotExist:
                continue