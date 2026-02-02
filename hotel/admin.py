from django.contrib import admin

from hotel.models import Booking, Room


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ["id", "description", "price_per_night", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["description"]
    ordering = ["-created_at"]


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ["id", "room", "date_start", "date_end", "created_at"]
    list_filter = ["date_start", "date_end", "created_at"]
    search_fields = ["room__description"]
    ordering = ["date_start"]
