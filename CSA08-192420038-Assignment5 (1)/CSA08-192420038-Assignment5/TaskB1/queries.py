"""B1.3 - the three questions of A1.3 answered with SQL on airquality.db AND from the clean CSV with Python loops."""
import csv, sqlite3, time
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
con = sqlite3.connect(ROOT / "TaskB1" / "airquality.db")

Q1 = "SELECT ROUND(AVG(pm25), 2) FROM readings r JOIN stations s USING (station_id) WHERE s.name = ? AND r.day BETWEEN '2026-10-01' AND '2026-10-31'"
Q2 = """SELECT s.name, ROUND(AVG(r.pm25), 2) AS mean_pm25 FROM readings r JOIN stations s USING (station_id)
        GROUP BY s.name ORDER BY mean_pm25 DESC LIMIT 3"""
Q3 = """SELECT s.name, COUNT(*) AS days_over_60 FROM
          (SELECT station_id, day, AVG(pm25) AS daily FROM readings GROUP BY station_id, day) d
        JOIN stations s USING (station_id) WHERE d.daily > 60 GROUP BY s.name ORDER BY days_over_60 DESC, s.name"""

print("Q1  Average PM2.5 of Adyar in October (SQL):", con.execute(Q1, ("Adyar",)).fetchone()[0])
print("Q2  Three stations with the highest monthly mean PM2.5 (SQL):")
for name, v in con.execute(Q2): print(f"      {name:<14}{v:>8}")
print("Q3  Days on which the daily mean exceeded 60 ug/m3, per station (SQL):")
res3 = con.execute(Q3).fetchall()
for name, n in res3: print(f"      {name:<14}{n:>4}")

# the same answers from the CSV with plain Python
names = {r["station_id"]: r["name"] for r in csv.DictReader(open(ROOT / "data" / "stations.csv"))}
t0 = time.perf_counter()
vals, by_day = defaultdict(list), defaultdict(list)
for r in csv.DictReader(open(ROOT / "data" / "clean" / "readings_clean.csv")):
    if r["pm25"] != "":
        v = float(r["pm25"]); vals[r["station_id"]].append(v); by_day[(r["station_id"], r["day"])].append(v)
q1 = round(sum(vals["ADY"]) / len(vals["ADY"]), 2)
q2 = sorted(((round(sum(v) / len(v), 2), names[k]) for k, v in vals.items()), reverse=True)[:3]
over = defaultdict(int)
for (sid, day), v in by_day.items():
    if sum(v) / len(v) > 60: over[names[sid]] += 1
t_csv = time.perf_counter() - t0
t0 = time.perf_counter()
con.execute(Q1, ("Adyar",)).fetchone(); list(con.execute(Q2)); list(con.execute(Q3))
t_sql = time.perf_counter() - t0
print(f"\nCSV + Python loops : Q1 {q1}   Q2 {[(n, v) for v, n in q2]}")
print("agree with SQL     :", q1 == con.execute(Q1, ("Adyar",)).fetchone()[0], [(n, v) for v, n in q2] == con.execute(Q2).fetchall(),
      dict(over) == dict(res3))
print(f"time for the 3 questions: CSV loops {t_csv*1000:.1f} ms (read + compute)   SQL {t_sql*1000:.1f} ms")
print("lines of code: SQL = 3 statements of 1-4 lines; CSV loops = about 12 lines")
con.close()
