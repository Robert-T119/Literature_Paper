from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_and_extract_view, name='upload'),
    # Add other paths as needed
]
