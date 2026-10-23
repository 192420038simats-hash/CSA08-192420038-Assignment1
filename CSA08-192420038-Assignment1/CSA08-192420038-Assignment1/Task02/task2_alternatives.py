"""Task 2 - alternatives: integer paise, float + round() after every addition."""
import sys, time
from decimal import Decimal

def total_paise(items):
    total = 0                                   # integer paise
    for a in items:
        rupees, _, paise = a.partition(".")
        total += int(rupees) * 100 + int((paise + "00")[:2])
    return total

def total_float_round(items):
    total = 0.0
    for a in items:
        total = round(total + float(a), 2)
    return total

def total_float(items):
    t = 0.0
    for a in items: t += float(a)
    return t

def total_decimal(items):
    t = Decimal("0")
    for a in items: t += Decimal(a)
    return t

payments = ["33.40"] * 1000 + ["0.10"] * 3
exact = Decimal("33400.30")
print("exact bank total      : 33400.30")
p = total_paise(payments);         print("integer paise         :", p, "->", f"{p//100}.{p%100:02d}")
r = total_float_round(payments);   print("float + round each add:", r)
print("plain float           :", total_float(payments))
print("Decimal               :", total_decimal(payments))

print("\nMemory per value (sys.getsizeof):")
for label, v in [("int paise 3340", 3340), ("float 33.4", 33.4), ("Decimal('33.40')", Decimal("33.40"))]:
    print(f"  {label:18} {sys.getsizeof(v):3} bytes")

print("\nTime for 200,000 additions:")
big = ["33.40"] * 200000
for name, fn in [("float", total_float), ("float+round", total_float_round), ("int paise", total_paise), ("Decimal", total_decimal)]:
    t0 = time.perf_counter(); res = fn(big); t1 = time.perf_counter()
    print(f"  {name:12} {t1-t0:7.4f} s  result {res}")
