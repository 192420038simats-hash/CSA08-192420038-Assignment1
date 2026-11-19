"""A1.1 - inspect the raw files and count every data-quality problem, with one example of each."""
import csv, glob, os, statistics
from collections import Counter, defaultdict

RAW = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "raw")
files = sorted(glob.glob(os.path.join(RAW, "*.csv")))
count, example, rows, seen = Counter(), {}, 0, set()
temps = defaultdict(list)


def note(kind, where, line):
    count[kind] += 1
    example.setdefault(kind, f"{where}: {line}")


for path in files:
    name = os.path.basename(path)
    with open(path, newline="", encoding="utf-8") as f:
        rd = csv.reader(f); header = next(rd)
        for n, rec in enumerate(rd, start=2):
            rows += 1; line = ",".join(rec); where = f"{name} line {n}"
            for col, v in zip(("pm25", "pm10", "no2", "temp"), rec[2:6]):
                s = v.strip().lower()
                if s == "": note("blank value", where, line)
                elif s in ("na", "n/a"): note("'NA' value", where, line)
                elif s in ("err", "--"): note("text instead of a number", where, line)
                else:
                    x = float(s)
                    if col != "temp" and x < 0: note("negative pollutant value", where, line)
                    if col != "temp" and x > 999: note("impossibly large pollutant value", where, line)
                    if col == "temp": temps[name.rsplit("_", 1)[0]].append(x)
            if "/" in rec[0]: note("date written dd/mm/yyyy", where, line)
            if int(rec[1]) > 23: note("hour 24 (does not exist)", where, line)
            if (name, rec[0], rec[1]) in seen: note("duplicate (date, hour) row", where, line)
            seen.add((name, rec[0], rec[1]))
print(f"{len(files)} files, {rows:,} data rows, header: {header}\n")
print(f"{'problem':<36}{'count':>6}   example")
for k, v in sorted(count.items(), key=lambda kv: -kv[1]):
    print(f"{k:<36}{v:>6}   {example[k]}")
print("\nMean of the temperature column per station (a value above 50 cannot be degrees Celsius):")
for st, v in sorted(temps.items(), key=lambda kv: -statistics.fmean(kv[1])):
    flag = "   <-- Fahrenheit" if statistics.fmean(v) > 50 else ""
    print(f"   {st:<14}{statistics.fmean(v):>7.1f}{flag}")
