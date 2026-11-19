"""B2 - four bad input files given to the cleaning pipeline: missing column, wrong delimiter, other encoding, empty file."""
import logging, os, sys, tempfile
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "TaskB1"))
from cleaning import read_text, clean_text, CleaningError

logging.basicConfig(level=logging.WARNING, format="   log: %(levelname)s %(message)s")
tmp = tempfile.mkdtemp()
files = {
    "missing column (no pm10)": ("date,hour,pm25,no2,temp\n2026-10-01,0,48,30,24\n", "utf-8"),
    "wrong delimiter (semicolon)": ("date;hour;pm25;pm10;no2;temp\n2026-10-01;0;48;80;30;24\n", "utf-8"),
    "Windows-1252 text (em dash)": ("date,hour,pm25,pm10,no2,temp\n2026-10-01,0,48,80,30,24\n2026-10-01,1,\u2014,82,31,24\n", "cp1252"),
    "UTF-16 with BOM": ("date,hour,pm25,pm10,no2,temp\n2026-10-01,0,48,80,30,24\n", "utf-16"),
    "empty file": ("", "utf-8"),
    "only a header": ("date,hour,pm25,pm10,no2,temp\n", "utf-8"),
    "extra column": ("date,hour,pm25,pm10,no2,temp,flag\n2026-10-01,0,48,80,30,24,x\n", "utf-8"),
}
for label, (text, enc) in files.items():
    path = os.path.join(tmp, "f.csv")
    with open(path, "wb") as fh:
        fh.write(text.encode(enc))
    print(f"{label}:")
    try:
        rows = clean_text(read_text(path))
        print(f"   accepted, {len(rows)} row(s): {[(r['hour'], r['pm25']) for r in rows]}")
    except CleaningError as e:
        print(f"   REJECTED by CleaningError: {e}")
print("\nWhat a naive csv.DictReader(open(path, encoding='utf-8')) program would do with the first three files:")
import csv
for label in list(files)[:3]:
    text, enc = files[label]
    path = os.path.join(tmp, "g.csv"); open(path, "wb").write(text.encode(enc))
    try:
        r = list(csv.DictReader(open(path, encoding="utf-8")))
        result = f"read {len(r)} row(s), then row['pm10'] -> {r[0]['pm10']}"
    except Exception as e:
        result = f"{type(e).__name__}: {e}"
    print(f"   {label:<30}{result}")
