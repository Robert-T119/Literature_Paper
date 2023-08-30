from django.urls import path
from . import views

app_name = 'paper_extract'

urlpatterns = [
    path('extract/', views.extract_dois_view, name='extract_dois'),
    path('upload/', views.upload_pdf_view, name='upload_pdf'),
    path('delete/<int:pdf_id>/', views.delete_pdf_view, name='delete_pdf'),

]
