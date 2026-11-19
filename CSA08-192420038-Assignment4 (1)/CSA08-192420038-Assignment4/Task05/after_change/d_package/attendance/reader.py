"""Reading the daily files."""
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
