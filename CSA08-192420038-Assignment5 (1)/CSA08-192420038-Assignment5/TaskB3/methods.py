"""B3 - the daily mean PM2.5 per station in three ways (plain Python + csv, pandas groupby, SQL GROUP BY) and the one-pass alternative."""
import csv, sqlite3, statistics
from collections import defaultdict
import pandas as pd


def by_python_loops(csv_path):
    """Store ALL readings of each (station, day), then statistics.mean()."""
    groups = defaultdict(list)
    with open(csv_path, newline="") as f:
        for rec in csv.DictReader(f):
            if rec["pm25"] != "":
                groups[(rec["station_id"], rec["day"])].append(float(rec["pm25"]))
    return {k: statistics.mean(v) for k, v in groups.items()}


def by_running_sum(csv_path):
    """One pass: keep only [sum, count] per (station, day)."""
    acc = {}
    with open(csv_path, newline="") as f:
        for rec in csv.DictReader(f):
            if rec["pm25"] != "":
                a = acc.setdefault((rec["station_id"], rec["day"]), [0.0, 0])
                a[0] += float(rec["pm25"]); a[1] += 1
    return {k: s / n for k, (s, n) in acc.items()}


def by_pandas(csv_path):
    df = pd.read_csv(csv_path, dtype={"station_id": str})
    return df.groupby(["station_id", "day"])["pm25"].mean().dropna().to_dict()


def load_sqlite(csv_path, db_path):
    """Load the CSV into SQLite with executemany (separate step, so that its time can be reported)."""
    con = sqlite3.connect(db_path)
    con.execute("DROP TABLE IF EXISTS readings")
    con.execute("CREATE TABLE readings (station_id TEXT, day TEXT, hour INTEGER, pm25 REAL, pm10 REAL, no2 REAL, temp_c REAL)")
    with open(csv_path, newline="") as f:
        r = csv.reader(f); next(r)
        batch = []
        for row in r:
            batch.append([None if x == "" else x for x in row])
            if len(batch) == 100_000:
                con.executemany("INSERT INTO readings VALUES (?,?,?,?,?,?,?)", batch); batch = []
        if batch: con.executemany("INSERT INTO readings VALUES (?,?,?,?,?,?,?)", batch)
    con.commit()
    return con


def by_sql(con):
    return {(s, d): m for s, d, m in con.execute("SELECT station_id, day, AVG(pm25) FROM readings GROUP BY station_id, day") if m is not None}


def same(a, b, tol=1e-9):
    return a.keys() == b.keys() and all(abs(a[k] - b[k]) < tol for k in a)
