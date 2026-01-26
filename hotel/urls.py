from django.urls import path

from hotel import views

urlpatterns = [
    # Rooms
    path("rooms/create", views.create_room, name="create_room"),
    path("rooms/<int:room_id>/delete", views.delete_room, name="delete_room"),
    path("rooms/list", views.list_rooms, name="list_rooms"),
    # Bookings
    path("bookings/create", views.create_booking, name="create_booking"),
    path("bookings/<int:booking_id>/delete", views.delete_booking, name="delete_booking"),
    path("bookings/list", views.list_bookings, name="list_bookings"),
]
