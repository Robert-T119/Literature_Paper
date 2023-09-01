from django.urls import path
from .views import paper_finder_view

urlpatterns = [
    path('', paper_finder_view, name='paper_finder'),
]
