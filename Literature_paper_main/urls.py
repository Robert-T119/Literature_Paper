from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Paper_Chat.urls')),
    path('Paper_Finder/', include('Paper_Finder.urls')),
    path('Paper_Extractor/', include('Paper_Extractor.urls', namespace='Paper_Extractor')),
    path('Paper_Search/', include('Paper_Search.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
