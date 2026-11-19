"""A4 alternative: print() for debugging versus the logging module. Cost of 200,000 debug messages in a cleaning loop."""
import io, logging, os, sys, tempfile, time

N = 200_000
values = [str(40 + i % 50) for i in range(N)]
tmp = os.path.join(tempfile.mkdtemp(), "debug.txt")


def loop(emit):
    total = 0.0
    for v in values:
        x = float(v)
        emit(f"cleaned value {x}")
        total += x
    return total


def timed(name, fn):
    t0 = time.perf_counter(); fn(); el = time.perf_counter() - t0
    return name, el


results = []
results.append(timed("no debugging at all", lambda: loop(lambda m: None)))
f = open(tmp, "w")
results.append(timed("print() to a file", lambda: loop(lambda m: print(m, file=f))))
f.close()
log = logging.getLogger("t"); log.setLevel(logging.DEBUG); log.propagate = False
h = logging.FileHandler(tmp, mode="w"); h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s")); log.addHandler(h)
results.append(timed("logging.debug, level DEBUG, to a file", lambda: loop(log.debug)))
log.setLevel(logging.WARNING)
results.append(timed("logging.debug, level WARNING (switched off)", lambda: loop(log.debug)))
logging.disable(logging.CRITICAL)
results.append(timed("logging.disable(CRITICAL)", lambda: loop(log.debug)))
logging.disable(logging.NOTSET)
DEBUG = False
results.append(timed("if DEBUG: print(...)  with DEBUG = False", lambda: loop(lambda m: print(m) if DEBUG else None)))
base = results[0][1]
print(f"{'method':<46}{'time s':>9}{'extra per call (microseconds)':>32}")
for name, el in results:
    print(f"{name:<46}{el:>9.3f}{(el - base) / N * 1e6:>32.2f}")
size = os.path.getsize(tmp)
print(f"\nlog file written by the DEBUG-level run: {size/1e6:.1f} MB for {N:,} messages")
