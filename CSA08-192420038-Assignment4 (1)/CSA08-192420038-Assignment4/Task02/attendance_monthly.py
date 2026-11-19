"""Task 2 - monthly attendance from the daily biometric files.
Input : data_oct/attendance_YYYY-MM-DD.txt   lines  register,date,P|A
Output: out_oct/attendance_report.csv  (register, present, total, percent)
        out_oct/below_75.txt           (students below 75 %)
        out_oct/damaged_lines.log      (file name, line number, reason, text)"""
import sys
from datetime import date
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

LIMIT = Decimal("75")


def parse_line(line):
    """'192311001,2026-10-08,P' -> ('192311001', '2026-10-08', 'P'); ValueError(reason) for a damaged line."""
    parts = line.strip().split(",")
    if len(parts) != 3:
        raise ValueError(f"expected 3 fields, found {len(parts)}")
    register, day, status = (p.strip() for p in parts)
    if not (register.isdigit() and len(register) == 9):
        raise ValueError(f"invalid register number '{register}'")
    try:
        date.fromisoformat(day)
    except ValueError:
        raise ValueError(f"invalid date '{day}'") from None
    if status not in ("P", "A"):
        raise ValueError(f"invalid status '{status}'")
    return register, day, status


def process_month(folder):
    """Read every daily file ONCE; return (counts, damaged). counts = {register: [present, total]}."""
    counts, damaged, seen = {}, [], set()
    files = sorted(Path(folder).glob("attendance_*.txt"))
    for path in files:
        with open(path, encoding="utf-8") as f:
            empty = True
            for number, line in enumerate(f, start=1):
                if not line.strip():
                    continue
                empty = False
                try:
                    register, day, status = parse_line(line)
                except ValueError as e:
                    damaged.append((path.name, number, str(e), line.strip()))
                    continue
                if (register, day) in seen:                       # same student, same day, twice
                    damaged.append((path.name, number, "duplicate record for this student and date", line.strip()))
                    continue
                seen.add((register, day))
                rec = counts.setdefault(register, [0, 0])
                rec[1] += 1
                if status == "P":
                    rec[0] += 1
            if empty:
                damaged.append((path.name, 0, "file is empty", ""))
    return counts, damaged, len(files)


def percent(present, total):
    """Percentage rounded half-up to 2 decimals (exact decimal arithmetic)."""
    return (Decimal(present * 100) / Decimal(total)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def write_reports(counts, damaged, out_folder):
    out = Path(out_folder); out.mkdir(exist_ok=True)
    rows = [(r, p, t, percent(p, t)) for r, (p, t) in sorted(counts.items())]
    with open(out / "attendance_report.csv", "w", encoding="utf-8") as f:           # "w": a fresh report on every run
        f.write("register,present,total,percent\n")
        for r, p, t, pc in rows:
            f.write(f"{r},{p},{t},{pc}\n")
    low = [row for row in rows if row[3] < LIMIT]                                   # exactly 75.00 is not below 75
    with open(out / "below_75.txt", "w", encoding="utf-8") as f:
        for r, p, t, pc in low:
            f.write(f"{r}  {pc}%  ({p}/{t})\n")
    with open(out / "damaged_lines.log", "w", encoding="utf-8") as f:
        for name, number, reason, text in damaged:
            f.write(f"{name}:{number}: {reason}: {text!r}\n")
    return rows, low


if __name__ == "__main__":
    folder = sys.argv[1] if len(sys.argv) > 1 else "data_oct"
    try:
        counts, damaged, n_files = process_month(folder)
    except FileNotFoundError:
        sys.exit(f"Folder '{folder}' not found")
    rows, low = write_reports(counts, damaged, "out_oct")
    print(f"{n_files} daily files read, {len(damaged)} damaged/duplicate/empty entries logged")
    print(f"{'register':<11}{'present':>8}{'total':>7}{'percent':>9}")
    for r, p, t, pc in rows:
        print(f"{r:<11}{p:>8}{t:>7}{pc:>9}")
    print("\nbelow 75 %:", [r for r, *_ in low])
    print("\n--- damaged_lines.log ---")
    print(open("out_oct/damaged_lines.log", encoding="utf-8").read().rstrip())
