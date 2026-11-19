"""B3.3 - profile the plain-Python version (12 stations, 105,120 rows) with cProfile."""
import cProfile, io, os, pstats, sys, tempfile
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data"))
import synth
import methods as m

path = os.path.join(tempfile.mkdtemp(), "d12.csv"); synth.write_csv(path, 12)
pr = cProfile.Profile(); pr.enable(); m.by_python_loops(path); pr.disable()
s = io.StringIO(); st = pstats.Stats(pr, stream=s).strip_dirs().sort_stats("tottime"); st.print_stats(9)
print("\n".join(l for l in s.getvalue().splitlines() if l.strip())[:3200])
print("\n--- the same, sorted by cumulative time ---")
s = io.StringIO(); pstats.Stats(pr, stream=s).strip_dirs().sort_stats("cumulative").print_stats(6)
print("\n".join(l for l in s.getvalue().splitlines() if l.strip())[:2200])

# what if statistics.mean() is replaced by sum()/len()?
import time, statistics
from collections import defaultdict
groups = defaultdict(list)
import csv
for rec in csv.DictReader(open(path)):
    if rec["pm25"] != "": groups[(rec["station_id"], rec["day"])].append(float(rec["pm25"]))
t0 = time.perf_counter(); a = {k: statistics.mean(v) for k, v in groups.items()}; t1 = time.perf_counter()
b = {k: sum(v) / len(v) for k, v in groups.items()}; t2 = time.perf_counter()
print(f"\nstatistics.mean on {len(groups):,} groups: {t1-t0:.3f} s    sum()/len(): {t2-t1:.3f} s   (max difference {max(abs(a[k]-b[k]) for k in a):.2e})")
