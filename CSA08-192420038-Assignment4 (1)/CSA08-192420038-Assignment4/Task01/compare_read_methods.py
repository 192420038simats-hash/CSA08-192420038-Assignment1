"""Task 1 alternative: f.read() / f.readlines() versus iterating over the file, 50,000 lines."""
import os, time, tracemalloc, random
from decimal import Decimal

random.seed(4)
path = "mess_50000.txt"
with open(path, "w", encoding="utf-8") as f:
    for i in range(50000):
        f.write(f"19231{i:05d},Student Name {i:05d},{random.randint(900, 1600)}.{random.choice(['00','25','50','75'])}\n")
print(f"file size: {os.path.getsize(path):,} bytes, 50,000 lines")


def by_iteration():
    total = Decimal(0)
    with open(path, encoding="utf-8") as f:
        for line in f:
            total += Decimal(line.rsplit(",", 1)[1])
    return total

def by_read():
    with open(path, encoding="utf-8") as f:
        data = f.read()
    total = Decimal(0)
    for line in data.split("\n"):
        if line:
            total += Decimal(line.rsplit(",", 1)[1])
    return total

def by_readlines():
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()
    total = Decimal(0)
    for line in lines:
        total += Decimal(line.rsplit(",", 1)[1])
    return total

print(f"{'method':<22}{'time s':>9}{'peak memory':>16}   total")
for name, fn in [("iterate over file", by_iteration), ("f.read()", by_read), ("f.readlines()", by_readlines)]:
    tracemalloc.start(); t0 = time.perf_counter(); r = fn(); el = time.perf_counter() - t0
    _, peak = tracemalloc.get_traced_memory(); tracemalloc.stop()
    print(f"{name:<22}{el:>9.4f}{peak/1024:>13,.0f} KiB   {r}")
os.remove(path)
