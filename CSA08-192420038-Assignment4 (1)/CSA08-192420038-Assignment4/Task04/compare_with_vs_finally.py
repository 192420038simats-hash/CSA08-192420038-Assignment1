"""Task 4 alternative: manual open/close in try/finally versus the with statement."""
import os, resource, time, tracemalloc, tempfile

path = os.path.join(tempfile.mkdtemp(), "log.txt")
def open_files(): return len(os.listdir("/proc/self/fd"))

def original(books):                       # no protection at all
    log = open(path, "a")
    for b in books: log.write(b)
    log.close()

def manual_finally(books):                 # manual try/finally
    log = open(path, "a")
    try:
        for b in books: log.write(b + "\n")
    finally:
        log.close()

def with_statement(books):                 # with
    with open(path, "a") as log:
        for b in books: log.write(b + "\n")

bad = ["A", None, "B"]
print(f"{'version':<20}{'files left open after 100 failed calls':>40}")
for name, fn in [("original (no close)", original), ("manual try/finally", manual_finally), ("with statement", with_statement)]:
    before = open_files(); held = []
    for _ in range(100):
        try: fn(bad)
        except TypeError as e: held.append(e)           # failures whose traceback is kept (log handler, test runner, debugger)
    print(f"{name:<20}{open_files() - before:>40}")
    del held
soft = resource.getrlimit(resource.RLIMIT_NOFILE)[0]
print(f"\noperating-system limit on open files for this process: {soft}  (the original would fail with 'Too many open files' after about that many errors)")

good = ["Python Basics"] * 100
print(f"\n{'version':<20}{'time for 20,000 calls':>24}{'peak memory':>14}")
for name, fn in [("manual try/finally", manual_finally), ("with statement", with_statement)]:
    tracemalloc.start(); t0 = time.perf_counter()
    for _ in range(20000): fn(good)
    el = time.perf_counter() - t0; _, peak = tracemalloc.get_traced_memory(); tracemalloc.stop()
    print(f"{name:<20}{el:>22.3f} s{peak/1024:>11.1f} KiB")
