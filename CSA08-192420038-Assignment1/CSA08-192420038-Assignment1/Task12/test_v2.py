"""Task 12 - tests for both seasons, two-decimal readings and the bonus, plus the impact on the ORIGINAL design."""
from decimal import Decimal as D
import milkpay_v2 as m

cards, months = m.load_cards()
std, summer = m.select_card(10, cards, months), m.select_card(5, cards, months)
assert m.select_card(3, cards, months) is std and m.select_card(4, cards, months) is summer
assert m.select_card(6, cards, months) is summer and m.select_card(7, cards, months) is std

print("A/B. ORIGINAL float whole-step design versus v2 on two-decimal readings (standard card)")
print(f"{'fat':>5} {'snf':>5} {'raw fat steps':>16} {'original rate':>14} {'v2 exact rate':>14}")
for fat, snf in [("4.23", "8.57"), ("4.27", "8.43"), ("3.54", "8.54"), ("3.46", "8.46")]:
    original = round(30.0 + round((float(fat) - 3.5) / 0.1) * 0.40 + round((float(snf) - 8.5) / 0.1) * 0.30, 2)
    print(f"{fat:>5} {snf:>5} {(float(fat)-3.5)/0.1:>16.12f} {original:>14} {str(m.rate_per_litre(D(fat), D(snf), std)):>14}")

print("\nD. Test table (expected = hand calculation)")
print(f"{'Case':<38}{'Expected':>22}{'Actual':>22}  Result")
rows = []
def check(label, got, expected):
    ok = got == expected
    rows.append(ok)
    print(f"{label:<38}{str(expected):>22}{str(got):>22}  {'PASS' if ok else 'FAIL'}")
    assert ok, label

check("std rate 4.2/8.7",                 m.rate_per_litre(D("4.2"), D("8.7"), std), D("33.40"))
check("std amount 8.5 L 4.2/8.7",         m.payout(D("8.5"), D("4.2"), D("8.7"), std), D("283.90"))
check("summer rate 4.2/8.7 (32+7*.45+2*.3)", m.rate_per_litre(D("4.2"), D("8.7"), summer), D("35.75"))
check("summer amount 8.5 L (303.875 up)", m.payout(D("8.5"), D("4.2"), D("8.7"), summer), D("303.88"))
check("summer standard milk 10 L",         m.payout(D("10"), D("3.50"), D("8.50"), summer), D("320.00"))
check("std rate 4.23/8.57 (7.3, 0.7 steps)", m.rate_per_litre(D("4.23"), D("8.57"), std), D("33.13"))
check("summer rate 4.23/8.57 (35.495 up)",  m.rate_per_litre(D("4.23"), D("8.57"), summer), D("35.50"))
check("std rate 3.46/8.46 (-0.4, -0.4)",    m.rate_per_litre(D("3.46"), D("8.46"), std), D("29.72"))

def run(l_each, n, last=None, card=summer):
    e = [(l_each, "3.50", "8.50")] * n + ([(last, "3.50", "8.50")] if last else [])
    return m.ten_day_total(e, card)

milk, b, grand, litres = run("26", 20)                       # 520 L
check("bonus: 520 L summer, bonus",         b, D("260.00"))
check("bonus: 520 L summer, grand total",   grand, D("16900.00"))
check("bonus: exactly 500 L -> no bonus",   run("25", 20)[1], D("0.00"))
milk, b, grand, litres = run("25", 19, "25.01")              # 500.01 L
check("bonus: 500.01 L (250.005 up)",       b, D("250.01"))
check("bonus: 500.01 L grand total",        grand, D("16250.33"))
check("std season 520 L grand total",       run("26", 20, card=std)[2], D("15860.00"))   # 15600 + 260
print(f"\nAll {len(rows)} v2 tests passed.")
