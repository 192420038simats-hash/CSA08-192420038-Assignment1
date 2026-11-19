"""Task B1 - whole pipeline: raw files -> clean -> CSV + SQLite database + cleaning report.
Run:  python pipeline.py      (creates data/clean/readings_clean.csv, airquality.db, cleaning_report.txt)"""
import csv, logging, os, sqlite3, time
from collections import Counter
from pathlib import Path
from cleaning import clean_text, fill_missing, read_text, CleaningError

ROOT = Path(__file__).resolve().parent.parent
RAW, CLEAN, DB = ROOT / "data" / "raw", ROOT / "data" / "clean", ROOT / "TaskB1" / "airquality.db"
SCHEMA = (ROOT / "TaskA1" / "schema.sql").read_text()

logging.basicConfig(level=logging.WARNING, format="%(levelname)s %(message)s")


def load_stations():
    st = list(csv.DictReader(open(ROOT / "data" / "stations.csv")))
    return {s["name"].lower().replace(" ", "_"): s for s in st}


def run(strategy="ffill"):
    stations = load_stations()
    counter, per_station, skipped = Counter(), {}, []
    t0 = time.perf_counter()
    for path in sorted(RAW.glob("*.csv")):
        key = path.stem.rsplit("_", 1)[0]
        st = stations[key]
        try:
            rows = clean_text(read_text(path), fahrenheit=(st["temp_unit"] == "F"), counter=counter)
        except CleaningError as e:
            skipped.append((path.name, str(e))); continue
        per_station.setdefault(st["station_id"], []).extend(rows)
        counter["files read"] += 1
    final = []
    for sid, rows in per_station.items():
        for r in fill_missing(rows, strategy, counter=counter):
            final.append((sid, r["day"], r["hour"], r["pm25"], r["pm10"], r["no2"], r["temp_c"]))
    final.sort(key=lambda t: (t[0], t[1], t[2]))
    CLEAN.mkdir(exist_ok=True)
    with open(CLEAN / "readings_clean.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["station_id", "day", "hour", "pm25", "pm10", "no2", "temp_c"])
        w.writerows(["" if v is None else v for v in t] for t in final)
    if DB.exists(): DB.unlink()
    con = sqlite3.connect(DB)
    con.executescript(SCHEMA)
    con.executemany("INSERT INTO stations VALUES (?,?,?,?,?)",
                    [(s["station_id"], s["name"], float(s["latitude"]), float(s["longitude"]), s["temp_unit"]) for s in stations.values()])
    con.executemany("INSERT INTO readings (station_id, day, hour, pm25, pm10, no2, temp_c) VALUES (?,?,?,?,?,?,?)", final)
    con.commit(); con.close()
    counter["rows stored in SQLite"] = len(final)
    return counter, skipped, time.perf_counter() - t0


if __name__ == "__main__":
    counter, skipped, secs = run()
    print(f"{'step':<34}{'count':>8}")
    for k in ["files read", "raw rows", "duplicate rows removed", "bad hour rows", "dates reformatted", "temperatures converted F->C",
              "missing values", "impossible values -> missing", "values forward-filled", "rows stored in SQLite"]:
        print(f"{k:<34}{counter[k]:>8}")
    print("files skipped:", skipped, f"| total time {secs:.2f} s")
