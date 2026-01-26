CREATE TABLE IF NOT EXISTS rooms (
    id SERIAL PRIMARY KEY,
    description TEXT NOT NULL,
    price_per_night INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS bookings (
    id SERIAL PRIMARY KEY,
    room_id INTEGER NOT NULL,
    date_start DATE NOT NULL,
    date_end DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (room_id) REFERENCES rooms (id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_rooms_price ON rooms (price_per_night);

CREATE INDEX IF NOT EXISTS idx_rooms_created ON rooms (created_at);

CREATE INDEX IF NOT EXISTS idx_bookings_room_dates ON bookings (room_id, date_start);