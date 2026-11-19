-- Task A1.2 - SQLite design for the air-quality network
CREATE TABLE stations (
    station_id  TEXT PRIMARY KEY,                 -- short code, e.g. 'ADY'
    name        TEXT NOT NULL UNIQUE,             -- standard name, e.g. 'Adyar'
    latitude    REAL,
    longitude   REAL,
    temp_unit   TEXT NOT NULL CHECK (temp_unit IN ('C','F'))   -- unit the station REPORTS (data is stored in Celsius)
);

CREATE TABLE readings (
    id          INTEGER PRIMARY KEY,              -- surrogate key
    station_id  TEXT    NOT NULL REFERENCES stations(station_id),
    day         TEXT    NOT NULL,                 -- ISO date 'YYYY-MM-DD'
    hour        INTEGER NOT NULL CHECK (hour BETWEEN 0 AND 23),
    pm25        REAL CHECK (pm25 IS NULL OR pm25 BETWEEN 0 AND 999),   -- ug/m3, NULL = no valid reading
    pm10        REAL CHECK (pm10 IS NULL OR pm10 BETWEEN 0 AND 999),
    no2         REAL CHECK (no2  IS NULL OR no2  BETWEEN 0 AND 999),
    temp_c      REAL CHECK (temp_c IS NULL OR temp_c BETWEEN -10 AND 55)
);
