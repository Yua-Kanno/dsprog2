CREATE TABLE IF NOT EXISTS area (
    area_code TEXT PRIMARY KEY,
    area_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS forecast (
    forecast_id INTEGER PRIMARY KEY AUTOINCREMENT,
    area_code TEXT NOT NULL,
    forecast_date TEXT NOT NULL,
    weather TEXT NOT NULL,
    temp_min INTEGER,
    temp_max INTEGER,
    fetched_at TEXT NOT NULL,
    FOREIGN KEY (area_code) REFERENCES area(area_code),
    UNIQUE (area_code, forecast_date)
);

