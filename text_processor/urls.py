from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('upload_pdf/', views.upload_pdf, name='upload_pdf'),
    path('process_text/', views.process_text, name='process_text'),
    # path('serve_pdf/', views.serve_pdf, name='serve_pdf'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
