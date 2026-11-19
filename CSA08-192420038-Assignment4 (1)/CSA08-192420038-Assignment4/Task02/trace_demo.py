"""Task 2.4 - trace of the processing of ONE small file that contains a damaged line."""
from attendance_monthly import parse_line
counts, seen = {}, set()
print(f"{'line':>4}  {'text':<26}{'action':<46}counts after")
with open("data_oct/attendance_2026-10-07.txt", encoding="utf-8") as f:
    for n, line in enumerate(f, 1):
        try:
            r, d, s = parse_line(line)
            rec = counts.setdefault(r, [0, 0]); rec[1] += 1; rec[0] += (s == "P")
            action = f"valid: total+1{', present+1' if s == 'P' else ''}"
        except ValueError as e:
            action = f"DAMAGED -> log ({e})"
        short = {k[-3:]: tuple(v) for k, v in counts.items()}
        print(f"{n:>4}  {line.strip():<26}{action:<46}{short}")
