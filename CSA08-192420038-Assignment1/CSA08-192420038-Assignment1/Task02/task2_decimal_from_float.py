"""Task 2 - what happens with Decimal(float(amount)) instead of Decimal(amount)."""
from decimal import Decimal
payments = ["33.40"] * 1000 + ["0.10"] * 3
total = Decimal("0")
for amount in payments:
    total += Decimal(float(amount))      # the float is converted exactly, error and all
print("Decimal(float(amount)) total:", total)
print("Decimal(33.40)  =", Decimal(33.40))
print("Decimal('33.40')=", Decimal("33.40"))
print("Rounded to paise:", total.quantize(Decimal("0.01")))
