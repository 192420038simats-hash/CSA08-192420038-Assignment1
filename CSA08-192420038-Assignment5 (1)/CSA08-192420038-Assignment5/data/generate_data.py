"""Generates the raw daily station files for October 2026 (12 stations x 31 days x 24 hours) with realistic problems.
Run:  python generate_data.py     -> data/raw/<station name with underscores>_<YYYY-MM-DD>.csv
Raw file header: date,hour,pm25,pm10,no2,temp   (the station is given by the file name)"""
import csv, math, os, random
from datetime import date, timedelta

random.seed(2026)
HERE = os.path.dirname(os.path.abspath(__file__))
stations = list(csv.DictReader(open(os.path.join(HERE, "stations.csv"))))
BASE = {"ADY": 45, "ALN": 55, "ANN": 50, "GND": 70, "KOD": 95, "MAN": 110, "PER": 60, "ROY": 85, "TNG": 58, "VEL": 52, "ENN": 100, "TON": 80}
out = os.path.join(HERE, "raw"); os.makedirs(out, exist_ok=True)
for f in os.listdir(out): os.remove(os.path.join(out, f))
dayshift = [random.gauss(0, 2) for _ in range(31)]          # regional weather: warm days are a little cleaner
problems = {"blank": 0, "NA": 0, "negative": 0, "too_large": 0, "text": 0, "duplicate": 0, "bad_hour": 0, "dmy_date": 0}
for st in stations:
    for d in range(31):
        day = date(2026, 10, 1) + timedelta(days=d)
        rows = []
        for h in range(24):
            rush = 1.35 if h in (7, 8, 9, 18, 19, 20) else (0.8 if 12 <= h <= 15 else 1.0)
            pm25 = max(5, random.gauss(BASE[st["station_id"]] * rush * (1 - 0.04 * dayshift[d]), 12))
            pm10 = pm25 * random.uniform(1.4, 1.9)
            no2 = random.gauss(30 + 0.2 * pm25, 6)
            tc = 27 + dayshift[d] + 4 * math.sin((h - 9) / 24 * 2 * math.pi) + random.gauss(0, 0.6)
            temp = tc * 9 / 5 + 32 if st["temp_unit"] == "F" else tc
            vals = [round(pm25, 1), round(pm10, 1), round(no2, 1), round(temp, 1)]
            for i in range(4):                                   # sensor and transmission problems
                r = random.random()
                if r < 0.020: vals[i] = ""; problems["blank"] += 1
                elif r < 0.032: vals[i] = "NA"; problems["NA"] += 1
                elif r < 0.036 and i < 3: vals[i] = -round(random.uniform(1, 40), 1); problems["negative"] += 1
                elif r < 0.040 and i < 3: vals[i] = random.choice([999.9, 1500, 9999]); problems["too_large"] += 1
                elif r < 0.042: vals[i] = random.choice(["ERR", "--", "n/a"]); problems["text"] += 1
            hour = h
            if random.random() < 0.0008: hour = 24; problems["bad_hour"] += 1
            ds = day.isoformat()
            if st["station_id"] == "TNG": ds = day.strftime("%d/%m/%Y"); problems["dmy_date"] += 1   # one station uses dd/mm/yyyy
            rows.append([ds, hour] + vals)
            if random.random() < 0.004: rows.append([ds, hour] + vals); problems["duplicate"] += 1  # row sent twice
        name = st["name"].lower().replace(" ", "_")
        with open(os.path.join(out, f"{name}_{day.isoformat()}.csv"), "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f); w.writerow(["date", "hour", "pm25", "pm10", "no2", "temp"]); w.writerows(rows)
print("files written:", len(os.listdir(out)))
print("injected problems:", problems)
