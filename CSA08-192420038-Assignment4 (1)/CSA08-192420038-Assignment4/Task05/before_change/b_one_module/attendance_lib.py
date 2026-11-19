"""(b) the library module: reading, statistics and reports."""
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path


def read_month(folder):
    """Read every attendance_*.txt in folder. Return (records, errors).
    records = [(register, date, status), ...]; errors = [(file name, line number, reason), ...]."""
    records, errors = [], []
    for path in sorted(Path(folder).glob("attendance_*.txt")):
        with open(path, encoding="utf-8") as f:
            for number, line in enumerate(f, start=1):
                parts = line.strip().split(",")
                if len(parts) != 3:
                    errors.append((path.name, number, f"expected 3 fields, found {len(parts)}"))
                elif parts[2] not in ("P", "A"):
                    errors.append((path.name, number, f"invalid status '{parts[2]}'"))
                else:
                    records.append(tuple(parts))
    return records, errors


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


def write_percentage_report(pcts, path):
    with open(path, "w", encoding="utf-8") as f:
        f.write("register,present,total,percent\n")
        for r, (p, t, pc) in pcts.items():
            f.write(f"{r},{p},{t},{pc}\n")


def write_error_log(errors, path):
    with open(path, "w", encoding="utf-8") as f:
        for name, number, reason in errors:
            f.write(f"{name}:{number}: {reason}\n")
