"""Task 6 alternative: duplicates found by searching a list of earlier registrations versus a set of register numbers."""
import random, time, sys

random.seed(6)
print(f"{'n':>8} {'list search s':>14} {'set s':>9} {'approx. comparisons (list)':>26} {'same duplicates':>16} {'list memory':>13} {'set memory':>12}")
for n in (2_000, 5_000, 10_000, 20_000, 40_000):
    regs = [str(192300000 + random.randint(0, int(n * 0.8))) for _ in range(n)]       # roughly 20 % repeated numbers
    t0 = time.perf_counter(); seen = []; dup_list = 0; comps = 0
    for r in regs:
        if r in seen:
            dup_list += 1
        else:
            seen.append(r)
    t_list = time.perf_counter() - t0
    t0 = time.perf_counter(); seen_set = set(); dup_set = 0
    for r in regs:
        if r in seen_set:
            dup_set += 1
        else:
            seen_set.add(r)
    t_set = time.perf_counter() - t0
    comps = n * len(seen) // 2
    print(f"{n:>8} {t_list:>14.4f} {t_set:>9.5f} {comps:>26,} {str(dup_list == dup_set):>16} {sys.getsizeof(seen):>13,} {sys.getsizeof(seen_set):>12,}")
