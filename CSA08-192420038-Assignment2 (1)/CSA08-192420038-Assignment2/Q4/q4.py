"""Q4 - Building long text: += versus join() (K4 Analyse)."""
import io
import sys
import time
import tracemalloc

items = [f"Item{i}:Rs{i % 50}" for i in range(200_000)]


def build_plus(parts):
    text = ""
    for p in parts:
        text += p + ";"
    return text


def build_join(parts):
    return ";".join(parts) + ";"          # single str.join() call (TODO 1)


def build_fstring(n):
    """(c) an f-string per line, collected and joined."""
    return "".join([f"Item{i}:Rs{i % 50};" for i in range(n)])


def build_stringio(parts):
    buf = io.StringIO()
    for p in parts:
        buf.write(p + ";")
    return buf.getvalue()


def timed(fn, *args):
    start = time.perf_counter()
    out = fn(*args)
    return out, time.perf_counter() - start


if __name__ == "__main__":
    print("Python", sys.version.split()[0])
    a, t_plus = timed(build_plus, items)
    b, t_join = timed(build_join, items)
    print("same text:", a == b, "| length:", len(b))
    print(f"+= time: {t_plus:.4f} s   join time: {t_join:.4f} s")

    print("\nAverage of 3 runs (seconds) with the assignment program:")
    tp = [timed(build_plus, items)[1] for _ in range(3)]
    tj = [timed(build_join, items)[1] for _ in range(3)]
    print(f"  += runs: {[round(x, 4) for x in tp]} avg {sum(tp) / 3:.4f}")
    print(f"  join runs: {[round(x, 4) for x in tj]} avg {sum(tj) / 3:.4f}")

    print("\nThree implementations at three sizes (avg of 3 runs, seconds):")
    print(f"{'lines':>8} | {'(a) +=':>9} | {'(b) join':>9} | {'(c) f-string':>12} | {'StringIO':>9} | same")
    for n in (1_000, 10_000, 200_000):
        sub = items[:n]
        row, outs = [], []
        for fn, arg in ((build_plus, sub), (build_join, sub), (build_fstring, n), (build_stringio, sub)):
            ts = []
            for _ in range(3):
                out, t = timed(fn, arg)
                ts.append(t)
            row.append(sum(ts) / 3)
            outs.append(out)
        print(f"{n:>8} | {row[0]:9.5f} | {row[1]:9.5f} | {row[2]:12.5f} | {row[3]:9.5f} | {len(set(outs)) == 1}")

    print("\nWhy += can look fast: CPython optimisation (single reference -> in-place realloc).")
    print("Keeping a second reference to the string defeats it and forces a copy each time:")
    for n in (5_000, 10_000, 20_000, 40_000):
        sub = items[:n]
        text, start = "", time.perf_counter()
        for p in sub:
            alias = text                  # second reference -> in-place resize impossible
            text += p + ";"
        t = time.perf_counter() - start
        print(f"  n={n:>6}: {t:8.4f} s")

    print("\nPeak extra memory (MiB) building 200,000 lines:")
    for fn in (build_plus, build_join, build_stringio):
        tracemalloc.start()
        fn(items)
        peak = tracemalloc.get_traced_memory()[1] / 2**20
        tracemalloc.stop()
        print(f"  {fn.__name__:<14} {peak:8.2f} MiB")
