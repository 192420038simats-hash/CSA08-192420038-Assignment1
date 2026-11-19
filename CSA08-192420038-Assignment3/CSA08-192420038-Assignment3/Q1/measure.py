"""Q1 - experiments: additions derived vs counted, timing, list operation costs, edge cases, insert cost."""
import time
from rainfall import *


def naive_count(r, w=7):
    adds = 0
    for i in range(len(r) - w + 1):
        s = r[i]
        for x in r[i + 1:i + w]:
            s += x; adds += 1
    return adds


def running_count(r, w=7):
    if len(r) < w: return 0
    s = r[0]; adds = 0
    for x in r[1:w]:
        s += x; adds += 1
    for i in range(w, len(r)):
        s += r[i]; adds += 1          # one addition per slide (and one subtraction, not counted here)
        s -= r[i - w]
    return adds


print(f"{'n':>8} {'derived naive':>14} {'counted':>10} {'derived running':>16} {'counted':>10} {'t naive s':>10} {'t running s':>12} {'max |diff|':>11}")
for n in (365, 36500, 365000):
    r = generate_readings(n)
    t0 = time.perf_counter(); a = moving_average_naive(r); t1 = time.perf_counter()
    b = moving_average_running(r); t2 = time.perf_counter()
    d = max(abs(x - y) for x, y in zip(a, b))
    cn, cr = naive_count(r), running_count(r)
    print(f"{n:>8} {count_additions_naive(n):>14} {cn:>10} {count_additions_running(n):>16} {cr:>10} {t1-t0:>10.4f} {t2-t1:>12.4f} {d:>11.2e}")
print("derived: naive 6(n-6) additions; running (w-1)+(n-w) = n-1 additions plus n-7 subtractions")

print("\nEdge cases")
print("  empty list: weekly", weekly_totals([]), " moving avg", moving_average_naive([]), moving_average_running([]), " max/min", max_min_with_position([]), " dry", dry_days([]))
short = [1.0, 0.0, 2.5]
print("  3 values  : weekly", weekly_totals(short), " moving avg", moving_average_naive(short), moving_average_running(short), " dry", dry_days(short))
exact = [1, 2, 3, 4, 5, 6, 7]
print("  7 values  : moving avg", moving_average_naive(exact), moving_average_running(exact))

print("\nList operation costs (n = 365,000, microseconds per operation)")
base = generate_readings(365000)


def per_op(fn, reps=1000):
    t0 = time.perf_counter()
    for _ in range(reps): fn()
    return (time.perf_counter() - t0) / reps * 1e6


L = base[:]
print(f"  append            : {per_op(lambda: L.append(1.0)):9.3f} us   O(1) amortised")
print(f"  pop() (end)       : {per_op(lambda: L.pop()):9.3f} us   O(1)")
print(f"  insert(0, x)      : {per_op(lambda: L.insert(0, 1.0)):9.3f} us   O(n)")
print(f"  insert(middle, x) : {per_op(lambda: L.insert(len(L)//2, 1.0)):9.3f} us   O(n)")
print(f"  pop(0)            : {per_op(lambda: L.pop(0)):9.3f} us   O(n)")
print(f"  sort() of 365,000 : {per_op(lambda: base[:].sort(), reps=5)/1000:9.3f} ms   O(n log n) (includes the copy)")

print("\nLate reading inserted at its date position: list.insert vs dict keyed by date")
for n in (365, 36500, 365000):
    L = generate_readings(n)
    t0 = time.perf_counter()
    for _ in range(200): L.insert(n // 2, 3.2)
    ti = (time.perf_counter() - t0) / 200 * 1e6
    D = {day: mm for day, mm in enumerate(generate_readings(n))}
    t0 = time.perf_counter()
    for k in range(200): D[n + k] = 3.2
    td = (time.perf_counter() - t0) / 200 * 1e6
    print(f"  n={n:>7}: list.insert {ti:8.3f} us   dict set {td:6.3f} us")
