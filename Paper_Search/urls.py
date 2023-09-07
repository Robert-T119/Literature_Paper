from django.urls import path
from . import views

urlpatterns = [
    path('', views.paper_search_view, name='paper_search_view'),
]
