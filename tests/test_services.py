from datetime import date

import pytest

from hotel.models import Booking, Room
from hotel.services import BookingService, RoomService


@pytest.mark.django_db
class TestRoomService:
    def test_create_room(self):
        room = RoomService.create_room(description="Test Room", price=5000)

        assert room.id is not None
        assert room.description == "Test Room"
        assert room.price_per_night == 5000

    def test_delete_room(self, sample_room):
        room_id = sample_room.id

        RoomService.delete_room(room_id)

        assert not Room.objects.filter(id=room_id).exists()

    def test_delete_nonexistent_room(self):
        with pytest.raises(ValueError):
            RoomService.delete_room(99999)

    def test_get_rooms_sorted_by_price(self):
        Room.objects.create(description="Room A", price_per_night=3000)
        Room.objects.create(description="Room B", price_per_night=1000)
        Room.objects.create(description="Room C", price_per_night=5000)

        rooms = RoomService.get_rooms(sort_by="price", order="asc")
        prices = [room.price_per_night for room in rooms]

        assert prices == sorted(prices)


@pytest.mark.django_db
class TestBookingService:
    def test_create_booking(self, sample_room):
        booking = BookingService.create_booking(
            room_id=sample_room.id, date_start=date(2026, 4, 1), date_end=date(2026, 4, 5)
        )

        assert booking.id is not None
        assert booking.room_id == sample_room.id

    def test_create_booking_nonexistent_room(self):
        with pytest.raises(ValueError):
            BookingService.create_booking(room_id=99999, date_start=date(2026, 4, 1), date_end=date(2026, 4, 5))

    def test_delete_booking(self, sample_booking):
        booking_id = sample_booking.id

        BookingService.delete_booking(booking_id)

        assert not Booking.objects.filter(id=booking_id).exists()

    def test_get_bookings_by_room(self, sample_room, sample_booking):
        bookings = BookingService.get_bookings_by_room(sample_room.id)

        assert len(bookings) >= 1
        assert bookings[0].id == sample_booking.id
