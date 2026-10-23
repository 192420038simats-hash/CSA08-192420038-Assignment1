"""Task 10 - float versus Decimal totals, timings, round-each versus round-total, and the rate-table alternative."""
import random, sys, os, time
from decimal import Decimal, ROUND_HALF_UP
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Task09"))
import calculator as calc

random.seed(2026)

def make_entries(n):
    """n random entries as text: litres 0.01 L steps, fat/snf 0.1 % steps inside the allowed ranges."""
    return [(f"{random.randint(100, 3000)/100:.2f}", f"{random.randint(20, 70)/10:.1f}", f"{random.randint(70, 100)/10:.1f}") for _ in range(n)]

def float_run(entries):
    total, rounded_amounts = 0.0, 0
    unrounded_total = 0.0
    mism_inputs = []
    for l, f, s in entries:
        l, f, s = float(l), float(f), float(s)
        rate = round(30.0 + round((f - 3.5) / 0.1) * 0.40 + round((s - 8.5) / 0.1) * 0.30, 2)
        amount = round(l * rate, 2)
        total += amount
        unrounded_total += l * rate
    return total, unrounded_total

def decimal_run(entries):
    total, unrounded = Decimal("0"), Decimal("0")
    amounts = []
    for l, f, s in entries:
        l, f, s = Decimal(l), Decimal(f), Decimal(s)
        r = calc.rate_per_litre(f, s)
        unrounded += l * r
        a = calc.money(l * r)
        amounts.append(a)
        total += a
    return total, unrounded, amounts

def float_amounts(entries):
    out = []
    for l, f, s in entries:
        l, f, s = float(l), float(f), float(s)
        rate = round(30.0 + round((f - 3.5) / 0.1) * 0.40 + round((s - 8.5) / 0.1) * 0.30, 2)
        out.append(round(l * rate, 2))
    return out

print(f"{'n':>8} {'float total':>20} {'Decimal total':>16} {'difference':>14} {'t float s':>10} {'t Decimal s':>12} {'payments differing':>19}")
for n in (300, 6000, 150000):
    e = make_entries(n)
    t0 = time.perf_counter(); ft, fu = float_run(e); t1 = time.perf_counter()
    dt, du, damounts = decimal_run(e); t2 = time.perf_counter()
    fam = float_amounts(e)
    differing = sum(1 for a, b in zip(fam, damounts) if Decimal(repr(a)) != b)
    print(f"{n:>8} {ft!r:>20} {str(dt):>16} {float(Decimal(repr(ft)) - dt):>14.8f} {t1-t0:>10.4f} {t2-t1:>12.4f} {differing:>19}")
    # round each payment versus round only the total
    print(f"         round-each (bank) total = {dt}   round-only-total = {du.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)}   "
          f"difference = {dt - du.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)}   (exact unrounded sum {du})")

# why float rounding of x.xx5 goes wrong
print("\nHalf-paisa example 8.25 L x Rs 30.50 = 251.625")
print("  float  round(8.25*30.5, 2) =", round(8.25 * 30.5, 2), "(banker's/representation)")
print("  Decimal ROUND_HALF_UP      =", calc.money(Decimal("8.25") * Decimal("30.50")))
print("  float  round(2.675, 2)     =", round(2.675, 2), "(2.675 is stored as 2.67499999...)")

# ---- alternative: rate table (dictionary cache) ----
print("\nRate table versus recalculation (Decimal rates, time for whole run)")
print(f"{'n':>8} {'recalculate s':>14} {'table build s':>14} {'table run s':>12} {'k pairs':>8} {'table bytes':>12} {'same total':>11}")
for n in (300, 6000, 150000):
    e = make_entries(n)
    ed = [(Decimal(l), Decimal(f), Decimal(s)) for l, f, s in e]
    t0 = time.perf_counter()
    tot1 = sum((calc.money(l * calc.rate_per_litre(f, s)) for l, f, s in ed), Decimal("0"))
    t1 = time.perf_counter()
    table = {}
    for f in range(20, 71):
        for s in range(70, 101):
            fd, sd = Decimal(f) / 10, Decimal(s) / 10
            table[(fd, sd)] = calc.rate_per_litre(fd, sd)
    t2 = time.perf_counter()
    tot2 = sum((calc.money(l * table[(f, s)]) for l, f, s in ed), Decimal("0"))
    t3 = time.perf_counter()
    print(f"{n:>8} {t1-t0:>14.4f} {t2-t1:>14.4f} {t3-t2:>12.4f} {len(table):>8} {sys.getsizeof(table):>12} {str(tot1==tot2):>11}")
