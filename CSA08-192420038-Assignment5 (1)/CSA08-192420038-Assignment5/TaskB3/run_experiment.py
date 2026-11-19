"""B3.1 / B3.2 - correctness on small data, then 1, 12 and 120 stations x 365 days x 24 hours."""
import os, sys, tempfile, time, tracemalloc
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data"))
import synth
import methods as m

tmp = tempfile.mkdtemp()
# ---- B3.1 correctness on a small file whose answer can be checked by hand ----
small = os.path.join(tmp, "small.csv")
open(small, "w").write("station_id,day,hour,pm25,pm10,no2,temp_c\nA,2026-10-01,0,40,0,0,0\nA,2026-10-01,1,60,0,0,0\nA,2026-10-01,2,,0,0,0\n"
                       "A,2026-10-02,0,100,0,0,0\nB,2026-10-01,0,30,0,0,0\nB,2026-10-01,1,50,0,0,0\n")
con = m.load_sqlite(small, os.path.join(tmp, "small.db"))
a, b, c = m.by_python_loops(small), m.by_pandas(small), m.by_sql(con)
print("small file by hand: A 2026-10-01 = (40 + 60) / 2 = 50 (the blank is ignored), A 2026-10-02 = 100, B 2026-10-01 = (30 + 50) / 2 = 40")
print("  Python loops:", dict(sorted(a.items())))
print("  pandas      :", dict(sorted(b.items())))
print("  SQL         :", dict(sorted(c.items())))
print("  all three agree with each other and with the hand calculation:", m.same(a, b) and m.same(a, c) and a == {("A", "2026-10-01"): 50, ("A", "2026-10-02"): 100, ("B", "2026-10-01"): 40})
con.close()

# ---- B3.2 growing data ----
print(f"\n{'stations':>8} {'rows':>10} | {'Python loops':>12} {'running sum':>12} {'pandas':>8} {'SQL load':>9} {'SQL query':>10} {'SQL load+query':>15} | all agree")
for n in (1, 12, 120):
    path = os.path.join(tmp, f"d{n}.csv"); rows = synth.write_csv(path, n)
    t0 = time.perf_counter(); a = m.by_python_loops(path); t_py = time.perf_counter() - t0
    t0 = time.perf_counter(); r = m.by_running_sum(path); t_rs = time.perf_counter() - t0
    t0 = time.perf_counter(); b = m.by_pandas(path); t_pd = time.perf_counter() - t0
    t0 = time.perf_counter(); con = m.load_sqlite(path, os.path.join(tmp, f"d{n}.db")); t_load = time.perf_counter() - t0
    t0 = time.perf_counter(); c = m.by_sql(con); t_q = time.perf_counter() - t0
    print(f"{n:>8} {rows:>10,} | {t_py:>10.3f} s {t_rs:>10.3f} s {t_pd:>6.3f} s {t_load:>7.3f} s {t_q:>8.3f} s {t_load + t_q:>13.3f} s | {m.same(a, b) and m.same(a, c) and m.same(a, r)}")
    con.close()

# ---- memory of two of the methods at 12 stations ----
path = os.path.join(tmp, "d12.csv")
print("\nPeak memory (tracemalloc) at 12 stations, 105,120 rows:")
for name, fn in (("Python loops (store all readings)", m.by_python_loops), ("running sum (sum and count only)", m.by_running_sum)):
    tracemalloc.start(); fn(path); peak = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
    print(f"  {name:<36}{peak/1e6:>8.1f} MB")
