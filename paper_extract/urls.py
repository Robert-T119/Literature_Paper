from django.urls import path
from . import views
from django.views.generic.base import RedirectView

app_name = 'Paper_Extractor'

urlpatterns = [
    path('', RedirectView.as_view(url='extract/'), name='root_redirect'),
    path('extract/', views.extract_dois_view, name='extract_dois'),
    path('upload/', views.upload_pdf_view, name='upload_pdf'),
    path('delete/<int:pdf_id>/', views.delete_pdf_view, name='delete_pdf'),
]
