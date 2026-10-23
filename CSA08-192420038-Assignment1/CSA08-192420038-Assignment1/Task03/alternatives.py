"""Task 3 alternatives: magic numbers (k places to edit) and a RATE_CARD dictionary (one place)."""
import time

# (a) magic numbers: the 30, 0.4 and 0.3 appear in every expression
def rate_magic_1(fat, snf): return round(30.0 + round((fat - 3.5) / 0.1) * 0.40 + round((snf - 8.5) / 0.1) * 0.30, 2)
def rate_magic_2(fat, snf): return 30.0 + round((fat - 3.5) / 0.1) * 0.40 + round((snf - 8.5) / 0.1) * 0.30   # copy in another script

# (b) dictionary: one place, but a lookup per use and a typo in a key is only found at run time
RATE_CARD = {"base": 30.0, "fat": 0.40, "snf": 0.30}
def rate_dict(fat, snf):
    return round(RATE_CARD["base"] + round((fat - 3.5) / 0.1) * RATE_CARD["fat"] + round((snf - 8.5) / 0.1) * RATE_CARD["snf"], 2)

# (c) module-level constants
BASE, FATV, SNFV = 30.0, 0.40, 0.30
def rate_const(fat, snf):
    return round(BASE + round((fat - 3.5) / 0.1) * FATV + round((snf - 8.5) / 0.1) * SNFV, 2)

N = 1_000_000
for name, fn in [("magic numbers", rate_magic_1), ("dictionary", rate_dict), ("constants", rate_const)]:
    t0 = time.perf_counter()
    for _ in range(N): fn(4.2, 8.7)
    print(f"{name:14} {time.perf_counter()-t0:6.3f} s for {N:,} calls -> {fn(4.2, 8.7)}")
print("Places to edit for a base-rate revision: magic numbers = k (every expression and every copy), dict = 1, constants = 1")
