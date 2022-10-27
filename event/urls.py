from django.urls import path

from . import views

urlpatterns = [
    path('', views.event_view, name='event_view'),
    path('<int:event_pk>/', views.event_detail, name='event_detail'),
    path('news/', views.news_view, name='news_view'),
    path('news/<int:news_pk>/', views.news_detail, name='news_detail'),
]
