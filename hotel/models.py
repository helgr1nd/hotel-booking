"""
Модели данных для системы бронирования отеля.

Содержит модели для номеров (Room) и бронирований (Booking).
"""

from django.db import models


class Room(models.Model):
    """
    Модель номера отеля.

    Attributes:
        description: Описание номера (тип, удобства и т.д.)
        price_per_night: Цена за одну ночь проживания
        created_at: Дата и время создания записи
    """

    description = models.TextField()
    price_per_night = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "rooms"
        ordering = ["-created_at"]  # Сортировка по умолчанию: новые номера первыми
        indexes = [
            # Индекс для быстрой сортировки по цене
            models.Index(fields=["price_per_night"], name="idx_rooms_price"),
            # Индекс для быстрой сортировки по дате создания
            models.Index(fields=["created_at"], name="idx_rooms_created"),
        ]

    def __str__(self):
        return f"Room {self.id}: {self.description[:50]}"


class Booking(models.Model):
    """
    Модель бронирования номера.

    Attributes:
        room: Связь с номером (при удалении номера удаляются все его бронирования)
        date_start: Дата начала бронирования
        date_end: Дата окончания бронирования
        created_at: Дата и время создания бронирования
    """

    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="bookings")
    date_start = models.DateField()
    date_end = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "bookings"
        ordering = ["date_start"]  # Сортировка по дате начала бронирования
        indexes = [
            # Составной индекс для быстрого поиска бронирований по номеру и датам
            models.Index(fields=["room", "date_start"], name="idx_bookings_room_dates"),
        ]

    def __str__(self):
        return f"Booking {self.id} for Room {self.room_id}: {self.date_start} - {self.date_end}"
