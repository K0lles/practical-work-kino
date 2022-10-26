from django.urls import path
from . import views

urlpatterns = [
    path('statistics/', views.statistics_view, name='statistics'),
    path('banner/', views.create_banner, name='create_banner'),
    path('cinema/', views.cinema_view, name='cinema'),
    path('cinema/create/', views.create_cinema, name='cinema_create'),
    path('cinema/update/<int:pk>/', views.update_cinema, name='update_cinema'),
    path('cinema/delete/<int:pk>/', views.delete_cinema, name='delete_cinema'),
    path('movie/', views.movie_view, name='movie'),
    path('movie/update/<int:pk>', views.update_movie, name='update_movie'),
    path('movie/create', views.create_movie, name='create_movie'),
    path('hall/<int:cinema_pk>/create/', views.create_hall, name='create_hall'),
    path('hall/update/<int:hall_pk>/', views.update_hall, name='update_hall'),
    path('news/', views.news_view, name='news'),
    path('news/create', views.news_create, name='create_news'),
    path('events/', views.event_view, name='events'),
    path('event/create/', views.event_create, name='create_event'),
    path('event/update/<int:pk>/', views.update_event, name='update_event'),
    path('event/delete/<int:pk>/', views.delete_event, name='delete_event'),
    path('pages/', views.page_view, name='pages'),
    path('main-page/create/', views.main_page_create_update, name='main_page_create_update'),
    path('contacts/create', views.contact_page_create, name='contacts_create'),
    path('page/create/', views.create_page, name='page_create'),
    path('page/update/<int:pk>', views.update_page, name='update_page'),
    path('page/delete/<int:pk>/', views.delete_page, name='delete_page'),
    path('users/', views.users, name='users'),
    path('user/<int:pk>/delete', views.user_delete, name='user_delete'),
    path('user/update/<int:pk>', views.user_update, name='user_update'),
    path('mailing/', views.send_email_view, name='mailing'),
    path('files/', views.files, name='files')   # this url is used for ajax-requests to save uploaded file while mailing
]