"""B4.2 - 112 stations (12 + 100 new) reporting every 15 minutes: 90 days = 967,680 rows. Effect of an index on (station_id, day)."""
import os, sqlite3, sys, tempfile, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data"))
import synth

path = os.path.join(tempfile.mkdtemp(), "big.db")
t0 = time.perf_counter(); rows = synth.build_db(path, 112, days=90, per_day=96); print(f"database built: {rows:,} rows in {time.perf_counter() - t0:.1f} s, {os.path.getsize(path)/1e6:.0f} MB\n")
con = sqlite3.connect(path)
Q = {
    "Q1 mean of ONE station for one month": ("SELECT AVG(pm25) FROM readings WHERE station_id = 'S050' AND day BETWEEN '2026-02-01' AND '2026-02-28'", ()),
    "Q2 daily summary of ONE station": ("SELECT day, MIN(pm25), MAX(pm25), AVG(pm25), COUNT(pm25) FROM readings WHERE station_id = 'S050' GROUP BY day", ()),
    "Q3 network mean of ONE day": ("SELECT AVG(pm25) FROM readings WHERE day = '2026-02-10'", ()),
    "Q4 mean of every station (GROUP BY station)": ("SELECT station_id, AVG(pm25) FROM readings GROUP BY station_id", ()),
    "Q5 days over 60 for every station": ("SELECT station_id, COUNT(*) FROM (SELECT station_id, day, AVG(pm25) a FROM readings GROUP BY station_id, day) WHERE a > 60 GROUP BY station_id", ()),
}


def best(sql, args, reps=3):
    ts = []
    for _ in range(reps):
        t0 = time.perf_counter(); con.execute(sql, args).fetchall(); ts.append(time.perf_counter() - t0)
    return min(ts)


def plan(sql):
    return " | ".join(r[-1] for r in con.execute("EXPLAIN QUERY PLAN " + sql))


size_before = os.path.getsize(path)
before = {k: best(*v) for k, v in Q.items()}
plans_before = {k: plan(v[0]) for k, v in Q.items()}
t0 = time.perf_counter(); con.execute("CREATE INDEX idx_station_day ON readings (station_id, day)"); con.commit(); t_idx = time.perf_counter() - t0
after = {k: best(*v) for k, v in Q.items()}
plans_after = {k: plan(v[0]) for k, v in Q.items()}
size_idx = os.path.getsize(path)
print(f"{'query':<46}{'no index':>10}{'index (station, day)':>22}{'change':>10}")
for k in Q:
    print(f"{k:<46}{before[k]*1000:>8.1f}ms{after[k]*1000:>20.1f}ms{before[k]/after[k]:>9.1f}x")
print(f"\nslowest query before the index: {max(before, key=before.get)}")
print(f"index creation time {t_idx:.2f} s; database file grew from {size_before/1e6:.0f} MB to {size_idx/1e6:.0f} MB")
for k in Q:
    print(f"plan {k[:2]} before: {plans_before[k][:90]}\n        after : {plans_after[k][:90]}")
con.execute("CREATE INDEX idx_cover ON readings (station_id, day, pm25)"); con.commit()
q5 = Q["Q5 days over 60 for every station"]
print(f"\nwith a COVERING index (station_id, day, pm25): Q5 = {best(*q5)*1000:.1f} ms   (plan: {plan(q5[0])[:80]})")
con.close()
