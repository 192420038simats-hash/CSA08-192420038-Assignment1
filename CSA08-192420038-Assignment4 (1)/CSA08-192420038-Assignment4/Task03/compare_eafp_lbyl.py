"""Task 3 alternative: 'ask forgiveness' (try/except) versus 'look before you leap' (if checks) - time per line."""
import random, time

STATUSES = ("P", "A")

def eafp(lines):
    good = bad = 0
    for line in lines:
        try:
            reg, day, status = line.split(",")          # ValueError when the number of fields is wrong
            if status not in STATUSES:
                raise ValueError(status)
            good += 1
        except ValueError:
            bad += 1
    return good, bad

def lbyl(lines):
    good = bad = 0
    for line in lines:
        parts = line.split(",")
        if len(parts) == 3 and parts[2] in STATUSES:
            good += 1
        else:
            bad += 1
    return good, bad

random.seed(8)
N = 300_000
print(f"{'bad lines':>10} {'EAFP ns/line':>13} {'LBYL ns/line':>13}   same result")
for pct in (0, 1, 10, 50):
    lines = ["192311001,2026-10-08,P" if random.random() * 100 >= pct else "192311001,2026-10-08" for _ in range(N)]
    t0 = time.perf_counter(); a = eafp(lines); t1 = time.perf_counter(); b = lbyl(lines); t2 = time.perf_counter()
    print(f"{pct:>9}% {(t1-t0)/N*1e9:>13.0f} {(t2-t1)/N*1e9:>13.0f}   {a == b}")
