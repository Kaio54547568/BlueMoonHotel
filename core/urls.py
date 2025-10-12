from django.urls import path
from . import views

urlpatterns = [
    path('', views.rooms_list, name='rooms_list'),
    path('room/<int:room_id>/book/', views.book_room, name='book_room'),
    path('booking/success/<int:pk>/', views.booking_success, name='booking_success'),
]
