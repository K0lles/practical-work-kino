from django.urls import path
from . import views

urlpatterns = [
    path('statistics/', views.statistics_view, name='statistics'),
    path('banner/', views.create_banner, name='create_banner'),
    path('cinema/', views.cinema_view, name='cinema'),
]
