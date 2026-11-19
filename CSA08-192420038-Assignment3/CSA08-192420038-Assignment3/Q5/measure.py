"""Q5 - timing and memory: loop vs comprehension vs map/filter; list vs generator."""
import sys, time
from sensors import *

print(f"{'n':>9} {'loop s':>9} {'comprehension s':>16} {'map/filter s':>13}   identical")
for n in (10_000, 100_000, 1_000_000):
    data = generate(n)
    res, t = [], []
    for fn in (clean_loop, clean_comprehension, clean_map_filter):
        t0 = time.perf_counter(); res.append(fn(data)); t.append(time.perf_counter() - t0)
    print(f"{n:>9} {t[0]:>9.4f} {t[1]:>16.4f} {t[2]:>13.4f}   {res[0] == res[1] == res[2]}")

print("\nMemory of the result container only (sys.getsizeof), valid readings of n values")
print(f"{'n':>9} {'list comprehension':>20} {'generator expression':>22}")
for n in (10_000, 100_000, 1_000_000):
    data = generate(n)
    lst = [c for c in data if -50 <= c <= 50]
    gen = (c for c in data if -50 <= c <= 50)
    print(f"{n:>9} {sys.getsizeof(lst):>20,} {sys.getsizeof(gen):>22,}")

print("\nSum of valid readings: list comprehension vs generator expression")
print(f"{'n':>9} {'sum(list) s':>12} {'sum(gen) s':>11}   same sum")
for n in (10_000, 100_000, 1_000_000):
    data = generate(n)
    t0 = time.perf_counter(); a = sum([c for c in data if -50 <= c <= 50]); t1 = time.perf_counter()
    b = sum(c for c in data if -50 <= c <= 50); t2 = time.perf_counter()
    print(f"{n:>9} {t1-t0:>12.4f} {t2-t1:>11.4f}   {abs(a - b) < 1e-6}")
import tracemalloc
data = generate(1_000_000)
tracemalloc.start(); sum([c for c in data if -50 <= c <= 50]); _, p1 = tracemalloc.get_traced_memory(); tracemalloc.stop()
tracemalloc.start(); sum(c for c in data if -50 <= c <= 50); _, p2 = tracemalloc.get_traced_memory(); tracemalloc.stop()
print(f"\npeak extra memory while summing 1,000,000 readings: list {p1/1024:,.0f} KiB   generator {p2/1024:,.1f} KiB")
