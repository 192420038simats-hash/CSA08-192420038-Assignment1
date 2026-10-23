"""Task 4 alternative: int() truncation and math.floor() instead of round() for the step count."""
import math, timeit
def rate_with(fn, fat, snf=8.5):
    return round(30.0 + fn((fat - 3.5) / 0.1) * 0.40 + fn((snf - 8.5) / 0.1) * 0.30, 2)
print("fat   raw_steps            round   int   floor   rate(round) rate(int) rate(floor)")
for fat in (4.2, 3.1):
    raw = (fat - 3.5) / 0.1
    print(f"{fat}  {raw!r:22} {round(raw):5} {int(raw):5} {math.floor(raw):6}   "
          f"{rate_with(round, fat):9}  {rate_with(int, fat):9}  {rate_with(math.floor, fat):9}")
for name, fn in [("round", round), ("int", int), ("floor", math.floor)]:
    t = timeit.timeit(lambda: fn(6.999999999999999), number=1_000_000)
    print(f"{name:6} 1,000,000 calls: {t:.3f} s   (O(1) time, O(1) space)")
