"""Task 11 alternative: start-up cost of reading t values from JSON versus constants in the module."""
import json, time, tempfile, os
from decimal import Decimal
for t in (6, 600, 60000):
    data = {f"k{i}": "30.00" for i in range(t)}
    path = os.path.join(tempfile.gettempdir(), "card_test.json")
    with open(path, "w") as fh: json.dump(data, fh)
    t0 = time.perf_counter()
    with open(path) as fh: card = {k: Decimal(v) for k, v in json.load(fh).items()}
    el = time.perf_counter() - t0
    print(f"t = {t:6} values: start-up {el*1000:8.3f} ms, file {os.path.getsize(path):8} bytes, one-time cost per program start")
