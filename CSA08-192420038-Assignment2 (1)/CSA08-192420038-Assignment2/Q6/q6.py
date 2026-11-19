"""Q6 - Recursion and its limits (K5 Evaluate)."""
import sys
import time
from functools import lru_cache

calls = 0


def ways_naive(n):
    """Ways to climb n temple steps taking 1 or 2 steps at a time."""
    global calls
    calls += 1
    if n <= 1:
        return 1
    return ways_naive(n - 1) + ways_naive(n - 2)


@lru_cache(maxsize=None)
def ways_memo(n):
    global calls
    calls += 1
    if n <= 1:                           # TODO 1: same base/recursive case, calling ways_memo
        return 1
    return ways_memo(n - 1) + ways_memo(n - 2)


def ways_loop(n):
    a = b = 1
    for _ in range(n - 1):
        a, b = b, a + b
    return b


def tree(n, depth=0):
    print("  " * depth + f"w{n}")
    if n > 1:
        tree(n - 1, depth + 1)
        tree(n - 2, depth + 1)


if __name__ == "__main__":
    print("Python", sys.version.split()[0])
    calls = 0; print("naive:", ways_naive(25), "calls =", calls)
    ways_memo.cache_clear()
    calls = 0; print("memo :", ways_memo(25), "calls =", calls)

    print("\nHand check n = 1..6 :", [ways_naive(n) for n in range(1, 7)], "(expected 1 2 3 5 8 13)")
    print("\nCall tree for n = 5:")
    tree(5)

    print("\nGrowth investigation (function calls):")
    print(f"{'n':>3} {'ways(n)':>10} {'naive calls':>12} {'2*ways-1':>10} {'memo calls':>11} {'n+1':>5}")
    for n in (10, 20, 25, 30):
        calls = 0; w = ways_naive(n); cn = calls
        ways_memo.cache_clear(); calls = 0; ways_memo(n); cm = calls
        print(f"{n:>3} {w:>10} {cn:>12} {2 * w - 1:>10} {cm:>11} {n + 1:>5}")

    print("\nDeployment decision, n = 1000:")
    print("sys.getrecursionlimit() =", sys.getrecursionlimit())
    ways_memo.cache_clear()
    try:
        ways_memo(1000)
    except RecursionError as e:
        print("RecursionError:", e)
    reference = ways_loop(1000)
    old = sys.getrecursionlimit()
    sys.setrecursionlimit(5000)
    ways_memo.cache_clear()
    print("memo with limit 5000 equals loop result:", ways_memo(1000) == reference)
    sys.setrecursionlimit(old)
    print("digits in ways(1000):", len(str(reference)))

    print("\nTiming for n = 1000 (average of 200 runs, seconds):")
    t = time.perf_counter()
    for _ in range(200): ways_loop(1000)
    print(f"  loop : {(time.perf_counter() - t) / 200:.6f}")
    sys.setrecursionlimit(5000)
    t = time.perf_counter()
    for _ in range(200):
        ways_memo.cache_clear(); ways_memo(1000)
    print(f"  memo : {(time.perf_counter() - t) / 200:.6f}")
    t = time.perf_counter(); ways_naive(30)
    print(f"  naive n=30 (single run): {time.perf_counter() - t:.4f}")
