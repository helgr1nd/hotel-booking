import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestRoomViews:
    def test_create_room(self, api_client):
        url = reverse("create_room")
        data = {"description": "Standard Room", "price": 3000}

        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert "room_id" in response.data
        assert response.data["room_id"] > 0

    def test_create_room_invalid_price(self, api_client):
        url = reverse("create_room")
        data = {"description": "Standard Room", "price": -100}

        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_delete_room(self, api_client, sample_room):
        url = reverse("delete_room", kwargs={"room_id": sample_room.id})

        response = api_client.delete(url)

        assert response.status_code == status.HTTP_200_OK
        assert "message" in response.data

    def test_delete_nonexistent_room(self, api_client):
        url = reverse("delete_room", kwargs={"room_id": 99999})

        response = api_client.delete(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_list_rooms(self, api_client, sample_room):
        url = reverse("list_rooms")

        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1

    def test_list_rooms_sorted_by_price(self, api_client, sample_room):
        from hotel.models import Room

        Room.objects.create(description="Budget Room", price_per_night=2000)
        Room.objects.create(description="Luxury Room", price_per_night=10000)

        url = reverse("list_rooms")
        response = api_client.get(url, {"sort_by": "price", "order": "asc"})

        assert response.status_code == status.HTTP_200_OK
        prices = [room["price_per_night"] for room in response.data]
        assert prices == sorted(prices)
