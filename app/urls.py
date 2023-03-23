from django.urls import path
from .views import Home,Friends

urlpatterns = [
    path('home',Home.as_view(),name='home'),
    path('friends',Friends,name='searchedfriends'),
]
