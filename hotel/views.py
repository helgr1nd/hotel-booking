from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from hotel.serializers import (
    BookingCreateSerializer,
    BookingSerializer,
    RoomCreateSerializer,
    RoomSerializer,
)
from hotel.services import BookingService, RoomService


@api_view(["POST"])
def create_room(request: Request) -> Response:
    serializer = RoomCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    room = RoomService.create_room(
        description=serializer.validated_data["description"], price=serializer.validated_data["price"]
    )

    return Response({"room_id": room.id}, status=status.HTTP_201_CREATED)


@api_view(["DELETE"])
def delete_room(request: Request, room_id: int) -> Response:
    try:
        RoomService.delete_room(room_id)
        return Response({"message": f"Room {room_id} and its bookings deleted"}, status=status.HTTP_200_OK)
    except ValueError as e:
        return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
def list_rooms(request: Request) -> Response:
    sort_by = request.query_params.get("sort_by", "created_at")
    order = request.query_params.get("order", "desc")

    rooms = RoomService.get_rooms(sort_by=sort_by, order=order)
    serializer = RoomSerializer(rooms, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def create_booking(request: Request) -> Response:
    serializer = BookingCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    try:
        booking = BookingService.create_booking(
            room_id=serializer.validated_data["room_id"],
            date_start=serializer.validated_data["date_start"],
            date_end=serializer.validated_data["date_end"],
        )
        return Response({"booking_id": booking.id}, status=status.HTTP_201_CREATED)
    except ValueError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
def delete_booking(request: Request, booking_id: int) -> Response:
    try:
        BookingService.delete_booking(booking_id)
        return Response({"message": f"Booking {booking_id} deleted"}, status=status.HTTP_200_OK)
    except ValueError as e:
        return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
def list_bookings(request: Request) -> Response:
    room_id = request.query_params.get("room_id")

    if not room_id:
        return Response({"error": "room_id parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        room_id = int(room_id)
    except ValueError:
        return Response({"error": "room_id must be an integer"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        bookings = BookingService.get_bookings_by_room(room_id)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except ValueError as e:
        return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
