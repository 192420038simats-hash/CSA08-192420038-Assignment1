"""Q6 - generate 100, 1,000 and 10,000 trains; time queries with and without the index; memory of the index."""
import random, sys, time
from railway import trains_at, build_index, trains_at_indexed, DAYS

random.seed(11)
STATIONS = [f"Station{i:03d}" for i in range(200)]


def make_timetable(n):
    tt = {}
    for i in range(n):
        k = random.randint(8, 15)
        stops = [(s, "10:00", "10:05") for s in random.sample(STATIONS, k)]
        tt[f"{10000 + i}"] = {"name": f"Train {i}", "stops": stops, "days": set(random.sample(DAYS, random.randint(3, 7)))}
    return tt


def deep_size(obj, seen=None):
    seen = seen or set()
    if id(obj) in seen: return 0
    seen.add(id(obj)); size = sys.getsizeof(obj)
    if isinstance(obj, dict): size += sum(deep_size(k, seen) + deep_size(v, seen) for k, v in obj.items())
    elif isinstance(obj, (list, tuple, set)): size += sum(deep_size(i, seen) for i in obj)
    return size


print(f"{'trains':>7} {'total stops':>12} {'scan us/query':>14} {'indexed us/query':>17} {'speed-up':>9} {'build index ms':>15} {'index bytes':>12} {'timetable bytes':>16}  same")
for n in (100, 1000, 10000):
    tt = make_timetable(n)
    total = sum(len(t["stops"]) for t in tt.values())
    t0 = time.perf_counter(); idx = build_index(tt); build = (time.perf_counter() - t0) * 1000
    queries = [(random.choice(STATIONS), random.choice(DAYS)) for _ in range(200 if n < 10000 else 60)]
    t0 = time.perf_counter(); r1 = [trains_at(s, d, tt) for s, d in queries]; ts = (time.perf_counter() - t0) / len(queries) * 1e6
    t0 = time.perf_counter(); r2 = [trains_at_indexed(s, d, tt, idx) for s, d in queries]; ti = (time.perf_counter() - t0) / len(queries) * 1e6
    same = all(sorted(a) == sorted(b) for a, b in zip(r1, r2))
    print(f"{n:>7} {total:>12} {ts:>14.1f} {ti:>17.2f} {ts/ti:>8.0f}x {build:>15.2f} {deep_size(idx):>12,} {deep_size(tt):>16,}  {same}")

# alternative: one flat list of tuples scanned for every query
print("\nAlternative design: one flat list of (train, station, arrival, departure, days) tuples scanned per query")
print(f"{'trains':>7} {'flat rows':>10} {'flat scan us/query':>19} {'nested scan us/query':>21} {'nested+index us/query':>22} {'flat bytes':>12}")
for n in (100, 1000, 10000):
    tt = make_timetable(n); idx = build_index(tt)
    flat = [(no, st, arr, dep, t["days"]) for no, t in tt.items() for st, arr, dep in t["stops"]]
    queries = [(random.choice(STATIONS), random.choice(DAYS)) for _ in range(200 if n < 10000 else 60)]
    t0 = time.perf_counter(); r1 = [[r[0] for r in flat if r[1] == s and d in r[4]] for s, d in queries]; tf = (time.perf_counter() - t0) / len(queries) * 1e6
    t0 = time.perf_counter(); r2 = [trains_at(s, d, tt) for s, d in queries]; tn = (time.perf_counter() - t0) / len(queries) * 1e6
    t0 = time.perf_counter(); r3 = [trains_at_indexed(s, d, tt, idx) for s, d in queries]; ti = (time.perf_counter() - t0) / len(queries) * 1e6
    print(f"{n:>7} {len(flat):>10} {tf:>19.1f} {tn:>21.1f} {ti:>22.2f} {deep_size(flat):>12,}")
