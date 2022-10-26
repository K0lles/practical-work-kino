from django.urls import path

from . import views

urlpatterns = [
    path('cafe-bar/', views.cafe_bar_detail, name='cafe_bar_detail'),
    path('advertisment/', views.advertisment_view, name='advertisment_view'),
    path('vip-hall/', views.vip_hall_view, name='vip_hall_view'),
    path('baby-room/', views.baby_room_view, name='baby_room_view'),
    path('contacts/', views.contacts_view, name='contacts_view'),
    path('mobile-applications/', views.mobile_applications, name='mobile_applications')
]
