from django.shortcuts import render

# Mock Data
MOVIES = [
    {'id': 1, 'title': 'Inception', 'image': 'https://images.unsplash.com/photo-1626814026160-2237a95fc5a0?q=80&w=2070&auto=format&fit=crop', 'year': 2010, 'desc': 'A thief who steals corporate secrets through the use of dream-sharing technology.'},
    {'id': 2, 'title': 'Interstellar', 'image': 'https://images.unsplash.com/photo-1419242902214-272b3f66ee7a?q=80&w=2013&auto=format&fit=crop', 'year': 2014, 'desc': 'A team of explorers travel through a wormhole in space in an attempt to ensure humanity\'s survival.'},
    {'id': 3, 'title': 'The Dark Knight', 'image': 'https://images.unsplash.com/photo-1559583985-b81d2100a93f?q=80&w=2070&auto=format&fit=crop', 'year': 2008, 'desc': 'When the menace known as the Joker wreaks havoc and chaos on the people of Gotham.'},
    {'id': 4, 'title': 'Avatar', 'image': 'https://images.unsplash.com/photo-1518709268805-4e9042af9f23?q=80&w=1968&auto=format&fit=crop', 'year': 2009, 'desc': 'A paraplegic Marine dispatched to the moon Pandora on a unique mission.'},
    {'id': 5, 'title': 'Dune', 'image': 'https://images.unsplash.com/photo-1541963463532-d68292c34b19?q=80&w=1976&auto=format&fit=crop', 'year': 2021, 'desc': 'Feature adaptation of Frank Herbert\'s science fiction novel.'},
    {'id': 6, 'title': 'Blade Runner 2049', 'image': 'https://images.unsplash.com/photo-1534447677768-be436bb09401?q=80&w=2094&auto=format&fit=crop', 'year': 2017, 'desc': 'A young blade runner\'s discovery of a long-buried secret leads him to track down former blade runner Rick Deckard.'},
    {'id': 7, 'title': 'The Matrix', 'image': 'https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?q=80&w=2070&auto=format&fit=crop', 'year': 1999, 'desc': 'A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.'},
    {'id': 8, 'title': 'Pulp Fiction', 'image': 'https://images.unsplash.com/photo-1594909122845-11baa439b7bf?q=80&w=2070&auto=format&fit=crop', 'year': 1994, 'desc': 'The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption.'},
    {'id': 9, 'title': 'Fight Club', 'image': 'https://images.unsplash.com/photo-1599058945522-28d584b6f0ff?q=80&w=2069&auto=format&fit=crop', 'year': 1999, 'desc': 'An insomniac office worker and a devil-may-care soapmaker form an underground fight club that evolves into much more.'},
]

def home(request):
    return render(request, 'home.html', {'movies': MOVIES})

def login_view(request):
    return render(request, 'login.html')

def signup_view(request):
    return render(request, 'signup.html')

def movie_detail(request, movie_id):
    movie = next((m for m in MOVIES if m['id'] == movie_id), None)
    return render(request, 'movie_detail.html', {'movie': movie})

def subscription(request):
    return render(request, 'subscription.html')
