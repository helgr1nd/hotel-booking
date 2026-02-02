import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def sample_room(db):
    from hotel.models import Room

    return Room.objects.create(description="Deluxe Room", price_per_night=5000)


@pytest.fixture
def sample_booking(db, sample_room):
    from datetime import date

    from hotel.models import Booking

    return Booking.objects.create(room=sample_room, date_start=date(2026, 2, 1), date_end=date(2026, 2, 5))
