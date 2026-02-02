import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Room",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("description", models.TextField()),
                ("price_per_night", models.IntegerField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "db_table": "rooms",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="Booking",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("date_start", models.DateField()),
                ("date_end", models.DateField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "room",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="bookings", to="hotel.room"
                    ),
                ),
            ],
            options={
                "db_table": "bookings",
                "ordering": ["date_start"],
            },
        ),
        migrations.AddIndex(
            model_name="room",
            index=models.Index(fields=["price_per_night"], name="idx_rooms_price"),
        ),
        migrations.AddIndex(
            model_name="room",
            index=models.Index(fields=["created_at"], name="idx_rooms_created"),
        ),
        migrations.AddIndex(
            model_name="booking",
            index=models.Index(fields=["room", "date_start"], name="idx_bookings_room_dates"),
        ),
    ]
