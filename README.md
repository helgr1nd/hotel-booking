# Hotel Booking Service

Сервис для управления номерами отеля и бронированиями.

## Стек

- Django 5.0 + DRF
- PostgreSQL
- Poetry
- Docker Compose

## Запуск

```bash
docker-compose up --build
```

Сервис на http://localhost:9000

## API

### Номера

```bash
# Создать
curl -X POST http://localhost:9000/roo[apps.py](hotel/apps.py)ms/create \
  -H "Content-Type: application/json" \
  -d '{"description": "Deluxe Room", "price": 5000}'

# Список (с сортировкой)
curl "http://localhost:9000/rooms/list?sort_by=price&order=asc"

# Удалить
curl -X DELETE http://localhost:9000/rooms/1/delete
```

### Бронирования

```bash
# Создать
curl -X POST http://localhost:9000/bookings/create \
  -H "Content-Type: application/json" \
  -d '{"room_id": 1, "date_start": "2026-03-01", "date_end": "2026-03-05"}'

# Список
curl "http://localhost:9000/bookings/list?room_id=1"

# Удалить
curl -X DELETE http://localhost:9000/bookings/1/delete
```

## Тесты

```bash
poetry run pytest
```

## Структура

```
hotel-booking-service/
├── config/          # Django настройки
├── hotel/           # Приложение
│   ├── models.py    # Room, Booking
│   ├── services.py  # Бизнес-логика
│   ├── views.py     # API endpoints
│   └── serializers.py
├── tests/
└── sql/schema.sql
```

## Архитектура

Views → Services → Models

Вся бизнес-логика в `hotel/services.py`.

## Локальный запуск

```bash
poetry install
poetry run python manage.py migrate
poetry run python manage.py runserver 9000
```

## Решения

- Проверка пересечения дат бронирований
- Каскадное удаление (номер → брони)
- Индексы для оптимизации запросов
- Сортировка по цене и дате создания
