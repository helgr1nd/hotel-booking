from datetime import date

from rest_framework import serializers

from hotel.models import Booking, Room


class RoomCreateSerializer(serializers.Serializer):
    description = serializers.CharField(min_length=1)
    price = serializers.IntegerField(min_value=1)


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ["id", "description", "price_per_night", "created_at"]


class BookingCreateSerializer(serializers.Serializer):
    room_id = serializers.IntegerField()
    date_start = serializers.DateField()
    date_end = serializers.DateField()

    def validate(self, data):
        if data["date_start"] >= data["date_end"]:
            raise serializers.ValidationError("date_end must be after date_start")

        if data["date_start"] < date.today():
            raise serializers.ValidationError("Cannot book dates in the past")

        return data


class BookingSerializer(serializers.ModelSerializer):
    booking_id = serializers.IntegerField(source="id", read_only=True)

    class Meta:
        model = Booking
        fields = ["booking_id", "date_start", "date_end"]
