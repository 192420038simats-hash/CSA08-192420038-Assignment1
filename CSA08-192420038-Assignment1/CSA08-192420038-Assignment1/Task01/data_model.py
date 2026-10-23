"""Task 1 - data model: one tuple per entry (design B) versus separate variables (design A)."""
import sys, time
from decimal import Decimal

# Named constants (never change during a run)
BASE_RATE, FAT_STEP_VALUE, SNF_STEP_VALUE = Decimal("30.00"), Decimal("0.40"), Decimal("0.30")
STD_FAT, STD_SNF, STEP = Decimal("3.5"), Decimal("8.5"), Decimal("0.1")
FAT_MIN, FAT_MAX = Decimal("2.0"), Decimal("7.0")

# One entry = one tuple (farmer_id:str, shift:str, litres:Decimal, fat:Decimal, snf:Decimal)
entry = ("F017", "M", Decimal("8.5"), Decimal("4.2"), Decimal("8.7"))
print("Design B, one entry:", entry)

def generate_design_a(n):
    """Source code a clerk would have to write for n farmers using separate variables."""
    lines = []
    for i in range(1, n + 1):
        lines.append(f"litres{i}, fat{i}, snf{i} = 0.0, 0.0, 0.0")
    lines.append("total = 0.0")
    for i in range(1, n + 1):
        lines.append(f"total += litres{i} * (30 + round((fat{i}-3.5)/0.1)*0.4 + round((snf{i}-8.5)/0.1)*0.3)")
    return "\n".join(lines)

for n in (3, 300, 6000):
    src = generate_design_a(n)
    print(f"Design A for {n:5} farmers: {src.count(chr(10))+1:6} lines of source, {len(src):8} characters")

# Design B: the same job in a loop, source size is constant
def total_design_b(entries):
    total = Decimal("0")
    for _id, _shift, litres, fat, snf in entries:
        rate = BASE_RATE + (fat - STD_FAT) / STEP * FAT_STEP_VALUE + (snf - STD_SNF) / STEP * SNF_STEP_VALUE
        total += litres * rate
    return total

for n in (300, 6000, 150000):
    data = [("F", "M", Decimal("8.5"), Decimal("4.2"), Decimal("8.7"))] * n
    t0 = time.perf_counter(); total_design_b(data); t1 = time.perf_counter()
    mem = sys.getsizeof(data)
    print(f"Design B n={n:7}: {t1-t0:8.4f} s, list object {mem} bytes, source size constant (12 lines)")
