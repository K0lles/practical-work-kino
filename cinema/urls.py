from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home_view, name='home'),
    path('poster/', views.poster_view, name='poster'),
    path('cinema/', views.cinema_view, name='cinema_view'),
    path('cinema/<int:cinema_pk>', views.cinema_detail, name='cinema_detail'),
    path('cinema/hall/<int:hall_pk>/', views.hall_detail, name='hall_detail'),

]
