"""Q4 - experiments: x in list vs x in set, nested loops vs & vs sort-and-walk."""
import random, time, timeit

random.seed(3)
print("Membership test, looking up 200 absent values (worst case for the list)")
print(f"{'n':>10} {'list s':>10} {'set s':>10} {'ratio':>10}")
for n in (10_000, 100_000, 1_000_000):
    nums = random.sample(range(10 * n), n)
    as_set = set(nums)
    probes = [-i - 1 for i in range(200)]                 # never present
    t0 = time.perf_counter()
    for p in probes: p in nums
    tl = time.perf_counter() - t0
    t0 = time.perf_counter()
    for p in probes: p in as_set
    ts = time.perf_counter() - t0
    print(f"{n:>10} {tl:>10.4f} {ts:>10.6f} {tl/ts:>10.0f}x")


def common_nested(a, b):
    out = []
    for x in a:
        for y in b:
            if x == y:
                out.append(x); break
    return out

def common_sorted(a, b):
    a, b = sorted(a), sorted(b)
    i = j = 0; out = []
    while i < len(a) and j < len(b):
        if a[i] == b[j]: out.append(a[i]); i += 1; j += 1
        elif a[i] < b[j]: i += 1
        else: j += 1
    return out

def common_set(a, b):
    return sorted(set(a) & set(b))

print("\nCommon students: two electives of n register numbers each")
print(f"{'n':>7} {'nested loops s':>15} {'sort + walk s':>14} {'set & s':>10}  same result")
for n in (500, 2000, 5000):
    pool = random.sample(range(10 * n), 2 * n)
    a, b = pool[:n] + pool[n:n + n // 5], pool[n // 2:n] + pool[n:2 * n]
    a, b = list(dict.fromkeys(a)), list(dict.fromkeys(b))
    t0 = time.perf_counter(); r1 = sorted(common_nested(a, b)); t1 = time.perf_counter()
    r2 = common_sorted(a, b); t2 = time.perf_counter()
    r3 = common_set(a, b); t3 = time.perf_counter()
    print(f"{n:>7} {t1-t0:>15.4f} {t2-t1:>14.4f} {t3-t2:>10.5f}  {r1 == r2 == r3}")

print("\nFor a bigger case only the O(n+m) methods are practical (n = m = 1,000,000)")
a = random.sample(range(5_000_000), 1_000_000); b = random.sample(range(5_000_000), 1_000_000)
t0 = time.perf_counter(); r2 = common_sorted(a, b); t1 = time.perf_counter(); r3 = common_set(a, b); t2 = time.perf_counter()
print(f"  sort + walk {t1-t0:.3f} s   set & {t2-t1:.3f} s   same result: {r2 == r3}")
