"""B1 - Complete the Code (TODO 1 and TODO 2 done) - the program exactly as given."""
import csv
import io

RAW = """station,date,pm25
Adyar,2026-10-01,48
Adyar,2026-10-02,NA
Adyar,2026-10-03,
Guindy,2026-10-01,95
Guindy,2026-10-02,-5
Guindy,2026-10-03,121
"""


def load_clean(text):
    """Returns (station, date, pm25) tuples for valid, non-negative readings only."""
    rows = []
    # TODO 1 done: csv.DictReader; skip rows whose pm25 is empty, 'NA' or negative; convert pm25 to float
    for rec in csv.DictReader(io.StringIO(text)):
        raw = rec["pm25"].strip()
        if raw == "" or raw.upper() == "NA":
            continue
        value = float(raw)
        if value < 0:
            continue
        rows.append((rec["station"], rec["date"], value))
    return rows


def min_max(values):
    # TODO 2 done: scale each value to 0-1 using (v - min) / (max - min), rounded to 3 decimals
    lo, hi = min(values), max(values)
    return [round((v - lo) / (hi - lo), 3) for v in values]


clean = load_clean(RAW)
print(clean)
print(min_max([pm for _, _, pm in clean]))
