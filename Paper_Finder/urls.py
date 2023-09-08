from django.urls import path
from .views import paper_finder_view
from . import views


urlpatterns = [
    path('', paper_finder_view, name='paper_finder'),
    path('download/', views.download_output_xlsx, name='download_output_xlsx'),

]
