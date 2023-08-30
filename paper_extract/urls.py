from django.urls import path
from . import views

app_name = 'paper_extract'

urlpatterns = [
    path('upload/', views.upload_pdf_view, name='upload_pdf'),
]
