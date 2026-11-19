"""B1 - the same program with the extra check: rows whose pm25 is above 999 are skipped, and a test row for it."""
import csv
import io

RAW = """station,date,pm25
Adyar,2026-10-01,48
Adyar,2026-10-02,NA
Adyar,2026-10-03,
Guindy,2026-10-01,95
Guindy,2026-10-02,-5
Guindy,2026-10-03,121
Guindy,2026-10-04,1500
"""                                                      # <- new test row: 1500 is a sensor fault


def load_clean(text):
    """Returns (station, date, pm25) tuples for valid readings only (0 to 999)."""
    rows = []
    for rec in csv.DictReader(io.StringIO(text)):
        raw = rec["pm25"].strip()
        if raw == "" or raw.upper() == "NA":
            continue
        value = float(raw)
        if value < 0 or value > 999:                     # <- new check
            continue
        rows.append((rec["station"], rec["date"], value))
    return rows


def min_max(values):
    lo, hi = min(values), max(values)
    return [round((v - lo) / (hi - lo), 3) for v in values]


clean = load_clean(RAW)
print(clean)
print(min_max([pm for _, _, pm in clean]))
assert all(pm <= 999 for _, _, pm in clean) and len(clean) == 3     # 1500 was skipped
print("999-check test passed: the 1500 row was skipped")
