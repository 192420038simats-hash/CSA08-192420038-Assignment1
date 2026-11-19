"""Synthetic CLEAN readings for the scaling experiments (A1, A2, A3, B3, B4). Deterministic (fixed seed).
rows(n_stations, days, per_day) yields (station_id, day, hour, pm25, pm10, no2, temp_c); about 3 % of pm25 are None."""
import csv, math, random, sqlite3
from datetime import date, timedelta
from pathlib import Path

SCHEMA = (Path(__file__).resolve().parent.parent / "TaskA1" / "schema.sql").read_text()


def rows(n_stations, days=365, per_day=24, seed=1, start=date(2026, 1, 1)):
    """Hourly-like PM2.5 = base level x season x time-of-day profile + AR(1) noise (neighbouring hours are similar)."""
    rnd = random.Random(seed)
    for s in range(n_stations):
        sid = f"S{s:03d}"
        base = rnd.uniform(35, 110)
        e = 0.0
        for d in range(days):
            day = (start + timedelta(days=d)).isoformat()
            season = 1 + 0.3 * math.sin(d / 365 * 2 * math.pi)
            for k in range(per_day):
                hour = k * 24 // per_day
                prof = 1.3 if hour in (7, 8, 9, 18, 19, 20) else 0.8 if 12 <= hour <= 15 else 1.0
                e = 0.85 * e + rnd.gauss(0, 7)
                pm25 = None if rnd.random() < 0.03 else round(max(5.0, base * season * prof + e), 1)
                yield (sid, day, hour, pm25, round(base * 1.6, 1), round(max(1.0, rnd.gauss(35, 8)), 1), round(rnd.gauss(28, 4), 1))


def write_csv(path, n_stations, days=365, per_day=24):
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["station_id", "day", "hour", "pm25", "pm10", "no2", "temp_c"])
        n = 0
        for r in rows(n_stations, days, per_day):
            w.writerow(["" if v is None else v for v in r]); n += 1
    return n


def build_db(path, n_stations, days=365, per_day=24, index=False):
    """SQLite file with the real schema; returns the number of rows. The table is created WITHOUT an index."""
    p = Path(path)
    if p.exists(): p.unlink()
    con = sqlite3.connect(p)
    con.executescript(SCHEMA)
    con.executemany("INSERT INTO stations VALUES (?,?,?,?,?)", [(f"S{s:03d}", f"Station {s}", 13.0, 80.2, "C") for s in range(n_stations)])
    n = 0
    batch = []
    for r in rows(n_stations, days, per_day):
        batch.append(r); n += 1
        if len(batch) == 50000:
            con.executemany("INSERT INTO readings (station_id, day, hour, pm25, pm10, no2, temp_c) VALUES (?,?,?,?,?,?,?)", batch); batch = []
    if batch:
        con.executemany("INSERT INTO readings (station_id, day, hour, pm25, pm10, no2, temp_c) VALUES (?,?,?,?,?,?,?)", batch)
    if index:
        con.execute("CREATE INDEX idx_station_day ON readings (station_id, day)")
    con.commit(); con.close()
    return n
