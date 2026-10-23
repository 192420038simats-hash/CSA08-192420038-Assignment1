"""Task 9 - assert-based tests; prints the test table (expected versus actual)."""
from decimal import Decimal as D
from calculator import process_entry, ten_day_total, InvalidEntry

valid_cases = [
    # description,                     litres, fat,   snf,   expected rate, expected amount
    ("standard milk",                   "10",  "3.5", "8.5", "30.00", "300.00"),
    ("fat above, snf above",            "8.5", "4.2", "8.7", "33.40", "283.90"),
    ("fat below, snf below",            "12",  "3.1", "8.3", "27.80", "333.60"),
    ("fat above, snf below",            "10",  "4.0", "8.0", "30.50", "305.00"),
    ("fat below, snf above",            "10",  "3.0", "9.0", "29.50", "295.00"),
    ("lowest allowed fat 2.0",          "10",  "2.0", "8.5", "24.00", "240.00"),
    ("highest allowed fat 7.0",         "10",  "7.0", "8.5", "44.00", "440.00"),
    ("7.5 L, 3.8/8.6",                  "7.5", "3.8", "8.6", "31.50", "236.25"),
    ("half-paisa: 8.25 L x 30.50",      "8.25","3.7", "8.4", "30.50", "251.63"),
]
invalid_cases = [
    ("text litres",         "abc", "3.5", "8.5"),
    ("negative litres",     "-5",  "3.5", "8.5"),
    ("zero litres",         "0",   "3.5", "8.5"),
    ("comma decimal",       "10",  "3,5", "8.5"),
    ("fat below 2.0",       "10",  "1.9", "8.5"),
    ("fat above 7.0",       "10",  "7.1", "8.5"),
    ("text fat",            "10",  "high", "8.5"),
    ("snf out of range",    "10",  "3.5", "11.0"),
    ("NaN",                 "10",  "NaN", "8.5"),
    ("two decimal fat",     "10",  "3.55", "8.5"),
    ("three decimal litres", "8.255", "3.5", "8.5"),
]
print(f"{'Case':<34}{'Expected':>20}{'Actual':>22}  Result")
for name, l, f, s, er, ea in valid_cases:
    r, a = process_entry(l, f, s)
    ok = (r, a) == (D(er), D(ea))
    assert ok, (name, r, a)
    print(f"{name:<34}{'rate '+er+' pay '+ea:>20}{'rate '+str(r)+' pay '+str(a):>22}  {'PASS' if ok else 'FAIL'}")
for name, l, f, s in invalid_cases:
    try:
        process_entry(l, f, s); got = "accepted"
    except InvalidEntry as e:
        got = "rejected"
    assert got == "rejected", name
    print(f"{name:<34}{'rejected':>20}{got:>22}  PASS")

hand = [("10", "3.5", "8.5"), ("8.5", "4.2", "8.7"), ("12", "3.1", "8.3"), ("10", "4.0", "8.0"), ("7.5", "3.8", "8.6")]
total = ten_day_total(hand)
assert total == D("1458.75")
print(f"{'5-entry hand-calculated total':<34}{'1458.75':>20}{str(total):>22}  PASS")
print("\nAll tests passed.")
