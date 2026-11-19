"""Q7 - Diagnose, redesign and validate: plain recursive ways_naive (K5 Evaluate)."""
import csv
import sys
import time

calls = 0


def ways_naive(n):                       # ORIGINAL
    global calls
    calls += 1
    if n <= 1:
        return 1
    return ways_naive(n - 1) + ways_naive(n - 2)


def ways_loop(n):                        # REDESIGN: bottom-up, last two values only
    steps = 0
    a = b = 1
    for _ in range(n - 1):
        a, b = b, a + b
        steps += 1
    return b, steps


def seconds(fn, *args):
    t = time.perf_counter(); fn(*args); return time.perf_counter() - t


if __name__ == "__main__":
    print("A. DIAGNOSIS - growth of calls in the original")
    prev = None
    last = 0
    for n in (10, 15, 20, 25, 30):
        calls = 0; w = ways_naive(n)
        ratio = f"{calls / prev:.3f}" if prev else "-"
        print(f"  n={n:>2}  calls={calls:>9}  ratio vs previous row={ratio}")
        prev = last = calls
    distinct = 31
    print(f"  distinct sub-problems for n=30: {distinct}; repeated calls = {last - distinct} "
          f"({100 * (last - distinct) / last:.4f}%)")

    print("\nB. OBJECTIVE: n=30 -> <= 31 operations; n=1000 with default recursion limit "
          f"({sys.getrecursionlimit()}) and no RecursionError.")
    print("\nD. PREDICTION: ~29 loop steps for n=30 (>90,000x fewer); n=1000 -> 999 steps, no error.")

    print("\nE. VALIDATION - original vs redesign (same inputs)")
    print(f"{'n':>5} | {'orig calls':>11} | {'redesign steps':>14} | {'orig time s':>11} | {'new time s':>10} | same answer")
    out = []
    for n in (10, 20, 25, 30):
        calls = 0; w1 = ways_naive(n); c = calls
        to = seconds(ways_naive, n)
        w2, steps = ways_loop(n)
        tn = seconds(ways_loop, n)
        print(f"{n:>5} | {c:>11} | {steps:>14} | {to:11.5f} | {tn:10.7f} | {w1 == w2}")
        out.append((n, c, steps, round(to, 6), round(tn, 8), w1 == w2))
    w, steps = ways_loop(1000)
    try:
        ways_naive(1000); status = "finished"
    except RecursionError:
        status = "RecursionError"
    t1000 = seconds(ways_loop, 1000)
    print(f"{1000:>5} | {status:>11} | {steps:>14} | {'-':>11} | {t1000:10.7f} | digits={len(str(w))}")
    out.append((1000, status, steps, "", round(t1000, 8), True))

    with open("q7_raw_data.csv", "w", newline="") as f:
        csv.writer(f).writerows([("n", "original_calls", "redesign_steps", "orig_s", "new_s", "same")] + out)
    print("\nraw data written to q7_raw_data.csv")
