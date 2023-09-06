from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search_papers, name='search_papers'),
]
