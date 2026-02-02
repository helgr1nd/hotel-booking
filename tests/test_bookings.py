import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestBookingViews:
    def test_create_booking(self, api_client, sample_room):
        url = reverse("create_booking")
        data = {"room_id": sample_room.id, "date_start": "2026-03-01", "date_end": "2026-03-05"}

        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert "booking_id" in response.data

    def test_create_booking_invalid_dates(self, api_client, sample_room):
        url = reverse("create_booking")
        data = {"room_id": sample_room.id, "date_start": "2026-03-05", "date_end": "2026-03-01"}

        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_booking_nonexistent_room(self, api_client):
        url = reverse("create_booking")
        data = {"room_id": 99999, "date_start": "2026-03-01", "date_end": "2026-03-05"}

        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_delete_booking(self, api_client, sample_booking):
        url = reverse("delete_booking", kwargs={"booking_id": sample_booking.id})

        response = api_client.delete(url)

        assert response.status_code == status.HTTP_200_OK

    def test_list_bookings(self, api_client, sample_room, sample_booking):
        url = reverse("list_bookings")

        response = api_client.get(url, {"room_id": sample_room.id})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1
        assert response.data[0]["booking_id"] == sample_booking.id

    def test_list_bookings_missing_room_id(self, api_client):
        url = reverse("list_bookings")

        response = api_client.get(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
