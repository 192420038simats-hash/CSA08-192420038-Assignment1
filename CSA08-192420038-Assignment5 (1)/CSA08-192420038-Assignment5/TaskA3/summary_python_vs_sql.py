"""A3 alternative: the daily summary (min, max, mean, number of valid readings per station and day) computed by
Python loops after fetching all rows, versus one SQL GROUP BY query."""
import os, sys, tempfile, time, sqlite3, tracemalloc
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data"))
import synth

SQL = """SELECT station_id, day, MIN(pm25), MAX(pm25), AVG(pm25), COUNT(pm25) FROM readings GROUP BY station_id, day"""


def python_loops(con):
    groups = {}
    for sid, day, pm in con.execute("SELECT station_id, day, pm25 FROM readings").fetchall():     # ALL rows in memory
        if pm is not None:
            groups.setdefault((sid, day), []).append(pm)
    return {k: (min(v), max(v), sum(v) / len(v), len(v)) for k, v in groups.items()}


tmp = tempfile.mkdtemp()
print(f"{'stations':>8} {'rows':>10} | {'Python loops: time':>19} {'peak memory':>12} | {'SQL GROUP BY: time':>19} {'peak memory':>12} | same result")
for n in (1, 12, 120):
    path = os.path.join(tmp, f"s{n}.db"); rows = synth.build_db(path, n)
    con = sqlite3.connect(path)
    tracemalloc.start(); t0 = time.perf_counter(); a = python_loops(con); ta = time.perf_counter() - t0; ma = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
    tracemalloc.start(); t0 = time.perf_counter(); b = con.execute(SQL).fetchall(); tb = time.perf_counter() - t0; mb = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
    same = len(a) == len(b) and all(abs(a[(s, d)][2] - m) < 1e-9 and a[(s, d)][3] == c for s, d, lo, hi, m, c in b if c)
    print(f"{n:>8} {rows:>10,} | {ta:>17.3f} s {ma/1e6:>9.1f} MB | {tb:>17.3f} s {mb/1e6:>9.2f} MB | {same}")
    con.close()
