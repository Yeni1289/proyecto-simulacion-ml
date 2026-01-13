from django.urls import path
from . import views

urlpatterns = [
    path('', views.dataset_loader, name='dataset_loader'),
    path('notebooks/', views.index, name='index'),
    path('notebook/<path:filename>/', views.notebook_view, name='notebook_view'),
    path('api/list-files/', views.list_files, name='list_files'),
    path('api/open-notebook/', views.open_notebook, name='open_notebook'),
]
