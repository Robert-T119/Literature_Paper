from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.homepage, name='homepage'),  # New centralized homepage
    path('pdf_chat/', views.index, name='index'),  # Previous main page of pdf_chat
    path('upload_pdf/', views.upload_pdf, name='upload_pdf'),
    path('process_text/', views.process_text, name='process_text'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
