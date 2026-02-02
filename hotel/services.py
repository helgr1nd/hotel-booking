from datetime import date

from django.db import transaction
from django.db.models import QuerySet

from hotel.models import Booking, Room


def create_room(description: str, price: int) -> Room:
    room = Room.objects.create(description=description, price_per_night=price)
    return room


@transaction.atomic
def delete_room(room_id: int) -> None:
    try:
        room = Room.objects.get(id=room_id)
        room.delete()
    except Room.DoesNotExist:
        raise ValueError(f"Room with id {room_id} not found") from None


def get_rooms(sort_by: str = "created_at", order: str = "desc") -> QuerySet[Room]:
    valid_sort_fields = {"price": "price_per_night", "created_at": "created_at"}

    if sort_by not in valid_sort_fields:
        sort_by = "created_at"

    field = valid_sort_fields[sort_by]

    if order == "asc":
        order_field = field
    else:
        order_field = f"-{field}"

    return Room.objects.all().order_by(order_field)


def create_booking(room_id: int, date_start: date, date_end: date) -> Booking:
    try:
        room = Room.objects.get(id=room_id)
    except Room.DoesNotExist:
        raise ValueError(f"Room with id {room_id} not found") from None

    overlapping = Booking.objects.filter(
        room_id=room_id, date_start__lt=date_end, date_end__gt=date_start
    ).exists()

    if overlapping:
        raise ValueError("Room is already booked for these dates")

    booking = Booking.objects.create(room=room, date_start=date_start, date_end=date_end)
    return booking


def delete_booking(booking_id: int) -> None:
    try:
        booking = Booking.objects.get(id=booking_id)
        booking.delete()
    except Booking.DoesNotExist:
        raise ValueError(f"Booking with id {booking_id} not found") from None


def get_bookings_by_room(room_id: int) -> list[Booking]:
    try:
        Room.objects.get(id=room_id)
    except Room.DoesNotExist:
        raise ValueError(f"Room with id {room_id} not found") from None

    return list(Booking.objects.filter(room_id=room_id).order_by("date_start"))
