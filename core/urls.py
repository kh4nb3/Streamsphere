from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('subscription/', views.subscription, name='subscription'),
]
