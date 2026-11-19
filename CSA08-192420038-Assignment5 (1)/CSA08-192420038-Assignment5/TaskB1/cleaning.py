"""Task B1 - cleaning rules (designed in A2) for the daily station files.

Raw file : date,hour,pm25,pm10,no2,temp   (station from the file name)
Clean row: dict(day 'YYYY-MM-DD', hour 0-23, pm25, pm10, no2 in ug/m3 (float or None), temp_c in Celsius (float or None))"""
import csv, io, logging, statistics
from collections import Counter
from datetime import datetime

log = logging.getLogger("cleaning")

EXPECTED_COLUMNS = ["date", "hour", "pm25", "pm10", "no2", "temp"]
MISSING_TOKENS = {"", "na", "n/a", "nan", "null", "none", "--", "err"}
LIMITS = {"pm25": (0, 999), "pm10": (0, 999), "no2": (0, 999), "temp_c": (-10, 55)}   # instrument ranges: anything else is a sensor fault
DATE_FORMATS = ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y")
FILL_LIMIT = 3                                    # forward fill at most 3 consecutive hours


class CleaningError(Exception):
    """A whole file cannot be used (empty, wrong delimiter, missing column, unreadable)."""


def read_text(path):
    """Read a file as text whatever its encoding: BOM detection, then UTF-8, then Windows-1252 (with a warning)."""
    data = open(path, "rb").read()
    if not data.strip():
        raise CleaningError("file is empty")
    if data.startswith(b"\xef\xbb\xbf"):
        return data.decode("utf-8-sig")
    if data.startswith((b"\xff\xfe", b"\xfe\xff")):
        return data.decode("utf-16")
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        log.warning("%s is not UTF-8; read as Windows-1252", path)
        return data.decode("cp1252")


def parse_date(text):
    """'2026-10-01' or '01/10/2026' or '01-10-2026' -> '2026-10-01'; None if it is not a date."""
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(text.strip(), fmt).date().isoformat()
        except ValueError:
            pass
    return None


def to_number(text):
    """Text -> float, or None for blank / NA / words / non-finite values."""
    t = text.strip()
    if t.lower() in MISSING_TOKENS:
        return None
    try:
        v = float(t)
    except ValueError:
        return None
    return v if v == v and abs(v) != float("inf") else None


def f_to_c(f):
    return round((f - 32) * 5 / 9, 1)


def clean_text(text, fahrenheit=False, counter=None):
    """Clean the text of one raw file. Returns the list of clean row dicts (duplicates removed, impossible values
    set to None). Missing values are NOT filled here (see fill_missing)."""
    c = counter if counter is not None else Counter()
    reader = csv.reader(io.StringIO(text))
    header = [h.strip().lower() for h in next(reader, [])]
    if header != EXPECTED_COLUMNS:
        missing = [col for col in EXPECTED_COLUMNS if col not in header]
        if len(header) == 1 and any(d in header[0] for d in ";|\t"):
            raise CleaningError(f"wrong delimiter: header read as one column '{header[0]}'")
        raise CleaningError(f"expected columns {EXPECTED_COLUMNS}, found {header}" + (f"; missing {missing}" if missing else ""))
    rows, seen = [], set()
    for rec in reader:
        if not any(x.strip() for x in rec):
            continue
        c["raw rows"] += 1
        if len(rec) != 6:
            c["damaged rows"] += 1; continue
        day = parse_date(rec[0])
        if day is None:
            c["bad date rows"] += 1; continue
        if not rec[0].strip().startswith(day):
            c["dates reformatted"] += 1
        try:
            hour = int(rec[1].strip())
        except ValueError:
            hour = -1
        if not 0 <= hour <= 23:
            c["bad hour rows"] += 1; continue
        if (day, hour) in seen:
            c["duplicate rows removed"] += 1; continue
        seen.add((day, hour))
        row = {"day": day, "hour": hour}
        for name, text_v in zip(("pm25", "pm10", "no2", "temp_c"), rec[2:6]):
            v = to_number(text_v)
            if v is None:
                c["missing values"] += 1
            else:
                if name == "temp_c" and fahrenheit:
                    v = f_to_c(v); c["temperatures converted F->C"] += 1
                lo, hi = LIMITS[name]
                if not lo <= v <= hi:
                    c["impossible values -> missing"] += 1
                    v = None
            row[name] = v
        rows.append(row)
    return rows


def fill_missing(rows, strategy="ffill", limit=FILL_LIMIT, counter=None):
    """rows of ONE station in time order. strategy: 'ffill' (previous valid value, at most `limit` hours in a row),
    'median' (median of the station), 'drop' (leave None; statistics ignore it). Returns a new list."""
    c = counter if counter is not None else Counter()
    out = [dict(r) for r in sorted(rows, key=lambda r: (r["day"], r["hour"]))]
    for col in ("pm25", "pm10", "no2", "temp_c"):
        if strategy == "ffill":
            last, gap = None, 0
            for r in out:
                if r[col] is None:
                    gap += 1
                    if last is not None and gap <= limit:
                        r[col] = last; c["values forward-filled"] += 1
                else:
                    last, gap = r[col], 0
        elif strategy == "median":
            valid = [r[col] for r in out if r[col] is not None]
            med = statistics.median(valid) if valid else None
            for r in out:
                if r[col] is None and med is not None:
                    r[col] = med; c["values filled with median"] += 1
        elif strategy != "drop":
            raise ValueError("strategy must be 'ffill', 'median' or 'drop'")
    return out


def min_max(values):
    """Scale to 0-1: (v - min) / (max - min); None stays None."""
    ok = [v for v in values if v is not None]
    lo, hi = min(ok), max(ok)
    return [None if v is None else (0.0 if hi == lo else round((v - lo) / (hi - lo), 3)) for v in values]


def z_score(values):
    """(v - mean) / population standard deviation; None stays None."""
    ok = [v for v in values if v is not None]
    mu, sd = statistics.fmean(ok), statistics.pstdev(ok)
    return [None if v is None else (0.0 if sd == 0 else round((v - mu) / sd, 3)) for v in values]
