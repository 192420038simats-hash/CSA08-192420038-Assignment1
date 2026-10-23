"""Task 7 alternative: copying functions into every script versus importing once (sys.modules cache)."""
import time, importlib
t0 = time.perf_counter(); import milkrate; first = time.perf_counter() - t0
t0 = time.perf_counter()
for _ in range(1000): importlib.import_module("milkrate")        # already in sys.modules -> dictionary lookup
again = (time.perf_counter() - t0) / 1000
print(f"first import {first*1e6:.1f} microseconds (find, load, run once)")
print(f"later import {again*1e6:.2f} microseconds each (cache hit in sys.modules)")
print("Copy-paste design: a rate revision must be edited in every copy (k scripts = k edits); module design: 1 edit.")
