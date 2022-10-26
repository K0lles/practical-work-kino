
from django.urls import path
from . import views

urlpatterns = [
    path('registration/', views.registration, name='registration'),
    path('login/', views.login_in, name='login'),
    path('logout/', views.log_out, name='logout'),
    path('change-password/', views.change_password, name='change_password'),
]