from django.urls import path
from . import views
from django.views.generic.base import RedirectView
from .views import download_excel


app_name = 'Paper_Extractor'

urlpatterns = [
    path('', RedirectView.as_view(url='extract/'), name='root_redirect'),
    path('extract/', views.display_upload_page, name='display_upload'),
    path('start_extraction/', views.process_and_display_results, name='extract_dois'),
    path('upload/', views.upload_pdf_view, name='upload_pdf'),
    path('delete/<int:pdf_id>/', views.delete_pdf_view, name='delete_pdf'),
    path('download_excel/', download_excel, name='download_excel'),

]
