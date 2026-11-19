"""Statistics."""
from decimal import Decimal, ROUND_HALF_UP


def percentage(present, total):
    """Percentage rounded half-up to 2 decimals."""
    return (Decimal(present * 100) / Decimal(total)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def attendance_percentages(records):
    """{register: (present, total, percent)} from the list of records."""
    counts = {}
    for register, _, status in records:
        rec = counts.setdefault(register, [0, 0])
        rec[1] += 1
        rec[0] += status == "P"
    return {r: (p, t, percentage(p, t)) for r, (p, t) in sorted(counts.items())}


def below_limit(pcts, limit=75):
    """Registers whose percentage is below the limit."""
    return [r for r, (_, _, pc) in pcts.items() if pc < limit]
