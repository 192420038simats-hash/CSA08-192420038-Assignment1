"""A1 alternative: CSV + pandas loaded for every question, versus SQLite (full scan and with an index).
Question: average PM2.5 of one station in October. 12, 120 stations x 365 days x 24 hours."""
import os, sys, time, sqlite3, tempfile
import pandas as pd
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data"))
import synth

tmp = tempfile.mkdtemp()
print(f"{'stations':>8} {'rows':>10} | {'pandas: read CSV + filter':>26} {'SQL scan (no index)':>20} {'SQL with index':>15} | {'CSV on disk':>12} {'DB on disk':>11} {'DataFrame in RAM':>17} | same answer")
for n in (12, 120):
    csvp, dbp = os.path.join(tmp, f"d{n}.csv"), os.path.join(tmp, f"d{n}.db")
    rows = synth.write_csv(csvp, n)
    synth.build_db(dbp, n)
    target = f"S{n // 2:03d}"
    t0 = time.perf_counter()
    df = pd.read_csv(csvp, dtype={"station_id": str})
    a = df[(df.station_id == target) & (df.day >= "2026-10-01") & (df.day <= "2026-10-31")].pm25.mean()
    t_pandas = time.perf_counter() - t0
    ram = df.memory_usage(deep=True).sum()
    con = sqlite3.connect(dbp)
    q = "SELECT AVG(pm25) FROM readings WHERE station_id = ? AND day BETWEEN '2026-10-01' AND '2026-10-31'"
    t0 = time.perf_counter(); b = con.execute(q, (target,)).fetchone()[0]; t_scan = time.perf_counter() - t0
    con.execute("CREATE INDEX idx_station_day ON readings (station_id, day)"); con.commit()
    t0 = time.perf_counter(); c = con.execute(q, (target,)).fetchone()[0]; t_idx = time.perf_counter() - t0
    plan = con.execute("EXPLAIN QUERY PLAN " + q, (target,)).fetchall()[0][-1]
    con.close()
    print(f"{n:>8} {rows:>10,} | {t_pandas:>24.3f} s {t_scan*1000:>17.2f} ms {t_idx*1000:>12.3f} ms | {os.path.getsize(csvp)/1e6:>9.1f} MB {os.path.getsize(dbp)/1e6:>8.1f} MB {ram/1e6:>14.1f} MB | {abs(a-b) < 1e-9 and abs(b-c) < 1e-9}")
print("query plan with index:", plan)
