"""Task 8 alternative: measure peak memory of list-storing versus running total."""
import tracemalloc, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from ten_day_total import total_store_list, total_running
for n in (300, 6000, 150000):
    raw = [("8.5", "4.2", "8.7")] * n
    for name, fn in [("list", lambda r: total_store_list(r)[0]), ("running", total_running)]:
        tracemalloc.start(); fn(raw); _, peak = tracemalloc.get_traced_memory(); tracemalloc.stop()
        print(f"n={n:7}  {name:8} peak extra memory {peak/1024:9.1f} KiB")
