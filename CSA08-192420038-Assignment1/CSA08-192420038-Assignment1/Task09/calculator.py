"""Task 9 - the complete payment calculator (Decimal, validation, ten-day total)."""
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation

BASE_RATE = Decimal("30.00")
FAT_STEP_VALUE = Decimal("0.40")
SNF_STEP_VALUE = Decimal("0.30")
STD_FAT, STD_SNF, STEP = Decimal("3.5"), Decimal("8.5"), Decimal("0.1")
FAT_MIN, FAT_MAX = Decimal("2.0"), Decimal("7.0")
SNF_MIN, SNF_MAX = Decimal("7.0"), Decimal("10.0")
LITRES_MAX = Decimal("1000")          # one farmer cannot bring more than this in one shift (assumption)
PAISE = Decimal("0.01")


class InvalidEntry(ValueError):
    """Raised when an entry breaks a validation rule."""


def to_decimal(text, name):
    """Convert text to a finite Decimal or raise InvalidEntry."""
    try:
        d = Decimal(str(text).strip())
    except InvalidOperation:
        raise InvalidEntry(f"{name} '{text}' is not a number")
    if not d.is_finite():
        raise InvalidEntry(f"{name} '{text}' is not a finite number")
    return d


def money(x):
    """Round a Decimal to whole paise, halves rounded up."""
    return x.quantize(PAISE, rounding=ROUND_HALF_UP)


def validate(litres, fat, snf):
    """Raise InvalidEntry if any rule is broken (all arguments Decimal)."""
    if not (0 < litres <= LITRES_MAX):
        raise InvalidEntry(f"litres {litres} must be above 0 and at most {LITRES_MAX}")
    if not (FAT_MIN <= fat <= FAT_MAX):
        raise InvalidEntry(f"fat {fat} must be between {FAT_MIN} and {FAT_MAX}")
    if not (SNF_MIN <= snf <= SNF_MAX):
        raise InvalidEntry(f"snf {snf} must be between {SNF_MIN} and {SNF_MAX}")
    if fat.as_tuple().exponent < -1 or snf.as_tuple().exponent < -1:
        raise InvalidEntry("fat and snf must have at most one decimal place")
    if litres.as_tuple().exponent < -2:
        raise InvalidEntry("litres must have at most two decimal places")


def rate_per_litre(fat, snf):
    """Rate (Rs/litre) for Decimal fat and snf."""
    fat_steps = (fat - STD_FAT) / STEP
    snf_steps = (snf - STD_SNF) / STEP
    return money(BASE_RATE + fat_steps * FAT_STEP_VALUE + snf_steps * SNF_STEP_VALUE)


def payout(litres, fat, snf):
    """Amount payable (Rs, whole paise) for Decimal litres, fat, snf."""
    return money(litres * rate_per_litre(fat, snf))


def process_entry(litres_text, fat_text, snf_text):
    """Validate text entries and return (rate, amount) as Decimals."""
    litres = to_decimal(litres_text, "litres")
    fat = to_decimal(fat_text, "fat")
    snf = to_decimal(snf_text, "snf")
    validate(litres, fat, snf)
    return rate_per_litre(fat, snf), payout(litres, fat, snf)


def ten_day_total(entries):
    """Sum of the payout of each (litres, fat, snf) text triple. Invalid entries raise InvalidEntry."""
    total = Decimal("0.00")
    for litres, fat, snf in entries:
        total += process_entry(litres, fat, snf)[1]
    return total


if __name__ == "__main__":
    sample = [("10", "3.5", "8.5"), ("8.5", "4.2", "8.7"), ("12", "3.1", "8.3"), ("10", "4.0", "8.0"), ("7.5", "3.8", "8.6")]
    for l, f, s in sample:
        r, a = process_entry(l, f, s)
        print(f"{l:>5} L  fat {f}  snf {s}  rate {r:6}  amount {a:8}")
    print("ten-day total:", ten_day_total(sample))
