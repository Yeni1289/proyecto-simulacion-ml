from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('notebook/<path:filename>/', views.notebook_view, name='notebook_view'),
]
