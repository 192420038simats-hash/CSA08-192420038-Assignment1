"""Task 8 - algorithm for one payment and the ten-day total, both ways (store list / running total)."""
from decimal import Decimal, ROUND_HALF_UP

BASE, FATV, SNFV = Decimal("30.00"), Decimal("0.40"), Decimal("0.30")
STD_FAT, STD_SNF, STEP, PAISE = Decimal("3.5"), Decimal("8.5"), Decimal("0.1"), Decimal("0.01")

def payment(litres, fat, snf):
    steps_f = (fat - STD_FAT) / STEP
    steps_s = (snf - STD_SNF) / STEP
    rate = BASE + steps_f * FATV + steps_s * SNFV
    return (litres * rate).quantize(PAISE, rounding=ROUND_HALF_UP)

def total_store_list(raw):
    """Version A: store every payment in a list, add at the end. Time O(n), space O(n)."""
    payments = []
    for l, f, s in raw:
        payments.append(payment(Decimal(l), Decimal(f), Decimal(s)))
    return sum(payments, Decimal("0")), payments

def total_running(raw):
    """Version B: keep a running total. Time O(n), space O(1)."""
    total = Decimal("0")
    for l, f, s in raw:
        total += payment(Decimal(l), Decimal(f), Decimal(s))
    return total

if __name__ == "__main__":
    entries = [("10", "3.5", "8.5"), ("8.5", "4.2", "8.7"), ("12", "3.1", "8.3")]   # hand-trace set
    total_a, plist = total_store_list(entries)
    print("payments:", [str(p) for p in plist])
    print("A (list) :", total_a)
    print("B (running):", total_running(entries))
    # trace with running total
    running = Decimal("0")
    print(f"{'i':>2} {'litres':>7} {'fat':>5} {'snf':>5} {'rate':>7} {'payment':>9} {'running':>9}")
    for i, (l, f, s) in enumerate(entries, 1):
        p = payment(Decimal(l), Decimal(f), Decimal(s)); running += p
        rate = BASE + (Decimal(f) - STD_FAT) / STEP * FATV + (Decimal(s) - STD_SNF) / STEP * SNFV
        print(f"{i:>2} {l:>7} {f:>5} {s:>5} {rate:>7} {p:>9} {running:>9}")
