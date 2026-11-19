"""Q1 - State electricity subsidy eligibility (K4 Analyse)."""
import timeit
from bisect import bisect_left


def separate_ifs(units, ration, senior):
    """Faulty developer version: independent if statements (no lower bound on slab 2)."""
    result = []
    if units <= 100:
        result.append("full subsidy")
    if units <= 200 and ration:            # BUG: missing 101 <= units
        result.append("partial subsidy")
    if units > 200 and senior:
        result.append("special subsidy (80+ member)")
    return result or ["no subsidy"]


def chained(units, ration, senior):
    """Correct version: exactly one branch can run."""
    if units <= 100:
        return "full subsidy"
    elif 101 <= units <= 200:
        return "partial subsidy" if ration else "no subsidy"
    else:
        return "special subsidy (80+ member)" if senior else "no subsidy"


SLABS = [(100, "full subsidy"), (200, "slab-2"), (float("inf"), "slab-3")]


def table_lookup(units, ration, senior):
    for limit, name in SLABS:
        if units <= limit:
            if name == "slab-2":
                return "partial subsidy" if ration else "no subsidy"
            if name == "slab-3":
                return "special subsidy (80+ member)" if senior else "no subsidy"
            return name


def match_version(units, ration, senior):
    match units:
        case u if u <= 100:
            return "full subsidy"
        case u if u <= 200:
            return "partial subsidy" if ration else "no subsidy"
        case _:
            return "special subsidy (80+ member)" if senior else "no subsidy"


CASES = [  # (units, ration card, member above 80, predicted decision)
    (50, False, False, "full subsidy"),
    (100, False, False, "full subsidy"),
    (101, True, False, "partial subsidy"),
    (101, False, False, "no subsidy"),
    (200, True, False, "partial subsidy"),
    (200, False, False, "no subsidy"),
    (201, False, True, "special subsidy (80+ member)"),
    (201, False, False, "no subsidy"),
    (50, True, False, "full subsidy"),   # extra case that exposes the bug
]

if __name__ == "__main__":
    print(f"{'Units':>5} {'Card':>5} {'80+':>5} | {'Separate ifs':<45} | {'if-elif-else':<30} | Predicted? ")
    print("-" * 115)
    for u, r, s, pred in CASES:
        a, b = separate_ifs(u, r, s), chained(u, r, s)
        flag = " <-- DOUBLE" if len(a) > 1 else ""
        ok = "OK" if b == pred == table_lookup(u, r, s) == match_version(u, r, s) else "MISMATCH"
        print(f"{u:>5} {str(r):>5} {str(s):>5} | {str(a):<45} | {b:<30} | {ok}{flag}")

    print("\nTime per decision (microseconds, 200,000 calls each, k = 3 slabs):")
    for f in (chained, table_lookup, match_version):
        t = timeit.timeit(lambda: [f(u, True, False) for u in (50, 150, 250)], number=200_000 // 3)
        print(f"  {f.__name__:<14} {t / 200_000 * 1e6:8.3f} us")

    print("\nScaling with k slabs (list scan O(k) vs bisect O(log k)), worst-case query:")
    for k in (10, 100, 1000, 10000):
        limits = list(range(100, 100 * k + 1, 100))
        q = limits[-1]
        scan = timeit.timeit(lambda: next(i for i, L in enumerate(limits) if q <= L), number=2000)
        bis = timeit.timeit(lambda: bisect_left(limits, q), number=2000)
        print(f"  k={k:>6}: scan {scan / 2000 * 1e6:10.3f} us   bisect {bis / 2000 * 1e6:8.3f} us")
