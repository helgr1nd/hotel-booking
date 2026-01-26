from django.db import models


class Room(models.Model):
    description = models.TextField()
    price_per_night = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "rooms"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["price_per_night"], name="idx_rooms_price"),
            models.Index(fields=["created_at"], name="idx_rooms_created"),
        ]

    def __str__(self):
        return f"Room {self.id}: {self.description[:50]}"


class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="bookings")
    date_start = models.DateField()
    date_end = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "bookings"
        ordering = ["date_start"]
        indexes = [
            models.Index(fields=["room", "date_start"], name="idx_bookings_room_dates"),
        ]

    def __str__(self):
        return f"Booking {self.id} for Room {self.room_id}: {self.date_start} - {self.date_end}"
